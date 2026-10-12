### INTERSECT - 查找共有行

`INTERSECT` 仅返回同时出现在**两个**查询结果中的行。
这就像找出两个集合的交集，即共同的元素。

### 基本语法

```sql
SELECT column1, column2 FROM table_a
INTERSECT
SELECT column1, column2 FROM table_b;
```

### INTERSECT 的工作原理

| 查询 A 结果 | 查询 B 结果 | INTERSECT 结果 |
| --- | --- | --- |
| Apple | Apple | Apple |
| Banana | Cherry | Grape |
| Grape | Grape |  |
| Orange | Mango |  |

仅返回存在于**两个**结果集中的行。

### 核心规则

1. **列数必须匹配** - 两个查询选择的列数必须相同
2. **数据类型必须兼容** - 对应的列必须具有兼容的数据类型
3. **自动去重** - 与 `UNION` 类似，`INTERSECT` 会自动去除重复行
4. **列的顺序很重要** - 查询 A 的第一列会与查询 B 的第一列进行比较

### INTERSECT 与 JOIN 的区别

```sql
-- INTERSECT 查找两个查询之间匹配的行
SELECT product_name FROM warehouse_a
INTERSECT
SELECT product_name FROM warehouse_b;

-- JOIN 根据条件连接行
SELECT a.product_name 
FROM warehouse_a a
INNER JOIN warehouse_b b ON a.product_name = b.product_name;
```

两者都可以找到共同的项目，但在比较简单的结果集时，`INTERSECT` 更加简洁清晰。

### 你的任务

你有两张仓库库存表：`warehouse_a_inventory` 和 `warehouse_b_inventory`。
每张表都包含了存放在该地点的产品。

编写一个查询以找出**同时在两个仓库中均有库存的产品**，即同时出现在两张库存表中的项目。

### 期望的列

- `product_name` - 两个仓库中均有现货的产品名称

### 期望的结果

```diff
product_name
------------
Laptop
Monitor
Keyboard
```

（顺序可能会有所不同）

### 解答

```sql
-- 找出同时存在于两个仓库中的产品
-- 使用 INTERSECT 合并两张库存表的结果

SELECT product_name FROM warehouse_a_inventory
INTERSECT
SELECT product_name FROM warehouse_b_inventory;
```
