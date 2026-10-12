### UNION ALL - 保留重复项合并结果

`UNION ALL` 用于合并多个 `SELECT` 语句的结果，并保留**包括重复项在内的所有行**。
与 `UNION` 不同，它不会去除重复行。

### UNION 与 UNION ALL

| 运算符 | 重复项 | 性能 |
| --- | --- | --- |
| UNION | 去除重复项 | 较慢（必须对比各行） |
| UNION ALL | 保留所有行 | 较快（无需对比） |

### 何时使用 UNION ALL

```sql
-- UNION 会删除重复项（可能隐藏重要数据）
SELECT product FROM sales_jan
UNION
SELECT product FROM sales_feb;

-- UNION ALL 保留所有交易（用于计算总数是正确的）
SELECT product FROM sales_jan
UNION ALL
SELECT product FROM sales_feb;
```

### 核心使用场景

- **金融交易**：每笔交易都很重要，即使金额与备注完全相同
- **日志记录**：重复事件本身就是有效数据
- **性能优化**：当你已知数据中不存在重复项时，`UNION ALL` 速度更快

### 语法规则

`UNION` 和 `UNION ALL` 都需要满足：

1. 每个 `SELECT` 中的列数相同
2. 对应列的数据类型互相兼容

```sql
SELECT date, amount, note FROM checking_transactions
UNION ALL
SELECT date, amount, note FROM savings_transactions
ORDER BY date;
```

### 你的任务

你有两个银行账户及其对应的交易表：`checking_transactions` 和 `savings_transactions`。
请编写一条查询语句，合并**来自这两个账户的所有交易**，包括任何重复的条目。
这对于准确的财务记录至关重要，因为同一金额可能会被多次存入或取出。

返回三列：`transaction_date`、`amount` 和 `description`。

### 预期结果

你的查询应返回全部 9 笔交易（包括在两张表中完全相同的故意重复行）。
使用 `UNION` 会错误地去除该重复行，因此你必须使用 `UNION ALL`。

### 解答

```sql
-- 合并两个账户的所有交易
-- 包含重复项（使用 UNION ALL）
-- 返回：transaction_date, amount, description

SELECT transaction_date, amount, description
FROM checking_transactions
UNION ALL
SELECT transaction_date, amount, description
FROM savings_transactions;
```
