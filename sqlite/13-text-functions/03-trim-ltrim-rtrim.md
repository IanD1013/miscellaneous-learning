### SQLite 中的修剪函数

现实世界中的数据往往杂乱无章。
姓名可能带有前导空格、末尾点号，以及由于复制粘贴错误或遗留数据导入而产生的杂乱字符。
SQLite 提供了三个修剪函数，让你可以从文本值中去除不需要的字符 - 这是数据清洗的一项基本技能。

### 工作原理

SQLite 的修剪函数会从字符串的两端去除字符。
它们绝不会影响内部内容 - 只作用于前导端、末尾端或两端。

- **`trim(text)`** - 从**两端**去除空格
- **`ltrim(text)`** - 仅从**左侧**（前导端）去除空格
- **`rtrim(text)`** - 仅从**右侧**（末尾端）去除空格

默认情况下，这三个函数都会去除**空格字符**。
但每个函数都接受一个可选的第二个参数：用于替代空格需要去除的字符集字符串。

### 语法

```sql
-- 从两端去除空格
trim(column_name)

-- 仅从左侧去除空格
ltrim(column_name)

-- 仅从右侧去除空格
rtrim(column_name)

-- 从两端去除指定字符
trim(column_name, 'characters_to_remove')

-- 从左侧 / 右侧去除指定字符
ltrim(column_name, 'characters_to_remove')
rtrim(column_name, 'characters_to_remove')
```

第二个参数是一个**字符集**，而不是子字符串。
`trim('***hello***', '*')` 会从两端移除所有的 `*`，返回 `hello`。

### 示例

```sql
-- 默认：去除空格
SELECT trim('   Seattle   ');          -- 'Seattle'
SELECT ltrim('   Seattle   ');         -- 'Seattle   '
SELECT rtrim('   Seattle   ');         -- '   Seattle'

-- 自定义字符
SELECT trim('###Price###', '#');       -- 'Price'
SELECT ltrim('...loading...', '.');    -- 'loading...'
SELECT rtrim('data////', '/');         -- 'data'

-- 字符集中包含多个字符
SELECT trim('-=Title=-', '-=');        -- 'Title'
-- 这会从两端去除任何 '-' 或 '='

-- 在查询中组合使用修剪函数
SELECT trim(city) AS clean_city,
       ltrim(zip_code, '0') AS short_zip
FROM addresses;
```

### 常见模式

| 模式 | 用途 | 结果 |
| --- | --- | --- |
| `trim(name)` | 清除姓名中的空白字符 | `' Alice ' → 'Alice'` |
| `trim(code, '0')` | 去除前导/末尾的零 | `'007200' → '72'` |
| `ltrim(price, '$')` | 去除货币前缀 | `'$49.99' → '49.99'` |
| `rtrim(path, '/')` | 规范化 URL 路径 | `'/api/users/' → '/api/users'` |
| `trim(trim(val), '.')` | 链式修剪以进行多步清洗 | 先去除空格，再去除点号 |

### 重要细节

字符参数是一个**字符集**，而不是模式匹配。
`trim('abcba', 'ab')` 会从两端移除任何 `a` 或 `b`，返回 `c` - 它并不会去查找子字符串 `"ab"`。

### 你的任务

你有一个包含格式不良数据的 `messy_contacts` 表。
编写一个查询，返回包含以下清洗后列的**所有行**：

1. **`clean_name`** - `name` 列包含前导和末尾空格。从两端将其去除。
2. **`clean_email`** - `email` 列包含前导点号和末尾点号。从两端去除点号（但不要去除空格 - 电子邮件中没有任何空格）。
3. **`clean_phone`** - `phone` 列仅在左侧包含前导短划线。仅从左侧去除短划线。
4. **`clean_notes`** - `notes` 列仅在右侧包含末尾星号和井号。仅从右侧去除 `*` 和 `#`。

按原始 `id` 列对结果进行排序。

### 预期输出列

| clean\_name | clean\_email | clean\_phone | clean\_notes |
| --- | --- | --- | --- |
| cleaned... | cleaned... | cleaned... | cleaned... |

### 解答

```sql
-- 使用修剪函数清洗 messy_contacts 数据
-- 返回：clean_name、clean_email、clean_phone、clean_notes
-- 按 id 排序
SELECT
  trim(name) AS clean_name,
  trim(email, '.') AS clean_email,
  ltrim(phone, '-') AS clean_phone,
  rtrim(notes, '*#') AS clean_notes
FROM messy_contacts
ORDER BY id;
```
