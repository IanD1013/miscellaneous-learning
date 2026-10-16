### SQLite 中的 GLOB 运算符

SQLite 提供了一个强大的模式匹配运算符，称为 `GLOB`，它遵循 Unix glob 语法。
与大多数 SQL 数据库中更常见的 `LIKE` 运算符不同，`GLOB` 是**区分大小写**的，并且使用不同的通配符。
这使得它在需要精确模式匹配时特别有用 - 例如过滤文件名、路径或任何区分大小写的文本。

### 工作原理

`GLOB` 使用两个通配符将字符串与模式进行比较：

| 通配符 | 含义 | LIKE 中的等效字符 |
| --- | --- | --- |
| `*` | 匹配零个或多个字符的任意序列 | `%` |
| `?` | 精确匹配一个字符 | `_` |

与 `LIKE` 的主要区别：

- **区分大小写**：`GLOB 'Hello'` 不会匹配 `'hello'` 或 `'HELLO'`
- **不同的通配符**：使用 `*` 代替 `%`，使用 `?` 代替 `_`
- **Unix 风格**：如果你使用过 Shell 通配符（`ls *.py`），GLOB 的工作方式与之相同

### 语法

```sql
SELECT columns
FROM table_name
WHERE column_name GLOB 'pattern';
```

### 示例

假设有一个名为 `documents` 的表，其中包含一个 `title` 列：

```sql
-- 查找所有以 'Report' 开头的文档
-- 区分大小写：匹配 'Report2024'，但不匹配 'report2024'
SELECT title FROM documents WHERE title GLOB 'Report*';

-- 查找扩展名恰好为 3 个字符的文档，例如 'memo.doc'、'data.csv'
SELECT title FROM documents WHERE title GLOB '*.???';

-- 查找以任意单个字符开头、后跟 'otes' 的文档
-- 匹配 'Notes'、'notes' 和 'votes'，因为 ? 代表任意一个字符
SELECT title FROM documents WHERE title GLOB '?otes*';

-- 比较 LIKE 与 GLOB：
-- 在 SQLite 中，LIKE 默认不区分大小写：
SELECT title FROM documents WHERE title LIKE 'report%';  -- 匹配 'Report2024'、'report2024'
-- GLOB 区分大小写：
SELECT title FROM documents WHERE title GLOB 'report*';  -- 仅匹配 'report2024'
```

### 字符范围（补充知识）

`GLOB` 还支持在方括号内指定字符范围：

```sql
-- 匹配以小写字母开头的文件名
SELECT name FROM items WHERE name GLOB '[a-z]*';

-- 匹配以数字开头的文件名
SELECT name FROM items WHERE name GLOB '[0-9]*';
```

### 你的任务

你有一个包含文件名及其大小的 `files` 表。
编写一个查询，选择文件名以 `.txt` 结尾的所有文件的 `filename` 和 `size`。

使用带有适当模式的 `GLOB` 运算符来匹配以 `.txt` 结尾的文件名。
请记住，`GLOB` 是区分大小写的，因此 `.txt` 不会匹配 `.TXT` 或 `.Txt`。

### 预期结果

你的查询应仅返回带有 `.txt` 扩展名（小写）的文件及其大小。

### 解答

```sql
-- 选择所有以 .txt 结尾的文件的 filename 和 size
-- 使用 GLOB 运算符和正确的模式
SELECT filename, size FROM files WHERE filename GLOB '*.txt';
```
