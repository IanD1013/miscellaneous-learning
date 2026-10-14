### CREATE TABLE 基础

`CREATE TABLE` 语句用于在数据库中定义一个包含指定列及其数据类型的新表。

### 基本语法

```sql
CREATE TABLE table_name (
    column1 data_type constraints,
    column2 data_type constraints,
    ...
);
```

### 常见数据类型

| 数据类型 | 描述 | 示例 |
| --- | --- | --- |
| SERIAL | 自增整数 | order\_id SERIAL |
| VARCHAR(n) | 最多包含 n 个字符的可变长度字符串 | city VARCHAR(50) |
| NUMERIC(p,s) | 精度为 p、小数位数为 s 的精确小数 | weight NUMERIC(6,3) |
| INTEGER | 整数 | quantity INTEGER |
| TEXT | 无限制长度字符串 | description TEXT |

### 约束

```sql
-- PRIMARY KEY：每一行的唯一标识符
order_id SERIAL PRIMARY KEY

-- NOT NULL：列不能为空
city VARCHAR(50) NOT NULL

-- UNIQUE：所有值必须互不相同
email VARCHAR(255) UNIQUE
```

### 你的任务

创建一个包含以下列的 `products` 表：

1. **id** - 自增主键
2. **name** - 产品名称，最多 100 个字符
3. **price** - 产品价格，总共最多 10 位数字，包含 2 位小数

### 预期表结构

| 列 | 要求 | 约束 |
| --- | --- | --- |
| id | 自增整数 | PRIMARY KEY |
| name | 文本，最多 100 个字符 | - |
| price | 精确小数，总共 10 位数字，2 位小数 | - |

### 解答

```sql
-- 创建包含 id、name 和 price 列的 products 表
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    price NUMERIC(10,2)
);
```
