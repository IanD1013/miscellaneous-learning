### 包含表达式的 UPDATE

当你使用引用列当前值的表达式时，UPDATE 语句会变得非常强大。
与其将列设置为固定值，不如根据已存储的内容执行计算。

### 在计算中使用当前值

要引用列的当前值，只需在赋值语句的右侧使用列名即可：

```sql
-- 薪资增加 500
UPDATE employees SET salary = salary + 500;

-- 数量翻倍
UPDATE inventory SET quantity = quantity * 2;

-- 打八折（减少 20%）
UPDATE products SET price = price * 0.80;
```

### 常见的表达式模式

| 操作 | 表达式 | 示例 |
| --- | --- | --- |
| 增加固定金额 | `column + value` | `price + 5.00` |
| 减去 | `column - value` | `stock - 10` |
| 百分比增加 | `column * (1 + rate)` | `price * 1.10`（增加 10%） |
| 百分比减少 | `column * (1 - rate)` | `price * 0.85`（打八五折） |
| 四舍五入结果 | `ROUND(expression, decimals)` | `ROUND(price * 1.10, 2)` |

### 与 WHERE 结合使用

你可以将表达式与 WHERE 结合使用，以仅更新特定行：

```sql
-- 给部门 3 的员工加薪 5%
UPDATE employees 
SET salary = salary * 1.05 
WHERE department_id = 3;
```

### 你的任务

你有一个包含各种商品及其价格的 `products` 表。
由于通货膨胀，商店需要将**所有价格提高 10%**。

编写一个 UPDATE 语句，使用表达式将每件商品的价格提高 10%。

### 预期结果

执行 UPDATE 后：

- Laptop: $999.99 → $1099.99（四舍五入）
- Mouse: $29.99 → $32.99（四舍五入）
- Keyboard: $79.99 → $87.99（四舍五入）
- Monitor: $349.99 → $384.99（四舍五入）
- Headphones: $149.99 → $164.99（四舍五入）

\*\*提示：\*\*使用 `ROUND(expression, 2)` 将价格保留 2 位小数。

### 解答

```sql
-- 将所有商品价格提高 10%
-- 使用 ROUND 保留 2 位小数
UPDATE products
SET price = ROUND(price * 1.10, 2);
```
