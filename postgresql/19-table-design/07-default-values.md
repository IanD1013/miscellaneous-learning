### DEFAULT 默认值

`DEFAULT` 约束在 INSERT 操作未提供值时为列指定一个自动默认值。
这减少了重复代码，并确保了初始值的一致性。

### 静态默认值

静态默认值使用固定的字面量值：

```sql
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    status VARCHAR(20) DEFAULT 'active',
    quantity INTEGER DEFAULT 0,
    is_featured BOOLEAN DEFAULT false
);

-- INSERT 时不指定 status、quantity 或 is_featured
INSERT INTO products (name) VALUES ('Widget');
-- 结果：status='active', quantity=0, is_featured=false
```

### 函数默认值

函数默认值通过调用 PostgreSQL 函数来生成动态值：

```sql
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    event_date DATE DEFAULT CURRENT_DATE,
    unique_code UUID DEFAULT gen_random_uuid()
);

-- 每次 INSERT 都会自动获得当前时间戳
INSERT INTO events (name) VALUES ('Launch Party');
-- 结果：created_at 获得插入时的确切时刻
```

### 常用默认值函数

| 函数 | 描述 | 示例结果 |
| --- | --- | --- |
| NOW() | 当前日期和时间 | 2024-01-15 14:30:00 |
| CURRENT\_DATE | 仅当前日期 | 2024-01-15 |
| CURRENT\_TIMESTAMP | 与 NOW() 相同 | 2024-01-15 14:30:00 |
| gen\_random\_uuid() | 随机 UUID | a1b2c3d4-e5f6-... |

### 静态默认值 vs 函数默认值

```sql
-- 静态：每一行都获得相同的值
rating INTEGER DEFAULT 5

-- 函数：每一行在插入时获得一个新的值
created_at TIMESTAMP DEFAULT NOW()
```

### 你的任务

为博客系统创建一个包含以下列的 `articles` 表：

1. `id` - 自增主键（使用 SERIAL）
2. `title` - 必填文本，最多 200 个字符
3. `status` - 文本，最多 20 个字符，默认值为 `'draft'`
4. `view_count` - 整数，默认值为 `0`
5. `created_at` - 时间戳，使用 `NOW()` 默认设置为当前时间

### 预期 Schema

```sql
CREATE TABLE articles (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    status VARCHAR(20) DEFAULT 'draft',
    view_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### 解答

```sql
-- 创建带有 DEFAULT 默认值的 articles 表
CREATE TABLE articles (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    status VARCHAR(20) DEFAULT 'draft',
    view_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);
```
