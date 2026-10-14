### PostgreSQL 中的文本类型

PostgreSQL 提供了三种主要的文本类型来存储字符数据。
选择正确的类型可以提高存储效率并强制执行数据约束。

### VARCHAR(n) - 限制长度的可变长文本

`VARCHAR(n)` 存储最多 `n` 个字符的字符串。
它仅占用实际内容所需的存储空间。

```sql
-- 用户名限制为 50 个字符
username VARCHAR(50)

-- 电子邮件限制为 255 个字符
email VARCHAR(255)
```

当需要强制限制最大长度时（例如用户名、电子邮件或代码），请使用 `VARCHAR(n)`。

### CHAR(n) - 定长文本

`CHAR(n)` 始终存储恰好 `n` 个字符，较短的字符串会用空格填充。

```sql
-- 国家/地区代码始终为 2 个字符
country_code CHAR(2)

-- 州缩写始终为 2 个字符
state_code CHAR(2)
```

对于固定长度的数据（例如国家/地区代码、邮政编码或标准化标识符），请使用 `CHAR(n)`。

### TEXT - 无限长度

`TEXT` 存储任意长度的字符串，没有上限限制。

```sql
-- 不限制长度的用户简介
bio TEXT

-- 文章内容
content TEXT
```

对于长篇内容（例如描述、评论或文章），请使用 `TEXT`。

### 对比表

| 类型 | 最大长度 | 存储方式 | 适用场景 |
| --- | --- | --- | --- |
| VARCHAR(n) | n 个字符 | 可变 | 用户名、电子邮件 |
| CHAR(n) | n 个字符 | 固定（填充） | 国家/地区代码、固定标识符 |
| TEXT | 无限制 | 可变 | 描述、文章 |

### 你的任务

已经存在一个具有以下结构的 `user_profiles` 表：

```sql
-- id: SERIAL PRIMARY KEY
-- username: VARCHAR(50) NOT NULL
-- display_name: VARCHAR(100)
-- country_code: CHAR(2)
-- bio: TEXT
-- website_url: VARCHAR(200)
```

插入一个包含以下值的新用户档案：

- username: `techie_jane`
- display\_name: `Jane Developer`
- country\_code: `US`
- bio: `Full-stack developer passionate about open source projects and teaching others to code.`
- website\_url: `https://janedev.example.com`

### 预期结果

在执行 INSERT 后，表中应包含一行具有上述值的数据。

### INSERT 示例

```sql
INSERT INTO user_profiles (username, display_name, country_code, bio, website_url)
VALUES ('example_user', 'Example User', 'CA', 'A short bio here.', 'https://example.com');
```

### 解答

```sql
-- 插入一条用户档案：
-- username: techie_jane
-- display_name: Jane Developer
-- country_code: US
-- bio: Full-stack developer passionate about open source projects and teaching others to code.
-- website_url: https://janedev.example.com

INSERT INTO user_profiles (username, display_name, country_code, bio, website_url)
VALUES (
    'techie_jane',
    'Jane Developer',
    'US',
    'Full-stack developer passionate about open source projects and teaching others to code.',
    'https://janedev.example.com'
);
```
