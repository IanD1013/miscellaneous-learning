### 组合使用 AND、OR 和 NOT 运算符

实际应用中的查询通常需要组合多个逻辑运算符来表达复杂的条件。
理解这些运算符如何协同工作及其优先级，对于编写正确的查询至关重要。

### 运算符优先级

SQL 按照以下顺序计算逻辑运算符：

1. **NOT**（最高优先级 - 最先计算）
2. **AND**（第二优先级）
3. **OR**（最低优先级 - 最后计算）

```sql
-- 没有括号时，AND 先于 OR 计算
SELECT * FROM orders WHERE status = 'Pending' AND total > 100 OR status = 'Completed';
-- 这意味着：(status = 'Pending' AND total > 100) OR (status = 'Completed')
```

### 使用括号提升可读性

务必使用括号明确表达意图并避免混淆：

```sql
-- 显式分组 - 清晰得多！
SELECT * FROM orders 
WHERE (status = 'Pending' AND total > 100) OR status = 'Completed';

-- 括号位置不同，含义也不同
SELECT * FROM orders 
WHERE status = 'Pending' AND (total > 100 OR status = 'Completed');
```

### 复杂示例

```sql
-- 查找未被冻结的活跃高级客户
SELECT * FROM customers 
WHERE (tier = 'Gold' OR tier = 'Platinum') 
  AND status = 'Active' 
  AND NOT on_hold = true;

-- 查找紧急订单：高金额的待处理订单，或任何已完成的订单
SELECT * FROM orders 
WHERE (status = 'Pending' AND total > 500) 
   OR status = 'Completed';
```

### 你的任务

你有一个包含订单信息的 `orders` 表。
编写一个查询以查找满足以下任一条件的订单：

1. 状态为 **'Pending'** 且总金额 **大于 100** 的订单，或者
2. 状态为 **'Completed'** 的订单（无论总金额为多少）

返回匹配订单的所有列。

### 表结构

| 列 | 类型 | 描述 |
| --- | --- | --- |
| id | SERIAL | 主键 |
| customer\_name | VARCHAR(100) | 客户姓名 |
| status | VARCHAR(20) | 订单状态 |
| total | NUMERIC(10,2) | 订单总额 |
| order\_date | DATE | 下单日期 |

### 预期结果

你的查询应返回满足以下条件的订单：

- 状态为 'Pending' 且 total > 100，或者
- 状态为 'Completed'（任何总金额）

### 解答

```sql
-- 选择满足以下任一条件的订单：
-- (状态为 'Pending' 且 total > 100) 或 (状态为 'Completed')
-- 返回所有列
SELECT * FROM orders
WHERE (status = 'Pending' AND total > 100) OR status = 'Completed';
```
