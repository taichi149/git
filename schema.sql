-- 文件：db/schema.sql
-- M3 员工管理：建表 + 演示数据（可选执行）
-- 用法：mysql -u root -p hardware_store < schema.sql
-- 说明：如果 M1 已经建过 employee 表，只需确认字段与下面一致；
--       缺字段时用文件末尾的 ALTER 语句补齐，不要重复建表。

CREATE DATABASE IF NOT EXISTS hardware_store
    DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE hardware_store;

-- ----------------------------------------------------------------------
-- 员工表（M3 的核心表）
-- ----------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS employee (
    id                INT AUTO_INCREMENT PRIMARY KEY,
    employee_id       VARCHAR(20)  NOT NULL COMMENT '工号（业务唯一）',
    name              VARCHAR(50)  NOT NULL COMMENT '姓名',
    age               INT          NULL COMMENT '年龄',
    position          VARCHAR(100) NULL COMMENT '岗位',
    salary            DECIMAL(10,2) NULL COMMENT '薪资（月薪）',
    department        VARCHAR(100) NULL COMMENT '部门',
    email             VARCHAR(100) NULL COMMENT '邮箱',
    contact_address   VARCHAR(100) NULL COMMENT '联系地址',
    emergency_contact VARCHAR(100) NULL COMMENT '紧急联系人',
    is_archived       TINYINT(1)   NOT NULL DEFAULT 0 COMMENT '1=已归档（软删除）',
    UNIQUE KEY uk_employee_id (employee_id),
    KEY idx_archived (is_archived)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------------------------------------------------
-- 账号表（M2 登录用；已存在可跳过）
-- ----------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS user (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    username        VARCHAR(50) NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    role            VARCHAR(20) NOT NULL COMMENT 'HRAdmin / StoreManager / Employee',
    UNIQUE KEY uk_username (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------------------------------------------------
-- 演示数据：只在表为空时插入，重复执行不会产生重复行
-- ----------------------------------------------------------------------
INSERT INTO employee (employee_id, name, age, position, salary, department, email,
                      contact_address, emergency_contact, is_archived)
SELECT * FROM (
    SELECT 'E001' AS employee_id, '张三' AS name, 28 AS age, '收银员' AS position,
           5200.00 AS salary, '门店' AS department, 'zhangsan@meiti.com' AS email,
           '郑州市二七区大学路 18 号' AS contact_address,
           '张父 13800000001' AS emergency_contact, 0 AS is_archived
    UNION ALL SELECT 'E002', '李四', 35, '库管', 6100.00, '仓库', 'lisi@meiti.com',
           '郑州市中原区建设路 66 号', '李母 13800000002', 0
    UNION ALL SELECT 'E003', '王五', 24, '理货员', 4800.00, '门店', 'wangwu@meiti.com',
           '郑州市金水区花园路 9 号', '王父 13800000003', 0
    UNION ALL SELECT 'E004', '赵六', 41, '店长', 9800.00, '门店', 'zhaoliu@meiti.com',
           '郑州市郑东新区商务内环 2 号', '赵妻 13800000004', 0
    UNION ALL SELECT 'E005', '孙七', 30, '采购', 7200.00, '采购部', 'sunqi@meiti.com',
           '郑州市高新区科学大道 100 号', '孙弟 13800000005', 0
) AS seed
WHERE NOT EXISTS (SELECT 1 FROM employee);

-- ----------------------------------------------------------------------
-- 如果 M1 的 employee 表缺少 M3 需要的字段，按需补（已存在会报错，忽略即可）
-- ----------------------------------------------------------------------
-- ALTER TABLE employee ADD COLUMN age INT NULL;
-- ALTER TABLE employee ADD COLUMN position VARCHAR(100) NULL;
-- ALTER TABLE employee ADD COLUMN salary DECIMAL(10,2) NULL;
-- ALTER TABLE employee ADD COLUMN department VARCHAR(100) NULL;
-- ALTER TABLE employee ADD COLUMN email VARCHAR(100) NULL;
-- ALTER TABLE employee ADD COLUMN contact_address VARCHAR(100) NULL;
-- ALTER TABLE employee ADD COLUMN emergency_contact VARCHAR(100) NULL;
-- ALTER TABLE employee ADD COLUMN is_archived TINYINT(1) NOT NULL DEFAULT 0;
-- ALTER TABLE employee ADD UNIQUE KEY uk_employee_id (employee_id);
