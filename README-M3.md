# M3：员工增删改查（Employee CRUD）

本目录是基于仓库 `taichi149/git` **feature 分支**（已含 M2 登录 + 员工列表）完成的 M3 实现。
按里程碑定义，M3 = 员工增 / 改 / 软归档 / 检索 / 详情，完成标准是「全部跑通」。

---

## 1. 本次改了什么

| 文件 | 类型 | 说明 |
|---|---|---|
| `dal/employee_dao.py` | 重写 | 从「只有 get_all_active」扩展为完整 DAO：详情 / 检索 / 工号查重 / 新增 / 修改 / 软归档 / 恢复 |
| `ui/routes.py` | 重写 | 新增 6 条路由 + 表单校验；原有登录、列表行为保持不变 |
| `templates/base.html` | 新增 | 统一布局：顶栏导航、Flash 提示、样式（按角色显示「新增员工」入口） |
| `templates/employees.html` | 重写 | 加搜索框、已归档视图切换、行内「详情 / 编辑 / 归档 / 恢复」按钮、空态提示 |
| `templates/employee_form.html` | 新增 | 新增与编辑共用表单，字段级错误提示、输入回填 |
| `templates/employee_detail.html` | 新增 | 单个员工完整档案 + 状态标签（在职 / 已归档） |
| `templates/employee_confirm_archive.html` | 新增 | 归档二次确认页（需求要求「显式确认」，不是 JS 弹窗） |
| `db/schema.sql` | 新增 | 建表 + 5 条演示数据；也可用于对照你 M1 的表结构 |
| `app.py` / `config.py` / `model/*` / `ui/auth.py` | 未改 | 保持原样，避免影响 M1/M2 已验收的部分 |

三层架构没有被打破：**UI 层不出现任何 SQL**，所有数据库访问都在 `dal/employee_dao.py`，实体只在 `model/employee.py`；所有 SQL 都是参数化查询。

---

## 2. 路由一览

| 方法 | 路径 | 作用 | 需求 | 谁能用 |
|---|---|---|---|---|
| GET | `/employees` | 员工列表 + `?q=` 检索 + `?archived=1` 已归档视图 | FR04 / FR05 | HRAdmin、StoreManager |
| GET | `/employees/<id>` | 员工详情 | FR07 | HRAdmin、StoreManager |
| GET/POST | `/employees/new` | 新增员工 | FR01 | 仅 HRAdmin |
| GET/POST | `/employees/<id>/edit` | 修改员工 | FR02 | 仅 HRAdmin |
| GET/POST | `/employees/<id>/archive` | 归档（GET 确认页 / POST 执行） | FR03 | 仅 HRAdmin |
| POST | `/employees/<id>/restore` | 恢复被归档员工 | FR03 | 仅 HRAdmin |

---

## 3. 业务规则

- **软归档，不物理删除**：`employee.is_archived = 1`。记录仍在库里，排班/统计等后续里程碑的历史数据不会断链。
- **工号唯一**：应用层先查重（`EmployeeDAO.employee_id_exists`），数据库层还有 `UNIQUE KEY uk_employee_id` 兜底，双保险。
- **归档需显式确认**：`GET .../archive` 出确认页，`POST` 才写库 —— 对应 FRS-03 的 "after an explicit confirmation"。
- **已归档员工不可编辑**：`UPDATE` 语句带 `AND is_archived = 0`，路由层也会拦下并提示。
- **输入校验**：工号/姓名必填；年龄 16~100 整数；薪资非负数字；邮箱格式校验；长文本 100 字符上限。
- **角色权限**：StoreManager 只读（列表/详情可看，看不到新增/编辑/归档按钮，直接访问写路由返回 403），与 NFR-08 一致。

---

## 4. 怎么跑起来

```bat
cd 你的项目目录
.venv\Scripts\activate

:: 依赖（M2 已有的话可跳过）
pip install flask pymysql

:: 建表 + 演示数据（可选，已有库就跳过）
mysql -u root -p hardware_store < db\schema.sql

:: 启动
python app.py
```

浏览器打开 <http://127.0.0.1:5000>，用 `/seed_users.py` 里设置的账号登录：

| 账号 | 密码 | 角色 |
|---|---|---|
| hr | hr123 | HRAdmin |
| manager | manager123 | StoreManager |
| zhangsan | zhangsan123 | Employee |

> 如果登录报「用户名或密码错误」，先跑一次 `python seed_users.py`，把占位密码换成真实哈希。

---

## 5. 怎么验收（建议按这个顺序点一遍）

1. 用 **hr** 登录 → 进入员工列表，能看到 5 条演示数据
2. 搜索框输入「库管」→ 只剩李四；输入「不存在」→ 空态提示
3. 点「+ 新增员工」→ 只填姓名就提交 → 看到工号/姓名必填的红字提示
4. 填完整 → 保存 → 列表出现新员工，顶部绿色提示
5. 点「详情」→ 看到全部字段；点「编辑」→ 改岗位和薪资 → 保存 → 详情已更新
6. 点「归档」→ 确认页 → 确认 → 列表里消失；点「查看已归档」→ 能看到，可「恢复」
7. 退出，用 **manager** 登录 → 能看列表和详情，但**没有**新增/编辑/归档按钮
8. 用 manager 直接访问 `/employees/new` → 403（验证 NFR-08）

---

## 6. 自动化冒烟测试

仓库里的 `tests/m3_smoke_test.py` 用内存假 DAO 跑完上面全部流程（36 项断言，不依赖 MySQL）：

```bat
:: 在项目根目录、已激活 venv 的前提下
set PYTHONPATH=.
python tests\m3_smoke_test.py
```

覆盖：未登录跳转、错误密码、列表、检索、新增合法/非法、工号重复、详情、404、修改回填、归档确认页、软归档后仍存在、归档后隐藏、恢复、以及三个角色权限断言。

---

## 7. 提交到 Git（feature 分支）

```bat
git add .
git commit -m "feat(M3): 员工增删改查 —— 新增/修改/软归档/检索/详情"
git push origin feature
```

建议提交前 `git status` 确认没有把 `.venv/`、`__pycache__/` 带进去（`.gitignore` 里已有）。

---

## 8. 已知未做（留给后续里程碑）

- 分页：员工数 <100 时没必要，M6 若加数据再说
- CSRF 保护：课程项目未引入 Flask-WTF，如需要可加 `Flask-WTF`
- 审计日志（FRS-17，Could）与员工自助改资料（FRS-14，M5）
- 排班（FRS-08~FRS-11，M4）
