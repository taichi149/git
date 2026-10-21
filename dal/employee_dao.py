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

    @staticmethod
    def get_by_username(username):
        """
        按登录用户名查员工（约定：员工登录账号 = 邮箱 @ 前缀，如 zhangsan ↔ zhangsan@meiti.com）。
        对应 FR14（查看本人档案）/ FR15（修改个人信息）。找不到返回 None。
        """
        sql = (
            "SELECT id, employee_id, name, age, position, salary, department, "
            "email, contact_address, emergency_contact, is_archived "
            "FROM employee WHERE email LIKE %s AND is_archived = %s LIMIT 1"
        )
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(sql, (username + "@%", 0))  # 参数化查询
                row = cur.fetchone()
            return Employee(*row) if row else None
        finally:
            conn.close()

    @staticmethod
    def update_self(employee_id, email, contact_address, emergency_contact):
        """
        员工自助修改邮箱 / 联系地址 / 紧急联系人（FR15）。
        薪资、岗位、部门不在本方法更新——员工无权修改。
        """
        sql = (
            "UPDATE employee SET email = %s, contact_address = %s, "
            "emergency_contact = %s WHERE id = %s"
        )
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(sql, (email, contact_address, emergency_contact, employee_id))
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def get_statistics():
        """
        统计（FR12）：员工总人数 + 分部门人数。
        返回 dict：{"total": int, "by_department": [(department, count), ...]}
        """
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT COUNT(*) FROM employee WHERE is_archived = %s", (0,))
                total = cur.fetchone()[0]
                cur.execute(
                    "SELECT department, COUNT(*) AS cnt FROM employee "
                    "WHERE is_archived = %s GROUP BY department ORDER BY cnt DESC",
                    (0,),
                )
                by_dept = cur.fetchall()
            return {"total": total, "by_department": by_dept}
        finally:
            conn.close()
