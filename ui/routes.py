# 文件：ui/routes.py
# UI 层：路由，只负责界面展示交互，不在这里写 SQL

from flask import Blueprint, render_template

from dal.employee_dao import EmployeeDAO

ui_bp = Blueprint("ui", __name__)


@ui_bp.route("/")
def home():
    return render_template("home.html")


@ui_bp.route("/employees")
def employee_list():
    """FR04 员工总览：查所有未归档员工并渲染列表页。"""
    employees = EmployeeDAO.get_all_active()
    return render_template("employees.html", employees=employees)