-- 文件：db/schema_m4.sql
-- M4 手动排班：排班表 + 演示数据（可选执行）
-- 用法：mysql -u root -p hardware_store < schema_m4.sql
-- 前提：employee 表已存在（M3 的 schema.sql 已建好）。

USE hardware_store;

-- ----------------------------------------------------------------------
-- 排班表（M4 的核心表）
-- 班次取值：Morning 早班 / Afternoon 中班 / Evening 晚班（和客户约定的一天三班）
-- (employee_id, shift_date) 唯一键：同一员工同一天最多一个班，重复排班即改班。
-- ----------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS shift (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT         NOT NULL COMMENT '员工主键（employee.id）',
    shift_date  DATE        NOT NULL COMMENT '排班日期',
    shift_type  VARCHAR(20) NOT NULL COMMENT 'Morning 早班 / Afternoon 中班 / Evening 晚班',
    UNIQUE KEY uk_emp_date (employee_id, shift_date),
    KEY idx_date (shift_date),
    CONSTRAINT fk_shift_employee FOREIGN KEY (employee_id) REFERENCES employee (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------------------------------------------------
-- 演示数据：以「今天」为基准排几天的班，方便打开全店周视图时立刻看到效果。
-- 用 ON DUPLICATE KEY UPDATE 保证重复执行不会报错、不会产生冲突。
-- ----------------------------------------------------------------------
INSERT INTO shift (employee_id, shift_date, shift_type)
SELECT id, CURDATE(), 'Morning' FROM employee WHERE employee_id = 'E001'
ON DUPLICATE KEY UPDATE shift_type = VALUES(shift_type);

INSERT INTO shift (employee_id, shift_date, shift_type)
SELECT id, CURDATE(), 'Afternoon' FROM employee WHERE employee_id = 'E002'
ON DUPLICATE KEY UPDATE shift_type = VALUES(shift_type);

INSERT INTO shift (employee_id, shift_date, shift_type)
SELECT id, DATE_ADD(CURDATE(), INTERVAL 1 DAY), 'Evening' FROM employee WHERE employee_id = 'E001'
ON DUPLICATE KEY UPDATE shift_type = VALUES(shift_type);

INSERT INTO shift (employee_id, shift_date, shift_type)
SELECT id, DATE_ADD(CURDATE(), INTERVAL 1 DAY), 'Morning' FROM employee WHERE employee_id = 'E003'
ON DUPLICATE KEY UPDATE shift_type = VALUES(shift_type);

INSERT INTO shift (employee_id, shift_date, shift_type)
SELECT id, DATE_ADD(CURDATE(), INTERVAL 2 DAY), 'Afternoon' FROM employee WHERE employee_id = 'E002'
ON DUPLICATE KEY UPDATE shift_type = VALUES(shift_type);
