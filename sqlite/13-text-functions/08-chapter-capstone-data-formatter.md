### 字符串函数综合练习：结合 substr()、instr()、replace()、|| 和 printf()

本次综合练习汇集了你学过的所有 SQLite 核心字符串函数。
在实际应用中，数据很少以干净、统一的格式呈现。
电话号码可能有几十种格式，姓名需要解析，而输出必须统一格式化以便用于报表、导出或展示层。

SQLite 提供了一组功能强大的字符串函数，将它们结合使用，你可以在单个查询中将杂乱的数据转换为干净、结构化的输出。

### 各函数的工作原理

**`instr(string, target)`** 返回 `target` 在 `string` 中第一次出现的位置（从 1 开始计数）。
如果未找到则返回 0。
这是用于定位空格、逗号或特殊字符等分隔符的工具。

**`substr(string, start, length)`** 提取子字符串。
`start` 从 1 开始计数。
如果省略 `length`，它将返回从 `start` 到末尾的所有内容。

**`replace(string, from, to)`** 将所有出现的 `from` 替换为 `to`。
你可以嵌套多个 `replace()` 调用以依次去除几种不同的字符。

**`||`** 是连接运算符 - 它将字符串连接在一起。

**`printf(format, ...)`** 使用 C 风格的格式说明符来格式化值。
`%s` 插入字符串，`%-20s` 将字符串左对齐并占据 20 个字符宽度的字段，`%10s` 右对齐并占据 10 个字符。

### 语法

```sql
-- 查找分隔符的位置
SELECT instr('John Smith', ' ');  -- 返回 5

-- 提取子字符串
SELECT substr('John Smith', 1, 4);  -- 返回 'John'

-- 嵌套 replace 以去除多个字符
SELECT replace(replace('a-b_c', '-', ''), '_', '');  -- 返回 'abc'

-- 拼接
SELECT 'Hello' || ' ' || 'World';  -- 返回 'Hello World'

-- printf 格式化
SELECT printf('%-10s | %s', 'Name', 'Value');  -- 'Name       | Value'
```

### 示例

```sql
-- 从 'City, State' 格式中提取城市名称
SELECT substr('Denver, CO', 1, instr('Denver, CO', ',') - 1);
-- 返回：'Denver'

-- 通过去除斜杠和短划线来清洗产品代码
SELECT replace(replace('AB/12-34', '/', ''), '-', '');
-- 返回：'AB1234'

-- 格式化一行库存报表
SELECT printf('%-15s %5d units', 'Widget', 42);
-- 返回：'Widget           42 units'

-- 结合提取与格式化
SELECT printf('%s (%s)', 
  substr('Alice Johnson', 1, instr('Alice Johnson', ' ') - 1),
  'VIP'
);
-- 返回：'Alice (VIP)'
```

### 嵌套 replace() 调用

当需要去除多个不同的字符时，每个 `replace()` 都会在上一层处理的结果上继续操作：

```sql
-- 从字符串中去除括号、短划线和点号
SELECT replace(replace(replace(replace('(A).B-C', '(', ''), ')', ''), '.', ''), '-', '');
-- 返回：'ABC'
```

当你将每个字符替换为空字符串时，顺序并不重要 - 每一层都会剥离一种字符类型。

### printf 格式说明符参考

| 说明符 | 描述 | 示例 |
| --- | --- | --- |
| `%s` | 字符串 | `printf('%s', 'hi')` → `hi` |
| `%-15s` | 左对齐，15 个字符宽 | `printf('%-15s', 'hi')` → `hi` |
| `%10s` | 右对齐，10 个字符宽 | `printf('%10s', 'hi')` →  `hi` |

### 你的任务

你有一个 `contacts` 表，其中电话号码以各种不一致的格式存储。
编写一个查询，为每个联系人返回三列，并按 `full_name` 排序：

1. **`first_name`** - 从 `full_name` 中提取的名（第一个空格之前的所有内容）
2. **`clean_phone`** - 去除了所有非数字字符的电话号码（去除 `(`、`)`、`-` 和空格）
3. **`display`** - 使用 `printf` 格式化的字符串，格式为：`Name: <first_name padded to 10 chars, left-aligned> | Phone: <clean_phone>` - 例如：`Name: Alice | Phone: 1234567890`

`printf` 格式应使用 `%-10s` 将名左对齐在 10 个字符宽度的字段中。

### 解答

```sql
-- 提取 first_name、clean_phone 以及格式化后的显示字符串
-- 按 full_name 对结果排序
SELECT
  substr(full_name, 1, instr(full_name, ' ') - 1) AS first_name,
  replace(replace(replace(replace(phone, '(', ''), ')', ''), '-', ''), ' ', '') AS clean_phone,
  printf('Name: %-10s | Phone: %s',
    substr(full_name, 1, instr(full_name, ' ') - 1),
    replace(replace(replace(replace(phone, '(', ''), ')', ''), '-', ''), ' ', '')
  ) AS display
FROM contacts
ORDER BY full_name;
```
