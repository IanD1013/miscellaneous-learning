### LIKE 运算符

`LIKE` 运算符根据文本列中的**模式匹配**来过滤行。
与使用 `=` 的精确比较不同，LIKE 允许您使用通配符来搜索部分匹配项。

### 通配符

| 通配符 | 含义 | 示例 | 匹配项 |
| --- | --- | --- | --- |
| `%` | 任意字符序列（包括零个字符） | `'J%'` | John, Jane, J |
| `_` | 恰好一个字符 | `'J_n'` | Jon, Jan, Jen |

### 使用 % 通配符

```sql
-- 以 'J' 开头的名字
SELECT * FROM customers WHERE name LIKE 'J%';

-- 以 'son' 结尾的名字
SELECT * FROM customers WHERE name LIKE '%son';

-- 包含 'ann' 的名字
SELECT * FROM customers WHERE name LIKE '%ann%';
```

### 使用 \_ 通配符

```sql
-- 恰好 3 个字符且以 'Jo' 开头的名字
SELECT * FROM customers WHERE name LIKE 'Jo_';

-- 第二个字符是 'a'
SELECT * FROM customers WHERE name LIKE '_a%';
```

### 组合使用通配符

```sql
-- 以任意字符开头，接着是 'oh'，然后是任意内容的名字
SELECT * FROM customers WHERE name LIKE '_oh%';
```

### 大小写敏感性

在 PostgreSQL 中，`LIKE` 是**区分大小写**的。
使用 `ILIKE` 进行不区分大小写的匹配：

```sql
-- 不区分大小写的匹配
SELECT * FROM customers WHERE name ILIKE 'j%';
```

### 你的任务

编写一个查询，选择名字**以字母 'J' 开头**的所有客户。

### 预期结果

你的查询应返回名为 James、Jennifer 和 Jessica 的客户。

### 解答

```sql
-- 选择名字以 'J' 开头的所有客户
SELECT * FROM customers WHERE name LIKE 'J%';
```
