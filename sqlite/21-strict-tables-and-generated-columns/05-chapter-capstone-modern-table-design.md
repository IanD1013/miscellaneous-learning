### SQLite 中带有生成列和约束的 STRICT 表

SQLite 的 `STRICT` 表在数据库层面上强制执行类型检查，防止了 SQLite 通常允许的灵活类型亲和性（type affinity）。
结合生成列（`STORED` 和 `VIRTUAL`）以及 `CHECK` 约束，你可以构建出强大的模式（schema），用以强制执行业务规则并在数据库内部自动计算派生值。

### STRICT 表的工作原理

默认情况下，SQLite 允许你将文本值插入到 INTEGER 列中而不会报错。
`STRICT` 表改变了这种行为 - 它会拒绝与声明的列类型不匹配的值。
STRICT 模式下允许的类型有：`INT`、`INTEGER`、`REAL`、`TEXT`、`BLOB` 和 `ANY`。

### 生成列

生成列通过涉及同一行中其他列的表达式来计算其值。
有两种类型：

- **VIRTUAL**：每次读取该行时即时计算。不占用存储空间。
- **STORED**：在插入或更新行时计算一次，然后物理存储在磁盘上。可以建立索引。

生成列不能直接写入 - 它们的值始终派生自表达式。

### 语法

```sql
-- 带有生成列的 STRICT 表
CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    price REAL NOT NULL CHECK(price >= 0),
    quantity INTEGER NOT NULL CHECK(quantity >= 0),
    line_total REAL GENERATED ALWAYS AS (round(price * quantity, 2)) STORED
) STRICT;
```

### 示例

```sql
-- 示例 1：带有虚拟生成列的 STRICT 表
CREATE TABLE rectangles (
    id INTEGER PRIMARY KEY,
    width REAL NOT NULL CHECK(width > 0),
    height REAL NOT NULL CHECK(height > 0),
    area REAL GENERATED ALWAYS AS (round(width * height, 2)) VIRTUAL
) STRICT;

INSERT INTO rectangles (width, height) VALUES (3.5, 2.0);
-- area 自动为 7.0

-- 示例 2：使用 IN 列表限定状态值的 CHECK 约束
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    priority TEXT NOT NULL DEFAULT 'medium' CHECK(priority IN ('low', 'medium', 'high'))
) STRICT;

INSERT INTO tasks (title) VALUES ('Review PR');
-- priority 默认为 'medium'

-- 示例 3：基于同一源数据的多个生成列
CREATE TABLE circles (
    id INTEGER PRIMARY KEY,
    radius REAL NOT NULL CHECK(radius > 0),
    circumference REAL GENERATED ALWAYS AS (round(2 * 3.14159 * radius, 2)) STORED,
    area REAL GENERATED ALWAYS AS (round(3.14159 * radius * radius, 2)) STORED
) STRICT;
```

### 约束参考

| 约束 | 作用 | 示例 |
| --- | --- | --- |
| `NOT NULL` | 列不能为空 | `name TEXT NOT NULL` |
| `CHECK(expr)` | 行必须满足表达式 | `CHECK(price >= 0)` |
| `DEFAULT val` | 省略列时使用的默认值 | `DEFAULT 'active'` |
| `PRIMARY KEY` | 行唯一标识符 | `id INTEGER PRIMARY KEY` |
| `GENERATED ALWAYS AS (expr) STORED` | 计算并保存到磁盘 | `total REAL GENERATED ALWAYS AS (a + b) STORED` |

### 你的任务

创建一个名为 `invoices` 的 `STRICT` 表，包含以下列：

| 列 | 类型 | 规则 |
| --- | --- | --- |
| `id` | INTEGER | PRIMARY KEY |
| `customer_name` | TEXT | NOT NULL |
| `subtotal` | REAL | NOT NULL，必须 >= 0 |
| `tax_rate` | REAL | NOT NULL，必须在 0 到 1 之间（包含 0 和 1） |
| `tax_amount` | REAL | STORED 生成列：`round(subtotal * tax_rate, 2)` |
| `total` | REAL | STORED 生成列：`round(subtotal + subtotal * tax_rate, 2)` |
| `status` | TEXT | NOT NULL，默认值为 `'draft'`，必须是 `'draft'`、`'sent'`、`'paid'` 之一 |

创建表后，插入以下三张发票：

1. 客户 `'Acme Corp'`，subtotal `1000.00`，tax\_rate `0.08`，status `'sent'`
2. 客户 `'Globex Inc'`，subtotal `2500.50`，tax\_rate `0.1`，status `'paid'`
3. 客户 `'Initech'`，subtotal `150.75`，tax\_rate `0.05`（使用默认 status）

生成列应自动为每行计算 `tax_amount` 和 `total`。

### 解答

```sql
-- 创建带有生成列和约束的 STRICT invoices 表
CREATE TABLE invoices (
    id INTEGER PRIMARY KEY,
    customer_name TEXT NOT NULL,
    subtotal REAL NOT NULL CHECK(subtotal >= 0),
    tax_rate REAL NOT NULL CHECK(tax_rate >= 0 AND tax_rate <= 1),
    tax_amount REAL GENERATED ALWAYS AS (round(subtotal * tax_rate, 2)) STORED,
    total REAL GENERATED ALWAYS AS (round(subtotal + subtotal * tax_rate, 2)) STORED,
    status TEXT NOT NULL DEFAULT 'draft' CHECK(status IN ('draft', 'sent', 'paid'))
) STRICT;

-- 插入三张示例发票
INSERT INTO invoices (customer_name, subtotal, tax_rate, status)
VALUES
    ('Acme Corp', 1000.00, 0.08, 'sent'),
    ('Globex Inc', 2500.50, 0.1, 'paid');

INSERT INTO invoices (customer_name, subtotal, tax_rate)
VALUES ('Initech', 150.75, 0.05);
```
