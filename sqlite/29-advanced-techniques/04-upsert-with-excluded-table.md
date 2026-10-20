### 使用 `excluded` 伪表的高级 UPSERT

在实际应用程序中，你经常需要“upsert”逻辑，如果某行不存在则插入它，如果存在则更新它。
SQLite 通过 `INSERT ... ON CONFLICT ... DO UPDATE SET` 支持此操作，有时也称为“upsert”语句。
其真正的强大之处来自于 `excluded` 伪表，它允许你访问在没有冲突的情况下*本应插入*的值。

这对于库存管理、投票计数、指标聚合或任何需要*累加*而非*覆盖*的场景至关重要。

### 工作原理

当你执行违反 `UNIQUE` 或 `PRIMARY KEY` 约束的 `INSERT` 时，SQLite 可以处理该冲突而不是报错。
`DO UPDATE SET` 子句允许你指定如何将传入的新行与现有行进行合并。

核心概念是在 `DO UPDATE SET` 子句中可用的两个伪表：

- **表本身**（例如 `inventory.quantity`）- 引用该行中已存储的*当前*值
- **`excluded`**（例如 `excluded.quantity`）- 引用导致冲突的 `INSERT` 中的*传入*值

这种区分使你能够编写强大的合并表达式来组合新旧数据。

### 语法

```sql
INSERT INTO table_name (col1, col2, col3)
VALUES (val1, val2, val3)
ON CONFLICT (conflict_column)
DO UPDATE SET
    col2 = expression_using_table_and_excluded,
    col3 = another_expression;
```

`ON CONFLICT (conflict_column)` 用于标识触发 upsert 的唯一性约束。
你可以指定具有 `UNIQUE` 或 `PRIMARY KEY` 约束的任何列（或列组合）。

### 示例

```sql
-- 示例 1：简单替换 - 用新值覆盖旧值
INSERT INTO scores (player_name, high_score)
VALUES ('Alice', 500)
ON CONFLICT (player_name)
DO UPDATE SET high_score = excluded.high_score;
-- 如果 Alice 已存在，无论旧值是多少，她的 high_score 都会变为 500

-- 示例 2：保留最大值 - 仅当新值更高时才更新
INSERT INTO scores (player_name, high_score)
VALUES ('Bob', 300)
ON CONFLICT (player_name)
DO UPDATE SET high_score = MAX(scores.high_score, excluded.high_score);
-- 如果 Bob 当前的分数是 450，则保持 450。如果是 200，则变为 300。

-- 示例 3：累加值 - 将新值与现有值相加
INSERT INTO page_views (url, view_count, last_seen)
VALUES ('/home', 15, '2025-01-15')
ON CONFLICT (url)
DO UPDATE SET
    view_count = page_views.view_count + excluded.view_count,
    last_seen = excluded.last_seen;
-- 如果 /home 之前有 100 次浏览，现在则为 115 次，且 last_seen 会被更新
```

### 常见模式

| 模式 | 表达式 | 使用场景 |
| --- | --- | --- |
| 替换 | `col = excluded.col` | 始终使用新值 |
| 累加 | `col = table.col + excluded.col` | 累计总数、计数器 |
| 保留最大值 | `col = MAX(table.col, excluded.col)` | 最高分、峰值 |
| 保留最小值 | `col = MIN(table.col, excluded.col)` | 最早日期、最低价格 |
| 条件更新 | `col = CASE WHEN ... THEN ... END` | 复杂的合并逻辑 |

请注意，在 `DO UPDATE SET` 子句中，你使用**表名**（例如 `inventory.quantity`）引用现有行，使用 **`excluded`**（例如 `excluded.quantity`）引用传入的值。

### 你的任务

你正在管理一个库存系统。
`inventory` 表记录产品，包含唯一的 `product_id`、`product_name`、`quantity` 以及 `last_updated` 时间戳。

该表中已包含一些带有现有数量的产品。
你需要编写一个**单个 upsert 语句**来实现：

1. 为产品 `'SKU-A100'` 插入一批新货物，名称为 `'Widget Alpha'`，数量为 `75`，`last_updated` 为 `'2025-07-15'`
2. 如果 `'SKU-A100'` 已存在（在 `product_id` 上发生冲突），则将传入的数量**累加**到现有数量上，而不是替换它
3. 发生冲突时，还将 `product_name` 和 `last_updated` 更新为传入的新值

`'SKU-A100'` 的现有行数量为 `120`。
在执行你的 upsert 之后，数量应变为 `195`（120 + 75）。

### 预期结果

执行 upsert 后：

- `product_id = 'SKU-A100'` 的 `quantity = 195`
- `product_name` 应为 `'Widget Alpha'`
- `last_updated` 应为 `'2025-07-15'`
- 表中的其他行应保持不变

### 解答

```sql
-- 在 product_id 冲突时，用 inventory.quantity + excluded.quantity 累加数量
-- product_name 和 last_updated 直接替换为 excluded 中的传入值
INSERT INTO inventory (product_id, product_name, quantity, last_updated)
VALUES ('SKU-A100', 'Widget Alpha', 75, '2025-07-15')
ON CONFLICT (product_id)
DO UPDATE SET
    quantity = inventory.quantity + excluded.quantity,
    product_name = excluded.product_name,
    last_updated = excluded.last_updated;
```
