### 集合操作中的 ORDER BY 和 LIMIT

当你使用像 `UNION` 或 `UNION ALL` 这样的集合操作合并来自多个表的结果时，通常需要对合并后的输出进行排序和限制。
一个常见的误解是将 `ORDER BY` 或 `LIMIT` 放在各个单独的 SELECT 语句中 - 在 SQLite 中，这些子句作用于**最终合并的结果集**，而不是各个独立的查询。

### 工作原理

当 SQLite 处理包含 `UNION ALL` 的查询时，它首先将两个 SELECT 语句中的所有行收集到一个结果集中，然后应用 `ORDER BY` 对该合并集进行排序，最后应用 `LIMIT` 来限制返回的行数。
可以把它想象成把两个装有编号球的桶倒进同一个容器中，然后把所有的球一起排序并挑选出前几个。

如果你尝试将 `ORDER BY` 放在其中一个单独的 SELECT 语句中（而不将其包装在子查询中），SQLite 会报错或忽略它 - 只有在所有结果合并后，排序才有意义。

### 语法

```sql
SELECT column1, column2 FROM table_a
UNION ALL
SELECT column1, column2 FROM table_b
ORDER BY column_name DESC
LIMIT n;
```

关键点：

- `ORDER BY` 位于集合操作中最后一个 SELECT **之后**
- `LIMIT` 位于 `ORDER BY` **之后**
- 两者都作用于整个合并后的结果，而不仅仅是最后一个 SELECT

### 示例

```sql
-- 合并国内和国际货件，获取最重的 5 个货件
SELECT package_id, weight FROM domestic_shipments
UNION ALL
SELECT package_id, weight FROM international_shipments
ORDER BY weight DESC
LIMIT 5;

-- 合并早晨和晚上的温度读数，获取最冷的 3 个读数
SELECT location, temp_celsius FROM morning_readings
UNION ALL
SELECT location, temp_celsius FROM evening_readings
ORDER BY temp_celsius ASC
LIMIT 3;
```

### UNION ALL 与 UNION

| 运算符 | 重复项 | 性能 |
| --- | --- | --- |
| `UNION ALL` | 保留所有行，包括重复项 | 更快 - 无去重步骤 |
| `UNION` | 移除重复行 | 较慢 - 必须比较各行 |

当你需要来自两个数据源的每一行数据（即使其中某些行相同）时，请使用 `UNION ALL`。

### 你的任务

你有两个表：`online_sales` 和 `in_store_sales`。
两个表都包含代表单笔销售交易的 `product_name` (TEXT) 和 `amount` (NUMERIC) 列。

编写一个查询以：

1. 合并来自两个渠道（线上和线下门店）的**所有**销售记录 - 保留重复项
2. 按 `amount` **降序**（最高金额优先）对合并后的结果进行排序
3. 仅返回**前 10 笔**销售记录

你的查询结果应包含两列：`product_name` 和 `amount`。

### 预期结果

该查询应返回两个渠道中金额最高的 10 笔销售记录，并按金额从大到小排序。

### 解答

```sql
-- 使用 UNION ALL 合并两个渠道的所有销售记录
-- 按 amount 降序排序并限制为前 10 笔
SELECT product_name, amount FROM online_sales
UNION ALL
SELECT product_name, amount FROM in_store_sales
ORDER BY amount DESC
LIMIT 10;
```
