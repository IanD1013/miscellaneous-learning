### DROP TABLE - 安全删除表

随着数据库的发展，你经常需要删除不再需要的表 - 可能是在迁移、清理脚本期间，或在重构模式（schema）时。
`DROP TABLE` 语句会永久删除表及其所有数据。
但是，尝试删除不存在的表会导致错误，从而可能中断迁移脚本或自动化工作流。
这就是 `IF EXISTS` 变得必不可少的原因。

### 工作原理

当你执行 `DROP TABLE table_name` 时，SQLite 会查找具有该确切名称的表。
如果找到，它将从数据库中移除表定义和所有行。
如果该表不存在，SQLite 会引发错误且语句执行失败。

添加 `IF EXISTS` 使该操作成为**条件性的** - SQLite 会首先检查表是否存在。
如果存在，则删除该表。
如果不存在，语句将静默成功且不报错。
这使得你的 DDL 脚本具有**幂等性**，意味着你可以多次运行它们而不会失败。

### 语法

```sql
-- 基本的 DROP TABLE（表不存在时会报错）
DROP TABLE table_name;

-- 安全的 DROP TABLE（表不存在时不会报错）
DROP TABLE IF EXISTS table_name;
```

### 示例

```sql
-- 安全地删除一个临时日志表
DROP TABLE IF EXISTS temp_logs;

-- 删除一个可能已被移除的旧归档表
DROP TABLE IF EXISTS orders_archive_2020;

-- 在迁移脚本中，重新创建前先清理
DROP TABLE IF EXISTS user_sessions;
CREATE TABLE user_sessions (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    token TEXT NOT NULL
);
```

### 重要提示

- `DROP TABLE` 是**不可逆的** - 表中的所有数据将被永久删除
- 在 SQLite 中，引用已删除表的外键约束不会自动清理
- 你可以通过查询 `sqlite_master` 来验证表是否存在：

```sql
-- 检查数据库中是否存在某个表
SELECT COUNT(*) as count
FROM sqlite_master
WHERE type = 'table' AND name = 'my_table';
-- 存在时返回 count = 1，不存在时返回 count = 0
```

### 常见使用场景

| 场景 | 为什么 IF EXISTS 有所帮助 |
| --- | --- |
| 数据库迁移 | 脚本可以安全地重新运行 |
| 测试设置/清理（teardown） | 在每次测试运行前提供干净的环境 |
| 功能移除 | 无需预先检查即可删除特定于功能的表 |
| 模式版本控制 | 安全删除已弃用的表 |

### 你的任务

数据库中包含一个不再需要的名为 `legacy_audit_log` 的表。
请编写一条语句，使用 `IF EXISTS` **安全删除**该表，以便即使该表已被移除，该语句也不会失败。

### 预期行为

- 运行语句后，`legacy_audit_log` 表应不再存在
- 即使多次执行，该语句也不应产生错误

### 解答

```sql
-- 安全地删除 legacy_audit_log 表
DROP TABLE IF EXISTS legacy_audit_log;
```
