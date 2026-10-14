### DROP INDEX

`DROP INDEX` 语句用于从数据库中删除索引。
虽然索引可以提升查询性能，但有时你仍需要将它们删除：

- 查询不再使用该索引
- 索引降低了写入操作（INSERT、UPDATE、DELETE）的性能
- 你需要使用不同的设置重新创建该索引
- 索引是误创建的

### 基本语法

```sql
DROP INDEX index_name;
```

### 使用 IF EXISTS

为了避免在索引不存在时报错：

```sql
DROP INDEX IF EXISTS index_name;
```

### DROP INDEX CONCURRENTLY

在生产数据库中，正常删除索引会在表上获取排他锁（exclusive lock），在操作完成之前阻塞所有读写操作。
`CONCURRENTLY` 选项允许其他操作继续进行：

```sql
DROP INDEX CONCURRENTLY index_name;
```

| 选项 | 锁级别 | 使用场景 |
| --- | --- | --- |
| 默认 | 排他（阻塞所有操作） | 开发环境、维护窗口 |
| CONCURRENTLY | 最小化锁定 | 生产环境、高流量表 |

**注意：** `CONCURRENTLY` 不能在事务块内使用，并且需要更长的时间来完成。

### 查看现有索引

在删除之前，你可以确认索引是否存在：

```sql
SELECT indexname, indexdef 
FROM pg_indexes 
WHERE tablename = 'products';
```

### 你的任务

`products` 表中有一个名为 `idx_products_category` 的索引，该索引已不再需要。
请使用 `IF EXISTS` 子句安全地删除此索引，以防在索引不存在时报错。

### 预期语句

```sql
DROP INDEX IF EXISTS idx_products_category;
```

### 解答

```sql
-- 安全地删除 idx_products_category 索引
-- 使用 IF EXISTS 防止索引不存在时报错
DROP INDEX IF EXISTS idx_products_category;
```
