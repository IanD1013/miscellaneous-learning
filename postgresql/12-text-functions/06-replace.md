### REPLACE 函数

`REPLACE` 函数在字符串中查找所有出现的某个子字符串，并用新的子字符串替换它们。
这对于数据清洗、模板处理和文本转换至关重要。

### 基本语法

```sql
REPLACE(source_string, old_substring, new_substring)
```

- `source_string`：要搜索的原始文本
- `old_substring`：要查找的文本模式
- `new_substring`：用于替换旧模式的文本

### 示例

```sql
-- 简单替换
SELECT REPLACE('Hello World', 'World', 'PostgreSQL');
-- 结果：'Hello PostgreSQL'

-- 替换所有匹配项（而不仅仅是第一个）
SELECT REPLACE('one-two-three', '-', ' ');
-- 结果：'one two three'

-- 通过替换为空字符串来删除文本
SELECT REPLACE('Hello!!!', '!', '');
-- 结果：'Hello'
```

### 关键特性

| 特性 | 描述 | 示例 |
| --- | --- | --- |
| 大小写敏感 | 仅匹配完全相同的大小写 | `REPLACE('Hello', 'hello', 'Hi')` → `'Hello'` |
| 所有匹配项 | 替换每一个匹配到的内容 | `REPLACE('aaa', 'a', 'b')` → `'bbb'` |
| 无匹配项 | 返回原始字符串 | `REPLACE('Hello', 'xyz', 'abc')` → `'Hello'` |
| 链式调用 | 可以嵌套多个 REPLACE 调用 | `REPLACE(REPLACE(text, 'a', 'b'), 'c', 'd')` |

### 你的任务

你有一个 `email_templates` 表，其中包含带有诸如 `{{NAME}}`、`{{PRODUCT}}` 和 `{{DATE}}` 等占位符的电子邮件模板。
编写一个查询，将这些占位符替换为实际值：

- 将 `{{NAME}}` 替换为 `John Smith`
- 将 `{{PRODUCT}}` 替换为 `Premium Subscription`
- 将 `{{DATE}}` 替换为 `January 15, 2025`

返回 `template_id` 以及处理后的模板内容（重命名为 `personalized_content`），并按 `template_id` 排序。

### 预期结果

```graphql
template_id | personalized_content
------------|----------------------------------------------------
1           | Dear John Smith, thank you for purchasing Premium Subscription.
2           | Hello John Smith! Your Premium Subscription is ready.
3           | John Smith, your order for Premium Subscription ships on January 15, 2025.
```

### 解答

```sql
-- 将占位符替换为实际值：
-- {{NAME}} -> John Smith
-- {{PRODUCT}} -> Premium Subscription
-- {{DATE}} -> January 15, 2025
-- 返回 template_id 和 personalized_content，按 template_id 排序

SELECT
    template_id,
    REPLACE(
        REPLACE(
            REPLACE(template_content, '{{NAME}}', 'John Smith'),
            '{{PRODUCT}}', 'Premium Subscription'
        ),
        '{{DATE}}', 'January 15, 2025'
    ) AS personalized_content
FROM email_templates
ORDER BY template_id;
```
