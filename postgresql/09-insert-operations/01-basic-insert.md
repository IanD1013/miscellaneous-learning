### 基本 INSERT 语句

INSERT 语句用于向表中添加新行。
基本语法显式列出要插入的列，后跟要插入的 VALUES。

### 语法

```sql
INSERT INTO table_name (column1, column2, column3)
VALUES (value1, value2, value3);
```

### 关键要点

| 概念 | 描述 |
| --- | --- |
| 列列表 | 指定哪些列接收值 |
| VALUES | 按照与列相同的顺序提供数据 |
| 字符串值 | 必须用单引号括起来 |
| 数字 | 不加引号直接写入 |
| 布尔值 | 使用 TRUE 或 FALSE（无引号） |

### 示例

```sql
-- 插入一个用户
INSERT INTO users (name, email, age)
VALUES ('Alice', 'alice@example.com', 28);

-- 插入布尔值
INSERT INTO tasks (title, completed)
VALUES ('Buy groceries', FALSE);
```

### 你的任务

向 `products` 表中插入一条包含以下值的新产品：

- **name**：'Mechanical Keyboard'
- **price**：89.99
- **category**：'Electronics'
- **in\_stock**：TRUE

### 预期结果

在执行 INSERT 后，查询 products 表应该会返回包含你所指定值的新行。

### 解答

```sql
-- 插入一个新产品：Mechanical Keyboard，价格 89.99，类别 Electronics，in_stock 为 TRUE
INSERT INTO products (name, price, category, in_stock)
VALUES ('Mechanical Keyboard', 89.99, 'Electronics', TRUE);
```
