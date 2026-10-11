### SQL 中的注释

注释是 SQL 代码中的注解，数据库在运行查询时会忽略它们。
它们可以帮助你（以及其他人）理解代码的作用，从而使日后的维护和调试更加轻松。

### 使用 -- 进行单行注释

使用两个连字符 `--` 可以开始一段延续到行尾的注释：

```sql
-- 这是一条单行注释
SELECT * FROM products; -- 这条注释位于行尾
```

在该行中，`--` 之后的所有内容都会被 PostgreSQL 忽略。

### 使用 /\* \*/ 进行多行注释

对于较长的说明，可以将注释包裹在 `/*` 和 `*/` 之间：

```sql
/* 这条注释
   跨越
   多行 */
SELECT name, price FROM products;
```

多行注释适用于：

- 临时禁用代码块
- 编写详细的说明文档
- 为复杂查询添加标题头

### 何时使用注释

| 场景 | 示例 |
| --- | --- |
| 解释复杂逻辑 | `-- Calculate total with 10% discount` |
| 记录代码用途 | `/* Returns all active customers */` |
| 临时禁用代码 | `-- SELECT * FROM old_table;` |
| 添加分段标题 | `/* === PRODUCT QUERIES === */` |

### 你的任务

编写一个仅从 `products` 表中选择 `name` 列的查询。
需包含：

1. 开头有一行单行注释，解释该查询的作用
2. SELECT 语句本身

### 预期查询结构

```sql
-- [你的描述性注释]
[你的 SELECT 语句]
```

### 预期结果

```markdown
name
--------
Laptop
Mouse
Keyboard
Monitor
```

### 解答

```sql
-- 查询 products 表中所有商品的名称
SELECT name FROM products;
```
