### 带有 RETURNING 的 INSERT

RETURNING 子句允许您从受 INSERT 语句影响的行中检索值。
这对于获取自动生成的值（例如 SERIAL ID）特别有用，而无需执行单独的查询。

### 基本语法

```sql
INSERT INTO table_name (column1, column2)
VALUES ('value1', 'value2')
RETURNING column_name;
```

### 获取自动生成的 ID

当表具有 SERIAL 或 BIGSERIAL 主键时，PostgreSQL 会自动生成 ID。
RETURNING 允许您立即获取它：

```sql
-- 不使用 RETURNING：你需要单独执行一次 SELECT 来查找新 ID
INSERT INTO users (name) VALUES ('Alice');
SELECT id FROM users WHERE name = 'Alice';  -- 如果存在重复项则不可靠！

-- 使用 RETURNING：在一条语句中获取 ID
INSERT INTO users (name) VALUES ('Alice')
RETURNING id;
-- 返回：id = 1（或任何生成的值）
```

### 返回多个列

您可以返回任何列，包括计算值和默认值：

```sql
INSERT INTO products (name, price)
VALUES ('Widget', 19.99)
RETURNING id, name, price, created_at;
```

### 返回所有列

使用 `*` 返回插入的整行：

```sql
INSERT INTO orders (customer_id, total)
VALUES (1, 99.99)
RETURNING *;
```

### 您的任务

插入一名具有以下详细信息的新员工：

- **name**: 'Sarah Johnson'
- **email**: '[sarah.johnson@company.com](mailto:sarah.johnson@company.com)'
- **department**: 'Engineering'

使用 RETURNING 子句**仅返回生成的 id** 列。

### 预期结果

您的查询应返回单行，其中包含一个名为 `id` 的列，该列包含自动生成的员工 ID。

### 解答

```sql
-- 插入一名新员工并返回生成的 id
-- 姓名：'Sarah Johnson'
-- 邮箱：'sarah.johnson@company.com'
-- 部门：'Engineering'

INSERT INTO employees (name, email, department)
VALUES ('Sarah Johnson', 'sarah.johnson@company.com', 'Engineering')
RETURNING id;
```
