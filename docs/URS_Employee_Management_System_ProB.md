# User Requirements Specification (URS)

## A Software Solution for Meítǐ Shāngchéng — Employee Management System

| | |
|---|---|
| **Document title** | User Requirements Specification — Employee Management System |
| **Project** | A software solution for Meítǐ Shāngchéng (Pro B) |
| **Date** | 14 October 2026 |
| **Location** | Zhengzhou University of Light Industry (ZZULI), Zhengzhou, China |
| **Tutor** | Stan van Hartingsveldt |
| **Version** | 1.1 |

**Project Team (Pro B)**

| Name | Student ID |
|---|---|
| Zhang Shaokang (张绍康) | 542512320327 |
| Zhang Yujie (张钰杰) | 542512320328 |
| Zhong Changlin (钟昌霖) | 542512320329 |
| Cheng Xiangrui (程祥睿) | 542512320402 |
| Cheng Qitian (程麒天) | 542512320403 |

---

## Document Change Record

| Date | Version | Author | Comments |
|---|---|---|---|
| 14-10-2026 | 1.0 | Pro B team | Initial release |
| 22-10-2026 | 1.1 | Pro B team | Aligned with final implementation: removed unimplemented salary-approval constraint (FR03); clarified UC02/UC04 to match delivered behaviour |

---

## Definitions, Abbreviations and Acronyms

| Term | Description |
|---|---|
| **URS** | User Requirements Specification |
| **FR** | Functional Requirement |
| **NFR** | Non-Functional Requirement |
| **HR** | Human Resources |
| **MoSCoW** | Prioritisation method: **M**ust / **S**hould / **C**ould / **W**on't have |
| **GUI** | Graphical User Interface |
| **PD** | Process Diagram |
| **Actor** | A role (person or system) that interacts with the system |
| **Use case** | A goal-oriented interaction between an actor and the system |
| **Meítǐ Shāngchéng** | The client — a new hardware store opening in Zhengzhou |
| **Jupiter** | The parent company that funds the store |
| **ZZULI** | Zhengzhou University of Light Industry |
| **MSS** | Main Success Scenario (of a use case) |

---

## Table of Contents

1. Introduction
   1.1 Document Purpose
   1.2 Document Overview
   1.3 Client Perspective vs. Development Team Perspective
2. Project Background
   2.1 Scope and Objectives
   2.2 Current Situation & Problem Analysis
       2.2.1 External Analysis — Existing Employee-Management Software
       2.2.2 Internal Analysis — Current Business Process and Pain Points
       2.2.3 Current Business Process Diagram (PD)
3. Stakeholders and User Analysis
   3.1 Stakeholders
   3.2 End Users (Actors)
4. Functional Requirements (FR)
   4.1 Data Requirements
   4.2 Functional Requirements Table
   4.3 Out of Scope (Won't have)
5. Non-Functional Requirements (NFR)
6. Use Case Model
   6.1 Actor List
   6.2 Use Case Descriptions
7. Use Case Diagram
8. Graphical User Interface (GUI)
   8.1 HR Administrator View
   8.2 Store Manager View
   8.3 Employee Self-Service View
9. Website Wireframes
10. Constraints
   10.1 Technical / Capability Constraints
   10.2 Team Collaboration Constraints
11. Assumptions
12. Agreement with the Client
13. Acceptance Criteria

---

## 1. Introduction

### 1.1 Document Purpose

This document is the final specification of the user requirements for the **Employee Management System** being developed for **Meítǐ Shāngchéng**, a new hardware store opening its first branch in Zhengzhou. It is the main input for the technical development phase and the primary basis for the acceptance criteria that evaluators and the client will use after development is complete.

This URS is produced during the **Problem Analysis** phase of the Waterfall model. It captures the client's *business problems*, translates them into *system requirements*, and defines what the system shall do. It is read by everyone responsible for managing the development of the project.

### 1.2 Document Overview

- **Section 2** gives an overall description of the product, the project goals (written with the SMART principle), and an analysis of the current situation (both external competitors and the client's internal process).
- **Section 3** identifies the stakeholders and the end users of the system.
- **Section 4** lists the functional requirements, prioritised using MoSCoW, together with the data fields the system must store.
- **Section 5** lists the non-functional requirements.
- **Section 6 and 7** describe the use cases and the use case diagram.
- **Sections 8 and 9** show the graphical user interfaces from several perspectives and the website wireframes.
- **Sections 10–13** describe constraints, assumptions, the agreement with the client, and the acceptance criteria.

### 1.3 Client Perspective vs. Development Team Perspective

This URS balances two points of view:

| Perspective | What they care about |
|---|---|
| **Client** (owner / manager of Meítǐ Shāngchéng) | Delivery time (the system must be ready before the store opens), total cost, quality of the delivered software, and the **scope** — which features are included and which are not. |
| **Development team** (Pro B) | Development effort and hours, development cost, workload per member, quality requirements, and the size of the scope — in order to judge whether the project can realistically be finished on time (the *Attainable* part of SMART). |

The project goals in Section 2.1 are therefore written so that they are ambitious for the client but still *attainable* by the team within six weeks.

---

## 2. Project Background

### 2.1 Scope and Objectives

Meítǐ Shāngchéng, funded by its parent company Jupiter, is opening its first hardware store in Zhengzhou. Because there is no existing employee-management system and no historical data, the client wants a new software solution. For this first phase, the project is scoped to a single **Employee Management module** (the store is a single branch, not a chain). Inventory and product management are explicitly deferred to a later phase.

The project goals, written according to the **SMART** principle and aligned with the project triangle (time, cost, quality, scope):

**Goal 1 — Simplify employee management (operational efficiency).**
- *Specific:* an authorised HR administrator shall be able to add, search and update a complete employee record through a graphical interface.
- *Measurable:* adding a new employee shall take no more than **3 minutes**; locating any employee's record shall take no more than **10 seconds** (down from an estimated 10–15 minutes with the current Excel/paper method).
- *Achievable:* the team already possesses the required database and programming skills (see Constraints, §10.1).
- *Relevant:* this directly solves the client's stated top priority — employee management.
- *Time-bound:* delivered by the end of week 9 (final presentation).

**Goal 2 — Scalability (growth-ready).**
- *Specific:* the system architecture shall allow new modules (attendance, inventory, additional departments) to be added later without rewriting the employee-management module.
- *Measurable:* the system shall support at least **100 employee records** with no noticeable drop in response time, comfortably exceeding the store's initial headcount.
- *Achievable:* achieved through a normalised relational data model and separated application layers.
- *Relevant:* the client explicitly asked for a system that remains easy to manage as the company grows.
- *Time-bound:* the data model is designed in the current phase and validated at final delivery.

**Project triangle alignment:**

| Dimension | Constraint |
|---|---|
| **Time** | 6 weeks (week 4 to week 9); final deliverable presented at the end of week 9. |
| **Cost** | Minimal — the team uses existing devices and free/open-source tools; no hardware purchase is required. |
| **Quality** | All **Must** and **Should** requirements implemented; **Could** requirements implemented if time permits. |
| **Scope** | Employee management module only; inventory, automated scheduling and payroll are **out of scope** (Won't have). |

### 2.2 Current Situation & Problem Analysis

#### 2.2.1 External Analysis — Existing Employee-Management Software

The team investigated the employee-management and HR software already on the market to justify why a new system is needed instead of buying an existing product.

**Existing products analysed:** DingTalk (Alibaba), WeCom (Tencent), Feishu/Lark (ByteDance), Yonyou & Kingdee (enterprise HR), BambooHR, Gusto, and manual Excel spreadsheets.

**Advantages of existing software:**
- Mature, feature-rich, and widely tested.
- Cloud-based with mobile applications.
- Built-in payroll, attendance and approval workflows (in enterprise suites).
- Good reporting and analytics dashboards.

**Disadvantages / shortfalls for this client:**
- **Cost:** enterprise HR suites charge per-user subscription fees that are unaffordable for a single small store.
- **Complexity:** these tools bundle dozens of features (chat, approval flows, OKRs) that a small hardware store does not need; the learning curve is steep for non-technical store staff.
- **Not tailored:** none of them support the store's specific model (three daily shifts — morning/afternoon/evening — and department-based store management) out of the box.
- **Overkill for scale:** international tools (BambooHR, Workday) assume large enterprises and Western HR compliance rules.
- **Data self-containment:** the client wants a simple, self-contained system it fully controls, without depending on a third-party cloud service.

**Conclusion:** no existing product matches the store's needs at an acceptable cost and complexity. This justifies building a dedicated, lightweight system.

#### 2.2.2 Internal Analysis — Current Business Process and Pain Points

The store is new, so it has **no existing system and no historical data**. Today employee management would be done manually, mirroring how other Jupiter stores currently work.

**Current (as-is) process:**
1. When an employee joins, HR writes their details on paper or into an Excel spreadsheet.
2. When information changes (address, salary, position), HR edits the spreadsheet cell by hand.
3. The manager creates the weekly shift schedule in an online calendar or another Excel file.
4. Employees must ask HR or the manager in person (or by chat) to see their own schedule or information.
5. When an employee leaves, HR deletes the row manually.
6. At the end of the month, HR counts rows by hand to report headcount.

**Pain points (the root problems this system must solve):**
- **Slow and error-prone:** finding or updating an employee's data takes many minutes and is easy to get wrong.
- **No central overview:** there is no single, up-to-date view of who works at the store, in which department.
- **Unreliable scheduling:** Excel/calendar schedules are cumbersome, conflict-prone and not authoritative.
- **No employee self-service:** employees cannot view their own schedule without asking a manager.
- **Not scalable:** as the store grows, manual spreadsheets become unmanageable.
- **No role-based control:** anyone with the file can see or change sensitive data such as salaries.

#### 2.2.3 Current Business Process Diagram (PD)

The following Process Diagram (drawn according to the classroom convention) shows the client's current employee-management workflow. It uses rounded rectangles for start/end, rectangles for activities, and diamonds for decisions.

```
                          ┌──────────────────────┐
                          │   New employee joins │
                          │       the store      │
                          └──────────┬───────────┘
                                     ▼
                          ┌──────────────────────┐
                          │  HR writes name, age,│
                          │ position, salary on  │
                          │   paper / Excel      │
                          └──────────┬───────────┘
                                     ▼
                          ┌──────────────────────┐
                          │  Data stored in an   │
                          │  Excel sheet or paper│
                          │  file (no database)  │
                          └──────────┬───────────┘
                 ┌───────────────────┴────────────────────┐
                 ▼                                        ▼
   ┌──────────────────────────┐              ┌──────────────────────────┐
   │ Info changes (address,   │              │ Manager creates weekly   │
   │ salary, position)        │              │ shift schedule in        │
   │ HR edits the Excel cell  │              │ Excel / online calendar  │
   └────────────┬─────────────┘              └────────────┬─────────────┘
                ▼                                          ▼
   ┌──────────────────────────┐              ┌──────────────────────────┐
   │ Employee asks HR for     │              │ Employee asks manager    │
   │ own info / schedule      │              │ for their shift details  │
   │ (in person or by chat)   │              │ (in person or by chat)   │
   └────────────┬─────────────┘              └──────────────────────────┘
                ▼
   ┌──────────────────────────┐
   │ End of month: HR counts  │
   │ rows by hand to report   │
   │ headcount and departments│
   └──────────────────────────┘
```

The proposed system replaces every manual activity above with database-backed, role-controlled operations (see §4 and §6).

---

## 3. Stakeholders and User Analysis

### 3.1 Stakeholders

| Stakeholder | Role | Interest in the system |
|---|---|---|
| **Meítǐ Shāngchéng owner** | Ultimate client | System is delivered on time, within budget, and solves employee management. |
| **Store Manager (Henriette)** | Primary client contact | Simplify employee administration; get a clear overview and statistics. |
| **HR Administrator** | End user | Add/remove/edit employees and assign departments and shifts quickly. |
| **Store employees** | End users | View and update their own information and work schedule. |
| **Jupiter (parent company)** | Funding body | The store opens with a working administration system. |
| **ZZULI / Fontys tutors** | Evaluators | The team follows a correct project process and meets acceptance criteria. |
| **Pro B development team** | Developers | Deliver a working, maintainable system within six weeks. |

### 3.2 End Users (Actors)

The system is **not** designed for "everyone". It is designed for three concrete roles, each with different permissions:

| Actor | Who they are | What they can do |
|---|---|---|
| **HR Administrator** | The HR/admin staff who manage employees | Add, remove, edit and search employees; assign departments; assign shifts; view the full store schedule. |
| **Store Manager** | The manager (Henriette) | View the employee overview, search employees, view details, view statistics, view the store schedule (read-only, no salary editing). |
| **Employee** | A normal store employee | Log in, view their own profile and schedule, and update selected personal fields (email, address, emergency contact). |

Characteristics that influence the requirements: the system will be used frequently by HR, but only occasionally by employees; users are not technical, so the interface must be simple and require little training; the system must keep salaries visible only to HR and management.

---

## 4. Functional Requirements (FR)

Each functional requirement has a unique ID, a name, a MoSCoW priority, and (where relevant) a constraint that describes a business rule outside the main function. Requirements are grouped by application: **Management application** (used by HR Administrator and Store Manager) and **Employee web portal** (used by employees).

### 4.1 Data Requirements

For every employee, the system shall store the following fields (copied from the client's stated requirements):

| Field | Notes |
|---|---|
| Name | Required |
| Age | Required |
| Position / job title | e.g., sales clerk, cashier, warehouse worker |
| Salary | Hourly wage or monthly salary — visible only to HR and management |
| Department | e.g., Sales, HR, Warehouse |
| Employee ID / ID-card number | Unique identifier |
| Email | Contact |
| Contact address | Contact |
| Emergency contact | Name and phone number, used when an employee has an accident |
| Work schedule (shifts) | Non-core; a "nice to have" enhancement |

### 4.2 Functional Requirements Table

**Management application**

| ID | Name | Priority | Requirement (the system **shall** …) | Constraint |
|---|---|---|---|---|
| FR01 | Add new employee | Must | The HR Administrator shall add a new employee by entering the data fields listed in §4.1. | The Employee ID shall be unique. |
| FR02 | Remove / archive employee | Must | The HR Administrator shall remove an employee from the active list when they resign, retire or are dismissed. | The record is archived, not permanently deleted. |
| FR03 | Edit employee information | Must | The HR Administrator shall modify any field of an existing employee record. | — |
| FR04 | View employee overview | Must | The HR Administrator and Store Manager shall view a complete, searchable list of all employees. | — |
| FR05 | Search for an employee | Must | The HR Administrator and Store Manager shall search for an employee by name, employee ID or department. | — |
| FR06 | View employee details | Must | Authorised users shall open and view the full detail record of a single employee. | Salary field hidden from the Employee role. |
| FR07 | Assign department | Must | The HR Administrator shall assign an employee to a department. | An employee may belong to exactly one department. |
| FR08 | Store employee data fields | Must | The system shall persist all data fields listed in §4.1 for every employee. | Emergency contact is stored for all employees. |
| FR09 | User login & authentication | Must | Every user shall log in with a unique account before using the system; access shall be restricted by role. | Passwords shall be stored securely (hashed). |
| FR10 | Assign work shift | Should | The HR Administrator shall assign an employee to one of the three daily shifts (morning / afternoon / evening) for a given date. | Manual assignment only in this phase. |
| FR11 | View store-wide schedule | Should | The HR Administrator and Store Manager shall view the schedule of all employees for a selected period. | — |
| FR12 | View employee statistics | Could | The Store Manager shall view summary statistics such as total headcount and employees per department. | — |

**Employee web portal**

| ID | Name | Priority | Requirement (the system **shall** …) | Constraint |
|---|---|---|---|---|
| FR13 | View personal schedule | Should | The Employee shall view their own work schedule for a selected period. | Employee sees only their own shifts. |
| FR14 | View personal information | Must | The Employee shall view their own stored profile. | — |
| FR15 | Update personal information | Could | The Employee shall update selected personal fields (email, address, emergency contact). | Employee cannot change salary, position or department. |

### 4.3 Out of Scope (Won't have)

The following capabilities are explicitly **not** delivered in this phase. They were identified during problem analysis and are recorded here to set the client's expectations (see also §10):

- **Inventory / product management** — the client's second priority; deferred to a future phase.
- **Automated shift scheduling** — the system supports manual assignment only.
- **Payroll processing** — salary is stored as a data field only; no payments are computed.
- **In-store attendance (clock-in/clock-out) registration** — a possible future module.
- **Multi-store / chain support** — the system serves a single store.

---

## 5. Non-Functional Requirements (NFR)

| ID | Name | Priority | Description |
|---|---|---|---|
| NFR01 | Performance | Must | Common operations (search, open a record) shall respond within **2 seconds** for up to 100 employees. |
| NFR02 | Usability | Must | A new user shall be able to perform the core tasks after at most **30 minutes** of training, without a manual. |
| NFR03 | Security & access control | Must | The system shall enforce role-based access; salary data shall be readable only by HR Administrator and Store Manager. |
| NFR04 | Scalability | Must | The system shall support at least **100 employee records** with no noticeable performance loss. |
| NFR05 | Reliability | Should | The system shall be available during store opening hours; a crash shall not corrupt stored data. |
| NFR06 | Data integrity & backup | Should | Employee data shall not be lost in the event of a failure (database transactions; exportable backup). |
| NFR07 | Compatibility | Must | The system shall run on standard office hardware and common browsers (Chrome, Edge). |
| NFR08 | Maintainability | Should | Code shall follow consistent naming and be documented so future modules can be added. |
| NFR09 | Localisation | Could | The interface may be provided in Chinese and English. |

---

## 6. Use Case Model

### 6.1 Actor List

| Actor | Description |
|---|---|
| **HR Administrator** | Manages employees, departments and schedules. |
| **Store Manager** | Oversees the store; views overviews, details and statistics (read-only for sensitive data). |
| **Employee** | A store worker who views and updates their own information and schedule. |

### 6.2 Use Case Descriptions

Each use case is written at the *user-goal* level and is linked to one or more functional requirements.

**UC01 — Add new employee** (FR01)

| | |
|---|---|
| **Use case** | HR Administrator adds a new employee |
| **Actor** | HR Administrator |
| **Preconditions** | HR Administrator is logged in |
| **Trigger** | HR Administrator opens the employee-management panel and selects "Add employee" |
| **Main Success Scenario** | 1. HR enters the required data fields (name, age, position, salary, department, ID, email, address, emergency contact). 2. System validates the data and confirms the employee ID is unique. 3. System saves the record and shows it in the employee list. |
| **Extensions** | 2a. Required field missing → 1. System shows a validation error. 2. Returns to MSS step 1.  2b. Employee ID already exists → 1. System shows "ID already in use". 2. Returns to MSS step 1. |

**UC02 — Remove / archive employee** (FR02)

| | |
|---|---|
| **Use case** | HR Administrator removes an employee |
| **Actor** | HR Administrator |
| **Preconditions** | HR Administrator is logged in; the employee exists |
| **Trigger** | HR selects "Remove" on an employee record |
| **Main Success Scenario** | 1. HR selects the employee. 2. System asks for confirmation. 3. HR confirms. 4. System archives the record and removes it from the active list. |
| **Extensions** | 2a. HR cancels → system makes no change. |

**UC03 — Search and view an employee** (FR05, FR06)

| | |
|---|---|
| **Use case** | Authorised user searches for and views an employee |
| **Actor** | HR Administrator, Store Manager |
| **Preconditions** | User is logged in |
| **Trigger** | User types a name, employee ID or department in the search box |
| **Main Success Scenario** | 1. User enters a search term. 2. System returns matching employees. 3. User opens a record. 4. System shows the full detail view. |
| **Extensions** | 2a. No match → system shows "No employees found". |

**UC04 — Assign work shift** (FR10)

| | |
|---|---|
| **Use case** | HR Administrator assigns a shift |
| **Actor** | HR Administrator |
| **Preconditions** | HR Administrator is logged in |
| **Trigger** | HR opens the schedule and selects a date and employee |
| **Main Success Scenario** | 1. HR selects the employee and date. 2. HR chooses a shift (morning / afternoon / evening). 3. System saves the assignment and updates the store schedule. |
| **Extensions** | 3a. Employee already assigned that day → system overwrites the existing shift for that day (re-scheduling). |

**UC05 — View personal schedule** (FR13)

| | |
|---|---|
| **Use case** | Employee views their own schedule |
| **Actor** | Employee |
| **Preconditions** | Employee is logged in |
| **Trigger** | Employee opens "My Schedule" |
| **Main Success Scenario** | 1. System shows the employee's shifts for the selected period. |
| **Extensions** | 1a. No shifts assigned → system shows "No shifts scheduled". |

**UC06 — Update personal information** (FR15)

| | |
|---|---|
| **Use case** | Employee updates their own profile |
| **Actor** | Employee |
| **Preconditions** | Employee is logged in |
| **Trigger** | Employee edits a field in "My Profile" and saves |
| **Main Success Scenario** | 1. Employee edits an allowed field (email, address, emergency contact). 2. System validates the data. 3. System saves the change. |
| **Extensions** | 2a. Invalid value → system shows an error and returns to MSS step 1. 1b. Employee attempts to change salary/position → system rejects (field is read-only). |

**UC07 — Log in** (FR09)

| | |
|---|---|
| **Use case** | User logs in |
| **Actor** | HR Administrator, Store Manager, Employee |
| **Preconditions** | The user has an account |
| **Trigger** | User opens the application and enters credentials |
| **Main Success Scenario** | 1. User enters username and password. 2. System verifies the credentials. 3. System opens the role-specific view. |
| **Extensions** | 2a. Wrong credentials → system shows "Invalid username or password" and returns to MSS step 1. |

**UC08 — View employee statistics** (FR12)

| | |
|---|---|
| **Use case** | Store Manager views statistics |
| **Actor** | Store Manager |
| **Preconditions** | Store Manager is logged in |
| **Trigger** | Store Manager opens the dashboard |
| **Main Success Scenario** | 1. System shows total headcount and employees per department. |
| **Extensions** | 1a. No data → system shows an empty state. |

---

## 7. Use Case Diagram

The diagram below shows the actors and their use cases. (This is a schematic; the final UML diagram is drawn in a modelling tool.)

```
        ┌──────────────────────────────────────────────────────┐
        │            Employee Management System                │
        │                                                      │
        │   (Add new employee)      (Remove employee)          │
        │   (Edit employee)         (Assign department)        │
        │   (Assign shift)          (View store schedule)      │
        │   (Search employee)       (View employee details)    │
        │   (View employee overview)  (View statistics)        │
        │   (View personal schedule) (Update personal info)    │
        │   (Log in)                                           │
        └──────┬──────────────────┬──────────────────┬─────────┘
               │                  │                  │
        ┌──────┴─────┐      ┌─────┴──────┐      ┌────┴─────┐
        │ HR Admin-  │      │  Store     │      │ Employee │
        │ istrator   │      │  Manager   │      │          │
        └────────────┘      └────────────┘      └──────────┘
```

- **HR Administrator** is linked to: Add new employee, Remove employee, Edit employee, Assign department, Assign shift, View store schedule, Search employee, View employee details, View employee overview.
- **Store Manager** is linked to: View employee overview, Search employee, View employee details, View statistics, View store schedule.
- **Employee** is linked to: Log in, View personal schedule, View personal information, Update personal information.

---

## 8. Graphical User Interface (GUI)

This section shows the graphical interface from each user's perspective, with a short explanation of how each view works. (These are wireframe sketches; final visual design is done during implementation.)

### 8.1 HR Administrator View

The HR Administrator's main screen is a dashboard with a left navigation and an employee list.

```
┌────────────────────────────────────────────────────────────────────┐
│  Employee Management System                          [ HR Admin ]  │
├───────────────┬────────────────────────────────────────────────────┤
│  Dashboard    │  Employees                         [+ Add]  [Search]│
│  Employees    │ ┌──────────────┬──────────┬────────┬─────────────┐ │
│  Departments  │ │ Name         │ Department│ Shift  │ Actions     │ │
│  Scheduling   │ │ Zhang San    │ Sales     │ Morning│ View Edit   │ │
│  Reports      │ │ Li Si        │ HR        │ —      │ View Edit   │ │
│               │ │ ...          │ ...       │ ...    │ ...         │ │
│               │ └──────────────┴──────────┴────────┴─────────────┘ │
└───────────────┴────────────────────────────────────────────────────┘
```

- **Dashboard** — summary counts. **Employees** — the main list (FR04). **[+ Add]** opens the new-employee form (UC01). **Search** filters the list (UC03). **View/Edit** opens the detail form (FR06/FR03). **Scheduling** opens the shift-assignment screen (FR10).

### 8.2 Store Manager View

The Store Manager sees the same overview but read-only, plus a statistics dashboard.

```
┌────────────────────────────────────────────────────────────────────┐
│  Employee Management System                          [ Manager ]   │
├───────────────┬────────────────────────────────────────────────────┤
│  Dashboard    │  Overview                                          │
│  Employees    │  Total employees:        12                        │
│  Schedule     │  Sales: 6   HR: 2   Warehouse: 4                  │
│  Statistics   │                                                    │
│               │  ┌───────────────────────────────────────────────┐ │
│               │  │ Department distribution (bar chart)          │ │
│               │  └───────────────────────────────────────────────┘ │
└───────────────┴────────────────────────────────────────────────────┘
```

- Shows headcount and per-department statistics (FR12). The manager can view employees and the schedule but cannot edit salary or remove employees.

### 8.3 Employee Self-Service View

The employee logs into a simple web portal with only their own data.

```
┌────────────────────────────────────────────────────────────────────┐
│  My Portal                                          [ Log out ]    │
├───────────────┬────────────────────────────────────────────────────┤
│  My Profile   │  My Profile (read-only fields greyed out)          │
│  My Schedule  │  Name:   Zhang San                                  │
│               │  Position: Sales clerk        [editable: email]    │
│               │  Email:   zhangsan@...        [editable: address]  │
│               │  Emergency contact: [editable]                     │
├───────────────┴────────────────────────────────────────────────────┤
│  My Schedule                                                       │
│  Mon: Morning   Tue: Afternoon   Wed: Evening   ...                │
└────────────────────────────────────────────────────────────────────┘
```

- The employee can view their profile (FR14) and schedule (FR13) and update only the allowed fields (FR15). Salary, position and department are read-only.

---

## 9. Website Wireframes

The employee-facing part of the system is a website. Its structure is:

```
                    ┌──────────────────────┐
                    │   Login page         │
                    │ (username/password)  │
                    └──────────┬───────────┘
                               ▼
                    ┌──────────────────────┐
                    │   Home / Dashboard   │
                    │ (personal summary)   │
                    └──────────┬───────────┘
             ┌─────────────────┼─────────────────┐
             ▼                 ▼                 ▼
   ┌──────────────────┐ ┌───────────────┐ ┌──────────────────┐
   │  My Profile      │ │  My Schedule  │ │  (Settings)      │
   │  view / edit     │ │  view shifts  │ │  change password │
   └──────────────────┘ └───────────────┘ └──────────────────┘
```

- **Login page** — the single entry point (UC07); after login the role determines the view.
- **Home / Dashboard** — a personal summary (name, department, next shift).
- **My Profile** — view and edit allowed personal fields (UC06).
- **My Schedule** — the employee's own shifts (UC05).

The management application (for HR Administrator and Store Manager) follows a similar structure with additional pages: **Employees**, **Departments**, **Scheduling**, and **Statistics**.

---

## 10. Constraints

This section records the limits of the project so that the scope stays realistic. It is an internal project-assessment item (not intended for the client) and is used to determine which features are "Won't have".

### 10.1 Technical / Capability Constraints

- The team consists of five undergraduate students with limited professional development experience; complex features (real-time push notifications, automated optimised shift-scheduling algorithms, full payroll integration) are **beyond the team's current ability** and are therefore out of scope.
- The system is built with a lightweight technology stack (a relational database plus a simple web application), using free/open-source tools so that cost remains near zero.
- No dedicated server is purchased; the system runs on standard office hardware and browsers.
- Automated shift scheduling, in-store attendance terminals and multi-store support are **not implemented** in this phase (recorded as "Won't have" in §4.3).

### 10.2 Team Collaboration Constraints

- The team works part-time alongside other courses; availability is limited to the fixed weekly meeting slots, so parallel work must be coordinated carefully.
- Communication is mostly asynchronous (chat), which can cause misalignment on requirements and interfaces; this risk is mitigated by weekly meetings with agendas and minutes.
- The team shares one Git repository; discipline in committing and branching is required to avoid merge conflicts.
- If a member falls ill or cannot attend a meeting, tasks may slip; the plan includes buffer time in the milestones (§13).

---

## 11. Assumptions

- The client provides a contact person (Store Manager) who is available to answer questions during the project.
- The system serves a **single store** with an initial headcount of roughly 10–20 employees, growing to at most 100 in the near future.
- The store uses three daily shifts (morning, afternoon, evening).
- Employees have basic computer literacy and access to a standard browser.
- The client agrees that inventory management, payroll and automated scheduling are deferred to a later phase.
- English (and optionally Chinese) is used as the interface language; the documents and deliverables are written in English.

---

## 12. Agreement with the Client

The parties agree that this User Requirements Specification defines the scope and quality of the Employee Management System to be delivered. By signing below, the client confirms that the requirements, priorities (MoSCoW), and out-of-scope items described in this document reflect their needs, and the development team confirms that these requirements are achievable within the stated constraints.

| | |
|---|---|
| **For the client (Meítǐ Shāngchéng)** | **For the development team (Pro B)** |
| Name: _____________________________ | Name: _____________________________ |
| Signature: _________________________ | Signature: _________________________ |
| Date: _____________________________ | Date: _____________________________ |

---

## 13. Acceptance Criteria

The system is considered accepted when the following are met (aligned with the assessment table in the Student Reader):

1. All **Must (M)** functional requirements (FR01–FR09, FR14) are implemented and working without severe bugs.
2. All **Should (S)** requirements (FR10, FR11, FR13) are implemented and functional.
3. **Could (C)** requirements (FR12, FR15) are implemented if time permits; their absence does not block acceptance.
4. The non-functional requirements NFR01–NFR04 are demonstrably satisfied (performance ≤ 2 s, role-based access, ≥ 100 employees supported).
5. The system is demonstrated to the client at the final presentation, and the client confirms the core flows (add employee, search employee, assign shift, view own schedule) match this specification.
6. The source code is committed to the shared Git repository by all team members, and the document set (Project Plan, this URS, Test Plan) is delivered.

---
