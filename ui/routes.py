# 文件：ui/routes.py
# UI 层：路由，只负责界面展示交互，不在这里写 SQL

import re

from flask import Blueprint, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash

# 邮箱格式校验（FR15 员工自助改邮箱用）
EMAIL_RE = re.compile(r"^[A-Za-z0-9_.+-]+@[A-Za-z0-9-]+\.[A-Za-z0-9-.]+$")

from dal.employee_dao import EmployeeDAO
from dal.user_dao import UserDAO
from ui.auth import login_required, role_required

ui_bp = Blueprint("ui", __name__)


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


@ui_bp.route("/employees")
@role_required("HRAdmin", "StoreManager")
def employee_list():
    """FR04 员工总览：仅 HR 与门店经理可访问。"""
    employees = EmployeeDAO.get_all_active()
    return render_template("employees.html", employees=employees)


@ui_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    """FR14 查看本人档案 + FR15 修改邮箱/地址/紧急联系人。"""
    employee = EmployeeDAO.get_by_username(session.get("username"))
    if employee is None:
        return "未找到你的员工档案，请联系 HR 确认登录账号与员工邮箱前缀一致", 404

    error = None
    success = None
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        contact_address = request.form.get("contact_address", "").strip()
        emergency_contact = request.form.get("emergency_contact", "").strip()
        if not EMAIL_RE.match(email):
            error = "邮箱格式不合法，请输入如 user@example.com"
        else:
            EmployeeDAO.update_self(employee.id, email, contact_address, emergency_contact)
            success = "保存成功"
            employee = EmployeeDAO.get_by_username(session.get("username"))

    return render_template("profile.html", employee=employee, error=error, success=success)


@ui_bp.route("/statistics")
@role_required("StoreManager", "HRAdmin")
def statistics():
    """FR12 统计：员工总人数 + 分部门人数。"""
    stats = EmployeeDAO.get_statistics()
    return render_template(
        "statistics.html",
        total=stats["total"],
        by_dept=stats["by_department"],
    )