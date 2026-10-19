### SQLite 中的 PRAGMA journal\_mode

SQLite 使用日志机制来确保事务期间的数据完整性。
如果数据库进程在写入过程中崩溃，日志可以帮助 SQLite 恢复到一致状态。
`PRAGMA journal_mode` 命令允许你控制 SQLite **如何**管理该日志，这对性能和并发性有着重大影响。

### 工作原理

当 SQLite 写入数据时，它需要一种策略来处理未完成的事务。
日志模式决定了该策略：

| 模式 | 行为 |
| --- | --- |
| `DELETE` | 默认模式。在每次事务之前创建一个回滚日志文件，提交时将其删除。安全但存在文件创建/删除的开销。 |
| `TRUNCATE` | 类似于 DELETE，但会将日志文件截断为零长度而不是删除它。在某些文件系统上速度更快。 |
| `PERSIST` | 保留日志文件，但在提交时用零覆盖其头部。避免了删除和截断的开销。 |
| `MEMORY` | 将回滚日志存储在 RAM 中。速度快，但在事务期间发生崩溃可能会损坏数据库。 |
| `WAL` | **Write-Ahead Logging（预写日志）**。WAL 不直接将更改写入数据库文件并记录原始内容，而是将更改追加到单独的 WAL 文件中。原始数据库文件在检查点之前保持不变。 |
| `OFF` | 完全禁用日志记录。速度最快，但没有崩溃恢复能力，写入过程中的断电可能会永久损坏数据库。 |

### 为什么 WAL 很重要

WAL 模式是默认 DELETE 模式的最重要替代方案，因为它支持**并发读取器和单个写入器**而互不阻塞。
在 DELETE 模式下，写入器在事务期间会锁定所有读取器。
在 WAL 模式下，即使正在进行写入，读取器也能看到数据库的一致快照。
这使得 WAL 成为大多数多线程或多进程应用程序的首选模式。

### 语法

```sql
-- 查询当前的日志模式
PRAGMA journal_mode;

-- 设置日志模式
PRAGMA journal_mode = WAL;
PRAGMA journal_mode = DELETE;
PRAGMA journal_mode = MEMORY;
```

当你**设置**日志模式时，SQLite 会返回实际应用的模式。
这很重要，某些模式在特定环境中可能不可用，返回的值可以确认实际生效的内容。

### 示例

```sql
-- 检查我们当前使用的模式
PRAGMA journal_mode;
-- 返回：| journal_mode |
--       | delete       |

-- 切换到 MEMORY 模式以进行快速临时工作
PRAGMA journal_mode = MEMORY;
-- 返回：| journal_mode |
--       | memory       |

-- 切换到 TRUNCATE 以获得比 DELETE 稍高的性能提升
PRAGMA journal_mode = TRUNCATE;
-- 返回：| journal_mode |
--       | truncate     |
```

请注意，无论你如何输入命令，返回的值始终是**小写**字符串。

### 重要提示

- `PRAGMA journal_mode` 返回一个结果集，其中包含名为 `journal_mode` 的单个列以及包含小写模式名称的单行。
- 当你**设置**日志模式时，返回值会确认已应用的模式 - 这既充当了设置操作，又充当了确认操作。
- 在此基于浏览器的练习环境中，你可以设置和查询日志模式，但实际效果（文件 I/O 行为、并发访问模式）与基于文件的 SQLite 数据库有所不同。
- 在基于文件的 SQLite 中，WAL 模式在数据库连接之间是持久的 - 一旦设置，它将保持不变，直到被显式更改。

### 你的任务

编写一条 SQL 语句将日志模式设置为 `wal`。
该语句应返回一个结果集，以确认日志模式已设置。
请记住，SQLite 会在名为 `journal_mode` 的列中以小写字符串形式返回应用的模式。

### 解答

```sql
-- 将日志模式设置为 WAL，SQLite 会在 journal_mode 列中返回 'wal' 作为确认
PRAGMA journal_mode = WAL;
```
