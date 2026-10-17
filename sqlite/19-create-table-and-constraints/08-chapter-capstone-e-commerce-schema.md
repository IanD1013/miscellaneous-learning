### 本章综合实战：带约束的多表模式

在实际应用中，数据库很少仅由单个表构成。
相反，数据分布在多个相关的表中，每个表都有精心选择的约束，以在数据库级别强制保证数据完整性。
本次综合实战将把你所学到的关于 `CREATE TABLE`、`PRIMARY KEY`、`NOT NULL`、`DEFAULT`、`UNIQUE`、`CHECK` 和 `FOREIGN KEY` 约束的全部知识融合到一个完整的模式（schema）中。

### 为什么约束很重要

约束是抵御不良数据的第一道防线。
约束不仅依赖应用程序代码来验证输入，而且能确保无论数据通过何种方式进入数据库（无论是通过应用程序、脚本还是手动查询），这些规则都会始终得到强制执行。

- **PRIMARY KEY**：唯一标识每一行
- **NOT NULL**：防止关键列中出现缺失值
- **UNIQUE**：确保没有重复值（例如邮箱地址）
- **DEFAULT**：在未指定值时提供自动默认值
- **CHECK**：在允许插入之前根据条件验证数据
- **FOREIGN KEY**：关联不同表中的行，确保引用完整性

### 语法回顾

```sql
-- 创建一个带有多种约束的表
CREATE TABLE employees (
    id INTEGER PRIMARY KEY,
    badge_number TEXT UNIQUE NOT NULL,
    full_name TEXT NOT NULL,
    salary REAL NOT NULL CHECK(salary >= 0),
    department_id INTEGER NOT NULL REFERENCES departments(id),
    hired_on TEXT DEFAULT (date('now'))
);
```

关键要点：

- SQLite 中的 `INTEGER PRIMARY KEY` 使该列成为 `rowid` 的别名（自增）
- `DEFAULT (expression)` 在诸如 `datetime('now')` 之类的表达式周围使用括号
- `REFERENCES table(column)` 在列定义中内联创建外键
- 可以在单个列上组合多个约束
- 多个 `CREATE TABLE` 语句之间用分号分隔

### 示例

```sql
-- 带有 UNIQUE 和 NOT NULL 的表
CREATE TABLE warehouses (
    id INTEGER PRIMARY KEY,
    code TEXT UNIQUE NOT NULL,
    location TEXT NOT NULL,
    capacity INTEGER NOT NULL DEFAULT 100 CHECK(capacity > 0)
);

-- 引用另一个表并带有 DEFAULT 日期的表
CREATE TABLE shipments (
    id INTEGER PRIMARY KEY,
    warehouse_id INTEGER NOT NULL REFERENCES warehouses(id),
    weight_kg REAL NOT NULL CHECK(weight_kg > 0),
    shipped_at TEXT NOT NULL DEFAULT (datetime('now'))
);
```

### SQLite 特别说明

| 特性 | SQLite 行为 |
| --- | --- |
| `INTEGER PRIMARY KEY` | 通过 rowid 自增 |
| `datetime('now')` | 以文本形式返回当前 UTC 日期时间 |
| `date('now')` | 以文本形式返回当前 UTC 日期 |
| `REFERENCES` | 外键需要 `PRAGMA foreign_keys = ON` 才能强制生效 |
| 多个语句 | 用分号分隔，按顺序执行 |

### 你的任务

在单个 SQL 脚本中创建三个相关的表：

**1. `customers`**

- `id` - integer 主键
- `email` - text，唯一，不能为空
- `name` - text，不能为空
- `joined_at` - text，默认为当前日期时间

**2. `products`**

- `id` - integer 主键
- `sku` - text，唯一，不能为空
- `name` - text，不能为空
- `price` - real，不能为空，必须大于 0
- `stock` - integer，不能为空，默认为 0，必须 >= 0

**3. `orders`**

- `id` - integer 主键
- `customer_id` - integer，不能为空，引用 customers 的外键
- `product_id` - integer，不能为空，引用 products 的外键
- `quantity` - integer，不能为空，必须大于 0
- `order_date` - text，不能为空，默认为当前日期

请记住：当涉及外键时，创建表的顺序至关重要！

### 解答

```sql
-- 创建全部三个表：customers、products 和 orders
-- 记得按要求定义所有约束！
-- 先创建父表 customers 和 products，再创建引用它们的 orders
CREATE TABLE customers (
    id INTEGER PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    joined_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    sku TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    price REAL NOT NULL CHECK(price > 0),
    stock INTEGER NOT NULL DEFAULT 0 CHECK(stock >= 0)
);

CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(id),
    product_id INTEGER NOT NULL REFERENCES products(id),
    quantity INTEGER NOT NULL CHECK(quantity > 0),
    order_date TEXT NOT NULL DEFAULT (date('now'))
);
```
