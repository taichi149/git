# Meítǐ Shāngchéng - Employee Management & Statistics System

本项目是面向 **Meítǐ Shāngchéng（美体商城）** 郑州首店的员工与排班管理系统。
本项目基于课程实践项目要求进行迭代开发，本分支为 **M5（Milestone 5）** 阶段产物。

---

## 📌 分支对应需求与功能范围 (Scope & Requirements)

根据 *Software Project Reader* 中的系统规划与用户访谈（Appendix A），本分支实现了以下核心功能点：

- **FR12 & FR14：管理端统计与分析 (Management Statistics)**
  - **人员总览**：实时统计在职员工总数、平均时薪及涵盖部门总数。
  - **部门人员分布**：按部门（如 Hardware、Electronics、Management 等）分类聚合在职人数。
  - **排班与工时分析**：统计三大班次（Morning、Afternoon、Evening）的排班分布及累计工时。
- **FR15：员工自助门户 (Employee Self-Service Portal)**
  - **身份凭证登录**：员工使用工号与密码登录个人中心。
  - **排班与资料查看**：查看个人在职信息及分配的所有班次。
  - **自主修改联系邮箱**：支持员工自主修改绑定邮箱，内置合法正则校验与全员邮箱唯一性查重校验。

---

## 📂 项目结构说明

```text
.
├── README.md                 # 项目与里程碑说明文档
├── models.py                 # 数据实体定义（Employee 员工、Shift 排班）
├── database.py               # 数据持久化管理（采用 JSON 本地存储，支持自动初始化默认数据）
├── statistics_service.py     # FR12/FR14 统计业务逻辑
├── self_service.py           # FR15 员工自助与邮箱修改业务逻辑
├── main.py                   # 系统交互主程序（管理端/员工端入口）
├── test_m5.py                # 针对 FR12、FR14、FR15 的单元测试套件
└── data/                     # 数据存储目录（运行后自动生成）
    ├── employees.json
    └── shifts.json