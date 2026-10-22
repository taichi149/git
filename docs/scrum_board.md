# Scrum Board — 美体商城员工管理系统 (Pro B)

> 团队：张绍康 / 张钰杰 / 钟昌霖 / 程祥睿 / 程麒天（5 人）
> 方法：瀑布（规划/设计）→ 迭代（M0~M6 里程碑交付）
> 仓库：github.com/taichi149/git

---

## 1. Sprint 规划（对应里程碑 M0~M6）

| Sprint | 目标 | 对应里程碑 | 主要 FR |
|---|---|---|---|
| Sprint 1 | 项目启动 + 三层架构框架 | M0 / M1 | 架构搭建 |
| Sprint 2 | 登录认证 + 角色权限 | M2 | FR09 |
| Sprint 3 | 员工增删改查 | M3 | FR01–FR08 |
| Sprint 4 | 手动排班 | M4 | FR10 / FR11 / FR13 |
| Sprint 5 | 员工自助 + 统计 | M5 | FR12 / FR14 / FR15 |
| Sprint 6 | 测试 + 交付 | M6 | 测试用例 / 测试报告 / 文档 |

---

## 2. Product Backlog（用户故事，按 MoSCoW 优先级）

| ID | 用户故事 (As a… I want… so that…) | FR | 优先级 | 状态 |
|---|---|---|---|---|
| US-01 | 作为 HR，我要新增员工，以便把新员工录入系统 | FR01 | Must | ✅ Done |
| US-02 | 作为 HR，我要归档离职员工，以便从在职列表移除但不丢历史 | FR02 | Must | ✅ Done |
| US-03 | 作为 HR，我要编辑员工信息，以便档案保持最新 | FR03 | Must | ✅ Done |
| US-04 | 作为 HR/经理，我要查看员工总览，以便看到完整名单 | FR04 | Must | ✅ Done |
| US-05 | 作为 HR/经理，我要搜索员工，以便快速定位某人 | FR05 | Must | ✅ Done |
| US-06 | 作为 HR/经理，我要查看员工详情，以便看到完整档案 | FR06 | Must | ✅ Done |
| US-07 | 作为 HR，我要给员工分配部门，以便按部门管理 | FR07 | Must | ✅ Done |
| US-08 | 系统要持久化 §4.1 全部员工字段 | FR08 | Must | ✅ Done |
| US-09 | 作为用户，我要登录，以便按角色限制访问 | FR09 | Must | ✅ Done |
| US-10 | 作为 HR，我要分配班次（早/中/晚），以便记录排班 | FR10 | Should | ✅ Done |
| US-11 | 作为 HR/经理，我要查看全店排班，以便看到所有班次 | FR11 | Should | ✅ Done |
| US-12 | 作为经理，我要查看统计，以便看到总人数和分部门人数 | FR12 | Could | ✅ Done |
| US-13 | 作为员工，我要查看自己的排班，以便知道自己的班次 | FR13 | Should | 🔄 Done（代码已补） |
| US-14 | 作为员工，我要查看自己的档案 | FR14 | Must | ✅ Done |
| US-15 | 作为员工，我要修改邮箱/地址/紧急联系人 | FR15 | Could | ✅ Done |

---

## 3. Sprint Board（当前 Sprint 6 看板）

### 🟡 To Do（待办）
- [ ] 测试用例文档（对应 FR01–FR15，表格：用例ID/前置条件/步骤/预期/实际）
- [ ] 测试报告（含 m3/m4 smoke test 运行结果）
- [ ] UML 类图（已完成 PlantUML 源，待导出 PNG）
- [ ] Scrum 看板（本文件，可同步到 GitHub Projects / Trello）
- [ ] 文档进 git（Project Plan / URS / Test Plan / 类图 / 测试用例 → docs/）
- [ ] 删除误传的空文件 `新建文本文档.txt`
- [ ] 代码注释 FR 编号对齐 URS

### 🟠 In Progress（进行中）
- [ ] FR13「员工查看本人排班」—— 代码已补（/my-shifts 路由 + 模板），待 commit 到 main

### 🟢 Done（已完成）
- [x] 三层架构基础框架（model / dal / ui / templates）
- [x] 登录认证 + 密码哈希 + 角色访问控制（FR09）
- [x] 员工增删改查 + 软归档 + 检索 + 详情（FR01–FR08）
- [x] 手动排班：分配 / 全店周视图 / 个人视图（FR10 / FR11 / FR13）
- [x] 员工自助：档案 + 改个人信息（FR14 / FR15）
- [x] 统计：总人数 + 分部门（FR12）
- [x] 数据库三表（employee / user / shift）+ 种子数据
- [x] main 分支合并收口并推送 origin/main

---

## 4. 建议分工（按实际姓名替换 A–E）

| 角色 | 负责模块 | 对应 Sprint |
|---|---|---|
| 组员 A | 员工增删改查（M3） | Sprint 3 |
| 组员 B | 排班（M4） | Sprint 4 |
| 组员 C | 自助 + 统计（M5） | Sprint 5 |
| 组员 D | 测试用例 + 测试报告（M6） | Sprint 6 |
| 组员 E | Git 合并协调 + 文档整理 | 全程 |

---

## 5. 怎么把它变成「真看板」（二选一，5 分钟）

**方案 A：GitHub Projects（推荐，和仓库一体）**
1. 打开 `github.com/taichi149/git` → 顶部 **Projects** 标签 → **New project**
2. 模板选 **Board（看板）**
3. 建 3 列：`To Do` / `In Progress` / `Done`
4. 把上面第 3 节的卡片逐条拖进去（或新建 Issue 再拖入）

**方案 B：Trello**
1. 建 Board「美体商城员工管理系统」
2. 建 3 列同上，卡片照第 3 节内容复制

看板本体留在 GitHub/Trello，需要证据就截图放 `docs/`。
