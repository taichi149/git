"""
models.py - 数据模型定义
"""
from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class Employee:
    emp_id: str
    name: str
    email: str
    password: str
    department: str
    hourly_rate: float
    role: str = "Employee"  # Role: Employee / Manager / Admin

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)


@dataclass
class Shift:
    shift_id: str
    emp_id: str
    date: str           # YYYY-MM-DD
    period: str         # Morning / Afternoon / Evening
    hours: float = 8.0

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)