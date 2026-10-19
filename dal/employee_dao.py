# 文件：dal/employee_dao.py
# DAL 数据访问层：员工数据访问对象（DAO）
# 封装员工相关的数据库查询；UI 层只调用这里的方法，不直接接触 SQL。
# 安全要求：所有查询必须使用参数化（%s 占位 + 参数元组），禁止字符串拼接 SQL。

from dal.db import get_connection
from model.employee import Employee


class EmployeeDAO:
    """员工表的数据访问对象。"""

    @staticmethod
    def get_all_active():
        """
        查询所有「未归档」员工（is_archived = 0），返回 Employee 列表。
        对应需求 FR04（查看员工总览）。
        """
        sql = (
            "SELECT id, employee_id, name, age, position, salary, department, "
            "email, contact_address, emergency_contact, is_archived "
            "FROM employee WHERE is_archived = %s ORDER BY id"
        )
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(sql, (0,))  # 参数化查询
                rows = cur.fetchall()
            return [Employee(*row) for row in rows]
        finally:
            conn.close()
