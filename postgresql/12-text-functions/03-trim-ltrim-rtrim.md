### TRIM、LTRIM 和 RTRIM 函数

PostgreSQL 提供了三个基本函数，用于从文本字符串的开头和/或结尾删除不需要的字符。
在处理可能包含额外空格或其他不需要字符的用户输入或导入数据时，这些函数非常有用。

### 基本语法

```sql
-- 删除两端的空格
TRIM(string)
TRIM(BOTH FROM string)

-- 删除左侧（开头）的空格
LTRIM(string)
TRIM(LEADING FROM string)

-- 删除右侧（结尾）的空格
RTRIM(string)
TRIM(TRAILING FROM string)
```

### 修剪特定字符

你还可以指定要删除的字符：

```sql
-- 删除两端的特定字符
TRIM(BOTH 'x' FROM string)
TRIM('xy' FROM string)

-- 删除左侧或右侧的特定字符
LTRIM(string, 'characters_to_remove')
RTRIM(string, 'characters_to_remove')
```

### 示例

```sql
-- 基本的空白修剪
SELECT TRIM('   Hello World   ');        -- 返回：'Hello World'
SELECT LTRIM('   Hello World   ');       -- 返回：'Hello World   '
SELECT RTRIM('   Hello World   ');       -- 返回：'   Hello World'

-- 修剪特定字符
SELECT TRIM(BOTH '-' FROM '---Hello---'); -- 返回：'Hello'
SELECT LTRIM('xxxHello', 'x');            -- 返回：'Hello'
SELECT RTRIM('Hello!!!', '!');            -- 返回：'Hello'
```

### 主要区别

| 函数 | 删除位置 | 默认字符 |
| --- | --- | --- |
| TRIM | 两端 | 空格 |
| LTRIM | 仅左侧 | 空格 |
| RTRIM | 仅右侧 | 空格 |

### 你的任务

你有一个数据格式不规范的 `customers` 表。
客户姓名中包含多余的空格，产品代码包含不需要的前缀/后缀字符。
请编写一个查询来清理这些数据。

返回以下列：

- `customer_id` - 客户的 ID
- `clean_name` - 删除了所有前导和尾随空格的客户姓名
- `clean_code` - 删除了前导零和尾随连字符的产品代码

按 `customer_id` 对结果进行排序。

### 预期结果

对于姓名为 `' John Smith '` 且代码为 `'000ABC--'` 的客户：

- `clean_name` 应为 `'John Smith'`
- `clean_code` 应为 `'ABC'`

### 解答

```sql
-- 清理客户数据，删除：
-- 1. 姓名的前导和尾随空格
-- 2. 产品代码的前导零和尾随连字符
-- 按 customer_id 排序

SELECT
    customer_id,
    TRIM(name) AS clean_name,
    RTRIM(LTRIM(product_code, '0'), '-') AS clean_code
FROM customers
ORDER BY customer_id;
```
