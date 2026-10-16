### INTERSECT - 查找查询之间的公共行

在处理多个数据源时，您经常需要找出它们的共同之处。
例如，零售公司可能想知道哪些客户同时出现在其线上和实体店数据库中，或者学校管理员可能需要找出同时注册了数学和科学课程的学生。
SQLite 的 `INTERSECT` 运算符通过仅返回**同时**出现在两个查询结果中的行来解决这个问题。

### 工作原理

`INTERSECT` 接收两个 `SELECT` 语句的结果，并仅返回在两者中完全相同的行。
可以将其想象成维恩图（Venn diagram） - `INTERSECT` 只给出重叠的中间部分。
如果某一行出现在第一个查询中但没有出现在第二个查询中，它将被排除。
如果它出现在第二个查询中但没有出现在第一个查询中，同样也会被排除。
只有同时存在于**两个**结果中的行才会保留。

几个重要细节：

- 两个 `SELECT` 语句必须返回**相同数量的列**
- 这些列必须具有**兼容的数据类型**
- 最终结果中会自动去除重复行

### 语法

```sql
SELECT column1, column2 FROM table_one
INTERSECT
SELECT column1, column2 FROM table_two;
```

无需 `JOIN` 或 `WHERE` 子句 - `INTERSECT` 会自动为您处理匹配。

### 示例

```sql
-- 查找航空公司 A 和航空公司 B 都提供服务的城市
SELECT destination_city FROM airline_a_routes
INTERSECT
SELECT destination_city FROM airline_b_routes;

-- 查找同时注册为学生的员工
SELECT email FROM employees
INTERSECT
SELECT email FROM students;

-- 查找在 Q1 和 Q2 都有销售的产品类别
SELECT category FROM q1_sales
INTERSECT
SELECT category FROM q2_sales;
```

### INTERSECT 与 JOIN 的对比

| 方法 | 适用场景 |
| --- | --- |
| `INTERSECT` | 您希望获取来自两个相似查询的匹配**整行** |
| `INNER JOIN` | 您希望使用键（key）组合来自相关表的列 |

当您只需要查找公共值时，`INTERSECT` 更简单 - 不需要连接条件。

### INTERSECT 与其他集合运算符

| 运算符 | 返回内容 |
| --- | --- |
| `UNION` | 两个查询的所有行（无重复项） |
| `UNION ALL` | 两个查询的所有行（包含重复项） |
| `INTERSECT` | 仅**同时**出现在两个查询中的行 |
| `EXCEPT` | 存在于第一个查询但**不在**第二个查询中的行 |

### 您的任务

一家公司运营着两个仓库：**Warehouse A** 和 **Warehouse B**。
每个仓库库存的产品组合各不相同。
管理层想知道哪些产品在**两个**仓库中都有库存 - 这些属于冗余库存产品，可以作为重新分配的候选对象。

编写一个查询，返回同时在 `warehouse_a` 和 `warehouse_b` 中有库存的每个产品的 `product_name`。

### 预期结果

根据表中的数据，您的查询应返回同时出现在两个仓库中的产品名称。

### 解答

```sql
-- 查找同时在 warehouse_a 和 warehouse_b 中有库存的产品
SELECT product_name FROM warehouse_a
INTERSECT
SELECT product_name FROM warehouse_b;
```
