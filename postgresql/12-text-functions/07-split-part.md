### SPLIT\_PART 函数

`SPLIT_PART` 函数根据指定的分隔符拆分字符串并返回特定的部分。
它对于解析存储在文本列中的定界数据至关重要。

### 语法

```sql
SPLIT_PART(string, delimiter, position)
```

- **string**：要拆分的文本
- **delimiter**：用于拆分的分隔字符
- **position**：要返回的部分（从 1 开始的索引）

### 基本示例

```sql
-- 按逗号拆分，获取第一部分
SELECT SPLIT_PART('apple,banana,cherry', ',', 1);  -- 返回：'apple'

-- 获取第二部分
SELECT SPLIT_PART('apple,banana,cherry', ',', 2);  -- 返回：'banana'

-- 获取第三部分
SELECT SPLIT_PART('apple,banana,cherry', ',', 3);  -- 返回：'cherry'
```

### 处理边界情况

```sql
-- 位置超出可用部分时返回空字符串
SELECT SPLIT_PART('apple,banana', ',', 5);  -- 返回：''

-- 未找到分隔符时返回整个字符串（位置 1）
SELECT SPLIT_PART('apple', ',', 1);  -- 返回：'apple'

-- 不同的分隔符
SELECT SPLIT_PART('2024-01-15', '-', 2);  -- 返回：'01'
SELECT SPLIT_PART('john@example.com', '@', 1);  -- 返回：'john'
```

### 常见用例

| 用例 | 示例 | 结果 |
| --- | --- | --- |
| 从电子邮件中提取域名 | `SPLIT_PART('user@company.com', '@', 2)` | 'company.com' |
| 从日期字符串中获取月份 | `SPLIT_PART('2024-03-15', '-', 2)` | '03' |
| 解析 CSV 数据 | `SPLIT_PART('red,green,blue', ',', 2)` | 'green' |

### 你的任务

你有一个 `inventory` 表，其中每个项目都有一个 `categories` 列，包含以逗号分隔的类别名称（例如，"Electronics,Gadgets,Accessories"）。

编写一个查询，从每个项目的类别列表中提取**第二个类别**。
返回 `item_name` 以及提取出的类别并将其命名为 `secondary_category`。

### 预期输出列

- `item_name` - 库存项目的名称
- `secondary_category` - 逗号分隔列表中的第二个类别

### 解答

```sql
-- 从每个项目的类别列表中提取第二个类别
-- 返回 item_name 和 secondary_category 列
SELECT item_name, SPLIT_PART(categories, ',', 2) AS secondary_category
FROM inventory;
```
