### SQLite 中的 WITHOUT ROWID 表

在 SQLite 中创建的每个表默认都会隐式包含一个名为 `rowid` 的隐藏列 - 这是一个唯一标识每行的 64 位整数。
SQLite 使用此 rowid 作为其 B-tree 存储引擎的内部键。
但如果你的表本身已经拥有一个非常合适的主键（例如文本标识符或复合键）呢？
在这种情况下，额外的 rowid 会浪费空间并增加开销。
SQLite 允许你通过将表声明为 `WITHOUT ROWID` 来选择不使用自动生成的 rowid。

WITHOUT ROWID 表直接按照你声明的 `PRIMARY KEY` 来组织并存储数据。
这意味着按该键进行查找的速度可能会更快（无需通过 rowid 进行额外的间接寻址），并且你可以节省隐藏 rowid 列所占用的存储空间。

### 工作原理

在普通（rowid）表中，SQLite 维护两个 B-tree 结构：一个按 `rowid` 索引并保存所有数据，另一个用于存放任何附加索引的独立 B-tree。
当你按非 rowid 主键进行查询时，SQLite 会首先搜索索引以找到 rowid，然后使用该 rowid 查找实际行 - 这是一个分两步的过程。

在 WITHOUT ROWID 表中，不存在隐藏的 rowid。
该表的 B-tree 直接由声明的 PRIMARY KEY 组织。
这消除了额外的查找步骤，并去除了 rowid 列的存储开销。
权衡之处在于，WITHOUT ROWID 表要求在表定义中显式指定一个 `PRIMARY KEY`。

### 语法

```sql
-- WITHOUT ROWID 表的通用语法
CREATE TABLE table_name (
    column1 datatype PRIMARY KEY,
    column2 datatype,
    ...
) WITHOUT ROWID;

-- 复合主键版本
CREATE TABLE table_name (
    col_a datatype NOT NULL,
    col_b datatype NOT NULL,
    col_c datatype,
    PRIMARY KEY (col_a, col_b)
) WITHOUT ROWID;
```

### 示例

```sql
-- 国家代码查找表 - ISO 代码本身就是天然键
CREATE TABLE country_codes (
    code TEXT PRIMARY KEY,
    name TEXT NOT NULL
) WITHOUT ROWID;

-- 带复合键的多对多关系表
CREATE TABLE student_courses (
    student_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    enrolled_date TEXT NOT NULL,
    PRIMARY KEY (student_id, course_id)
) WITHOUT ROWID;

-- 用于图的边权重表
CREATE TABLE edges (
    source TEXT NOT NULL,
    target TEXT NOT NULL,
    weight REAL DEFAULT 1.0,
    PRIMARY KEY (source, target)
) WITHOUT ROWID;
```

### 何时使用 WITHOUT ROWID

| 场景 | 优势 |
| --- | --- |
| 非整数主键（TEXT、BLOB） | 避免存储冗余的 rowid |
| 复合主键 | 单次 B-tree 查找而不是两次 |
| 列数较少的小型数据行 | 显著节省存储空间 |
| 键值存储（Key-value stores） | 基于键的直接访问，无间接寻址 |

当行数据较大或经常需要直接使用 `rowid` 时，请避免使用 WITHOUT ROWID。

### 你的任务

创建一个名为 `settings` 的表，以键值对形式存储应用程序配置。
该表应满足以下要求：

- 包含一个 `TEXT` 类型的 `key` 列，作为主键
- 包含一个 `TEXT NOT NULL` 类型的 `value` 列
- 创建为 **WITHOUT ROWID** 表，因为文本键是天然的查找标识符，无需隐藏的 rowid

### 预期结果

```sql
-- 你的 DDL 运行后：
-- 'settings' 表存在于 sqlite_master 中
-- 该表的 SQL 定义包含 WITHOUT ROWID
-- 该表包含以下列：key (TEXT)、value (TEXT NOT NULL)
-- 按 key 插入和查询都能正常工作
```

### 解答

```sql
-- 创建一个名为 'settings' 的 WITHOUT ROWID 表
-- 包含以下列：key (TEXT PRIMARY KEY) 和 value (TEXT NOT NULL)
CREATE TABLE settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
) WITHOUT ROWID;
```
