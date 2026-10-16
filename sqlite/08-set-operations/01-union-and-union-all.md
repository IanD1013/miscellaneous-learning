### UNION 和 UNION ALL

在使用关系型数据库时，你经常需要将来自多个查询的结果合并为一个结果集。
SQL 提供了两个用于此操作的操作符：`UNION` 和 `UNION ALL`。
当数据分布在相似的表中时（例如活跃记录与归档记录、区域数据集或不同时间段），这些操作符至关重要。

### 工作原理

`UNION` 接受两个或多个 `SELECT` 语句，并将它们的结果垂直堆叠为一个结果集。
可以把它想象成将一个电子表格追加到另一个电子表格下方。

- **`UNION`** 合并结果并**去除重复行**。如果同一行在两个查询中都出现，它只会出现一次。
- **`UNION ALL`** 合并结果并**保留所有行**，包括重复项。它的速度更快，因为它跳过了重复项检查步骤。

这两个操作符都要求每个 `SELECT` 语句具有**相同数量的列**，并且对应的列应具有兼容的数据类型。

### 语法

```sql
SELECT column1, column2 FROM table_a
UNION
SELECT column1, column2 FROM table_b;

-- 保留重复项：
SELECT column1, column2 FROM table_a
UNION ALL
SELECT column1, column2 FROM table_b;
```

### 示例

假设你有 `summer_menu` 和 `winter_menu` 两个表，每个表都包含 `dish_name` 和 `category` 列：

```sql
-- 获取两个季节提供的所有不重复菜品
SELECT dish_name, category FROM summer_menu
UNION
SELECT dish_name, category FROM winter_menu;

-- 获取所有菜品，包括同时出现在两个菜单上的菜品（重复项出现两次）
SELECT dish_name, category FROM summer_menu
UNION ALL
SELECT dish_name, category FROM winter_menu;
```

如果类别为 "Starter" 的 "Tomato Soup" 在两个表中都存在：

- `UNION` 会返回它 **一次**
- `UNION ALL` 会返回它 **两次**

你还可以合并两个以上的查询：

```sql
SELECT city FROM north_stores
UNION
SELECT city FROM south_stores
UNION
SELECT city FROM west_stores;
```

### 常见模式

| 模式 | 适用场景 |
| --- | --- |
| `UNION` | 你需要一个没有重复行的干净列表 |
| `UNION ALL` | 你需要每一行，或者你知道没有重复项并希望获得更好的性能 |
| 添加标签列 | 使用字符串字面量来追踪某一行来自哪个查询：`SELECT name, 'Summer' AS season FROM summer_menu` |

### 重要规则

- 每个 `SELECT` 中的列数必须匹配
- 最终结果中的列名来自**第一个** `SELECT` 语句
- 你可以在最后（在最后一个 `SELECT` 之后）添加 `ORDER BY` 来对合并后的结果进行排序

### 你的任务

你有两个表：

- **`current_employees`** - 当前在公司工作的员工（`name`, `department`）
- **`former_employees`** - 之前在公司工作的员工（`name`, `department`）

某些人可能同时出现在两个表中（例如离职后又被重新雇佣的人，或数据重叠）。

编写一个查询，返回**所有员工（现任和前任），且不包含重复行**。
结果应包含两列：`name` 和 `department`。

### 预期结果

根据示例数据，你的查询应返回合并两个表并去重后的 8 个唯一行。

### 解答

```sql
-- 合并所有员工（现任和前任），不包含重复项
-- 结果应包含列：name, department
SELECT name, department FROM current_employees
UNION
SELECT name, department FROM former_employees;
```
