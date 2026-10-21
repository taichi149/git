# 文件：config.py
# 全局配置：数据库连接 + Flask 设置

DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "zhong1653",
    "database": "hardware_store",
    "charset": "utf8mb4",
}

DEBUG = True
SECRET_KEY = "meiti-shangcheng-demo-secret-key"