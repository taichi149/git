# 文件：ui/routes.py
# UI 层：路由，只负责界面展示交互，不在这里写 SQL
# M3：员工增删改查（FR01~FR08）—— 新增 / 修改 / 软归档 / 检索 / 详情
# M4：手动排班（FR10 排班 / FR11 个人排班视图 / FR13 全店排班视图）

import re
from datetime import date, timedelta
from decimal import Decimal, InvalidOperation

from flask import (
    Blueprint,
    abort,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash

from dal.employee_dao import EmployeeDAO
from dal.shift_dao import ShiftDAO
from dal.user_dao import UserDAO
from model.employee import Employee
from model.shift import Shift
from ui.auth import login_required, role_required

ui_bp = Blueprint("ui", __name__)

# 员工表单字段（顺序与模板、DAO 保持一致）
FORM_FIELDS = (
    "employee_id",
    "name",
    "age",
    "position",
    "salary",
    "department",
    "email",
    "contact_address",
    "emergency_contact",
)

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


# ----------------------------------------------------------------------
# 表单读取与校验（UI 层职责：只做输入校验，不写 SQL）
# ----------------------------------------------------------------------
def _empty_form():
    return {field: "" for field in FORM_FIELDS}


def _form_from_employee(employee):
    """把 Employee 对象转成模板可直接回填的字典。"""
    return {
        "employee_id": employee.employee_id or "",
        "name": employee.name or "",
        "age": "" if employee.age is None else str(employee.age),
        "position": employee.position or "",
        "salary": "" if employee.salary is None else str(employee.salary),
        "department": employee.department or "",
        "email": employee.email or "",
        "contact_address": employee.contact_address or "",
        "emergency_contact": employee.emergency_contact or "",
    }


def _validate_form():
    """
    读取并校验表单，返回 (data, errors)。
    data 里的 age 已转 int（可 None）、salary 已转 Decimal（可 None）；
    只要 errors 非空，就重新渲染表单并把用户输入原样回填。
    """
    data = {field: request.form.get(field, "").strip() for field in FORM_FIELDS}
    errors = {}

    # 工号：必填，唯一，最长 20
    if not data["employee_id"]:
        errors["employee_id"] = "工号不能为空"
    elif len(data["employee_id"]) > 20:
        errors["employee_id"] = "工号最长 20 个字符"

    # 姓名：必填，最长 50
    if not data["name"]:
        errors["name"] = "姓名不能为空"
    elif len(data["name"]) > 50:
        errors["name"] = "姓名最长 50 个字符"

    # 年龄：选填，16~100 的整数
    age = None
    if data["age"]:
        try:
            age = int(data["age"])
        except ValueError:
            errors["age"] = "年龄必须是整数"
        else:
            if age < 16 or age > 100:
                errors["age"] = "年龄需在 16~100 之间"

    # 薪资：选填，非负数字，最多两位小数
    salary = None
    if data["salary"]:
        try:
            salary = Decimal(data["salary"])
        except InvalidOperation:
            errors["salary"] = "薪资必须是数字"
        else:
            if salary < 0:
                errors["salary"] = "薪资不能为负数"

    # 邮箱：选填，格式校验
    if data["email"] and not EMAIL_RE.match(data["email"]):
        errors["email"] = "邮箱格式不正确"

    # 其余文本字段长度限制
    for field, label in (("position", "岗位"), ("department", "部门"),
                         ("contact_address", "联系地址"),
                         ("emergency_contact", "紧急联系人")):
        if len(data[field]) > 100:
            errors[field] = label + "最长 100 个字符"

    data["age"] = age
    data["salary"] = salary
    return data, errors


def _to_employee(data, emp_pk=None):
    """把校验后的表单数据组装成 Employee 实体。"""
    return Employee(
        id=emp_pk,
        employee_id=data["employee_id"],
        name=data["name"],
        age=data["age"],
        position=data["position"] or None,
        salary=data["salary"],
        department=data["department"] or None,
        email=data["email"] or None,
        contact_address=data["contact_address"] or None,
        emergency_contact=data["emergency_contact"] or None,
        is_archived=0,
    )


# ----------------------------------------------------------------------
# 首页 / 登录 / 退出
# ----------------------------------------------------------------------
@ui_bp.route("/")
def home():
    """首页：已登录按角色跳转，未登录去登录页。"""
    if "user_id" in session:
        if session.get("role") == "Employee":
            return redirect(url_for("ui.profile"))
        return redirect(url_for("ui.employee_list"))
    return redirect(url_for("ui.login"))


@ui_bp.route("/login", methods=["GET", "POST"])
def login():
    """FR09 登录认证：校验用户名密码，按角色跳转。"""
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user = UserDAO.get_by_username(username)
        if user and check_password_hash(user.hashed_password, password):
            session["user_id"] = user.id
            session["username"] = user.username
            session["role"] = user.role
            if user.role == "Employee":
                return redirect(url_for("ui.profile"))
            return redirect(url_for("ui.employee_list"))
        return render_template("login.html", error="用户名或密码错误")
    return render_template("login.html")


@ui_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("ui.login"))


# ----------------------------------------------------------------------
# FR04 / FR05：员工总览 + 检索
# ----------------------------------------------------------------------
@ui_bp.route("/employees")
@role_required("HRAdmin", "StoreManager")
def employee_list():
    """
    员工总览：支持关键词检索（q）与「已归档」视图切换（archived=1）。
    StoreManager 只读，HRAdmin 可见新增/编辑/归档按钮（模板里按角色控制）。
    """
    keyword = request.args.get("q", "").strip()
    archived = request.args.get("archived") == "1"
    flag = 1 if archived else 0

    if keyword:
        employees = EmployeeDAO.search(keyword, archived=flag)
    elif archived:
        employees = EmployeeDAO.get_all_archived()
    else:
        employees = EmployeeDAO.get_all_active()

    return render_template(
        "employees.html",
        employees=employees,
        keyword=keyword,
        archived=archived,
        can_edit=session.get("role") == "HRAdmin",
    )


# ----------------------------------------------------------------------
# FR07：员工详情
# ----------------------------------------------------------------------
@ui_bp.route("/employees/<int:emp_pk>")
@role_required("HRAdmin", "StoreManager")
def employee_detail(emp_pk):
    """员工详情：展示单个员工的完整档案。"""
    employee = EmployeeDAO.get_by_pk(emp_pk)
    if employee is None:
        abort(404)
    return render_template(
        "employee_detail.html",
        employee=employee,
        can_edit=session.get("role") == "HRAdmin",
    )


# ----------------------------------------------------------------------
# FR01：新增员工
# ----------------------------------------------------------------------
@ui_bp.route("/employees/new", methods=["GET", "POST"])
@role_required("HRAdmin")
def employee_new():
    """新增员工：GET 显示空表单，POST 校验通过后写入数据库。"""
    if request.method == "POST":
        data, errors = _validate_form()

        # 工号唯一性校验（数据库层也应有 UNIQUE 约束兜底）
        if not errors.get("employee_id"):
            if EmployeeDAO.employee_id_exists(data["employee_id"]):
                errors["employee_id"] = "该工号已存在"

        if errors:
            return render_template(
                "employee_form.html", mode="new", form=data, errors=errors
            )

        EmployeeDAO.create(_to_employee(data))
        flash("员工「%s」已新增" % data["name"], "success")
        return redirect(url_for("ui.employee_list"))

    return render_template(
        "employee_form.html", mode="new", form=_empty_form(), errors={}
    )


# ----------------------------------------------------------------------
# FR02：修改员工
# ----------------------------------------------------------------------
@ui_bp.route("/employees/<int:emp_pk>/edit", methods=["GET", "POST"])
@role_required("HRAdmin")
def employee_edit(emp_pk):
    """修改员工信息：已归档的员工不允许编辑。"""
    employee = EmployeeDAO.get_by_pk(emp_pk)
    if employee is None:
        abort(404)
    if employee.is_archived:
        flash("该员工已归档，不能修改；如需修改请先恢复。", "error")
        return redirect(url_for("ui.employee_list", archived=1))

    if request.method == "POST":
        data, errors = _validate_form()

        if not errors.get("employee_id"):
            if EmployeeDAO.employee_id_exists(data["employee_id"], exclude_pk=emp_pk):
                errors["employee_id"] = "该工号已被其他员工占用"

        if errors:
            return render_template(
                "employee_form.html", mode="edit", form=data, errors=errors,
                emp_pk=emp_pk,
            )

        affected = EmployeeDAO.update(_to_employee(data, emp_pk=emp_pk))
        if affected:
            flash("员工「%s」的信息已更新" % data["name"], "success")
        else:
            flash("更新失败：记录不存在或已被归档", "error")
        return redirect(url_for("ui.employee_detail", emp_pk=emp_pk))

    return render_template(
        "employee_form.html",
        mode="edit",
        form=_form_from_employee(employee),
        errors={},
        emp_pk=emp_pk,
    )


# ----------------------------------------------------------------------
# FR03：软归档（需二次确认）+ 恢复
# ----------------------------------------------------------------------
@ui_bp.route("/employees/<int:emp_pk>/archive", methods=["GET", "POST"])
@role_required("HRAdmin")
def employee_archive(emp_pk):
    """
    软归档：GET 显示确认页（需求要求「显式确认」），POST 才真正写库。
    只把 is_archived 置 1，不删除记录。
    """
    employee = EmployeeDAO.get_by_pk(emp_pk)
    if employee is None:
        abort(404)
    if employee.is_archived:
        flash("该员工已经归档过了", "info")
        return redirect(url_for("ui.employee_list", archived=1))

    if request.method == "POST":
        EmployeeDAO.set_archived(emp_pk, True)
        flash("员工「%s」已归档" % employee.name, "success")
        return redirect(url_for("ui.employee_list"))

    return render_template("employee_confirm_archive.html", employee=employee)


@ui_bp.route("/employees/<int:emp_pk>/restore", methods=["POST"])
@role_required("HRAdmin")
def employee_restore(emp_pk):
    """恢复被软归档的员工（软归档的可逆操作）。"""
    employee = EmployeeDAO.get_by_pk(emp_pk)
    if employee is None:
        abort(404)
    EmployeeDAO.set_archived(emp_pk, False)
    flash("员工「%s」已恢复" % employee.name, "success")
    return redirect(url_for("ui.employee_list"))


# ----------------------------------------------------------------------
# 员工个人主页（M2 占位；完整档案在 M5 实现）
# ----------------------------------------------------------------------
@ui_bp.route("/profile")
@login_required
def profile():
    return render_template(
        "profile.html",
        username=session.get("username"),
        role=session.get("role"),
    )


# ======================================================================
# M4：手动排班（FR10 / FR11 / FR13）
# ======================================================================

# 班次类型：数据库存英文代码，页面显示中文（和客户约定的一天三班）
SHIFT_TYPES = (
    ("Morning", "早班"),
    ("Afternoon", "中班"),
    ("Evening", "晚班"),
)
SHIFT_TYPE_LABELS = dict(SHIFT_TYPES)

WEEKDAYS_CN = ("周一", "周二", "周三", "周四", "周五", "周六", "周日")


def _week_range(week_str):
    """
    把 ?week=YYYY-MM-DD 解析成这一周的周一~周日。
    参数缺失或格式非法时，默认取今天所在的周。
    """
    try:
        any_day = date.fromisoformat(week_str)
    except (TypeError, ValueError):
        any_day = date.today()
    monday = any_day - timedelta(days=any_day.weekday())
    return monday, monday + timedelta(days=6)


def _week_nav(monday):
    """上一周 / 本周 / 下一周的跳转参数（拼 URL 用）。"""
    return {
        "prev_week": (monday - timedelta(days=7)).isoformat(),
        "this_week": date.today().isoformat(),
        "next_week": (monday + timedelta(days=7)).isoformat(),
    }


# ----------------------------------------------------------------------
# FR10：手动排班（仅 HRAdmin）
# ----------------------------------------------------------------------
@ui_bp.route("/shifts/assign", methods=["GET", "POST"])
@role_required("HRAdmin")
def shift_assign():
    """
    排班：GET 显示表单（支持 ?emp_pk= 和 ?date= 预填），POST 校验通过后写库。
    同一员工同一天只能有一个班：重复排班会被 DAO 覆盖，相当于改班。
    """
    employees = EmployeeDAO.get_all_active()  # 已归档员工不出现在下拉里

    if request.method == "POST":
        form = {
            "emp_pk": request.form.get("emp_pk", "").strip(),
            "shift_date": request.form.get("shift_date", "").strip(),
            "shift_type": request.form.get("shift_type", "").strip(),
        }
        errors = {}

        # 员工：必选，且必须是在职员工
        emp_pk = None
        employee = None
        if not form["emp_pk"]:
            errors["emp_pk"] = "请选择员工"
        else:
            try:
                emp_pk = int(form["emp_pk"])
            except ValueError:
                errors["emp_pk"] = "员工选择无效"
            else:
                employee = EmployeeDAO.get_by_pk(emp_pk)
                if employee is None or employee.is_archived:
                    errors["emp_pk"] = "该员工不存在或已归档，不能排班"

        # 日期：必填，格式 YYYY-MM-DD
        shift_date = None
        if not form["shift_date"]:
            errors["shift_date"] = "请选择日期"
        else:
            try:
                shift_date = date.fromisoformat(form["shift_date"])
            except ValueError:
                errors["shift_date"] = "日期格式不正确"

        # 班次：必须是约定的三种之一
        if form["shift_type"] not in SHIFT_TYPE_LABELS:
            errors["shift_type"] = "请选择班次"

        if errors:
            return render_template(
                "shift_assign.html",
                employees=employees,
                shift_types=SHIFT_TYPES,
                form=form,
                errors=errors,
            )

        ShiftDAO.assign(Shift(
            employee_id=emp_pk,
            shift_date=shift_date,
            shift_type=form["shift_type"],
        ))
        flash(
            "已为「%s」安排 %s %s"
            % (employee.name, shift_date.isoformat(), SHIFT_TYPE_LABELS[form["shift_type"]]),
            "success",
        )
        return redirect(url_for("ui.shifts_week", week=shift_date.isoformat()))

    # GET：允许从周视图 / 个人视图带参数跳过来预填
    form = {
        "emp_pk": request.args.get("emp_pk", ""),
        "shift_date": request.args.get("date", ""),
        "shift_type": "",
    }
    return render_template(
        "shift_assign.html",
        employees=employees,
        shift_types=SHIFT_TYPES,
        form=form,
        errors={},
    )


# ----------------------------------------------------------------------
# FR13：全店排班周视图（HRAdmin / StoreManager）
# ----------------------------------------------------------------------
@ui_bp.route("/shifts")
@role_required("HRAdmin", "StoreManager")
def shifts_home():
    """/shifts 只是入口，直接跳到本周的全店周视图。"""
    return redirect(url_for("ui.shifts_week"))


@ui_bp.route("/shifts/week")
@role_required("HRAdmin", "StoreManager")
def shifts_week():
    """
    全店周视图：一行一个在职员工，一列一天，格子里是班次。
    没排班的员工也会显示出来，方便 HR 看到谁还空着。
    """
    monday, sunday = _week_range(request.args.get("week"))
    days = [monday + timedelta(days=i) for i in range(7)]

    # 先按员工铺好行，再把排班填进格子：{日期: Shift}
    employees = EmployeeDAO.get_all_active()
    rows = []
    row_index = {}
    for e in employees:
        row_index[e.id] = len(rows)
        rows.append({"employee": e, "cells": {}})

    for s in ShiftDAO.get_store_range(monday, sunday):
        if s.employee_id in row_index:  # 归档员工的排班已被 SQL 过滤，这里再保险一次
            rows[row_index[s.employee_id]]["cells"][s.shift_date] = s

    return render_template(
        "shifts_week.html",
        rows=rows,
        days=days,
        monday=monday,
        sunday=sunday,
        weekdays_cn=WEEKDAYS_CN,
        labels=SHIFT_TYPE_LABELS,
        can_edit=session.get("role") == "HRAdmin",
        **_week_nav(monday),
    )


# ----------------------------------------------------------------------
# FR11：个人排班视图（HRAdmin / StoreManager）
# ----------------------------------------------------------------------
@ui_bp.route("/employees/<int:emp_pk>/shifts")
@role_required("HRAdmin", "StoreManager")
def employee_shifts(emp_pk):
    """某个员工一周的排班：{日期: Shift} 按格子展示。"""
    employee = EmployeeDAO.get_by_pk(emp_pk)
    if employee is None:
        abort(404)

    monday, sunday = _week_range(request.args.get("week"))
    days = [monday + timedelta(days=i) for i in range(7)]
    shifts = ShiftDAO.get_by_employee_range(emp_pk, monday, sunday)
    cells = {s.shift_date: s for s in shifts}

    return render_template(
        "employee_shifts.html",
        employee=employee,
        days=days,
        cells=cells,
        monday=monday,
        sunday=sunday,
        weekdays_cn=WEEKDAYS_CN,
        labels=SHIFT_TYPE_LABELS,
        can_edit=session.get("role") == "HRAdmin",
        **_week_nav(monday),
    )


# ----------------------------------------------------------------------
# 删除排班（仅 HRAdmin；删除后跳回原来的页面）
# ----------------------------------------------------------------------
@ui_bp.route("/shifts/<int:shift_id>/delete", methods=["POST"])
@role_required("HRAdmin")
def shift_delete(shift_id):
    affected = ShiftDAO.delete(shift_id)
    if affected:
        flash("该排班已删除", "success")
    else:
        flash("删除失败：这条排班不存在", "error")
    # 表单里带了 next 隐藏字段，删完跳回原来的周视图 / 个人视图
    return redirect(request.form.get("next") or url_for("ui.shifts_week"))
