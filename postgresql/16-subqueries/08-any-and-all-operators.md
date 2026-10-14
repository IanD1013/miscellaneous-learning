### ANY 和 ALL 运算符

`ANY` 和 `ALL` 运算符允许你将一个值与子查询返回的一组值进行比较。
它们是 `IN` 的强大替代方案，并提供了更灵活的比较选项。

### ANY 运算符

如果子查询结果中**至少有一个**值使比较成立，`ANY` 就会返回 `TRUE`。

```sql
-- 查找价格高于类别 1 中任意一个产品的产品
SELECT product_name, price
FROM products
WHERE price > ANY (SELECT price FROM products WHERE category_id = 1);
```

这等价于：“价格大于子查询中的最小值”。

### ALL 运算符

只有当子查询结果中的**每一个**值都使比较成立时，`ALL` 才会返回 `TRUE`。

```sql
-- 查找价格高于类别 1 中所有产品的产品
SELECT product_name, price
FROM products
WHERE price > ALL (SELECT price FROM products WHERE category_id = 1);
```

这等价于：“价格大于子查询中的最大值”。

### 比较总结

| 表达式 | 等价于 |
| --- | --- |
| `> ANY (subquery)` | 大于最小值 |
| `< ANY (subquery)` | 小于最大值 |
| `> ALL (subquery)` | 大于最大值 |
| `< ALL (subquery)` | 小于最小值 |
| `= ANY (subquery)` | 等同于 `IN (subquery)` |

### 空子查询的行为

- `ANY` 处理空结果：返回 `FALSE`（没有可供比较的值）
- `ALL` 处理空结果：返回 `TRUE`（恒真/无条件成立 - 没有值违背该条件）

### 你的任务

你有两张表：

- `products` - 你店铺中的产品及其价格
- `competitor_prices` - 竞争对手对类似产品的定价

找出你店铺中定价**低于同款产品的所有竞争对手价格（ALL competitor prices）**的产品。
这意味着你需要找到价格击败了每一个竞争对手的产品。

返回比所有竞争对手价格都要便宜的产品的 `product_id`、`product_name` 和 `price`。

### 预期结果

| product\_id | product\_name | price |
| --- | --- | --- |
| 2 | Wireless Mouse | 24.99 |
| 4 | USB-C Cable | 9.99 |

### 解答

```sql
-- 查找价格低于该产品所有竞争对手价格的产品
-- 返回：product_id, product_name, price
SELECT product_id, product_name, price
FROM products p
WHERE price < ALL (
    SELECT competitor_price
    FROM competitor_prices cp
    WHERE cp.product_id = p.product_id
);
```
