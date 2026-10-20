"""
statistics_service.py - FR12 & FR14: 统计报表分析模块
"""
from typing import Dict, Any
from database import Database

class StatisticsService:
    def __init__(self, db: Database):
        self.db = db

    def get_overview_statistics(self) -> Dict[str, Any]:
        """统计员工总人数、平均时薪、部门数"""
        total_employees = len(self.db.employees)
        if total_employees == 0:
            return {"total_employees": 0, "avg_hourly_rate": 0, "total_departments": 0}

        avg_hourly_rate = sum(e.hourly_rate for e in self.db.employees) / total_employees
        departments = set(e.department for e in self.db.employees)

        return {
            "total_employees": total_employees,
            "avg_hourly_rate": round(avg_hourly_rate, 2),
            "total_departments": len(departments),
            "department_list": list(departments)
        }

    def get_department_distribution(self) -> Dict[str, int]:
        """统计每个部门的员工分布"""
        distribution: Dict[str, int] = {}
        for emp in self.db.employees:
            distribution[emp.department] = distribution.get(emp.department, 0) + 1
        return distribution

    def get_shift_statistics(self) -> Dict[str, Any]:
        """统计班次分布（Morning / Afternoon / Evening）及计划总工时"""
        period_counts = {"Morning": 0, "Afternoon": 0, "Evening": 0}
        total_scheduled_hours = 0.0

        for shift in self.db.shifts:
            if shift.period in period_counts:
                period_counts[shift.period] += 1
            total_scheduled_hours += shift.hours

        return {
            "total_shifts": len(self.db.shifts),
            "total_scheduled_hours": total_scheduled_hours,
            "period_breakdown": period_counts
        }