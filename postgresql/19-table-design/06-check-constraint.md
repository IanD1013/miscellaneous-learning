### CHECK 约束

`CHECK` 约束用于验证列中的值是否满足特定条件。
它就像一个守门人，会拒绝任何不符合业务规则的数据。

### 基本语法

```sql
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price NUMERIC(10,2) CHECK (price > 0)
);
```

`CHECK` 后面的表达式必须包裹在括号中。
`CHECK (price > 0)` 是有效的，而 `CHECK price > 0` 会导致语法错误。

### 常见的 CHECK 表达式

```sql
-- 数值范围
CHECK (quantity >= 0)
CHECK (age BETWEEN 0 AND 150)
CHECK (discount >= 0 AND discount <= 100)

-- 字符串验证
CHECK (status IN ('pending', 'active', 'completed'))
CHECK (LENGTH(code) = 6)

-- 比较列
CHECK (end_date > start_date)
```

### 命名的 CHECK 约束

你可以为约束命名，以获得更清晰的错误消息：

```sql
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    quantity INTEGER CONSTRAINT positive_quantity CHECK (quantity > 0)
);
```

### CHECK 与应用程序逻辑

| 方式 | 优点 | 缺点 |
| --- | --- | --- |
| CHECK 约束 | 在数据库级别强制执行，始终保持一致 | 仅限于 SQL 表达式 |
| 应用程序验证 | 更灵活，错误提示更友好 | 可能会被绕过，存在不一致性 |

最佳实践：对于绝对不应被违反的基本业务规则，请使用 CHECK。

### 你的任务

创建一个包含以下列的 `products` 表：

- `id` - 自增主键
- `name` - 产品名称，必填，最多 100 个字符
- `price` - 带有 2 位小数的数值，必须大于 0
- `stock` - 整数，必须为 0 或更大（非负数）

### 预期表结构

```sql
products
├── id (SERIAL PRIMARY KEY)
├── name (VARCHAR(100) NOT NULL)
├── price (NUMERIC(10,2), CHECK (price > 0))
└── stock (INTEGER, CHECK (stock >= 0))
```

### 解答

```sql
-- 创建带有 CHECK 约束的 products 表
-- price 必须大于 0
-- stock 必须为 0 或更大

CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price NUMERIC(10,2) CHECK (price > 0),
    stock INTEGER CHECK (stock >= 0)
);
```
