# 文件：dal/shift_dao.py
# DAL 数据访问层：排班数据访问对象（DAO）
# M4 手动排班（FR10 排班 / FR11 个人排班视图 / FR13 全店排班视图）。
# 安全要求：所有查询必须使用参数化（%s 占位 + 参数元组），禁止字符串拼接 SQL。

from dal.db import get_connection
from model.shift import Shift


class ShiftDAO:
    """排班表（shift）的数据访问对象。"""

    @staticmethod
    def get_by_employee_range(emp_pk, start_date, end_date):
        """
        FR11 个人排班：查询某员工在 [start_date, end_date] 内的排班，按日期排序。
        返回 Shift 列表（只有排班表自身的 4 个字段）。
        """
        sql = (
            "SELECT id, employee_id, shift_date, shift_type "
            "FROM shift "
            "WHERE employee_id = %s AND shift_date BETWEEN %s AND %s "
            "ORDER BY shift_date"
        )
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(sql, (emp_pk, start_date, end_date))  # 参数化查询
                rows = cur.fetchall()
            return [Shift(*row) for row in rows]
        finally:
            conn.close()

    @staticmethod
    def get_store_range(start_date, end_date):
        """
        FR13 全店排班：查询一段时间内所有「在职员工」的排班。
        联查 employee 表带上工号和姓名，方便页面直接显示；
        返回的 Shift 对象会多出 employee_code / employee_name 两个属性。
        """
        sql = (
            "SELECT s.id, s.employee_id, s.shift_date, s.shift_type, "
            "       e.employee_id, e.name "
            "FROM shift s "
            "JOIN employee e ON e.id = s.employee_id "
            "WHERE e.is_archived = %s AND s.shift_date BETWEEN %s AND %s "
            "ORDER BY e.id, s.shift_date"
        )
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(sql, (0, start_date, end_date))  # 参数化查询
                rows = cur.fetchall()
            return [Shift(*row) for row in rows]
        finally:
            conn.close()

    @staticmethod
    def assign(shift):
        """
        FR10 排班 / 改班：写入一条排班。
        表上有 (employee_id, shift_date) 唯一键，所以同一员工同一天再排班时，
        会自动覆盖旧班次（ON DUPLICATE KEY UPDATE），实现「改班」。
        返回受影响行数（1=新排，2=改班）。
        """
        sql = (
            "INSERT INTO shift (employee_id, shift_date, shift_type) "
            "VALUES (%s, %s, %s) "
            "ON DUPLICATE KEY UPDATE shift_type = VALUES(shift_type)"
        )
        params = (shift.employee_id, shift.shift_date, shift.shift_type)
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(sql, params)
                affected = cur.rowcount
            conn.commit()
            return affected
        finally:
            conn.close()

    @staticmethod
    def delete(shift_id):
        """删除一条排班（按排班表主键 id）。返回受影响行数。"""
        sql = "DELETE FROM shift WHERE id = %s"
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(sql, (shift_id,))
                affected = cur.rowcount
            conn.commit()
            return affected
        finally:
            conn.close()
