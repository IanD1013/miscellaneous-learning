### FOREIGN KEY 约束

`FOREIGN KEY` 约束通过引用另一个表的 PRIMARY KEY 在两个表之间建立关联。
这强制执行了**引用完整性**（referential integrity），确保表之间的关系保持有效。

### 基本语法

```sql
CREATE TABLE child_table (
    id SERIAL PRIMARY KEY,
    parent_id INTEGER REFERENCES parent_table(id)
);

-- 或者使用显式的 FOREIGN KEY 语法：
CREATE TABLE child_table (
    id SERIAL PRIMARY KEY,
    parent_id INTEGER,
    FOREIGN KEY (parent_id) REFERENCES parent_table(id)
);
```

### 引用完整性

外键通过确保以下几点来防止孤立记录（orphan records）：

- 你不能插入一个 `parent_id` 在父表中不存在的子行
- 如果有子行引用了父行，则不能删除该父行（默认情况下）

```sql
-- 如果 customer_id 999 在 customers 表中不存在，这将执行失败：
INSERT INTO orders (customer_id, total) VALUES (999, 50.00);
```

### ON DELETE 动作

控制当父行被删除时子行发生的操作：

| 动作 | 行为 |
| --- | --- |
| `NO ACTION` | 默认值。如果存在子行，则阻止删除 |
| `RESTRICT` | 与 NO ACTION 相同，立即进行检查 |
| `CASCADE` | 自动删除所有关联的子行 |
| `SET NULL` | 将外键列设置为 NULL |
| `SET DEFAULT` | 将外键列设置为其默认值 |

```sql
-- CASCADE：删除客户的同时也会删除他们的订单
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(id) ON DELETE CASCADE
);

-- SET NULL：订单保留，但 customer_id 变为 NULL
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(id) ON DELETE SET NULL
);
```

### ON UPDATE 动作

`ON UPDATE` 也提供相同的动作，用于控制当父表的主键发生变化时的行为：

```sql
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(id) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE
);
```

### 你的任务

创建一个具有以下规范的 `orders` 表：

- `id` 为 SERIAL PRIMARY KEY
- `customer_id` 为 INTEGER，引用 `customers` 表，并在删除时使用 CASCADE（级联删除）
- `order_date` 为 DATE，带有 NOT NULL 约束
- `total_amount` 为 NUMERIC(10,2)，带有 NOT NULL 约束

CASCADE 删除动作意味着当一个客户被删除时，其所有的订单都会被自动移除。

### 列要求

| 列 | 类型 | 约束 |
| --- | --- | --- |
| id | SERIAL | PRIMARY KEY |
| customer\_id | INTEGER | 关联 customers 的外键，级联删除（cascade on delete） |
| order\_date | DATE | NOT NULL |
| total\_amount | NUMERIC(10,2) | NOT NULL |

### 解答

```sql
-- 创建带有指向 customers 外键的 orders 表
-- 使用 ON DELETE CASCADE，使客户被删除时其订单也被删除

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(id) ON DELETE CASCADE,
    order_date DATE NOT NULL,
    total_amount NUMERIC(10,2) NOT NULL
);
```
