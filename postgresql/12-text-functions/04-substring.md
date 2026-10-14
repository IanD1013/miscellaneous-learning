### SUBSTRING 函数

`SUBSTRING` 函数从指定位置开始提取指定长度的字符串片段。
这对于解析诸如产品代码、电话号码或任何具有可预测模式的文本等结构化数据至关重要。

### 基本语法

```sql
-- PostgreSQL 的语法选项
SUBSTRING(string FROM start FOR length)
SUBSTRING(string, start, length)
SUBSTR(string, start, length)  -- 更短的别名
```

### 位置和长度

```sql
-- 位置从 1 开始（而不是像许多编程语言那样从 0 开始）
SELECT SUBSTRING('PROD-12345' FROM 1 FOR 4);   -- 返回：'PROD'
SELECT SUBSTRING('PROD-12345' FROM 6 FOR 5);   -- 返回：'12345'
SELECT SUBSTRING('PROD-12345' FROM 6);         -- 返回：'12345'（直到末尾）
```

### 常见模式

| 模式 | 示例 | 结果 |
| --- | --- | --- |
| 前 N 个字符 | `SUBSTRING('Hello' FROM 1 FOR 3)` | 'Hel' |
| 跳过前 N 个 | `SUBSTRING('Hello' FROM 3)` | 'llo' |
| 中间部分 | `SUBSTRING('Hello' FROM 2 FOR 3)` | 'ell' |

### 处理结构化代码

```sql
-- 产品代码：'PROD-12345'
-- 提取前缀：SUBSTRING(code FROM 1 FOR 4) -> 'PROD'
-- 提取数字：SUBSTRING(code FROM 6 FOR 5) -> '12345'

-- 电话：'555-123-4567'
-- 区号：SUBSTRING(phone FROM 1 FOR 3) -> '555'
-- 最后 4 位数字：SUBSTRING(phone FROM 9 FOR 4) -> '4567'
```

### 你的任务

你有一个 `products` 表，其中的产品代码格式为 `XXXX-NNNNN`，其中 `XXXX` 是 4 个字母的类别前缀，`NNNNN` 是 5 位数字标识符。

编写一个查询，仅从每个产品代码中提取数字部分。

返回列：

- `product_name` - 产品名称
- `numeric_code` - 从产品代码中提取的 5 位数字部分

按 `numeric_code` 升序排列结果。

### 预期结果

| product\_name | numeric\_code |
| --- | --- |
| Laptop Stand | 10234 |
| Wireless Mouse | 20156 |
| USB Hub | 30789 |
| Keyboard | 45012 |

### 解答

```sql
-- 从 product_code 中提取数字部分（最后 5 个字符）
-- 返回 product_name 和提取出的 numeric_code
-- 按 numeric_code 升序排序
SELECT product_name, SUBSTRING(product_code FROM 6 FOR 5) AS numeric_code
FROM products
ORDER BY numeric_code;
```
