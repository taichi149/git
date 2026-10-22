# Test Report

**A software solution for Meítǐ Shāngchéng — Employee Management System**

| | |
|---|---|
| **Document** | Test Report |
| **Project** | A software solution for Meítǐ Shāngchéng (Pro B) |
| **Team** | 张绍康 / 张钰杰 / 钟昌霖 / 程祥睿 / 程麒天 |
| **Tutor** | Stan van Hartingsveldt |
| **Date** | 22 October 2026 |
| **Version** | 1.0 |

---

## 1. Introduction

This report completes the Test Plan by recording the **actual results** of executing each test case against the running system (black-box), together with a summary and a recommendation for the client.

---

## 2. Test Results

| ID | UC | Name | Pre-condition | Test data | Expected result | Test Result | Status |
|---|---|---|---|---|---|---|---|
| TC-01 | UC-01 | Add new employee — success | HR logged in (`hr` / `hr123`) | employee_id: EMP004, name: 赵六, age: 30, position: 收银员, salary: 5000, department: 门店, email: zhaoliu@meiti.com | System shows “员工「赵六」已新增” and returns to the employee list; EMP004 赵六 appears | Prompt shown; EMP004 appears in the list | Pass |
| TC-02 | UC-01 | Add new employee — missing required field (name) | HR logged in | employee_id: EMP005, name: *(empty)* | System shows “姓名不能为空”; no record saved | “姓名不能为空” shown; no record created | Pass |
| TC-03 | UC-01 | Add new employee — duplicate employee ID | HR logged in; EMP001 exists | employee_id: EMP001 *(duplicate)* | System shows “该工号已存在” | “该工号已存在” shown; no duplicate created | Pass |
| TC-04 | UC-02 | Archive employee — success | HR logged in; 王五 (EMP003) active | select 王五 → confirm | Confirmation page, then “员工「王五」已归档”; 王五 leaves active list | 王五 moved to archived view | Pass |
| TC-05 | UC-02 | Archive employee — cancel | HR logged in; 王五 active | select 王五 → cancel | No change; 王五 stays active | 王五 remains in active list | Pass |
| TC-06 | UC-03 | Search employee — success | Store Manager logged in | keyword: 张三 | List shows only 张三 (EMP001) | Only 张三 listed | Pass |
| TC-07 | UC-03 | Search employee — no match | Store Manager logged in | keyword: 不存在的人 | List shows no matching rows | Empty list shown | Pass |
| TC-08 | UC-04 | Assign shift — success | HR logged in; 张三 active | employee: 张三, date: 2026-10-26, shift: Morning | “已为「张三」安排 2026-10-26 早班”; 张三 shows 早班 | Shift saved; 早班 shown in weekly view | Pass |
| TC-09 | UC-04 | Assign shift — overwrite existing shift | HR logged in; 张三 has Morning on 2026-10-26 | same day, shift: Evening | Existing shift overwritten; 张三 shows 晚班 | Shift replaced by 晚班 (no duplicate) | Pass |
| TC-10 | UC-05 | View personal schedule — success | Employee logged in; 张三 has shifts | click “查看我的排班” | 张三's weekly schedule with shift labels | Weekly schedule displayed | Pass |
| TC-11 | UC-05 | View personal schedule — no shifts | Employee logged in; no shifts | click “查看我的排班” | “休息” every day; “本周共排班 0 天” | 休息 / 0 天 shown | Pass |
| TC-12 | UC-06 | Update personal info — success | Employee logged in | email: newzhangsan@meiti.com, … | “保存成功”; profile shows new email | 保存成功; email updated | Pass |
| TC-13 | UC-06 | Update personal info — invalid email | Employee logged in | email: abc | “邮箱格式不合法…”; email not updated | Error shown; email unchanged | Pass |
| TC-14 | UC-06 | Update personal info — restricted field read-only | Employee logged in | try salary/position/department | Shown read-only; cannot change | Read-only; no input fields | Pass |
| TC-15 | UC-07 | Login — success (role-based redirect) | Not logged in | hr / hr123 | Login succeeds; redirected to employee list | Redirected to employee list | Pass |
| TC-16 | UC-07 | Login — wrong password | Not logged in | hr / wrongpass | “用户名或密码错误”; stays on login page | Error shown; stays on login | Pass |
| TC-17 | UC-08 | View statistics — success | Store Manager logged in | open statistics page | Total = 3; count per department | Total 3; 销售部/仓储部/管理部 listed | Pass |
| TC-18 | UC-08 | View statistics — no data | Store Manager logged in; no active employees | open statistics page | Total = 0; empty department list | Total 0 shown | Pass |

---

## 3. Test Summary

| Item | Value |
|---|---|
| Total test cases | 18 |
| Pass | 18 |
| Fail | 0 |
| Blocked / Not executed | 0 |
| Pass rate | 100% |

All **Must** and **Should** functional requirements (FR01–FR11, FR13, FR14) are verified working; the **Could** requirements (FR12, FR15) are also implemented and passing.

---

## 4. Evaluation & Recommendation for the Client

**Deployment recommendation: ✅ The system is ready to deploy.**

The core employee-management flows (add, archive, edit, search, view, assign shift, view schedule, statistics, login, and employee self-service) all behave as specified in the URS. No critical or blocking defects were found during this test cycle.

**Known minor issues (non-blocking):**
1. The employee self-service "view my schedule" (FR13) was added in the final iteration and has not yet been merged to `main` — merge before final delivery.
2. Internal code comments still reference a few FR numbers that differ from the URS numbering — cosmetic only, no functional impact.

**Workaround:** none required — no critical defect was found that would block use.

**Conclusion:** subject to merging the FR13 change and archiving the documentation set into the Git repository, the system satisfies the acceptance criteria (§13 of the URS) and can be delivered to the client.
