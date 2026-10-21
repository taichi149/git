# 文件：dal/employee_dao.py
# DAL 数据访问层：员工数据访问对象（DAO）
# 封装员工相关的数据库查询；UI 层只调用这里的方法，不直接接触 SQL。
# 安全要求：所有查询必须使用参数化（%s 占位 + 参数元组），禁止字符串拼接 SQL。

from dal.db import get_connection
from model.employee import Employee


class EmployeeDAO:
    """员工表的数据访问对象（M3 增删改查 + M5 统计/自助）。"""

    # ------------------------------------------------------------------
    # 查询
    # ------------------------------------------------------------------
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
    def get_all_archived():
        """查询所有「已归档」员工，供总览页的「已归档」视图使用。"""
        sql = (
            "SELECT id, employee_id, name, age, position, salary, department, "
            "email, contact_address, emergency_contact, is_archived "
            "FROM employee WHERE is_archived = %s ORDER BY id"
        )
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(sql, (1,))
                rows = cur.fetchall()
            return [Employee(*row) for row in rows]
        finally:
            conn.close()

    @staticmethod
    def search(keyword, archived=0):
        """
        FR05 检索：按姓名 / 工号 / 岗位 / 部门 / 邮箱 / 地址模糊匹配。
        keyword 作为参数传入 LIKE，不做字符串拼接（防 SQL 注入）。
        """
        like = "%" + keyword + "%"
        sql = (
            "SELECT id, employee_id, name, age, position, salary, department, "
            "email, contact_address, emergency_contact, is_archived "
            "FROM employee "
            "WHERE is_archived = %s AND ("
            "name LIKE %s OR employee_id LIKE %s OR position LIKE %s "
            "OR department LIKE %s OR email LIKE %s OR contact_address LIKE %s"
            ") ORDER BY id"
        )
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(sql, (archived, like, like, like, like, like, like))
                rows = cur.fetchall()
            return [Employee(*row) for row in rows]
        finally:
            conn.close()

    @staticmethod
    def get_by_pk(emp_pk):
        """
        FR07 详情：按主键 id 查询单个员工；不存在返回 None。
        注意：这里用表主键 id，不是业务工号 employee_id。
        """
        sql = (
            "SELECT id, employee_id, name, age, position, salary, department, "
            "email, contact_address, emergency_contact, is_archived "
            "FROM employee WHERE id = %s"
        )
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(sql, (emp_pk,))
                row = cur.fetchone()
            return Employee(*row) if row else None
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
    def employee_id_exists(employee_id, exclude_pk=None):
        """
        校验工号是否已被占用（新增 / 修改时用）。
        exclude_pk：修改时排除自己这条记录。
        """
        if exclude_pk is None:
            sql = "SELECT 1 FROM employee WHERE employee_id = %s LIMIT 1"
            params = (employee_id,)
        else:
            sql = "SELECT 1 FROM employee WHERE employee_id = %s AND id <> %s LIMIT 1"
            params = (employee_id, exclude_pk)

        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(sql, params)
                return cur.fetchone() is not None
        finally:
            conn.close()

    # ------------------------------------------------------------------
    # 写入
    # ------------------------------------------------------------------
    @staticmethod
    def create(employee):
        """
        FR01 新增员工：插入一条记录，返回新记录的主键 id。
        is_archived 默认 0（未归档）。
        """
        sql = (
            "INSERT INTO employee (employee_id, name, age, position, salary, "
            "department, email, contact_address, emergency_contact, is_archived) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        )
        params = (
            employee.employee_id,
            employee.name,
            employee.age,
            employee.position,
            employee.salary,
            employee.department,
            employee.email,
            employee.contact_address,
            employee.emergency_contact,
            0,
        )
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(sql, params)
                new_id = cur.lastrowid
            conn.commit()
            return new_id
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
    def update(employee):
        """
        FR02 修改员工：按主键更新档案字段（不动 is_archived）。
        返回受影响行数（0 表示记录不存在或已被归档）。
        """
        sql = (
            "UPDATE employee SET employee_id = %s, name = %s, age = %s, "
            "position = %s, salary = %s, department = %s, email = %s, "
            "contact_address = %s, emergency_contact = %s "
            "WHERE id = %s AND is_archived = 0"
        )
        params = (
            employee.employee_id,
            employee.name,
            employee.age,
            employee.position,
            employee.salary,
            employee.department,
            employee.email,
            employee.contact_address,
            employee.emergency_contact,
            employee.id,
        )
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
    def set_archived(emp_pk, archived):
        """
        FR03 软归档 / 恢复：只改 is_archived 标志，不物理删除记录。
        历史数据（排班、统计）因此不会因为「删除员工」而断链。
        """
        sql = "UPDATE employee SET is_archived = %s WHERE id = %s"
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(sql, (1 if archived else 0, emp_pk))
                affected = cur.rowcount
            conn.commit()
            return affected
        finally:
            conn.close()

    # ------------------------------------------------------------------
    # 统计
    # ------------------------------------------------------------------
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
