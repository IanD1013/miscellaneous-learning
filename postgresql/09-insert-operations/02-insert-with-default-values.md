### 带默认值的 INSERT (INSERT with Default Values)

当表中的列定义了 DEFAULT 默认值时，你有两种方法让数据库使用这些默认值：

### 省略列

只需在 INSERT 语句中省略具有默认值的列即可：

```sql
-- 表：orders (id SERIAL, customer_name VARCHAR, status VARCHAR DEFAULT 'pending', created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
INSERT INTO orders (customer_name) VALUES ('Alice');
-- id 自动生成，status 变为 'pending'，created_at 变为当前时间戳
```

### 使用 DEFAULT 关键字

显式请求默认值：

```sql
INSERT INTO orders (customer_name, status, created_at) 
VALUES ('Bob', DEFAULT, DEFAULT);
-- 结果相同：status = 'pending'，created_at = 当前时间戳
```

### 何时使用哪种方法

| 方法 | 适用场景 |
| --- | --- |
| 省略列 | 你希望使用默认值并保持 SQL 更简洁 |
| DEFAULT 关键字 | 将显式值与部分默认值混合使用 |

### 你的任务

你有一个包含以下列的 `orders` 表：

- `id` - 自增主键 (SERIAL)
- `customer_name` - 必填的客户姓名 (VARCHAR)
- `status` - 订单状态，默认值为 'pending' (VARCHAR)
- `priority` - 优先级，默认值为 1 (INTEGER)
- `notes` - 可选备注，默认值为 'No notes' (TEXT)

仅使用必填列为客户 **'Sarah Johnson'** 插入一条新订单。
让数据库为 `status`、`priority` 和 `notes` 应用默认值。

### 预期结果

在执行 INSERT 后，orders 表应包含一行数据：

- customer\_name: 'Sarah Johnson'
- status: 'pending'（来自默认值）
- priority: 1（来自默认值）
- notes: 'No notes'（来自默认值）

### 解答

```sql
-- 为 'Sarah Johnson' 插入一条订单，其余列使用默认值
INSERT INTO orders (customer_name) VALUES ('Sarah Johnson');
```
