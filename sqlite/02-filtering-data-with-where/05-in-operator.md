### IN 运算符

当需要检查某一列的值是否匹配多个可能的值之一时，编写多个 `OR` 条件会变得繁琐且难以阅读。
`IN` 运算符提供了一种简洁明了的替代方案，使你的查询更易于编写和维护。

### 工作原理

`IN` 运算符用于检查某个值是否存在于指定的值列表中。
它在逻辑上等同于将多个 `OR` 条件链接在一起，但可读性要好得多。
数据库会评估每一行，并在列值匹配列表中**任意**一项时将其包含在结果中。

例如，与其编写：

```sql
WHERE color = 'Red' OR color = 'Blue' OR color = 'Green'
```

你可以编写：

```sql
WHERE color IN ('Red', 'Blue', 'Green')
```

两者产生的结果完全相同，但 `IN` 版本更简短，并且随着列表项的增加具有更好的扩展性。

### 语法

```sql
SELECT column1, column2
FROM table_name
WHERE column_name IN (value1, value2, value3, ...);
```

你也可以使用 `NOT IN` 进行否定，以排除特定的值：

```sql
SELECT column1, column2
FROM table_name
WHERE column_name NOT IN (value1, value2);
```

### 示例

假设你有一个包含 `name`、`category` 和 `price` 列的 `products` 表。

查找处于 Electronics 或 Books 分类的所有产品：

```sql
SELECT name, category
FROM products
WHERE category IN ('Electronics', 'Books');
```

查找不属于 Clothing 或 Toys 分类的产品：

```sql
SELECT name, price
FROM products
WHERE category NOT IN ('Clothing', 'Toys');
```

`IN` 运算符也适用于数值：

```sql
SELECT name, price
FROM products
WHERE price IN (9.99, 19.99, 29.99);
```

### 重要注意事项

| 细节 | 说明 |
| --- | --- |
| 字符串值 | 必须用单引号括起来：`'value'` |
| 大小写敏感性 | SQLite 字符串比较默认区分大小写 |
| 列表大小 | 你可以根据需要在列表中包含任意数量的值 |
| NULL 处理 | `IN` 不会匹配 `NULL` 值 - 请单独使用 `IS NULL` |

### 你的任务

你有一个包含 `name` 和 `department` 列的 `employees` 表。
编写一个查询，选择在 **Sales**、**Marketing** 或 **Engineering** 部门工作的所有员工的 `name` 和 `department`。

在结果中返回这两列。

### 预期结果

根据示例数据，你的查询应返回来自这三个部门的员工，同时排除来自 HR 和 Finance 等其他部门的员工。

### 解答

```sql
-- 选择 Sales、Marketing 或 Engineering 部门的员工
SELECT name, department
FROM employees
WHERE department IN ('Sales', 'Marketing', 'Engineering');
```
