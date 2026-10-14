### NOT NULL 约束

`NOT NULL` 约束确保列不能包含 NULL 值，使其成为每行都必须有值的必填字段。

### 为什么使用 NOT NULL？

NULL 表示缺失或未知的数据。
虽然有时是合理的，但许多列应该始终具有值：

- 人的姓名不应该为空
- 订单必须有日期
- 产品需要有价格

### 语法

```sql
CREATE TABLE table_name (
    column_name data_type NOT NULL,
    optional_column data_type  -- 默认允许 NULL
);
```

### 示例

```sql
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,      -- 必填
    price NUMERIC(10,2) NOT NULL,    -- 必填
    description TEXT                  -- 可选（允许 NULL）
);
```

### 使用 NOT NULL 会发生什么？

```sql
-- 这会成功：
INSERT INTO products (name, price) VALUES ('Widget', 9.99);

-- 这会因错误而失败：
INSERT INTO products (name, price) VALUES (NULL, 9.99);
-- ERROR: null value in column "name" violates not-null constraint
```

### 与 PRIMARY KEY 结合使用

PRIMARY KEY 列会自动设为 NOT NULL，因此无需同时指定两者：

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,           -- 隐式 NOT NULL
    email VARCHAR(255) NOT NULL      -- 显式 NOT NULL
);
```

### 你的任务

创建包含以下列的 `employees` 表：

| 列 | 类型 | 约束 |
| --- | --- | --- |
| id | SERIAL | PRIMARY KEY |
| first\_name | VARCHAR(50) | NOT NULL |
| last\_name | VARCHAR(50) | NOT NULL |
| email | VARCHAR(100) | NOT NULL |
| phone | VARCHAR(20) | （可选，允许 NULL） |
| hire\_date | DATE | NOT NULL |

该表强制要求每位员工都必须有名（first name）、姓（last name）、电子邮箱（email）和入职日期（hire date），但电话号码（phone number）是可选的。

### 解答

```sql
-- 创建带有恰当 NOT NULL 约束的 employees 表
CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    -- 添加其余带有恰当约束的列
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    hire_date DATE NOT NULL
);
```
