# 文件：model/user.py
# Model 层：账号实体类


class User:
    def __init__(self, id=None, username=None, hashed_password=None, role=None):
        self.id = id
        self.username = username
        self.hashed_password = hashed_password
        self.role = role