### FETCH FIRST 语法

`FETCH FIRST` 子句是用于限制查询返回行数的 SQL 标准方法。
虽然 PostgreSQL 同时支持 `LIMIT` 和 `FETCH FIRST`，但使用 `FETCH FIRST` 可以让您的 SQL 在不同的数据库系统之间更具可移植性。

### 基本语法

```sql
SELECT columns
FROM table_name
ORDER BY column
FETCH FIRST n ROWS ONLY;
```

### FETCH FIRST 与 LIMIT 对比

| 语法 | 标准 | 示例 |
| --- | --- | --- |
| LIMIT | PostgreSQL/MySQL | `LIMIT 5` |
| FETCH FIRST | SQL 标准 | `FETCH FIRST 5 ROWS ONLY` |

两者可以达到相同的效果，但 `FETCH FIRST` 是 ANSI SQL 标准：

```sql
-- PostgreSQL 风格
SELECT * FROM products ORDER BY price DESC LIMIT 3;

-- SQL 标准风格
SELECT * FROM products ORDER BY price DESC FETCH FIRST 3 ROWS ONLY;
```

### 变体

您可以使用 `ROW` 或 `ROWS`，它们的作用完全相同：

```sql
FETCH FIRST 1 ROW ONLY   -- 单数
FETCH FIRST 5 ROWS ONLY  -- 复数
```

### 您的任务

您拥有一个包含来自不同玩家游戏得分的 `scores` 表。
请使用 `FETCH FIRST` 语法编写一个查询，以选择**最高的前 3 个分数**。

返回 `player_name` 和 `score` 列，按分数从高到低排序。

### 预期结果

| player\_name | score |
| --- | --- |
| Diana | 9850 |
| Charlie | 8720 |
| Alice | 7500 |

### 解答

```sql
-- 使用 FETCH FIRST 语法选择最高的前 3 个分数
-- 返回 player_name 和 score 列
SELECT player_name, score
FROM scores
ORDER BY score DESC
FETCH FIRST 3 ROWS ONLY;
```
