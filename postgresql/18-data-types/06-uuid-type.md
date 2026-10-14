### PostgreSQL 中的 UUID 类型

UUID（通用唯一标识符 / Universally Unique Identifier）是一个 128 位的值，无需系统之间进行协调即可提供全局唯一标识符。
PostgreSQL 的 `UUID` 类型非常适合多个服务器需要独立生成唯一 ID 的分布式系统。

### UUID 格式

UUID 显示为由连字符分隔为五组的 32 位十六进制数字：

```sql
-- 示例 UUID: 550e8400-e29b-41d4-a716-446655440000
-- 格式: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

### 生成 UUID

PostgreSQL 提供了 `gen_random_uuid()` 用于生成随机 UUID（版本 4）：

```sql
-- 生成一个随机 UUID
SELECT gen_random_uuid();
-- 结果: 7c9e6679-7425-40de-944b-e07fc1f90ae7

-- 在 INSERT 语句中使用
INSERT INTO sessions (id, user_id) 
VALUES (gen_random_uuid(), 1);
```

### UUID 与 SERIAL：何时使用何种类型

| 方面 | SERIAL | UUID |
| --- | --- | --- |
| 大小 | 4-8 字节 | 16 字节 |
| 可预测性 | 顺序、可预测 | 随机、不可预测 |
| 分布式生成 | 需要协调 | 无需协调 |
| 索引性能 | 更快（顺序） | 略慢（随机） |
| URL 安全性 | 可能会暴露记录总数 | 可以安全地公开展现 |

### 操作 UUID 列

```sql
-- 按 UUID 过滤
SELECT * FROM sessions 
WHERE id = '550e8400-e29b-41d4-a716-446655440000';

-- 将文本转换为 UUID
SELECT * FROM sessions 
WHERE id = '550e8400-e29b-41d4-a716-446655440000'::uuid;

-- 检查某个值是否为有效的 UUID 格式
SELECT '550e8400-e29b-41d4-a716-446655440000'::uuid;
```

### 你的任务

你正在处理一个分布式系统，其中多个服务器独立创建记录。
一个名为 `distributed_records` 且包含 UUID 主键的表已存在。

编写一个查询以查找来自 `us-east` 区域的所有记录，返回 `id`、`server_region`、`payload` 和 `created_at` 列。
按 `created_at` 降序对结果进行排序（最新的排在最前面）。

### 表结构

```sql
CREATE TABLE distributed_records (
    id UUID PRIMARY KEY,
    server_region VARCHAR(50) NOT NULL,
    payload TEXT,
    created_at TIMESTAMP
);
```

### 预期结果

```sql
SELECT ... FROM distributed_records WHERE server_region = 'us-east' ORDER BY created_at DESC;
-- 返回所有 us-east 记录，最新的排在最前面
```

### 解答

```sql
-- 查找来自 'us-east' 区域的所有记录
-- 返回 id、server_region、payload 和 created_at
-- 按 created_at 降序排序（最新的在前）
SELECT id, server_region, payload, created_at
FROM distributed_records
WHERE server_region = 'us-east'
ORDER BY created_at DESC;
```
