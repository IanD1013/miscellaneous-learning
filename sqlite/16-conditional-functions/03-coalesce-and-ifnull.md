### COALESCE 和 IFNULL - 处理 NULL 值

在现实世界的数据库中，列经常包含 NULL 值 - 客户可能没有提供电话号码，订单可能没有发货日期，或者产品可能缺少描述。
在构建报表或面向用户的查询时，你需要一些策略来用有意义的备用值替换 NULL。
这正是 `COALESCE` 和 `IFNULL` 的用武之地。

### 工作原理

**COALESCE** 接受两个或更多参数，并从左到右返回**第一个非 NULL** 的值。
如果所有参数都是 NULL，它将返回 NULL。
可以把它想象成在检查一条备选方案链：尝试第一个选择，如果为空则尝试第二个，然后是第三个，依此类推。

**IFNULL** 是 SQLite 特有的简写形式，工作方式类似于 `COALESCE`，但**仅接受两个**参数。
如果第一个参数不是 NULL，则返回第一个参数；否则返回第二个参数。

### 语法

```sql
-- COALESCE：从任意数量的参数中返回第一个非 NULL 值
COALESCE(value1, value2, value3, ..., fallback)

-- IFNULL：SQLite 中恰好接受两个参数的简写形式
IFNULL(value, fallback)
```

### 示例

考虑一个包含 `sale_price`、`retail_price` 和 `list_price` 列的 `products` 表：

```sql
-- 如果有 sale_price 则使用它，否则使用 retail_price，再否则使用 list_price
SELECT product_name,
       COALESCE(sale_price, retail_price, list_price) AS display_price
FROM products;

-- 用默认字符串替换 NULL 描述
SELECT product_name,
       IFNULL(description, 'No description available') AS description
FROM products;

-- 在末尾结合一个字面量备用值
SELECT employee_name,
       COALESCE(nickname, first_name, 'Unknown') AS display_name
FROM employees;
```

### 求值顺序

COALESCE **严格从左到右**对参数求值，并在遇到第一个非 NULL 值时停止：

| 参数 | 结果 |
| --- | --- |
| `COALESCE(NULL, 'B', 'C')` | `B` |
| `COALESCE('A', 'B', 'C')` | `A` |
| `COALESCE(NULL, NULL, 'C')` | `C` |
| `COALESCE(NULL, NULL, NULL)` | `NULL` |

### IFNULL 与 COALESCE

| 特性 | COALESCE | IFNULL |
| --- | --- | --- |
| SQL 标准 | 是 (ANSI SQL) | SQLite 特有 |
| 参数数量 | 2 个或更多 | 正好 2 个 |
| 行为 | 第一个非 NULL 值 | 第一个非 NULL 值 |

当你需要检查多个备选列时，请使用 `COALESCE`。
当你只需要单个备用值时，请使用 `IFNULL` - 它稍微更简洁一些，但在功能上与两个参数的 `COALESCE` 完全相同。

### 你的任务

你有一个 `contacts` 表，其中的联系人可能提供或未提供其手机号码、电话号码或电子邮件地址。
编写一个查询，选择每位联系人的 `name` 及其**最佳可用联系方式**。

联系某人的优先级顺序应为：

1. `mobile`（最优先）
2. `phone`
3. `email`
4. 如果以上都不存在，请使用字面量字符串 `No contact info`

将结果列别名命名为 `best_contact`。
按 `name` 升序对结果进行排序。

### 预期结果

```sql
name          | best_contact
--------------|-----------------
Alice Chen    | 555-0101
Bob Martinez  | bob@example.com
Carla Smith   | 555-9999
Diana Park    | 555-0202
Evan Brooks   | No contact info
```

### 解答

```sql
-- 选择每位联系人的姓名及其最佳可用联系方式
-- 优先级：mobile > phone > email > 'No contact info'
-- 将该列别名为 best_contact，并按 name 排序
SELECT
  name,
  COALESCE(mobile, phone, email, 'No contact info') AS best_contact
FROM contacts
ORDER BY name ASC;
```
