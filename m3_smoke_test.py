"""M3 冒烟测试：不依赖 MySQL，用内存假 DAO 跑通所有路由与模板。

运行（在项目根目录、已装好 flask/pymysql 的 venv 里）：
  set PYTHONPATH=.
  python tests\\m3_smoke_test.py
"""

import os
import sys

PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT)

from werkzeug.security import generate_password_hash  # noqa: E402

from model.employee import Employee  # noqa: E402
from model.user import User  # noqa: E402

import ui.routes as routes  # noqa: E402
from app import app  # noqa: E402


# ---------------------------------------------------------------- fake DAL
class FakeEmployeeDAO:
    rows = {}
    seq = 0

    @classmethod
    def reset(cls):
        cls.rows = {}
        cls.seq = 0
        cls.add(Employee(employee_id="E001", name="张三", age=28, position="收银员",
                         salary=5000, department="门店", email="zs@example.com",
                         contact_address="郑州", emergency_contact="李四 13800000000"))
        cls.add(Employee(employee_id="E002", name="李四", age=35, position="库管",
                         salary=6000, department="仓库", email="ls@example.com",
                         contact_address="郑州", emergency_contact="张三 13900000000"))

    @classmethod
    def add(cls, emp):
        cls.seq += 1
        emp.id = cls.seq
        emp.is_archived = 0
        cls.rows[emp.id] = emp
        return emp.id

    @classmethod
    def get_all_active(cls):
        return [e for e in cls.rows.values() if not e.is_archived]

    @classmethod
    def get_all_archived(cls):
        return [e for e in cls.rows.values() if e.is_archived]

    @classmethod
    def search(cls, keyword, archived=0):
        kw = keyword.lower()
        out = []
        for e in cls.rows.values():
            if bool(e.is_archived) != bool(archived):
                continue
            hay = " ".join(str(x or "") for x in
                           (e.name, e.employee_id, e.position, e.department,
                            e.email, e.contact_address)).lower()
            if kw in hay:
                out.append(e)
        return out

    @classmethod
    def get_by_pk(cls, pk):
        return cls.rows.get(pk)

    @classmethod
    def employee_id_exists(cls, employee_id, exclude_pk=None):
        return any(e.employee_id == employee_id and e.id != exclude_pk
                   for e in cls.rows.values())

    @classmethod
    def create(cls, emp):
        return cls.add(emp)

    @classmethod
    def update(cls, emp):
        old = cls.rows.get(emp.id)
        if old is None or old.is_archived:
            return 0
        cls.rows[emp.id] = emp
        return 1

    @classmethod
    def set_archived(cls, pk, archived):
        e = cls.rows.get(pk)
        if e is None:
            return 0
        e.is_archived = 1 if archived else 0
        return 1


class FakeUserDAO:
    @staticmethod
    def get_by_username(username):
        users = {
            "hr": ("hr", "hr123", "HRAdmin"),
            "manager": ("manager", "manager123", "StoreManager"),
        }
        if username not in users:
            return None
        _, pw, role = users[username]
        return User(id=1, username=username,
                    hashed_password=generate_password_hash(pw), role=role)


routes.EmployeeDAO = FakeEmployeeDAO
routes.UserDAO = FakeUserDAO

app.config["WTF_CSRF_ENABLED"] = False
app.config["TESTING"] = True

FAILS = []


def check(name, cond, extra=""):
    if cond:
        print("  PASS", name)
    else:
        print("  FAIL", name, extra)
        FAILS.append(name)


def login(client, username="hr", password="hr123"):
    return client.post("/login", data={"username": username, "password": password},
                       follow_redirects=False)


def main():
    FakeEmployeeDAO.reset()
    client = app.test_client()

    print("[1] 未登录访问受保护页面")
    r = client.get("/employees")
    check("未登录跳转登录页", r.status_code == 302 and "/login" in r.headers["Location"])

    print("[2] 登录")
    r = client.post("/login", data={"username": "hr", "password": "wrong"})
    check("错误密码提示", r.status_code == 200 and "用户名或密码错误" in r.get_data(as_text=True))
    r = login(client)
    check("HR 登录成功跳转", r.status_code == 302 and "/employees" in r.headers["Location"])

    print("[3] 列表 + 检索")
    r = client.get("/employees")
    body = r.get_data(as_text=True)
    check("列表返回 200", r.status_code == 200)
    check("列表含张三", "张三" in body)
    check("列表含新增按钮", "新增员工" in body)
    r = client.get("/employees?q=库管")
    body = r.get_data(as_text=True)
    check("检索命中李四", "李四" in body and "张三" not in body)
    r = client.get("/employees?q=不存在的人")
    check("检索无结果显示空态", "没有匹配" in r.get_data(as_text=True))

    print("[4] 新增员工（合法）")
    r = client.post("/employees/new", data={
        "employee_id": "E003", "name": "王五", "age": "30", "position": "理货员",
        "salary": "4800.50", "department": "门店", "email": "ww@example.com",
        "contact_address": "郑州二七区", "emergency_contact": "王父 13700000000",
    })
    check("新增后重定向到列表", r.status_code == 302)
    wang = [e for e in FakeEmployeeDAO.get_all_active() if e.name == "王五"]
    check("数据库里新增成功", len(wang) == 1)
    check("工号保存正确", wang and wang[0].employee_id == "E003")
    wang_pk = wang[0].id

    print("[5] 新增校验")
    r = client.post("/employees/new", data={
        "employee_id": "", "name": "", "age": "9", "salary": "abc", "email": "bad-email",
    })
    body = r.get_data(as_text=True)
    check("必填校验", "工号不能为空" in body and "姓名不能为空" in body)
    check("年龄范围校验", "年龄需在 16~100 之间" in body)
    check("薪资数字校验", "薪资必须是数字" in body)
    check("邮箱格式校验", "邮箱格式不正确" in body)
    check("校验失败不写库", len(FakeEmployeeDAO.get_all_active()) == 3)
    r = client.post("/employees/new", data={
        "employee_id": "E001", "name": "重复工号",
    })
    check("工号唯一性校验", "该工号已存在" in r.get_data(as_text=True))

    print("[6] 详情")
    r = client.get("/employees/%d" % wang_pk)
    body = r.get_data(as_text=True)
    check("详情 200", r.status_code == 200)
    check("详情字段齐全", all(k in body for k in ("E003", "王五", "理货员", "4800.50", "ww@example.com")))
    r = client.get("/employees/99999")
    check("不存在返回 404", r.status_code == 404)

    print("[7] 修改")
    r = client.post("/employees/%d/edit" % wang_pk, data={
        "employee_id": "E003", "name": "王五五", "age": "31", "position": "主管",
        "salary": "5500", "department": "门店", "email": "ww@example.com",
        "contact_address": "郑州金水区", "emergency_contact": "王父 13700000000",
    })
    check("修改后重定向到详情", r.status_code == 302 and "/employees/%d" % wang_pk in r.headers["Location"])
    updated = FakeEmployeeDAO.get_by_pk(wang_pk)
    check("字段已更新", updated.name == "王五五" and updated.position == "主管" and updated.age == 31)
    r = client.get("/employees/%d/edit" % wang_pk)
    body = r.get_data(as_text=True)
    check("编辑页回填", 'value="王五五"' in body and 'value="主管"' in body)

    print("[8] 软归档")
    r = client.get("/employees/%d/archive" % wang_pk)
    body = r.get_data(as_text=True)
    check("归档确认页", r.status_code == 200 and "确认归档" in body and "不会被删除" in body)
    r = client.post("/employees/%d/archive" % wang_pk)
    check("归档后重定向", r.status_code == 302)
    check("记录仍在库里", FakeEmployeeDAO.get_by_pk(wang_pk) is not None)
    check("标记为已归档", FakeEmployeeDAO.get_by_pk(wang_pk).is_archived == 1)
    client.get("/employees")  # 先消费掉 flash 提示，避免它把姓名带进页面
    body = client.get("/employees").get_data(as_text=True)
    check("在职列表不再显示", "王五五" not in body)
    body = client.get("/employees?archived=1").get_data(as_text=True)
    check("已归档视图显示", "王五五" in body)
    r = client.get("/employees/%d/edit" % wang_pk)
    check("已归档不可编辑", r.status_code == 302)

    print("[9] 恢复")
    r = client.post("/employees/%d/restore" % wang_pk)
    check("恢复后重定向", r.status_code == 302)
    check("恢复为在职", FakeEmployeeDAO.get_by_pk(wang_pk).is_archived == 0)
    body = client.get("/employees").get_data(as_text=True)
    check("在职列表重新出现", "王五五" in body)

    print("[10] 角色权限")
    client2 = app.test_client()
    login(client2, "manager", "manager123")
    r = client2.get("/employees")
    check("StoreManager 可查看列表", r.status_code == 200)
    body = r.get_data(as_text=True)
    check("StoreManager 看不到新增按钮", "新增员工" not in body)
    r = client2.get("/employees/new")
    check("StoreManager 不能新增（403）", r.status_code == 403)
    r = client2.get("/employees/%d/edit" % wang_pk)
    check("StoreManager 不能编辑（403）", r.status_code == 403)
    r = client2.post("/employees/%d/archive" % wang_pk)
    check("StoreManager 不能归档（403）", r.status_code == 403)
    r = client2.get("/employees/%d" % wang_pk)
    check("StoreManager 可看详情", r.status_code == 200)

    print()
    if FAILS:
        print("FAILED:", len(FAILS), FAILS)
        return 1
    print("ALL PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
