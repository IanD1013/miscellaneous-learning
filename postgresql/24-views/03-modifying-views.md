### 使用 CREATE OR REPLACE 修改视图

当你需要更改视图的定义时，有两种选择：

1. `DROP VIEW` 紧接着 `CREATE VIEW` - 需要删除依赖对象
2. `CREATE OR REPLACE VIEW` - 原地修改视图，同时保留权限和依赖关系

### CREATE OR REPLACE VIEW 语法

```sql
CREATE OR REPLACE VIEW view_name AS
SELECT column1, column2, new_column
FROM table_name
WHERE condition;
```

### 替换视图的关键规则

| 规则 | 描述 |
| --- | --- |
| 列顺序 | 新列必须添加到末尾 |
| 现有列 | 不能删除或重命名现有列 |
| 数据类型 | 不能更改现有列的数据类型 |
| 新列 | 可以自由添加新列 |

### 添加计算列

```sql
-- 原始视图
CREATE VIEW order_totals AS
SELECT order_id, quantity, unit_price
FROM order_items;

-- 带有计算列的修改后视图
CREATE OR REPLACE VIEW order_totals AS
SELECT order_id, quantity, unit_price,
       quantity * unit_price AS line_total
FROM order_items;
```

### 你的任务

现有的视图 `product_inventory` 展示了产品及其库存数量。
请使用 `CREATE OR REPLACE VIEW` 修改此视图，以添加两个新的计算列：

1. `inventory_value` - 计算方式为 `stock_quantity * unit_price`
2. `stock_status` - 一个文本列，显示：
   - 当 stock\_quantity = 0 时显示 `'Out of Stock'`
   - 当 stock\_quantity 介于 1 和 10 之间（含 1 和 10）时显示 `'Low Stock'`
   - 当 stock\_quantity > 10 时显示 `'In Stock'`

### 期望的视图列

修改后，视图应按顺序包含以下列：

- `product_id`
- `product_name`
- `stock_quantity`
- `unit_price`
- `inventory_value`（新增）
- `stock_status`（新增）

### 解答

```sql
-- 修改 product_inventory 视图，添加：
-- 1. inventory_value（stock_quantity * unit_price）
-- 2. stock_status（'Out of Stock'、'Low Stock' 或 'In Stock'）
CREATE OR REPLACE VIEW product_inventory AS
SELECT
    product_id,
    product_name,
    stock_quantity,
    unit_price,
    stock_quantity * unit_price AS inventory_value,
    CASE
        WHEN stock_quantity = 0 THEN 'Out of Stock'
        WHEN stock_quantity BETWEEN 1 AND 10 THEN 'Low Stock'
        ELSE 'In Stock'
    END AS stock_status
FROM products;
```
