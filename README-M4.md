# M4：手动排班（FR10 / FR11 / FR13）

基于仓库 `taichi149/git` **feature 分支**（已含 M3 员工增删改查）完成的 M4 实现。
按里程碑定义，M4 = 手动排班，完成标准是「能排班、能看排班视图（个人 + 全店）」。

班次与客户约定一致：一天三班 —— **早班 Morning / 中班 Afternoon / 晚班 Evening**。

---

## 1. 本次改了什么

| 文件 | 类型 | 说明 |
|---|---|---|
| `dal/shift_dao.py` | 新增 | 排班 DAO：个人时段查询、全店时段查询（联查员工表）、排班/改班（唯一键覆盖）、删除 |
| `model/shift.py` | 修改 | 增加 `employee_code` / `employee_name` 两个展示用属性（联查时带出，平时为 None） |
| `ui/routes.py` | 修改 | 新增 5 条排班路由 + 周计算辅助函数；原有 M1~M3 路由一行未动 |
| `templates/shift_assign.html` | 新增 | 排班表单：员工下拉（仅在职）+ 日期 + 班次，字段级错误提示、输入回填 |
| `templates/shifts_week.html` | 新增 | 全店周视图：一行一个员工、一列一天，空格可点「+ 排班」直接预填 |
| `templates/employee_shifts.html` | 新增 | 个人周视图：某员工一周七天的班次，显示「本周共排班 N 天」 |
| `templates/base.html` | 修改 | 导航加「全店排班」「排班」（排班仅 HRAdmin 可见）；加班次三色标签样式 |
| `templates/employees.html` | 修改 | 员工列表每行加「排班」入口，直达该员工的个人排班视图 |
| `schema_m4.sql` | 新增 | 排班表建表 + 以今天为基准的演示数据（幂等，可重复执行） |
| `m4_smoke_test.py` | 新增 | 冒烟测试：37 项断言全部通过（不依赖 MySQL，用内存假 DAO） |

三层架构没有被打破：**UI 层不出现任何 SQL**，所有数据库访问都在 `dal/shift_dao.py`，
所有 SQL 都是参数化查询；`model/shift.py` 只放属性。

---

## 2. 路由一览

| 方法 | 路径 | 作用 | 需求 | 谁能用 |
|---|---|---|---|---|
| GET/POST | `/shifts/assign` | 手动排班 / 改班（支持 `?emp_pk=`、`?date=` 预填） | FR10 | 仅 HRAdmin |
| GET | `/shifts` | 入口，跳到本周全店视图 | — | HRAdmin、StoreManager |
| GET | `/shifts/week?week=YYYY-MM-DD` | 全店排班周视图（上一周/本周/下一周翻页） | FR13 | HRAdmin、StoreManager |
| GET | `/employees/<id>/shifts?week=...` | 个人排班周视图 | FR11 | HRAdmin、StoreManager |
| POST | `/shifts/<id>/delete` | 删除一条排班（删完跳回来源页） | FR10 | 仅 HRAdmin |

权限设计与 M3 保持一致：**HRAdmin 能排能删，StoreManager 只读，Employee 一律 403**。

---

## 3. 业务规则

1. **一天三班**：班次只能是 早班 / 中班 / 晚班，数据库存英文代码，页面显示中文。
2. **同一员工同一天最多一个班**：数据库 `(employee_id, shift_date)` 唯一键兜底；
   重复排班时 `ON DUPLICATE KEY UPDATE` 自动覆盖旧班次 —— 这就是「改班」，不用单独做编辑页。
3. **已归档员工不能排新班**：排班表单的下拉只列在职员工，POST 时后端再校验一次；
   但归档员工的**历史排班保留可查**（和 M3 软归档的设计一致）。
4. **没排班的员工也显示在全店视图里**，HR 一眼能看到谁还空着，点格子里的「+ 排班」直接预填员工和日期。

---

## 4. 怎么跑

```bash
# 1) 建排班表 + 演示数据（在 MySQL 里执行）
mysql -u root -p hardware_store < schema_m4.sql

# 2) 跑冒烟测试（不需要数据库，37 项全过即 OK）
set PYTHONPATH=.          :: Windows；macOS/Linux 用 export PYTHONPATH=.
python m4_smoke_test.py

# 3) 启动系统，用 hr / hr123 登录，点导航栏「全店排班」「排班」验收
python app.py
```

验收对照里程碑完成标志：
- ✅ 能排班：HR 登录 → 排班 → 选员工/日期/班次 → 保存 → 周视图出现对应班次标签
- ✅ 能看排班视图：全店周视图（FR13）+ 点员工姓名进个人视图（FR11），都能翻周

---

## 5. Git 提交步骤（按小组流程，走 feature/shift 分支）

```bash
cd 你的项目目录
git checkout main
git pull origin main
git checkout -b feature/shift

# 把本目录里的文件按相同路径覆盖 / 新增进项目后：
git add .
git commit -m "feat: M4手动排班-排班/改班/删除与全店+个人周视图(FR10/FR11/FR13)"
git push -u origin feature/shift

# 测试通过后合并回 main
git checkout main
git pull origin main
git merge feature/shift
git push origin main
git branch -d feature/shift
```
