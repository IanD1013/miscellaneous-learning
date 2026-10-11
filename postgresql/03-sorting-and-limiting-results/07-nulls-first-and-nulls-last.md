### NULLS FIRST 和 NULLS LAST

在对包含 NULL 值的数据进行排序时，PostgreSQL 的默认行为可能并不符合你的需求。
`NULLS FIRST` 和 `NULLS LAST` 修饰符让你可以显式控制 NULL 值在排序结果中的出现位置。

### 默认的 NULL 排序行为

在 PostgreSQL 中，默认行为如下：

- `ASC`（升序）将 NULL 排在**最后**
- `DESC`（降序）将 NULL 排在**最前**

```sql
-- 使用 ASC 时，NULL 默认出现在末尾
SELECT name, price FROM items ORDER BY price ASC;

-- 使用 DESC 时，NULL 默认出现在开头
SELECT name, price FROM items ORDER BY price DESC;
```

### 覆盖默认行为

你可以使用 `NULLS FIRST` 或 `NULLS LAST` 覆盖这些默认设置：

```sql
-- 升序时强制 NULL 出现在最前
SELECT name, price FROM items ORDER BY price ASC NULLS FIRST;

-- 降序时强制 NULL 出现在最后
SELECT name, price FROM items ORDER BY price DESC NULLS LAST;
```

### 实际应用场景

| 场景 | 解决方案 |
| --- | --- |
| 将没有价格的产品显示在最后 | `ORDER BY price ASC NULLS LAST` |
| 优先显示不完整的记录以便审核 | `ORDER BY field ASC NULLS FIRST` |
| 折扣从高到低排序，无折扣的排在最后 | `ORDER BY discount DESC NULLS LAST` |

### 你的任务

你有一个包含产品信息的 `products` 表。
某些产品具有 `discount_percent` 值，而其他产品的该字段为 NULL（表示无折扣）。

编写一个查询以：

1. 选择 `product_name`、`category` 和 `discount_percent` 列
2. 按 `discount_percent` 升序排序
3. 确保折扣为 NULL 的产品在结果中排在**最后**
4. 对于折扣相同的产品（包括 NULL），通过 `id` 保持排序一致

### 预期结果

折扣最小的产品应首先出现，无折扣（NULL）的产品应出现在列表的末尾。

### 解答

```sql
-- 选择 product_name、category 和 discount_percent
-- 按 discount_percent 升序排序，NULL 排在最后
-- 再按 id 进行次要排序以保证顺序一致
SELECT product_name, category, discount_percent
FROM products
ORDER BY discount_percent ASC NULLS LAST, id ASC;
```
