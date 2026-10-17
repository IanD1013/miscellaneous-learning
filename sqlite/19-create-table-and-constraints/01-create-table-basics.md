### SQLite 中的 CREATE TABLE

`CREATE TABLE` 语句是最基础的 SQL 命令之一 - 它在存储任何数据之前先定义数据的结构。
你在数据库中操作的每一个表都是通过该语句创建的，用来指定列名、它们的类型亲和性（type affinities）以及主键等约束。

### 工作原理

当你执行 `CREATE TABLE` 时，SQLite 会在数据库中创建一个包含你所定义列的新表。
每列都有一个**名称**和一个**类型亲和性**（type affinity），用来告诉 SQLite 如何处理存储在其中的数据。
与许多其他数据库不同，SQLite 使用基于**类型亲和性**的灵活类型系统，而不是严格的类型系统 - 但为了清晰性、兼容性和优化，声明类型仍然非常重要。

### 语法

```sql
CREATE TABLE table_name (
    column1 TYPE_AFFINITY CONSTRAINTS,
    column2 TYPE_AFFINITY CONSTRAINTS,
    column3 TYPE_AFFINITY
);
```

每个列定义包括：

1. **列名** - 具有描述性的标识符
2. **类型亲和性** - 指导 SQLite 如何存储和比较值
3. **约束**（可选） - 例如 `PRIMARY KEY`、`NOT NULL`、`UNIQUE`、`DEFAULT` 等规则

### SQLite 类型亲和性

SQLite 有五种决定存储行为的类型亲和性：

| 亲和性 | 适用场景 | 示例 |
| --- | --- | --- |
| `INTEGER` | 整数、ID、计数 | `42`, `-7`, `1000000` |
| `TEXT` | 字符串、作为字符串的日期、描述 | `'hello'`, `'2024-01-15'` |
| `REAL` | 浮点数、测量值 | `3.14`, `99.99` |
| `BLOB` | 二进制数据（图像、文件） | 原始字节 |
| `NUMERIC` | 既可以是整数也可以是实数的值 | `10`, `10.5`, `'20'` |

### 示例

```sql
-- 包含多种列类型的员工表
CREATE TABLE employees (
    id INTEGER PRIMARY KEY,
    full_name TEXT NOT NULL,
    salary REAL,
    department TEXT DEFAULT 'General',
    hire_date TEXT
);

-- 传感器读数表
CREATE TABLE readings (
    id INTEGER PRIMARY KEY,
    sensor_id INTEGER NOT NULL,
    temperature REAL,
    recorded_at TEXT NOT NULL
);

-- 文件存储表
CREATE TABLE attachments (
    id INTEGER PRIMARY KEY,
    filename TEXT NOT NULL,
    file_data BLOB,
    file_size INTEGER
);
```

### SQLite 中的 INTEGER PRIMARY KEY

当你将一列声明为 `INTEGER PRIMARY KEY` 时，SQLite 会将其视为内部 **rowid** 的别名。
这意味着：

- 如果在插入时未提供值，它会自动递增
- 它能唯一标识每一行
- 这是在 SQLite 中定义主键最高效的方式

这与 `INT PRIMARY KEY` 不同 - 只有 `INTEGER`（确切的关键字）才会触发特殊的 rowid 行为。

### 选择合适的亲和性

选择最符合你数据的亲和性：

- 计数相关？ → `INTEGER`
- 存储名称、描述、ISO 日期？ → `TEXT`
- 金额、测量值、百分比？ → `REAL`
- 原始二进制内容？ → `BLOB`
- 混合数值数据？ → `NUMERIC`

### 你的任务

创建一个包含以下各列的 `products` 表：

| 列名 | 类型亲和性 | 用途 |
| --- | --- | --- |
| `id` | `INTEGER PRIMARY KEY` | 产品唯一标识符 |
| `name` | `TEXT` | 产品名称 |
| `price` | `REAL` | 产品价格 |
| `created_at` | `TEXT` | 以文本形式存储的时间戳 |

请确保使用上面指定的完全相同的列名和类型亲和性。

### 预期结果

在你的语句运行后，`products` 表应该存在，且恰好包含四列：`id`、`name`、`price` 和 `created_at`，每一列都具有正确的类型亲和性。

### 解答

```sql
-- 创建包含所需列的 products 表
CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    name TEXT,
    price REAL,
    created_at TEXT
);
```
