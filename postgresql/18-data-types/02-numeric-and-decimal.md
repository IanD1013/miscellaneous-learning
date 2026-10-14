### PostgreSQL 中的 NUMERIC 和 DECIMAL 类型

PostgreSQL 的 `NUMERIC`（也称为 `DECIMAL`）类型用于存储用户指定精度的精确小数。
与浮点类型不同，NUMERIC 会保留精确的值，这对于不允许出现舍入误差的金融计算至关重要。

### 精度（Precision）和标度（Scale）

```sql
NUMERIC(precision, scale)
-- precision：总位数（小数点两侧合计）
-- scale：小数点后的位数

NUMERIC(10, 2)  -- 最大 99999999.99（小数点前 8 位，小数点后 2 位）
NUMERIC(5, 4)   -- 最大 9.9999（小数点前 1 位，小数点后 4 位）
NUMERIC         -- 无限精度（很少需要）
```

### 常见金融场景的精度

| 使用场景 | 类型 | 示例值 |
| --- | --- | --- |
| 货币 (USD, EUR) | NUMERIC(12, 2) | 1234567890.99 |
| 加密货币 | NUMERIC(18, 8) | 0.00000001 |
| 利率 | NUMERIC(5, 4) | 0.0525 (5.25%) |
| 汇率 | NUMERIC(10, 6) | 1.234567 |

### NUMERIC 对比 REAL/DOUBLE PRECISION

```sql
-- 永远不要用浮点数存储金额！
SELECT 0.1::REAL + 0.2::REAL;           -- 返回 0.30000001（舍入误差！）
SELECT 0.1::NUMERIC + 0.2::NUMERIC;     -- 返回 0.3（精确）

-- 金融计算的准确性
SELECT (1000000.00 * 0.0001)::REAL;     -- 可能丢失精度
SELECT (1000000.00 * 0.0001)::NUMERIC;  -- 精确：100.0000
```

### 查看 NUMERIC 列

你可以使用 PostgreSQL 的 `information_schema` 来查看 NUMERIC 列的结构。
该系统目录包含数据库中所有表和列的元数据。

```sql
-- 查看列信息，包括精度和标度
SELECT column_name, data_type, numeric_precision, numeric_scale
FROM information_schema.columns
WHERE table_name = 'some_table';
```

### 你的任务

数据库中已经创建了一个包含各种用于金融数据的 NUMERIC 列的 `financial_records` 表。
编写一个查询来查看该表中所有 NUMERIC 列的结构。

你的查询应返回：

- **column\_name**：每个 NUMERIC 列的名称
- **numeric\_precision**：该列可以存储的总位数
- **numeric\_scale**：小数位数

过滤结果以仅显示 `data_type = 'numeric'` 的列，并按列名对结果进行排序。

### 预期查询结构

```sql
SELECT column_name, numeric_precision, numeric_scale
FROM information_schema.columns
WHERE table_name = '...' AND data_type = '...'
ORDER BY ...;
```

### 解答

```sql
-- 查询 information_schema 以获取 NUMERIC 列的详细信息
-- 返回：column_name, numeric_precision, numeric_scale
-- 过滤：table_name = 'financial_records' AND data_type = 'numeric'
-- 排序：column_name

SELECT column_name, numeric_precision, numeric_scale
FROM information_schema.columns
WHERE table_name = 'financial_records' AND data_type = 'numeric'
ORDER BY column_name;
```
