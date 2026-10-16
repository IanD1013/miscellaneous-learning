### SQLite 中的 `instr()` 函数

在 SQLite 中处理文本数据时，你经常需要定位字符串中的特定字符或子字符串。
`instr()` 函数可以返回子字符串首次出现的位置，这对于解析 URL、文件路径或格式化标识符等结构化文本至关重要。

### 工作原理

`instr(string, substring)` 从左到右扫描 `string`，并返回 `substring` 首次出现的位置（基于 1 的索引）。
如果未找到子字符串，则返回 `0`。
这与许多基于 0 索引的编程语言不同 - 在 SQLite 中，第一个字符的位置是 1。

当与 `substr()` 结合使用时，这会变得特别强大，可以根据分隔符出现的位置提取字符串的部分内容。

### 语法

```sql
-- 查找子字符串在字符串中的位置
instr(source_string, search_string)

-- 从某个位置开始提取字符串的一部分
substr(source_string, start_position)
substr(source_string, start_position, length)
```

### 示例

```sql
-- 查找某个字符的位置
SELECT instr('hello-world', '-');  -- 返回 6

-- 未找到时返回 0
SELECT instr('helloworld', '-');   -- 返回 0

-- 提取分隔符之后的所有内容
-- 如果短划线位于位置 6，则它之后的部分从位置 7 开始
SELECT substr('hello-world', instr('hello-world', '-') + 1);  -- 返回 'world'

-- 查找多字符子字符串的位置
SELECT instr('2024-01-15T10:30:00', 'T');  -- 返回 11

-- 使用带长度参数的 substr 提取日期部分（T 之前）
SELECT substr('2024-01-15T10:30:00', 1, instr('2024-01-15T10:30:00', 'T') - 1);  -- 返回 '2024-01-15'
```

### 常见模式

```sql
-- 按分隔符拆分：获取其之前的部分
SELECT substr(filename, 1, instr(filename, '.') - 1) AS name_part
FROM files;

-- 按分隔符拆分：获取其之后的部分
SELECT substr(filename, instr(filename, '.') + 1) AS extension
FROM files;

-- 条件逻辑：检查子字符串是否存在
SELECT filename,
       CASE WHEN instr(filename, '.') > 0 THEN 'Has extension'
            ELSE 'No extension'
       END AS status
FROM files;
```

### 实用参考

| 函数 | 描述 | 示例 |
| --- | --- | --- |
| `instr(X, Y)` | X 中首次出现 Y 的位置（基于 1），若未找到则返回 0 | `instr('abc', 'b')` → 2 |
| `substr(X, N)` | X 中从位置 N 开始到末尾的子字符串 | `substr('abc', 2)` → 'bc' |
| `substr(X, N, L)` | X 中从位置 N 开始、长度为 L 的子字符串 | `substr('abc', 1, 2)` → 'ab' |

### 你的任务

你有一个包含 `id`、`name` 和 `email` 列的 `contacts` 表。
编写一个查询以返回：

- `name` - 联系人姓名
- `email` - 完整电子邮件地址
- `at_position` - 电子邮件中 `@` 字符的位置
- `domain` - 电子邮件的域名部分（`@` **之后**的所有内容）

按 `name` 升序对结果进行排序。

### 预期结果

```kotlin
name         | email                    | at_position | domain
-------------|--------------------------|-------------|------------------
Alice Chen   | alice@techcorp.com       | 6           | techcorp.com
Bob Martinez | bob.martinez@gmail.com   | 13          | gmail.com
Carla Jones  | carla.j@university.edu   | 8           | university.edu
Dan Smith    | dansmith@company.co.uk   | 9           | company.co.uk
Eva Brown    | eva_brown@data-labs.org  | 10          | data-labs.org
```

### 解答

```sql
-- 查找 '@' 的位置并从每个电子邮件中提取域名
-- 使用 instr() 和 substr()
SELECT
  name,
  email,
  instr(email, '@') AS at_position,
  substr(email, instr(email, '@') + 1) AS domain
FROM contacts
ORDER BY name;
```
