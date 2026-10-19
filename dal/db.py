# 文件：dal/db.py
# DAL 数据访问层：封装数据库连接
# 注意：后续所有查询必须使用参数化，禁止字符串拼接 SQL（防 SQL 注入）

import pymysql
import config


def get_connection():
    """获取数据库连接，用完记得 close()"""
    return pymysql.connect(**config.DB_CONFIG)