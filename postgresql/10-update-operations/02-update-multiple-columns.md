### UPDATE 多个列

你可以在单个 UPDATE 语句中通过在 SET 子句中用逗号分隔每个列赋值来更新多个列。

### 语法

```sql
UPDATE table_name
SET column1 = value1,
    column2 = value2,
    column3 = value3
WHERE condition;
```

### 为什么同时更新多个列？

- **效率**：使用一条语句代替多次单独的更新
- **原子性**：所有更改要么全部发生，要么全部不发生
- **减少数据库往返次数**：为应用程序带来更好的性能

### 示例

```sql
-- 同时更新用户的姓名和邮箱
UPDATE users
SET name = 'Jane Smith',
    email = 'jane.smith@example.com'
WHERE user_id = 5;
```

### 重要注意事项

- 列出以逗号分隔的各个 column = value 对
- 最后一个列赋值后面不要加逗号
- WHERE 子句适用于所有列的更新
- 所有指定的列都会同时更新

### 你的任务

将 `product_id = 2` 的产品（Wireless Mouse）更新为：

- `price` 为 `34.99`
- `stock` 为 `75`

编写一条 UPDATE 语句，在单个查询中同时修改这两个列。

### 解答

```sql
-- 将 product_id = 2 的 price 更新为 34.99，stock 更新为 75
UPDATE products
SET price = 34.99,
    stock = 75
WHERE product_id = 2;
```
