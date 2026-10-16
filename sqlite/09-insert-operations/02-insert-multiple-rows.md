### 使用单个 INSERT 插入多行

在向数据库表中填充数据时，你通常需要一次添加多行。
SQL 支持**多行 VALUES** 语法，允许你在单个语句中插入多行，而不是为每一行编写单独的 `INSERT` 语句。
这种方式更清晰、更快速，并减少了与数据库的往返通信。

### 工作原理

标准的单行 `INSERT` 在 `VALUES` 关键字后的一对圆括号中提供一组值。
多行形式只需添加更多组由逗号分隔的圆括号即可。
每个带括号的组代表一个新行。
数据库会将所有行作为单次操作的一部分进行插入。

### 语法

```sql
INSERT INTO table_name (column1, column2, ...)
VALUES
    (value1a, value2a, ...),
    (value1b, value2b, ...),
    (value1c, value2c, ...);
```

要点：

- 每个带括号的组必须具有与列列表匹配的**相同数量的值**
- 每个组内的值用逗号分隔
- 各组之间用逗号分隔
- 用一个分号结束整个语句

### 示例

```sql
-- 向 colors 表中插入三种颜色
INSERT INTO colors (name, hex_code)
VALUES
    ('Red', '#FF0000'),
    ('Green', '#00FF00'),
    ('Blue', '#0000FF');

-- 插入两个不同部门的员工
INSERT INTO employees (first_name, last_name, department)
VALUES
    ('Maria', 'Garcia', 'Engineering'),
    ('James', 'Wilson', 'Marketing');

-- 如果为所有列提供值，也可以省略列名
-- （SQLite 中的自增主键除外，它可以省略）
INSERT INTO status_codes (code, description)
VALUES
    (200, 'OK'),
    (404, 'Not Found'),
    (500, 'Internal Server Error');
```

### 常见模式

| 模式 | 示例 |
| --- | --- |
| 单列插入 | `INSERT INTO tags (name) VALUES ('sql'), ('python'), ('rust');` |
| 多列插入 | `INSERT INTO products (name, price) VALUES ('A', 9.99), ('B', 19.99);` |
| 包含自增主键（PK） | 省略主键列，SQLite 会自动分配 ID |

### 你的任务

你有一个包含两列的空表 `categories`：

- `id` - 自增整数主键
- `name` - 类别名称的文本字段

编写**单个** `INSERT` 语句来添加以下四个类别：

- Electronics
- Books
- Clothing
- Food

使用多行 `VALUES` 语法，以便通过一条语句插入所有四行。
你不需要指定 `id` 列 - SQLite 会自动分配它。

### 预期结果

在你的语句运行后，查询 `SELECT name FROM categories ORDER BY name` 应该返回：

| name |
| --- |
| Books |
| Clothing |
| Electronics |
| Food |

### 解答

```sql
-- 在单个 INSERT 语句中插入 4 个类别
INSERT INTO categories (name)
VALUES
    ('Electronics'),
    ('Books'),
    ('Clothing'),
    ('Food');
```
