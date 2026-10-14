### PostgreSQL 中的数组类型

PostgreSQL 支持任何内置类型或用户自定义类型的数组。
数组允许你在单个列中存储多个值，这对于标签（tags）、分类（categories）、电话号码或任何类似列表的数据非常有用。

### 声明数组列

```sql
-- 使用方括号或 ARRAY 关键字
CREATE TABLE example (
    id SERIAL PRIMARY KEY,
    tags TEXT[],              -- 文本数组
    scores INTEGER[],         -- 整数数组
    matrix INTEGER[][]        -- 多维数组
);
```

### 数组字面量

```sql
-- 使用 ARRAY 构造器
INSERT INTO example (tags) VALUES (ARRAY['red', 'blue', 'green']);

-- 使用花括号语法
INSERT INTO example (tags) VALUES ('{red, blue, green}');

-- 空数组
INSERT INTO example (tags) VALUES (ARRAY[]::TEXT[]);
INSERT INTO example (tags) VALUES ('{}');
```

### 数组操作符

| 操作符 | 描述 | 示例 |
| --- | --- | --- |
| `@>` | 包含 | `tags @> ARRAY['sale']` |
| `<@` | 被包含于 | `ARRAY['sale'] <@ tags` |
| `&&` | 重叠（包含共有元素） | `tags && ARRAY['sale', 'new']` |
| `=` | 等于 | `tags = ARRAY['a', 'b']` |

### 数组函数

| 函数 | 描述 | 示例结果 |
| --- | --- | --- |
| `array_length(arr, dim)` | 指定维度的长度 | `array_length(ARRAY[1,2,3], 1)` → 3 |
| `array_position(arr, elem)` | 元素的位置 | `array_position(ARRAY['a','b'], 'b')` → 2 |
| `unnest(arr)` | 将数组展开为多行 | 返回多行 |
| `array_agg(col)` | 聚合为数组 | 将值分组为数组 |
| `ANY(arr)` | 匹配任意元素 | `'sale' = ANY(tags)` |

### 访问数组元素

```sql
-- PostgreSQL 中数组下标从 1 开始！
SELECT tags[1] FROM products;           -- 第一个元素
SELECT tags[1:2] FROM products;         -- 切片（第 1 和第 2 个元素）
```

### 你的任务

你有一个 `products` 表，其中包含一个存储文本标签数组的 `tags` 列。

编写一个查询，找出所有包含标签 `'electronics'` 的产品。

返回 `name` 和 `price` 列，并按 `name` 的字母顺序排序。

### 预期列

```
name, price
```

### 提示

使用 `@>`（包含）操作符来检查 tags 数组是否包含特定值：`tags @> ARRAY['value']`

### 解答

```sql
-- 查找所有包含 'electronics' 标签的产品
-- 返回 name 和 price，按 name 排序
SELECT name, price
FROM products
WHERE tags @> ARRAY['electronics']
ORDER BY name;
```
