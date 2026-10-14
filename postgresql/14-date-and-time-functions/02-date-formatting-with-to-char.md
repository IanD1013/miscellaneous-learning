### 使用 TO\_CHAR 格式化日期

`TO_CHAR` 函数将日期和时间戳转换为格式化字符串。
这对于在报表和应用程序中以用户友好的格式显示日期至关重要。

### 基本语法

```sql
TO_CHAR(date_value, 'format_pattern')
```

### 常用格式模式

| 模式 | 描述 | 示例 |
| --- | --- | --- |
| `YYYY` | 4 位数年份 | 2024 |
| `YY` | 2 位数年份 | 24 |
| `MM` | 月份数字 (01-12) | 03 |
| `Month` | 完整月份名称（带填充空格） | March |
| `Mon` | 月份缩写 | Mar |
| `DD` | 月中的日期 (01-31) | 15 |
| `Day` | 完整星期名称（带填充空格） | Friday |
| `Dy` | 星期缩写 | Fri |
| `HH24` | 小时 (00-23) | 14 |
| `HH12` | 小时 (01-12) | 02 |
| `MI` | 分钟 (00-59) | 30 |
| `SS` | 秒 (00-59) | 45 |
| `AM` / `PM` | 上下午标识符 | PM |

### 格式示例

```sql
-- 'March 15, 2024'
SELECT TO_CHAR(DATE '2024-03-15', 'Month DD, YYYY');

-- '2024-03-15'
SELECT TO_CHAR(DATE '2024-03-15', 'YYYY-MM-DD');

-- '03/15/24'
SELECT TO_CHAR(DATE '2024-03-15', 'MM/DD/YY');

-- '14:30:45'
SELECT TO_CHAR(TIMESTAMP '2024-03-15 14:30:45', 'HH24:MI:SS');

-- 'Friday, March 15'
SELECT TO_CHAR(DATE '2024-03-15', 'Day, Month DD');
```

### 重要提示

- `Month` 和 `Day` 模式会用空格填充至 9 个字符
- 使用 `FM` 前缀去除填充：`FMMonth` 会得到 'March' 而不是 'March '
- 格式中的文本字面量必须用双引号括起来：`'"at" HH24:MI'`

### 你的任务

你有一个包含订单信息（包括时间戳）的 `orders` 表。
编写一个查询：

1. 选择 `order_id`
2. 将 `order_date` 格式化为 **'Month DD, YYYY'**（例如 'January 05, 2024'）
3. 将格式化后的列命名为 `formatted_date`
4. 按 `order_id` 对结果进行排序

### 预期输出格式

```yaml
order_id | formatted_date
---------|------------------
1        | January  05, 2024
2        | February 14, 2024
```

注意：`Month` 模式会用空格将月份名称填充至 9 个字符。

### 解答

```sql
-- 将订单日期格式化为 'Month DD, YYYY'
-- 选择 order_id 和格式化后的日期
-- 按 order_id 排序

SELECT order_id, TO_CHAR(order_date, 'Month DD, YYYY') AS formatted_date
FROM orders
ORDER BY order_id;
```
