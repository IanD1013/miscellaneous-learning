### SQLite 的 printf() 函数

SQLite 包含一个内置的 `printf()` 函数，其工作原理类似于 C 语言的 `printf` - 它允许你直接在 SQL 查询中构建格式化字符串。
当你需要生成人类可读的输出、格式化货币值或将多列组合成特定文本模式而无需依赖应用程序代码时，这非常有用。

### 工作原理

`printf()` 将**格式字符串**作为其第一个参数，后跟用于填充占位符的值。
SQLite 会扫描格式字符串中的 `%` 说明符，并将每个说明符替换为对应的参数，同时应用所要求的格式。

### 语法

```sql
printf(format_string, value1, value2, ...)
```

### 格式说明符

| 说明符 | 描述 | 示例 |
| --- | --- | --- |
| `%d` | 整数（整数值） | `printf('%d units', 42)` → `42 units` |
| `%f` | 浮点数（默认 6 位小数） | `printf('%f', 3.14)` → `3.140000` |
| `%.Nf` | 保留 N 位小数的浮点数 | `printf('%.2f', 3.14159)` → `3.14` |
| `%s` | 字符串 | `printf('Hello %s', 'World')` → `Hello World` |
| `%%` | 字面百分号 | `printf('Score: %d%%', 85)` → `Score: 85%` |

### 示例

```sql
-- 格式化员工摘要
SELECT printf('%s earns %d per year', 'Alice', 75000);
-- 结果：Alice earns 75000 per year

-- 显示保留一位小数的温度
SELECT printf('Temperature: %.1f°C', 36.667);
-- 结果：Temperature: 36.7°C

-- 用字面 % 符号显示折扣百分比
SELECT printf('Discount: %d%%', 15);
-- 结果：Discount: 15%

-- 组合多个说明符
SELECT printf('%s scored %.1f%% on the exam', 'Bob', 92.456);
-- 结果：Bob scored 92.5% on the exam
```

### 常见模式

在对表列使用 `printf()` 时，可以直接引用列名作为参数值：

```sql
-- 格式化表中的行
SELECT printf('%s (Qty: %d)', item_name, quantity) AS summary
FROM inventory;
```

`%.2f` 说明符在货币格式化中尤其常用，因为大多数货币都显示为两位小数。

### 你的任务

你有一个包含 `name`（文本）和 `price`（实数）列的 `products` 表。
编写一个查询，将每个产品格式化为符合以下模式的单个字符串：

```bash
ProductName: $X.XX
```

例如，名为 "Widget" 且价格为 9.99 的产品应显示为 `Widget: $9.99`。
价格必须始终显示为恰好**两位小数**。

返回别名为 `formatted` 的单个列，并按产品名称的字母顺序排序。

### 预期结果

```bash
formatted
-------------------------
Bolt: $0.50
Gadget: $149.99
Gizmo: $24.00
Widget: $9.99
```

### 解答

```sql
-- 将每个产品格式化为："Name: $X.XX"
-- 返回名为 'formatted' 的列，按 name 排序
SELECT printf('%s: $%.2f', name, price) AS formatted
FROM products
ORDER BY name;
```
