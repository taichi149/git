"""
self_service.py - FR15: 员工自助服务（登录、查看资料、更新个人邮箱）
"""
import re
from typing import Tuple, Optional
from database import Database
from models import Employee

class SelfServicePortal:
    def __init__(self, db: Database):
        self.db = db

    @staticmethod
    def validate_email(email: str) -> bool:
        """邮箱格式正则校验"""
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return bool(re.match(pattern, email.strip()))

    def authenticate(self, emp_id: str, password: str) -> Optional[Employee]:
        """员工身份验证"""
        emp = self.db.get_employee_by_id(emp_id)
        if emp and emp.password == password:
            return emp
        return None

    def update_own_email(self, emp_id: str, new_email: str) -> Tuple[bool, str]:
        """
        员工修改自身邮箱（含验证与防重逻辑）
        """
        emp = self.db.get_employee_by_id(emp_id)
        if not emp:
            return False, "未找到该员工账户！"

        new_email = new_email.strip()
        if not self.validate_email(new_email):
            return False, "邮箱格式不合法，请输入正确的邮箱地址（例如 user@example.com）！"

        # 检查是否与其他员工冲突
        for other in self.db.employees:
            if other.emp_id != emp_id and other.email.lower() == new_email.lower():
                return False, "该邮箱已被其他员工绑定，请更换！"

        old_email = emp.email
        emp.email = new_email
        self.db.save_employees()
        return True, f"邮箱修改成功：{old_email} -> {new_email}"