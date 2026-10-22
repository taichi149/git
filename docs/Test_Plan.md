# Test Plan

**A software solution for Meítǐ Shāngchéng — Employee Management System**

| | |
|---|---|
| **Document** | Test Plan |
| **Project** | A software solution for Meítǐ Shāngchéng (Pro B) |
| **Team** | 张绍康 / 张钰杰 / 钟昌霖 / 程祥睿 / 程麒天 |
| **Tutor** | Stan van Hartingsveldt |
| **Date** | 22 October 2026 |
| **Version** | 1.0 |

---

## 1. Introduction

### 1.1 Document Purpose

This Test Plan defines the black-box test cases for the Employee Management System. The tests are written from the **user's perspective only** (input → expected system output); internal code, Flask routes and class methods are **not** referenced. A tester who knows nothing about the implementation can execute every test case using this document alone.

### 1.2 Document Overview

- **Section 2** contains the test-case table. Each test case links to one use case (UC) from the URS (§6), making the document chain traceable: *FR → UC → TC*.
- Each use case's **Main Success Scenario (MSS)** is covered by at least one test case, and **every extension / exception branch has its own separate test case**.
- Columns `Test Result` and `Status` are intentionally left blank in this plan; they are filled in after execution to produce the **Test Report**.

---

## 2. Test Plan

| ID | UC | Name | Pre-condition | Test data | Expected result | Test Result | Status |
|---|---|---|---|---|---|---|---|
| TC-01 | UC-01 | Add new employee — success | HR logged in (`hr` / `hr123`) | employee_id: EMP004, name: 赵六, age: 30, position: 收银员, salary: 5000, department: 门店, email: zhaoliu@meiti.com | System shows “员工「赵六」已新增” and returns to the employee list; EMP004 赵六 appears in the list |  |  |
| TC-02 | UC-01 | Add new employee — missing required field (name) | HR logged in | employee_id: EMP005, name: *(empty)*, other fields filled | System shows “姓名不能为空” on the form; no record saved; EMP005 is not in the list |  |  |
| TC-03 | UC-01 | Add new employee — duplicate employee ID | HR logged in; EMP001 already exists | employee_id: EMP001 *(duplicate)*, name: 测试员工 | System shows “该工号已存在”; no new record created |  |  |
| TC-04 | UC-02 | Archive employee — success | HR logged in; employee 王五 (EMP003) is active | select 王五 → confirm archive | System shows a confirmation page; after confirming shows “员工「王五」已归档”; 王五 disappears from the active list and appears in the archived view |  |  |
| TC-05 | UC-02 | Archive employee — cancel | HR logged in; 王五 is active | select 王五 → cancel on the confirmation page | No change; 王五 remains in the active list |  |  |
| TC-06 | UC-03 | Search employee — success | Store Manager logged in (`manager` / `manager123`) | keyword: 张三 | The list shows only 张三 (EMP001) |  |  |
| TC-07 | UC-03 | Search employee — no match | Store Manager logged in | keyword: 不存在的人 | The list shows no matching rows (empty) |  |  |
| TC-08 | UC-04 | Assign shift — success | HR logged in; 张三 is active | employee: 张三, date: 2026-10-26, shift: Morning | System shows “已为「张三」安排 2026-10-26 早班” and returns to the weekly schedule; 张三 shows “早班” on 2026-10-26 |  |  |
| TC-09 | UC-04 | Assign shift — overwrite existing shift | HR logged in; 张三 already has Morning on 2026-10-26 | employee: 张三, date: 2026-10-26, shift: Evening | The existing shift is overwritten; 张三 shows “晚班” on 2026-10-26 (no duplicate row) |  |  |
| TC-10 | UC-05 | View personal schedule — success | Employee logged in (`zhangsan` / `zhangsan123`); 张三 has shifts this week | click “查看我的排班” | System shows 张三's weekly schedule with shift labels (早班/中班/晚班) |  |  |
| TC-11 | UC-05 | View personal schedule — no shifts | Employee logged in; 张三 has no shifts this week | click “查看我的排班” | System shows “休息” for every day and “本周共排班 0 天” |  |  |
| TC-12 | UC-06 | Update personal info — success | Employee logged in (`zhangsan`) | email: newzhangsan@meiti.com, contact_address: 新地址, emergency_contact: 张父 13800000001 | System shows “保存成功”; the profile displays the updated email |  |  |
| TC-13 | UC-06 | Update personal info — invalid email | Employee logged in | email: abc *(no @, invalid)* | System shows “邮箱格式不合法，请输入如 user@example.com”; email is not updated |  |  |
| TC-14 | UC-06 | Update personal info — restricted field is read-only | Employee logged in | try to change salary / position / department | Salary, position and department are shown as read-only text (no input field); the employee cannot change them |  |  |
| TC-15 | UC-07 | Login — success (role-based redirect) | Not logged in | username: hr, password: hr123 | Login succeeds; the user is redirected to the employee list (HR view) |  |  |
| TC-16 | UC-07 | Login — wrong password | Not logged in | username: hr, password: wrongpass | System shows “用户名或密码错误”; the user stays on the login page |  |  |
| TC-17 | UC-08 | View statistics — success | Store Manager logged in | open the statistics page | System shows total headcount (3) and count per department (销售部 / 仓储部 / 管理部) |  |  |
| TC-18 | UC-08 | View statistics — no data | Store Manager logged in; no active employees | open the statistics page | System shows total = 0 and an empty department list |  |  |
