# 文件：seed_users.py
# 一次性脚本：把 user 表里的占位密码（demo_hash_*）替换为真实密码哈希。
# 运行：.venv/Scripts/python.exe seed_users.py
# 说明：M2 登录认证依赖真实的哈希密码，本脚本用 werkzeug 生成并写回数据库。

from werkzeug.security import generate_password_hash

from dal.db import get_connection

# 演示用初始账号与明文密码（登录后可按需改）
INITIAL_ACCOUNTS = {
    "hr": "hr123",
    "manager": "manager123",
    "zhangsan": "zhangsan123",
}


def seed():
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            for username, password in INITIAL_ACCOUNTS.items():
                hashed = generate_password_hash(password)
                cur.execute(
                    "UPDATE user SET hashed_password = %s WHERE username = %s",
                    (hashed, username),  # 参数化查询
                )
        conn.commit()
    finally:
        conn.close()
    print(f"完成：已更新 {len(INITIAL_ACCOUNTS)} 个账号的密码哈希")


if __name__ == "__main__":
    seed()
