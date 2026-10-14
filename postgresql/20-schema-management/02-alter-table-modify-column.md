### ALTER TABLE - 修改列

创建表之后，你通常需要修改现有的列。
PostgreSQL 的 `ALTER TABLE` 命令允许你更改列的数据类型、添加或删除约束，以及设置或移除默认值。

### 更改列的数据类型

使用 `ALTER COLUMN ... TYPE` 更改列的数据类型：

```sql
-- 将 price 从 INTEGER 改为 NUMERIC 以支持小数
ALTER TABLE products
ALTER COLUMN price TYPE NUMERIC(10,2);

-- 将 description 从 VARCHAR(100) 改为 TEXT
ALTER TABLE products
ALTER COLUMN description TYPE TEXT;
```

**注意：** 类型更改必须相互兼容。
PostgreSQL 可以在某些类型之间自动转换，但其他类型可能需要 `USING` 子句：

```sql
-- 通过显式类型转换将文本转换为整数
ALTER TABLE orders
ALTER COLUMN quantity TYPE INTEGER USING quantity::INTEGER;
```

### 添加 NOT NULL 约束

使用 `SET NOT NULL` 要求某列必须始终有值：

```sql
-- 将 email 设为必填
ALTER TABLE users
ALTER COLUMN email SET NOT NULL;
```

**重要提示：** 在添加此约束之前，所有现有行在该列中的值必须为非 NULL！

### 删除 NOT NULL 约束

使用 `DROP NOT NULL` 允许 NULL 值：

```sql
-- 将 phone 设为可选
ALTER TABLE users
ALTER COLUMN phone DROP NOT NULL;
```

### 设置与删除默认值

```sql
-- 设置默认值
ALTER TABLE products
ALTER COLUMN stock SET DEFAULT 0;

-- 移除默认值
ALTER TABLE products
ALTER COLUMN stock DROP DEFAULT;
```

### 合并多项更改

你可以在一条语句中合并多个修改操作：

```sql
ALTER TABLE products
ALTER COLUMN price TYPE NUMERIC(10,2),
ALTER COLUMN price SET NOT NULL;
```

### 你的任务

你有一个 `products` 表，其中的 `price` 列当前被定义为 `INTEGER` 并且允许 NULL 值。
业务需求发生了变更：

1. 将 `price` 列的类型从 `INTEGER` 改为 `NUMERIC(10,2)` 以支持小数价格
2. 添加 `NOT NULL` 约束以确保每个产品都有价格

编写一条 ALTER TABLE 语句来完成这两项修改。

### 修改后的预期模式（Schema）

| 列 | 类型 | 是否可为空 |
| --- | --- | --- |
| id | integer | NO |
| name | varchar(100) | NO |
| price | numeric(10,2) | NO |
| stock | integer | YES |

### 解答

```sql
-- 修改 price 列：
-- 1. 将类型从 INTEGER 改为 NUMERIC(10,2)
-- 2. 添加 NOT NULL 约束

ALTER TABLE products
ALTER COLUMN price TYPE NUMERIC(10,2),
ALTER COLUMN price SET NOT NULL;
```
