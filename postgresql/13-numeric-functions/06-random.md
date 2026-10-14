### RANDOM 函数

PostgreSQL 提供了 `RANDOM()` 函数来生成随机数，并实现从数据中进行随机选择。

### 生成随机数

`RANDOM()` 返回一个介于 0（包含）到 1（不包含）之间的随机值：

```sql
-- 返回类似 0.7234561892 的值
SELECT RANDOM();

-- 生成 1 到 100 之间的随机整数
SELECT FLOOR(RANDOM() * 100) + 1 AS random_number;

-- 生成指定范围（min 到 max）内的随机数
SELECT FLOOR(RANDOM() * (max - min + 1)) + min;
```

### 从表中随机选择

`RANDOM()` 最常见的用法是从表中随机选择行：

```sql
-- 随机选择一行
SELECT * FROM products ORDER BY RANDOM() LIMIT 1;

-- 随机选择 5 行
SELECT * FROM products ORDER BY RANDOM() LIMIT 5;
```

### 工作原理

当你使用 `ORDER BY RANDOM()` 时：

1. PostgreSQL 会为每一行分配一个随机数
2. 各行按照这些随机数进行排序
3. `LIMIT` 从该随机排序中获取前 N 行

### 实际应用

| 用例 | 示例 |
| --- | --- |
| 随机抽样 | `SELECT * FROM surveys ORDER BY RANDOM() LIMIT 100;` |
| 随机抽取获奖者 | `SELECT winner FROM entries ORDER BY RANDOM() LIMIT 1;` |
| A/B 测试分组 | `SELECT *, RANDOM() < 0.5 AS group_a FROM users;` |
| 随机打乱结果 | `SELECT * FROM playlist ORDER BY RANDOM();` |

### 你的任务

你有一个包含各种商品的 `products` 表。
编写一个查询，从表中随机选择 **3 个产品**。

你的查询应该：

- 返回 `product_id`、`product_name` 和 `price` 列
- 恰好选择 3 个产品
- **使用 `RANDOM()` 对结果进行随机排序**（这是必须的！）

### 预期结果结构

```markdown
 product_id | product_name | price
------------+--------------+-------
          ? | ?            | ?
          ? | ?            | ?
          ? | ?            | ?
```

由于是随机选择，每次执行返回的实际产品都会有所不同。

### 解答

```sql
-- 随机选择 3 个产品
-- 返回 product_id、product_name 和 price 列
-- 必须使用 RANDOM() 进行随机选择
SELECT product_id, product_name, price
FROM products
ORDER BY RANDOM()
LIMIT 3;
```
