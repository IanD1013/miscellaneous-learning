### PostgreSQL 中的连接算法 (Join Algorithms)

当 PostgreSQL 执行 JOIN 时，它会选择三种算法之一来合并来自多个表的数据行。
理解这些算法有助于你预测查询性能并优化慢连接。

### 三种连接算法

| 算法 | 适用场景 | 工作原理 |
| --- | --- | --- |
| Nested Loop | 小表、索引查找 | 针对外表的每一行，扫描内表 |
| Hash Join | 没有可用索引的大表 | 基于较小的表构建哈希表，使用较大的表进行探测 |
| Merge Join | 预排序数据、已建立索引的列 | 同时遍历两个已排序的输入 |

### Nested Loop Join

```sql
EXPLAIN SELECT * FROM small_table s
JOIN large_table l ON s.id = l.small_id;
-- 显示：Nested Loop
--        -> Seq Scan on small_table
--        -> Index Scan on large_table
```

当外表较小且内表的连接列上建有索引时，Nested Loop 非常高效。
它会遍历外表的每一行，并在内表中查找匹配的行。

### Hash Join

```sql
EXPLAIN SELECT * FROM orders o
JOIN order_items oi ON o.id = oi.order_id;
-- 显示：Hash Join
--        Hash Cond: (oi.order_id = o.id)
--        -> Seq Scan on order_items (probe)
--        -> Hash
--              -> Seq Scan on orders (build hash)
```

Hash Join 会基于较小的表在内存中构建哈希表（即“构建”阶段），然后扫描较大的表并探测哈希表以寻找匹配项（即“探测”阶段）。
对于没有可用索引的大表非常高效。

### Merge Join

```sql
EXPLAIN SELECT * FROM sorted_a a
JOIN sorted_b b ON a.key = b.key;
-- 显示：Merge Join
--        Merge Cond: (a.key = b.key)
--        -> Sort (or Index Scan if already sorted)
--        -> Sort (or Index Scan if already sorted)
```

Merge Join 要求两个输入都按连接键排序。
它同时遍历两个已排序的数据集，因此对于预先排序或带有索引的数据非常高效。

### 读取 EXPLAIN 输出

EXPLAIN 命令会返回一个基于文本的执行计划，包含 `QUERY PLAN` 列：

```sql
QUERY PLAN
------------------------------------------------------------
Hash Join  (cost=1.11..2.19 rows=7 width=98)
  Hash Cond: (o.customer_id = c.id)
  ->  Seq Scan on orders o  (cost=0.00..1.07 rows=7 width=78)
  ->  Hash  (cost=1.05..1.05 rows=5 width=24)
        ->  Seq Scan on customers c  (cost=0.00..1.05 rows=5 width=24)
```

第一行内容显示顶层操作，通常是连接算法（Hash Join、Nested Loop 或 Merge Join）。

### 你的任务

编写一条 EXPLAIN 语句来分析 `customers` 和 `orders` 表之间的连接。
你的查询应该展示 PostgreSQL 为该操作选择了哪种连接算法。

### 预期查询结构

```sql
EXPLAIN SELECT [columns]
FROM customers c
JOIN orders o ON [join condition];
```

### 观察重点

- 连接算法出现在计划的第一行（Hash Join、Nested Loop 或 Merge Join）
- `Hash Cond` 或 `Join Filter` 显示了连接条件
- 子节点显示了每个表的访问方式（Seq Scan、Index Scan 等）
- 对于类似这样的小型数据集，PostgreSQL 通常会选择 Hash Join

### 解答

```sql
-- 编写 EXPLAIN 语句分析 customers 和 orders 之间的连接
-- 选择客户姓名（c.name）和订单日期（o.order_date）
-- 通过 customer_id 外键进行连接
EXPLAIN SELECT c.name, o.order_date
FROM customers c
JOIN orders o ON c.id = o.customer_id;
```
