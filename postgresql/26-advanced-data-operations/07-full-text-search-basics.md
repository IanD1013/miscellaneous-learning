### PostgreSQL 中的全文搜索基础

全文搜索支持超越简单模式匹配的高级文本搜索。
PostgreSQL 提供了强大的函数来对文本进行分词、创建搜索查询并高效匹配文档。

### 核心函数

| 函数 | 用途 | 示例 |
| --- | --- | --- |
| `to_tsvector(config, text)` | 将文本转换为可搜索的词元（tokens） | `to_tsvector('english', 'The quick fox')` → `'fox':3 'quick':2` |
| `to_tsquery(config, query)` | 从词条创建搜索查询 | `to_tsquery('english', 'quick & fox')` |
| `@@` | 匹配运算符 | `tsvector @@ tsquery` 返回 true/false |

### to\_tsvector

将文本转换为 `tsvector`，包含位置信息的已排序词位（规范化后的词条）列表：

```sql
SELECT to_tsvector('english', 'The cats are running quickly');
-- 结果：'cat':2 'quick':5 'run':4
```

请注意：

- 像 "The" 和 "are" 这样的停用词会被移除
- 单词会被提取词干："cats" → "cat"，"running" → "run"，"quickly" → "quick"
- 保留了词的位置信息，以便进行邻近搜索

### to\_tsquery

使用布尔运算符创建搜索查询：

```sql
-- 单个单词
to_tsquery('english', 'database')

-- AND：两个词条都必须存在
to_tsquery('english', 'database & performance')

-- OR：任一词条匹配即可
to_tsquery('english', 'postgres | mysql')

-- NOT：排除词条
to_tsquery('english', 'database & !oracle')

-- 带邻近关系的短语
to_tsquery('english', 'full <-> text')  -- adjacent words
```

### @@ 匹配运算符

结合 tsvector 和 tsquery 来查找匹配项：

```sql
-- 查找与数据库相关的文档
SELECT title, content
FROM articles
WHERE to_tsvector('english', content) @@ to_tsquery('english', 'database');

-- 搜索多个列
SELECT title
FROM articles
WHERE to_tsvector('english', title || ' ' || content) 
      @@ to_tsquery('english', 'postgresql & tutorial');
```

### 你的任务

查询 `documents` 表，找出内容中**同时**包含 "data" 和 "analysis" 两个词的所有文档。
返回 `id`、`title` 和 `content` 列，并按 `id` 排序。

### 查询签名

```sql
SELECT id, title, content
FROM documents
WHERE to_tsvector('english', content) @@ to_tsquery('english', '...')
ORDER BY id;
```

### 预期结果

你的查询应返回在 content 中同时包含 "data" 和 "analysis"（或它们的词干变体）的文档。

### 解答

```sql
-- 找出同时包含 'data' 和 'analysis' 的文档
-- 使用 to_tsvector、to_tsquery 和 @@ 运算符
-- 结果按 id 排序
SELECT id, title, content
FROM documents
WHERE to_tsvector('english', content) @@ to_tsquery('english', 'data & analysis')
ORDER BY id;
```
