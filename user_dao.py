# 文件：dal/user_dao.py
# DAL 数据访问层：账号数据访问对象（DAO）
# 封装账号相关的数据库查询；参数化查询，禁止字符串拼接 SQL。

from dal.db import get_connection
from model.user import User


class UserDAO:
    """账号表（user）的数据访问对象。"""

    @staticmethod
    def get_by_username(username):
        """
        按用户名查询账号，返回 User 对象；不存在返回 None。
        对应需求 FR09（登录认证）。
        """
        sql = "SELECT id, username, hashed_password, role FROM user WHERE username = %s"
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(sql, (username,))  # 参数化查询
                row = cur.fetchone()
            return User(*row) if row else None
        finally:
            conn.close()
