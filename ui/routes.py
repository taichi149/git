# 文件：ui/routes.py
# UI 层：路由，只负责界面展示交互，不在这里写 SQL

from flask import Blueprint

ui_bp = Blueprint("ui", __name__)


@ui_bp.route("/")
def home():
    return "Employee Management System - Home Page"