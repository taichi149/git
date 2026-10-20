"""M4 冒烟测试：不依赖 MySQL，用内存假 DAO 跑通排班相关的路由与模板。

运行（在项目根目录、已装好 flask/pymysql 的 venv 里）：
  set PYTHONPATH=.          （Windows；macOS/Linux 用 export PYTHONPATH=.）
  python m4_smoke_test.py
"""

import os
import sys
from datetime import date, timedelta

PROJECT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT)

from werkzeug.security import generate_password_hash  # noqa: E402

from model.employee import Employee  # noqa: E402
from model.shift import Shift  # noqa: E402
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
        cls.add(Employee(employee_id="E001", name="张三", position="收银员"))
        cls.add(Employee(employee_id="E002", name="李四", position="库管"))
        archived = cls.add(Employee(employee_id="E003", name="王五", position="理货员"))
        cls.rows[archived].is_archived = 1  # 王五已归档

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
    def get_by_pk(cls, emp_pk):
        return cls.rows.get(emp_pk)


class FakeUserDAO:
    users = {}

    @classmethod
    def reset(cls):
        cls.users = {
            "hr": User(1, "hr", generate_password_hash("hr123"), "HRAdmin"),
            "manager": User(2, "manager", generate_password_hash("manager123"),
                            "StoreManager"),
            "zhangsan": User(3, "zhangsan", generate_password_hash("zhangsan123"),
                             "Employee"),
        }

    @classmethod
    def get_by_username(cls, username):
        return cls.users.get(username)


class FakeShiftDAO:
    rows = {}
    seq = 0

    @classmethod
    def reset(cls):
        cls.rows = {}
        cls.seq = 0

    @classmethod
    def _wrap(cls, s):
        """模拟联查：给 Shift 补上工号姓名（get_store_range 的效果）。"""
        e = FakeEmployeeDAO.rows.get(s.employee_id)
        if e:
            s.employee_code = e.employee_id
            s.employee_name = e.name
        return s

    @classmethod
    def get_by_employee_range(cls, emp_pk, start, end):
        out = [s for s in cls.rows.values()
               if s.employee_id == emp_pk and start <= s.shift_date <= end]
        return sorted(out, key=lambda s: s.shift_date)

    @classmethod
    def get_store_range(cls, start, end):
        out = []
        for s in cls.rows.values():
            e = FakeEmployeeDAO.rows.get(s.employee_id)
            if e and not e.is_archived and start <= s.shift_date <= end:
                out.append(cls._wrap(s))
        return out

    @classmethod
    def assign(cls, shift):
        # 唯一键效果：同一员工同一天覆盖旧班次（改班）
        for old in cls.rows.values():
            if (old.employee_id == shift.employee_id
                    and old.shift_date == shift.shift_date):
                old.shift_type = shift.shift_type
                return 2
        cls.seq += 1
        shift.id = cls.seq
        cls.rows[shift.id] = shift
        return 1

    @classmethod
    def delete(cls, shift_id):
        return 1 if cls.rows.pop(shift_id, None) else 0


# ---------------------------------------------------------------- 测试辅助
routes.EmployeeDAO = FakeEmployeeDAO
routes.UserDAO = FakeUserDAO
routes.ShiftDAO = FakeShiftDAO

app.config["TESTING"] = True
app.config["WTF_CSRF_ENABLED"] = False

TODAY = date.today()
MONDAY = TODAY - timedelta(days=TODAY.weekday())

passed = []
failed = []


def check(name, ok):
    (passed if ok else failed).append(name)
    print(("  PASS " if ok else "  FAIL ") + name)


def login(client, username, password):
    return client.post("/login", data={"username": username, "password": password},
                       follow_redirects=False)


def reset():
    FakeEmployeeDAO.reset()
    FakeUserDAO.reset()
    FakeShiftDAO.reset()


# ---------------------------------------------------------------- 用例
def t1_login_required():
    print("[1] 未登录拦截")
    reset()
    c = app.test_client()
    r = c.get("/shifts/week")
    check("未登录访问全店排班 → 跳登录页", r.status_code == 302 and "/login" in r.headers["Location"])
    r = c.get("/shifts/assign")
    check("未登录访问排班表单 → 跳登录页", r.status_code == 302 and "/login" in r.headers["Location"])


def t2_assign_form():
    print("[2] 排班表单")
    reset()
    c = app.test_client()
    login(c, "hr", "hr123")
    r = c.get("/shifts/assign")
    check("HR 打开排班表单 200", r.status_code == 200)
    check("下拉里有在职员工张三", "张三".encode() in r.data)
    check("下拉里没有已归档的王五", "王五".encode() not in r.data)
    r = c.get("/shifts/assign?emp_pk=1&date=%s" % TODAY.isoformat())
    check("URL 参数预填员工和日期", ('value="%s"' % TODAY.isoformat()).encode() in r.data)


def t3_assign_post():
    print("[3] 排班提交 / 改班")
    reset()
    c = app.test_client()
    login(c, "hr", "hr123")
    r = c.post("/shifts/assign", data={
        "emp_pk": "1", "shift_date": TODAY.isoformat(), "shift_type": "Morning",
    })
    check("排班成功 → 302 跳周视图", r.status_code == 302 and "week=" in r.headers["Location"])
    check("DAO 里多了一条早班", len(FakeShiftDAO.rows) == 1
          and list(FakeShiftDAO.rows.values())[0].shift_type == "Morning")
    # 同一员工同一天再排 = 改班
    c.post("/shifts/assign", data={
        "emp_pk": "1", "shift_date": TODAY.isoformat(), "shift_type": "Evening",
    })
    check("同一天再排 → 覆盖为晚班（只有一条记录）",
          len(FakeShiftDAO.rows) == 1
          and list(FakeShiftDAO.rows.values())[0].shift_type == "Evening")


def t4_validation():
    print("[4] 表单校验")
    reset()
    c = app.test_client()
    login(c, "hr", "hr123")
    r = c.post("/shifts/assign", data={
        "emp_pk": "", "shift_date": "", "shift_type": "",
    })
    check("全空 → 重新渲染并提示请选择员工", "请选择员工".encode() in r.data)
    check("提示请选择班次", "请选择班次".encode() in r.data)
    r = c.post("/shifts/assign", data={
        "emp_pk": "1", "shift_date": "2026-13-99", "shift_type": "Morning",
    })
    check("非法日期 → 提示日期格式不正确", "日期格式不正确".encode() in r.data)
    r = c.post("/shifts/assign", data={
        "emp_pk": "3", "shift_date": TODAY.isoformat(), "shift_type": "Morning",
    })
    check("给已归档员工排班 → 拒绝", "已归档".encode() in r.data
          and len(FakeShiftDAO.rows) == 0)


def t5_week_view():
    print("[5] 全店周视图（FR13）")
    reset()
    FakeShiftDAO.assign(Shift(employee_id=1, shift_date=MONDAY, shift_type="Morning"))
    FakeShiftDAO.assign(Shift(employee_id=2, shift_date=MONDAY + timedelta(days=1),
                              shift_type="Evening"))
    c = app.test_client()
    login(c, "manager", "manager123")
    r = c.get("/shifts/week?week=%s" % MONDAY.isoformat())
    check("经理打开周视图 200", r.status_code == 200)
    check("显示员工张三", "张三".encode() in r.data)
    check("显示早班标签", "早班".encode() in r.data)
    check("显示晚班标签", "晚班".encode() in r.data)
    check("有上一周/下一周导航", "上一周".encode() in r.data and "下一周".encode() in r.data)
    check("经理看不到排班按钮（只读）", ">+ 排班</a>".encode() not in r.data)
    login(c, "hr", "hr123")
    r = c.get("/shifts/week")
    check("HR 能看到 + 排班按钮", ">+ 排班</a>".encode() in r.data)


def t6_employee_shifts():
    print("[6] 个人排班视图（FR11）")
    reset()
    FakeShiftDAO.assign(Shift(employee_id=1, shift_date=MONDAY, shift_type="Afternoon"))
    FakeShiftDAO.assign(Shift(employee_id=2, shift_date=MONDAY, shift_type="Evening"))
    c = app.test_client()
    login(c, "hr", "hr123")
    r = c.get("/employees/1/shifts?week=%s" % MONDAY.isoformat())
    check("打开张三的排班 200", r.status_code == 200)
    check("标题是张三的排班", "张三 的排班".encode() in r.data)
    check("显示中班（张三的）", "中班".encode() in r.data)
    check("不显示晚班（李四的）", "晚班".encode() not in r.data)
    check("本周共排班 1 天", "本周共排班 1 天".encode() in r.data)
    r = c.get("/employees/999/shifts")
    check("不存在的员工 → 404", r.status_code == 404)


def t7_delete():
    print("[7] 删除排班")
    reset()
    FakeShiftDAO.assign(Shift(employee_id=1, shift_date=TODAY, shift_type="Morning"))
    sid = 1
    c = app.test_client()
    login(c, "hr", "hr123")
    r = c.post("/shifts/%d/delete" % sid, data={"next": "/shifts/week"})
    check("删除成功 → 302 跳回 next", r.status_code == 302 and r.headers["Location"] == "/shifts/week")
    check("DAO 里记录没了", len(FakeShiftDAO.rows) == 0)
    r = c.post("/shifts/999/delete")
    check("删不存在的记录 → 不报错", r.status_code == 302)


def t8_roles():
    print("[8] 角色权限")
    reset()
    c = app.test_client()
    login(c, "manager", "manager123")
    check("经理不能打开排班表单（403）", c.get("/shifts/assign").status_code == 403)
    check("经理不能提交排班（403）", c.post("/shifts/assign", data={}).status_code == 403)
    check("经理不能删除排班（403）", c.post("/shifts/1/delete").status_code == 403)
    check("经理能看全店周视图", c.get("/shifts/week").status_code == 200)
    check("经理能看个人排班", c.get("/employees/1/shifts").status_code == 200)
    c2 = app.test_client()
    login(c2, "zhangsan", "zhangsan123")
    check("普通员工不能看周视图（403）", c2.get("/shifts/week").status_code == 403)
    check("普通员工不能排班（403）", c2.get("/shifts/assign").status_code == 403)


def t9_employee_list_entry():
    print("[9] 员工列表入口")
    reset()
    c = app.test_client()
    login(c, "hr", "hr123")
    r = c.get("/employees")
    check("员工列表有「排班」入口", "排班".encode() in r.data)


if __name__ == "__main__":
    t1_login_required()
    t2_assign_form()
    t3_assign_post()
    t4_validation()
    t5_week_view()
    t6_employee_shifts()
    t7_delete()
    t8_roles()
    t9_employee_list_entry()
    print()
    if failed:
        print("FAILED: %d 项未通过 -> %s" % (len(failed), failed))
        sys.exit(1)
    print("ALL PASS（共 %d 项）" % len(passed))
