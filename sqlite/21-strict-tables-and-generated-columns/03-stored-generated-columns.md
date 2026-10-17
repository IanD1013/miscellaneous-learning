### SQLite 中的存储生成列

从 SQLite 3.31.0 开始，你可以定义其值根据同行中其他列自动计算得出的列。
**存储生成列**（stored generated column）会在插入或更新数据时进行计算，并像普通列一样物理保存到磁盘上。
这非常适合用于对计算值进行反范式化处理，而无需担心它们与源数据不同步。

### 工作原理

当你定义一个生成列时，每当插入或更新一行时，SQLite 都会计算你提供的表达式。
使用 `STORED` 关键字时，计算结果将与其它列一起写入磁盘。
你无需手动为生成列提供值 - SQLite 会全权处理。
如果你尝试显式插入或更新生成列，SQLite 将会报错。

**存储**生成列与**虚拟**生成列之间的主要区别在于：

- **STORED**：在写入时计算，保存到磁盘，可以创建索引
- **VIRTUAL**：在读取时计算，不保存到磁盘（如果省略该关键字，则为默认行为）

### 语法

```sql
CREATE TABLE table_name (
    column1 TYPE,
    column2 TYPE,
    computed_column TYPE GENERATED ALWAYS AS (expression) STORED
);
```

表达式可以引用同一张表中的任何非生成列。
它不能引用其他表、使用子查询或调用像 `random()` 这样的非确定性函数。

### 示例

```sql
-- 跟踪矩形尺寸并自动计算面积的表
CREATE TABLE rectangles (
    id INTEGER PRIMARY KEY,
    width REAL NOT NULL,
    height REAL NOT NULL,
    area REAL GENERATED ALWAYS AS (width * height) STORED
);

INSERT INTO rectangles (width, height) VALUES (5.0, 3.0);
-- area 自动计算为 15.0 - 无需手动指定！

SELECT * FROM rectangles;
-- 返回: 1 | 5.0 | 3.0 | 15.0
```

```sql
-- 包含计算得出的全名（full name）的表
CREATE TABLE employees (
    id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    full_name TEXT GENERATED ALWAYS AS (first_name || ' ' || last_name) STORED
);

INSERT INTO employees (first_name, last_name) VALUES ('Grace', 'Hopper');
SELECT full_name FROM employees;
-- 返回: Grace Hopper
```

```sql
-- 计算折扣价格
CREATE TABLE promotions (
    id INTEGER PRIMARY KEY,
    original_price REAL NOT NULL,
    discount_pct REAL NOT NULL DEFAULT 0.0,
    final_price REAL GENERATED ALWAYS AS (original_price * (1.0 - discount_pct / 100.0)) STORED
);

INSERT INTO promotions (original_price, discount_pct) VALUES (100.0, 25.0);
SELECT final_price FROM promotions;
-- 返回: 75.0
```

### 重要细节

- 你**不能**直接插入或更新生成列 - 由 SQLite 进行管理
- 表达式必须是确定性的（相同的输入始终产生相同的输出）
- `PRAGMA table_info(table_name)` 可以显示列的元数据；生成列会显示其类型，其他方面与普通列一样列出
- 生成列可以参与索引，这是 `STORED` 相对于 `VIRTUAL` 的一个主要优势

### 你的任务

创建一个包含以下列的 `order_items` 表：

| 列名 | 类型 | 详情 |
| --- | --- | --- |
| `id` | INTEGER | PRIMARY KEY |
| `product_name` | TEXT | NOT NULL |
| `quantity` | INTEGER | NOT NULL |
| `unit_price` | REAL | NOT NULL |
| `total_price` | REAL | GENERATED ALWAYS AS (`quantity * unit_price`) STORED |

创建表之后，插入以下三行数据（**不要**为 `total_price` 提供值）：

| product\_name | quantity | unit\_price |
| --- | --- | --- |
| Widget | 3 | 9.99 |
| Gadget | 1 | 24.50 |
| Sprocket | 10 | 1.75 |

生成的 `total_price` 列应该会自动为每一行计算 `quantity * unit_price` 的结果。

### 预期结果

```makefile
Widget:    total_price = 29.97
Gadget:    total_price = 24.5
Sprocket:  total_price = 17.5
```

### 解答

```sql
-- 第 1 步：创建带有存储生成列的 order_items 表
CREATE TABLE order_items (
    id INTEGER PRIMARY KEY,
    product_name TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price REAL NOT NULL,
    total_price REAL GENERATED ALWAYS AS (quantity * unit_price) STORED
);

-- 第 2 步：插入三行（不要包含 total_price）
INSERT INTO order_items (product_name, quantity, unit_price)
VALUES
    ('Widget', 3, 9.99),
    ('Gadget', 1, 24.50),
    ('Sprocket', 10, 1.75);

-- 第 3 步：查询所有行以进行验证
SELECT * FROM order_items;
```
