### 结合 ORDER BY 和 LIMIT 进行 DELETE

在生产系统中，诸如日志、审计追踪和事件队列等表会持续增长。
你经常需要清理旧记录 - 但删除*全部*记录又过于激进。
如果你只想删除最旧的 100 行，或者优先级最低的 10 个项目该怎么办？

### 子查询模式

在 SQLite 中删除限定数量行的标准方法是使用带有 `rowid` 的子查询：

```sql
DELETE FROM table_name
WHERE rowid IN (
    SELECT rowid FROM table_name
    ORDER BY column_name ASC
    LIMIT count
);
```

它的工作原理如下：

1. 内部的 `SELECT` 查找要删除行的 `rowid` 值，并进行排序和数量限制
2. 外部的 `DELETE` 精确删除这些行
3. `rowid` 是每个 SQLite 表都具备的内置唯一标识符（除非是 WITHOUT ROWID 表）

> **注意：** 某些 SQLite 构建版本直接支持 `DELETE ... ORDER BY ... LIMIT`（当使用 `SQLITE_ENABLE_UPDATE_DELETE_LIMIT` 编译时），但它**并非在所有环境中都可用** - 包括此处使用的基于浏览器的 SQLite。
> 子查询模式在所有环境下均有效，是推荐的做法。

### 示例

```sql
-- 从库存中删除最便宜的 3 个产品
DELETE FROM products
WHERE rowid IN (
    SELECT rowid FROM products
    ORDER BY price ASC
    LIMIT 3
);

-- 删除最近的 10 个 error 级别事件
DELETE FROM events
WHERE rowid IN (
    SELECT rowid FROM events
    WHERE level = 'error'
    ORDER BY event_time DESC
    LIMIT 10
);

-- 删除运行时间最长的单个任务
DELETE FROM tasks
WHERE rowid IN (
    SELECT rowid FROM tasks
    ORDER BY duration DESC
    LIMIT 1
);
```

请注意内部 SELECT 是如何使用 ORDER BY 和 LIMIT 精确识别目标行，以及外部 DELETE 是如何将其删除的。

### 常见模式

| 模式 | 使用场景 |
| --- | --- |
| `ORDER BY created_at ASC LIMIT N` | 删除 N 条最旧的记录 |
| `ORDER BY created_at DESC LIMIT N` | 删除 N 条最新的记录 |
| `ORDER BY priority ASC LIMIT N` | 删除 N 个优先级最低的项目 |
| `WHERE status = 'done' ORDER BY finished_at ASC LIMIT N` | 清理 N 条最旧的已完成记录 |

### 实用参考

| 关键字 | 描述 |
| --- | --- |
| `DELETE FROM` | 指定要从中删除行的表 |
| `WHERE rowid IN (SELECT ...)` | 定位子查询所识别的特定行 |
| `ORDER BY ... ASC` | 升序排列（最小/最旧排在最前） |
| `ORDER BY ... DESC` | 降序排列（最大/最新排在最前） |
| `LIMIT N` | 将子查询限制为最多 N 行 |

### 你的任务

你有一个 `logs` 表，其中存储了带有时间戳的应用程序日志消息。
随着时间的推移，该表已累积了 10 条日志记录。
你的任务是从表中**删除 5 条最旧的日志记录**，仅保留最新的 5 条记录。

使用带有 `rowid IN (SELECT ...)` 子查询的 `DELETE` 语句，在单个语句中完成此操作。

### 预期结果

在你的语句执行后，`logs` 表应恰好包含 **5 行** - 即最新的 5 条记录。

### 解答

```sql
-- 从 logs 表中删除 5 条最旧的日志记录
-- 提示：使用 WHERE rowid IN (SELECT rowid FROM ... ORDER BY ... LIMIT ...)
DELETE FROM logs
WHERE rowid IN (
    SELECT rowid FROM logs
    ORDER BY created_at ASC
    LIMIT 5
);
```
