### TRUNCATE 语句

`TRUNCATE` 语句用于从表中删除所有行，其速度比 `DELETE` 快得多，因为它不需要逐行扫描表。

### TRUNCATE 与 DELETE

| 特性 | DELETE | TRUNCATE |
| --- | --- | --- |
| 速度 | 较慢（逐行） | 非常快 |
| WHERE 子句 | 支持 | 不支持 |
| 触发器 | 触发行级触发器 | 仅触发 TRUNCATE 触发器 |
| 事务 | 可回滚 | 可回滚（在 PostgreSQL 中） |
| 标识重置 | 手动 | 使用 RESTART IDENTITY |

### 基础 TRUNCATE

```sql
-- 删除表中的所有行
TRUNCATE TABLE logs;

-- 等价于（但比它快得多）：
DELETE FROM logs;
```

### RESTART IDENTITY

当表中包含 `SERIAL` 或 `IDENTITY` 列时，TRUNCATE 可以重置它：

```sql
-- 将自增计数器重置为 1
TRUNCATE TABLE users RESTART IDENTITY;

-- 保留当前的计数器值
TRUNCATE TABLE users CONTINUE IDENTITY;
```

### CASCADE 选项

```sql
-- 同时清空具有外键引用的表
TRUNCATE TABLE orders CASCADE;
```

### 你的任务

`session_logs` 表包含需要完全清空的旧用户会话数据。
该表有一个自增的 `id` 列。

编写一条 `TRUNCATE` 语句，以实现：

1. 删除 `session_logs` 表中的所有行
2. 重置标识列，使下一次插入从 id = 1 开始

### 预期行为

- `session_logs` 中的所有行都应被删除
- 标识序列应被重置，以便下一个插入的行获得 `id = 1`
- 该操作应在没有错误的情况下完成

### 解答

```sql
-- 清空 session_logs 表并重置其标识列
TRUNCATE TABLE session_logs RESTART IDENTITY;
```
