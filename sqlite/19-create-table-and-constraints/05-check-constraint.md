### SQLite 中的 CHECK 约束

CHECK 约束允许你对可存储在列中的数据强制执行规则。
它们就像守门员一样，每当插入或更新一行时，SQLite 都会对 CHECK 约束中的布尔表达式进行求值。
如果表达式求值结果为 false（或零），则该操作将被拒绝并报错。
这就是防止无效数据进入数据库的方法。

### 工作原理

CHECK 约束是附加到列或表定义的布尔表达式。
当你执行 INSERT 或 UPDATE 一行时，SQLite 会针对受影响的行评估该表达式。
如果结果为 NULL 或任何非零值，则约束通过。
如果结果恰好为 0（false），则约束失败，语句将被中止。

你可以将 CHECK 约束与列定义内联放置（列级约束），也可以放在所有列之后（表级约束）。
列级约束通常只引用其自身列，而表级约束可以引用多个列。

### 语法

```sql
-- 列级 CHECK 约束
CREATE TABLE table_name (
    column_name DATA_TYPE CHECK(boolean_expression),
    another_column DATA_TYPE CHECK(boolean_expression)
);

-- 表级 CHECK 约束（可以引用多个列）
CREATE TABLE table_name (
    col_a INTEGER,
    col_b INTEGER,
    CHECK(col_a < col_b)
);
```

### 示例

```sql
-- 确保员工年龄在 18 到 120 之间
CREATE TABLE employees (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER CHECK(age >= 18 AND age <= 120)
);

-- 确保折扣百分比保持在有效范围内
CREATE TABLE promotions (
    id INTEGER PRIMARY KEY,
    code TEXT NOT NULL,
    discount_percent REAL CHECK(discount_percent > 0 AND discount_percent <= 100)
);

-- 表级约束，确保 end_date 晚于 start_date
CREATE TABLE events (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    CHECK(end_date > start_date)
);
```

### 常见模式

| 模式 | 表达式 | 使用场景 |
| --- | --- | --- |
| 正数 | `CHECK(column > 0)` | 价格、薪资 |
| 非负数 | `CHECK(column >= 0)` | 数量、计数 |
| 范围验证 | `CHECK(column BETWEEN 1 AND 100)` | 评分、百分比 |
| 枚举类值 | `CHECK(column IN ('A','B','C'))` | 状态代码、类别 |
| 字符串长度 | `CHECK(LENGTH(column) >= 3)` | 最小输入长度 |

### 组合约束

你可以将 CHECK 与同一列上的其他约束（如 NOT NULL、UNIQUE 和 PRIMARY KEY）结合使用。
SQLite 会评估所有约束 - 只要其中任何一个失败，操作就会被拒绝。

```sql
CREATE TABLE accounts (
    id INTEGER PRIMARY KEY,
    email TEXT NOT NULL UNIQUE,
    balance REAL NOT NULL CHECK(balance >= 0)
);
```

### 你的任务

创建一个包含以下列和约束的 `products` 表：

- **id** - `INTEGER PRIMARY KEY`
- **name** - `TEXT NOT NULL`
- **price** - `REAL`，带有 CHECK 约束以确保价格严格大于零
- **quantity** - `INTEGER`，带有 CHECK 约束以确保数量为零或更大（非负）

你的 CREATE TABLE 语句应该强制执行这些数据完整性规则，以使任何产品都不会具有负数价格或负数数量。

### 解答

```sql
-- 创建带有相应 CHECK 约束的 products 表
CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    price REAL CHECK(price > 0),
    quantity INTEGER CHECK(quantity >= 0)
);
```
