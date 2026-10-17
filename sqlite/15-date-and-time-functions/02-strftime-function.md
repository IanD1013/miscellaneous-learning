### 在 SQLite 中使用 `strftime()` 格式化日期

SQLite 没有像 `DATE` 或 `TIMESTAMP` 这样的专用日期类型。
相反，日期以文本字符串的形式存储，并且 SQLite 提供了功能强大的 `strftime()` 函数来提取和格式化日期组成部分。
每当您需要按月份对销售额进行分组、按年份筛选记录或以人类可读的方式显示日期时，这都是必不可少的。

### 工作原理

`strftime()` 接受一个**格式字符串**和一个**日期值**，然后返回一个将日期组件替换到格式占位符中的文本字符串。
可以把它想象成一个模板 - 您描述输出的格式，SQLite 填充相应的值。

日期值可以是日期字符串（`'2024-03-15'`）、日期时间字符串（`'2024-03-15 14:30:00'`）或特殊关键字 `'now'`。

### 语法

```sql
strftime(format_string, date_value)
```

### 关键格式说明符

| 说明符 | 描述 | 输出示例 |
| --- | --- | --- |
| `%Y` | 4 位年份 | `2024` |
| `%m` | 月份 (01–12) | `03` |
| `%d` | 月中的天数 (01–31) | `15` |
| `%H` | 小时 (00–23) | `14` |
| `%M` | 分钟 (00–59) | `30` |
| `%S` | 秒 (00–59) | `00` |
| `%w` | 星期几 (0=Sunday, 6=Saturday) | `5` |
| `%j` | 一年中的天数 (001–366) | `075` |
| `%W` | 一年中的周数 (00–53, 周一开始) | `10` |

请注意，`%m` 返回的是**带前导零**的字符串（如 `'03'`），而不是整数。
同样，`%w` 返回的是单个字符的字符串（如 `'5'`）。

### 示例

```sql
-- 仅从时间戳中提取年份
SELECT strftime('%Y', '2023-11-20 09:15:00');
-- 结果：'2023'

-- 获取星期几（0=Sunday）
SELECT strftime('%w', '2023-11-20');
-- 结果：'1'（Monday）

-- 在一次调用中组合多个说明符
SELECT strftime('%Y-%m', '2023-11-20') AS year_month;
-- 结果：'2023-11'

-- 统计每年入职的员工数
SELECT strftime('%Y', hire_date) AS hire_year, COUNT(*) AS total
FROM employees
GROUP BY hire_year;

-- 使用 CASE 将数字月份转换为名称
SELECT name, 
       CASE strftime('%m', birth_date)
           WHEN '01' THEN 'January'
           WHEN '02' THEN 'February'
           WHEN '06' THEN 'June'
           -- ... 其他月份
       END AS birth_month
FROM employees;
```

### 结合使用 `strftime()` 与 `CASE`

由于 `strftime('%m', ...)` 返回诸如 `'01'`、`'02'` 等带前导零的字符串，您可以使用 `CASE` 表达式将每个值映射为其完整的英文月份名称。
请记住要与**字符串**进行比较，而不是整数 - 应使用 `'01'` 而不是 `1`。

```sql
CASE strftime('%m', some_date)
    WHEN '01' THEN 'January'
    WHEN '02' THEN 'February'
    -- ... 全部 12 个月
END
```

### 星期参考表

| `%w` 值 | 星期 |
| --- | --- |
| `0` | Sunday |
| `1` | Monday |
| `2` | Tuesday |
| `3` | Wednesday |
| `4` | Thursday |
| `5` | Friday |
| `6` | Saturday |

### 您的任务

编写一个针对 `orders` 表的查询，为每个订单返回以下列，并按 `order_id` 排序：

1. **`order_id`** - 订单 ID
2. **`order_year`** - 从 `order_date` 中提取的 4 位年份
3. **`month_name`** - 从 `order_date` 派生的完整英文月份名称（例如 `January`、`March`）
4. **`day_of_week`** - 从 `order_date` 派生的星期名称（例如 `Sunday`、`Monday`）

您必须处理所有 12 个月份和全部 7 个星期值。
结果应按 `order_id` 升序排序。

### 预期结果

```yaml
order_id | order_year | month_name | day_of_week
---------|------------|------------|------------
1        | 2024       | January    | Monday
2        | 2024       | March      | Friday
3        | 2024       | June       | Wednesday
4        | 2024       | September  | Sunday
5        | 2024       | December   | Tuesday
6        | 2023       | October    | Saturday
```

### 解答

```sql
-- 从 order_date 中提取年份、月份名称和星期名称
-- 使用 strftime() 和 CASE 表达式
SELECT
  order_id,
  strftime('%Y', order_date) AS order_year,
  CASE strftime('%m', order_date)
    WHEN '01' THEN 'January'
    WHEN '02' THEN 'February'
    WHEN '03' THEN 'March'
    WHEN '04' THEN 'April'
    WHEN '05' THEN 'May'
    WHEN '06' THEN 'June'
    WHEN '07' THEN 'July'
    WHEN '08' THEN 'August'
    WHEN '09' THEN 'September'
    WHEN '10' THEN 'October'
    WHEN '11' THEN 'November'
    WHEN '12' THEN 'December'
  END AS month_name,
  CASE strftime('%w', order_date)
    WHEN '0' THEN 'Sunday'
    WHEN '1' THEN 'Monday'
    WHEN '2' THEN 'Tuesday'
    WHEN '3' THEN 'Wednesday'
    WHEN '4' THEN 'Thursday'
    WHEN '5' THEN 'Friday'
    WHEN '6' THEN 'Saturday'
  END AS day_of_week
FROM orders
ORDER BY order_id;
```
