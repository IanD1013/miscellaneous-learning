### SQLite 中的 REPLACE() 函数

在数据库中处理文本数据时，经常需要替换字符串的一部分 - 无论是清理数据、生成格式化输出，还是填充模板占位符。
SQLite 的 `replace()` 函数可以查找子字符串的每一次出现，并将其替换为新值。

### 工作原理

`replace()` 会扫描整个源字符串，并将目标子字符串的**每一次**出现都替换为替换值。
与某些只替换首次匹配的语言不同，SQLite 的 `replace()` 是全局替换的 - 它会在一次调用中替换所有匹配项。
该函数区分大小写，因此 `'{Name}'` 和 `'{name}'` 会被视为不同的子字符串。

### 语法

```sql
replace(source_string, target_substring, replacement_string)
```

- **source\_string**：要在其中搜索的原始文本
- **target\_substring**：要查找的确切子字符串
- **replacement\_string**：用于替换的内容

如果未找到目标子字符串，则原样返回原始字符串。

### 示例

```sql
-- 简单替换：替换一个单词
SELECT replace('Hello World', 'World', 'SQLite');
-- 结果：'Hello SQLite'

-- 所有出现都会被替换，而不仅仅是第一次
SELECT replace('go go go', 'go', 'stop');
-- 结果：'stop stop stop'

-- 嵌套 replace() 以执行多次替换
SELECT replace(replace('Dear {title} {surname}', '{title}', 'Dr.'), '{surname}', 'Smith');
-- 结果：'Dear Dr. Smith'

-- 当未找到目标时，不会有任何改变
SELECT replace('No match here', 'xyz', 'abc');
-- 结果：'No match here'
```

### 嵌套多次替换

每次调用 `replace()` 只能处理一次替换。
要替换多个不同的占位符，可以嵌套调用 - 内层的 `replace()` 先运行，其结果作为外层 `replace()` 的输入：

```sql
SELECT replace(
         replace(
           replace(template, '{city}', 'London'),
           '{country}', 'UK'),
         '{code}', '44')
FROM locations;
```

只要占位符与替换值不重叠，嵌套顺序就没有影响。

### 实用参考

| 模式 | 描述 | 结果 |
| --- | --- | --- |
| `replace(col, 'a', 'b')` | 将所有的 'a' 替换为 'b' | 单次替换 |
| `replace(replace(col, 'a', 'b'), 'c', 'd')` | 两次替换 | 嵌套调用 |
| `replace(col, '{ph}', other_col)` | 替换为列值 | 动态替换 |

### 你的任务

你有一个包含通知模板的 `messages` 表，其中含有占位符 `{name}` 和 `{date}`。
编写一个查询，返回替换了这两个占位符的每条消息：

- 将 `{name}` 替换为 `'Alice'`
- 将 `{date}` 替换为 `'2024-03-15'`

返回两列：

- `id` - 消息 ID
- `formatted_content` - 替换了所有占位符后的内容

按 `id` 升序对结果进行排序。

### 预期结果

```yaml
id | formatted_content
1  | Hello Alice, your appointment is on 2024-03-15.
2  | Dear Alice, we confirm your booking for 2024-03-15. Thank you, Alice!
3  | Reminder: Alice, don't forget 2024-03-15.
4  | Hi Alice! See you on 2024-03-15. - Alice's team
5  | No placeholders in this message.
```

### 解答

```sql
-- 将 {name} 替换为 'Alice'，将 {date} 替换为 '2024-03-15'
-- 返回列：id、formatted_content
SELECT
  id,
  replace(replace(content, '{name}', 'Alice'), '{date}', '2024-03-15') AS formatted_content
FROM messages
ORDER BY id;
```
