### PostgreSQL 中的整数类型

PostgreSQL 提供了四种针对不同取值范围进行了优化的整数类型。
选择合适的类型可以节省存储空间并提高性能。

### 可用的整数类型

| 类型 | 存储大小 | 范围 |
| --- | --- | --- |
| SMALLINT | 2 字节 | -32,768 到 32,767 |
| INTEGER | 4 字节 | -2,147,483,648 到 2,147,483,647 |
| BIGINT | 8 字节 | -9,223,372,036,854,775,808 到 9,223,372,036,854,775,807 |
| SERIAL | 4 字节 | 自增 INTEGER (1 到 2,147,483,647) |

### 何时使用各类型

**SMALLINT** - 用于小型计数器、评分（1-5）、百分比（0-100）或任何小于 32,000 的值：

```sql
-- star_rating 仅限于较小的值
-- page_number 很少超过几千
```

**INTEGER** - 大多数整数、ID 和计数的默认选择：

```sql
-- stock_count, price_cents, user_id
-- 通用整数最常见的选择
```

**BIGINT** - 用于非常大的数字，例如总字节数、全局计数器或天文数字：

```sql
-- 跨年份累计的 total_page_views
-- 数据中心中传输的 bytes_transferred
```

### 你的任务

系统中已存在一个具有以下结构的 `website_metrics` 表。
编写一个查询以插入一条包含以下值的新记录：

- `page_views_today`: 25000（适合 SMALLINT）
- `unique_visitors`: 1500000（需要 INTEGER）
- `total_bytes_served`: 5000000000（50 亿，需要 BIGINT）
- `error_count`: 150（适合 SMALLINT）
- `active_sessions`: 8500（适合 SMALLINT）

注意：`id` 列会自动递增，因此你无需指定它。

### 表结构

| 列名 | 类型 | 描述 |
| --- | --- | --- |
| id | SERIAL | 自增主键 |
| page\_views\_today | SMALLINT | 每日页面浏览量 |
| unique\_visitors | INTEGER | 每月独立访客数 |
| total\_bytes\_served | BIGINT | 累计服务的字节数 |
| error\_count | SMALLINT | 每日错误计数 |
| active\_sessions | SMALLINT | 当前活跃会话数 |

### 预期结果

在执行 INSERT 之后，表中应包含一行具有指定值的数据。

### 解答

```sql
-- 向 website_metrics 插入一条记录
-- id 为 SERIAL，会自动递增，无需指定

INSERT INTO website_metrics (page_views_today, unique_visitors, total_bytes_served, error_count, active_sessions)
VALUES (25000, 1500000, 5000000000, 150, 8500);
```
