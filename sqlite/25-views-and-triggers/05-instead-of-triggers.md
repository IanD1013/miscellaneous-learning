### SQLite 中视图上的 INSTEAD OF 触发器

SQLite 中的视图是由 `SELECT` 查询定义的虚拟表。
默认情况下，视图是**只读的**，你不能通过它们来 `INSERT`、`UPDATE` 或 `DELETE` 行。
然而，SQLite 支持一种称为 **INSTEAD OF 触发器**（INSTEAD OF trigger）的特殊触发器类型，它可以拦截对视图的 DML 操作，并允许你定义自定义逻辑来修改底层的基表。

这是将复杂的多表操作封装在简单的视图接口之后的一种强大技术。

### 工作原理

当你在包含 `INSTEAD OF INSERT` 触发器的视图上执行 `INSERT` 时：

1. SQLite **不会**尝试向视图中插入数据（这将会失败）
2. 相反，它会触发该触发器主体
3. 在触发器内部，你可以通过 `NEW.column_name` 访问正在插入的值
4. 你编写自己的 `INSERT` 语句来针对实际的基表进行操作

`NEW` 伪表保存了调用方尝试插入到视图中的行。
对于 `UPDATE` 触发器，`NEW` 和 `OLD` 均可用。
对于 `DELETE` 触发器，只有 `OLD` 可用。

### 语法

```sql
-- 视图上 INSTEAD OF INSERT 触发器的通用语法
CREATE TRIGGER trigger_name
INSTEAD OF INSERT ON view_name
BEGIN
    -- 使用 NEW.column 引用插入的值
    INSERT INTO base_table1 (col1, col2) VALUES (NEW.col1, NEW.col2);
    INSERT INTO base_table2 (col3, col4) VALUES (NEW.col3, NEW.col4);
END;
```

### 示例

考虑一个包含 `departments` 和 `employees` 表的数据库，以及连接它们的视图：

```sql
-- 连接两个表的视图
CREATE VIEW department_staff AS
SELECT d.name AS dept_name, e.name AS emp_name, e.salary
FROM departments d
JOIN employees e ON d.id = e.department_id;

-- 让视图变得“可插入”
CREATE TRIGGER insert_department_staff
INSTEAD OF INSERT ON department_staff
BEGIN
    -- 查找或创建部门，然后插入员工
    INSERT OR IGNORE INTO departments (name) VALUES (NEW.dept_name);
    INSERT INTO employees (name, salary, department_id)
    VALUES (NEW.emp_name, NEW.salary,
            (SELECT id FROM departments WHERE name = NEW.dept_name));
END;
```

现在你可以编写：

```sql
INSERT INTO department_staff (dept_name, emp_name, salary)
VALUES ('Engineering', 'Alice', 95000);
```

触发器会拦截该操作，并对 `departments` 和 `employees` 执行实际的插入操作。

### 关键要点

| 概念 | 描述 |
| --- | --- |
| `INSTEAD OF` | 替换默认操作 - 视图本身绝不会被修改 |
| `NEW` | 包含用户尝试插入的行的伪表 |
| `OLD` | 用于 UPDATE/DELETE 触发器的伪表（在 INSERT 中不可用） |
| `INSERT OR IGNORE` | 在向查找表插入数据时，用于避免重复项非常有用 |
| `sqlite_master` | 存储触发器定义的系统表 |

### 你的任务

你会获得两个基表：`authors` 和 `books`，以及一个连接它们的名为 `book_catalog` 的视图。
该视图显示 `author_name`、`author_country`、`book_title`、`book_year` 和 `book_price`。

在 `book_catalog` 视图上创建一个名为 `insert_book_catalog` 的 **INSTEAD OF INSERT** 触发器。
当有人向该视图插入数据时，你的触发器应该：

1. 如果作者尚不存在，则将其插入到 `authors` 表中（使用 `INSERT OR IGNORE`，因为 `author_name` 具有 UNIQUE 约束）
2. 将书籍插入到 `books` 表中，从 `authors` 表中查找对应的 `author_id`

创建触发器后，通过视图执行插入以添加：

- 作者：`'Ursula K. Le Guin'`，国家：`'USA'`
- 书籍：`'The Left Hand of Darkness'`，年份：`1969`，价格：`14.99`

编写 `CREATE TRIGGER` 语句和 `INSERT INTO book_catalog` 语句**两者**。

### 解答

```sql
-- 第 1 步：在 book_catalog 视图上创建 INSTEAD OF INSERT 触发器
CREATE TRIGGER insert_book_catalog
INSTEAD OF INSERT ON book_catalog
BEGIN
    -- 作者不存在时才插入（name 有 UNIQUE 约束）
    INSERT OR IGNORE INTO authors (name, country)
    VALUES (NEW.author_name, NEW.author_country);
    -- 插入书籍，并通过作者姓名查找 author_id
    INSERT INTO books (title, year, price, author_id)
    VALUES (NEW.book_title, NEW.book_year, NEW.book_price,
            (SELECT id FROM authors WHERE name = NEW.author_name));
END;

-- 第 2 步：通过视图插入新作者和新书
INSERT INTO book_catalog (author_name, author_country, book_title, book_year, book_price)
VALUES ('Ursula K. Le Guin', 'USA', 'The Left Hand of Darkness', 1969, 14.99);
```
