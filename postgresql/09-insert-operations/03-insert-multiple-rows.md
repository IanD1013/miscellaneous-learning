### 插入多行数据（INSERT Multiple Rows）

PostgreSQL 允许你在一条语句中插入多行数据，而无需为每一行执行单独的 INSERT 语句。
这种做法效率更高，并且能减少与数据库的往返通信。

### 单行插入（Single Row INSERT）

```sql
INSERT INTO products (name, price) VALUES ('Apple', 1.50);
INSERT INTO products (name, price) VALUES ('Banana', 0.75);
INSERT INTO products (name, price) VALUES ('Cherry', 2.00);
```

这需要 3 条单独的语句。

### 多行插入（Multi-Row INSERT）

```sql
INSERT INTO products (name, price) VALUES 
    ('Apple', 1.50),
    ('Banana', 0.75),
    ('Cherry', 2.00);
```

这会在一条语句中插入全部 3 行，效率要高得多！

### 语法

```sql
INSERT INTO table_name (column1, column2, ...)
VALUES 
    (value1a, value2a, ...),
    (value1b, value2b, ...),
    (value1c, value2c, ...);
```

每一组圆括号代表一行。
行与行之间用逗号分隔。

### 你的任务

在一条 INSERT 语句中向 `categories` 表插入 5 个类别：

| name | description |
| --- | --- |
| Electronics | Gadgets and devices |
| Clothing | Apparel and accessories |
| Books | Literature and textbooks |
| Home & Garden | Furniture and outdoor items |
| Sports | Athletic equipment and gear |

### 表结构（Table Schema）

```sql
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT
);
```

### 预期结果

在执行 INSERT 之后，`categories` 表中应包含全部 5 个类别。

### 解答

```sql
-- 在一条 INSERT 语句中插入全部 5 个类别
INSERT INTO categories (name, description) VALUES
    ('Electronics', 'Gadgets and devices'),
    ('Clothing', 'Apparel and accessories'),
    ('Books', 'Literature and textbooks'),
    ('Home & Garden', 'Furniture and outdoor items'),
    ('Sports', 'Athletic equipment and gear');
```
