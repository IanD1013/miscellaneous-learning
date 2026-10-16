### INSERT INTO - 向表中添加新行

每个数据库应用程序都需要存储新数据。
无论是新用户注册、下单，还是向库存中添加商品，`INSERT INTO` 语句都是向表中添加行的方式。
理解其语法是使用任何 SQL 数据库的基础。

### 工作原理

`INSERT INTO` 语句会在指定的表中创建新行。
列出想要填充的列，然后按相同顺序提供对应的值。
任何省略的列都将获得其默认值 - 对于 SQLite 中的 `INTEGER PRIMARY KEY`，这意味着自动分配下一个可用的整数。

可以将其想象为填写表单：指定要填写的字段并为每个字段提供数据。
数据库会处理剩下的工作。

### 语法

```sql
INSERT INTO table_name (column1, column2, column3)
VALUES (value1, value2, value3);
```

关键点：

- 列名放在表名后面的括号中
- 值放在 `VALUES` 关键字后面的括号中
- 值的顺序必须与列的顺序相匹配
- 文本值用单引号括起来：`'some text'`
- 数值不带引号书写：`42`、`3.14`
- 可以省略具有默认值或自动递增行为的列

### 示例

```sql
-- 一个表：employees(id INTEGER PRIMARY KEY, name TEXT, department TEXT, salary REAL)

-- 插入单个员工，让 id 自动分配
INSERT INTO employees (name, department, salary)
VALUES ('Maria Chen', 'Engineering', 95000.00);

-- 显式插入所有列，包括 id
INSERT INTO employees (id, name, department, salary)
VALUES (50, 'James Park', 'Marketing', 72000.00);

-- 仅插入必需的列（如果 department 有默认值）
INSERT INTO employees (name, salary)
VALUES ('Aisha Patel', 88000.00);
```

### 常见模式

| 模式 | 示例 | 说明 |
| --- | --- | --- |
| 省略自增列 | `INSERT INTO t (col1) VALUES ('x')` | 让 SQLite 分配 ID |
| 文本值 | `VALUES ('hello')` | 始终使用单引号 |
| 数值 | `VALUES (42, 3.14)` | 无需引号 |
| NULL 值 | `VALUES (NULL)` | 显式插入 NULL |

### SQLite 自增行为

在 SQLite 中，声明为 `INTEGER PRIMARY KEY` 的列会自动用作行 ID。
如果在插入时省略它，SQLite 将分配下一个可用的整数。
这是 SQLite 中处理自动生成 ID 的惯用方式 - 只需在 `INSERT` 语句中忽略该列即可。

### 你的任务

`products` 表中已经包含三个产品。
你的任务是插入一个包含以下详细信息的**新产品**：

- **name**：`'Widget'`
- **price**：`9.99`
- 让 `id` 由 SQLite 自动分配

编写一条 `INSERT INTO` 语句将该产品添加到表中。

### 预期结果

插入完成后，查询新产品应返回：

| name | price |
| --- | --- |
| Widget | 9.99 |

### 解答

```sql
-- 插入一个新产品：name 为 'Widget'，price 为 9.99
-- 让 id 自动分配
INSERT INTO products (name, price)
VALUES ('Widget', 9.99);
```
