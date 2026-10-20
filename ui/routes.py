# 文件：ui/routes.py
# UI 层：路由，只负责界面展示交互，不在这里写 SQL

from flask import Blueprint, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash

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


@ui_bp.route("/profile")
@login_required
def profile():
    """员工个人主页（M2 占位；FR14 完整档案在 M5 实现）。"""
    return render_template(
        "profile.html",
        username=session.get("username"),
        role=session.get("role"),
    )