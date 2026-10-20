"""
database.py - 本地 JSON 数据持久化
"""
import json
import os
from typing import List, Optional
from models import Employee, Shift

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
EMP_FILE = os.path.join(DATA_DIR, "employees.json")
SHIFT_FILE = os.path.join(DATA_DIR, "shifts.json")


class Database:
    def __init__(self):
        os.makedirs(DATA_DIR, exist_ok=True)
        self.employees: List[Employee] = []
        self.shifts: List[Shift] = []
        self.load_data()

    def load_data(self):
        # 初始化员工数据
        if os.path.exists(EMP_FILE):
            with open(EMP_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.employees = [Employee.from_dict(item) for item in data]
        else:
            self._seed_default_employees()

        # 初始化排班数据
        if os.path.exists(SHIFT_FILE):
            with open(SHIFT_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.shifts = [Shift.from_dict(item) for item in data]
        else:
            self._seed_default_shifts()

    def save_employees(self):
        with open(EMP_FILE, "w", encoding="utf-8") as f:
            json.dump([e.to_dict() for e in self.employees], f, ensure_ascii=False, indent=2)

    def save_shifts(self):
        with open(SHIFT_FILE, "w", encoding="utf-8") as f:
            json.dump([s.to_dict() for s in self.shifts], f, ensure_ascii=False, indent=2)

    def get_employee_by_id(self, emp_id: str) -> Optional[Employee]:
        for emp in self.employees:
            if emp.emp_id == emp_id:
                return emp
        return None

    def _seed_default_employees(self):
        self.employees = [
            Employee("E001", "张三", "zhangsan@meiti.com", "123456", "Hardware", 25.0, "Employee"),
            Employee("E002", "李四", "lisi@meiti.com", "123456", "Electronics", 28.0, "Employee"),
            Employee("E003", "王五", "wangwu@meiti.com", "123456", "Hardware", 22.0, "Employee"),
            Employee("E004", "赵主管", "manager@meiti.com", "admin888", "Management", 45.0, "Manager"),
        ]
        self.save_employees()

    def _seed_default_shifts(self):
        self.shifts = [
            Shift("S01", "E001", "2026-10-21", "Morning", 8.0),
            Shift("S02", "E002", "2026-10-21", "Afternoon", 8.0),
            Shift("S03", "E003", "2026-10-21", "Evening", 8.0),
            Shift("S04", "E001", "2026-10-22", "Afternoon", 8.0),
        ]
        self.save_shifts()