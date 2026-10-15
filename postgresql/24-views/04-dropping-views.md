### 删除视图 (Dropping Views)

当不再需要某些视图时，可以使用 `DROP VIEW` 将它们从数据库中移除。
了解可用的选项有助于你安全地管理视图并正确处理依赖项。

### DROP VIEW 基本语法

```sql
-- 简单删除（视图不存在时会失败）
DROP VIEW view_name;

-- 使用 IF EXISTS 安全删除（不存在时不报错）
DROP VIEW IF EXISTS view_name;
```

### IF EXISTS 选项

如果没有 `IF EXISTS`，删除一个不存在的视图会导致报错。
使用 `IF EXISTS` 可以使你的脚本更加安全并具备幂等性（idempotent）：

```sql
-- 如果 my_view 不存在，这会报错
DROP VIEW my_view;

-- 即使 my_view 不存在，这也会静默成功
DROP VIEW IF EXISTS my_view;
```

### 使用 CASCADE 处理依赖项

视图可能会依赖其他视图。
默认情况下，PostgreSQL 会阻止删除被其他视图所依赖的视图：

```sql
-- 如果有其他视图依赖它则会失败
DROP VIEW base_view;

-- 删除该视图以及所有依赖它的视图
DROP VIEW base_view CASCADE;

-- 如果存在依赖则显式失败（默认行为）
DROP VIEW base_view RESTRICT;
```

### 理解视图依赖关系

```sql
-- 视图 B 依赖于视图 A
CREATE VIEW view_a AS SELECT id, name FROM products;
CREATE VIEW view_b AS SELECT * FROM view_a WHERE name LIKE 'A%';

-- 这会失败：view_b 依赖于 view_a
DROP VIEW view_a;

-- 这会成功：同时删除 view_a 和 view_b
DROP VIEW view_a CASCADE;
```

### 删除多个视图

```sql
-- 一次删除多个视图
DROP VIEW IF EXISTS view1, view2, view3;

-- 对所有视图使用 CASCADE
DROP VIEW IF EXISTS view1, view2, view3 CASCADE;
```

### 你的任务

数据库中有一个名为 `order_summary` 的视图，另一个视图 `high_value_orders` 依赖于它。
请安全地删除 `order_summary` 视图以及依赖它的所有视图。

### 预期语句

```sql
DROP VIEW IF EXISTS order_summary CASCADE;
```

### 它的作用

1. `IF EXISTS` - 防止在视图不存在时报错
2. `CASCADE` - 自动删除依赖于 `order_summary` 的 `high_value_orders`

### 解答

```sql
-- 安全地删除 order_summary 视图，包括所有依赖它的视图
-- 使用 IF EXISTS 防止报错，使用 CASCADE 处理依赖关系
DROP VIEW IF EXISTS order_summary CASCADE;
```
