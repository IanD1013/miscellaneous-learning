### SQLite 中的整除与取模运算符

在 SQL 中处理数值数据时，你经常需要将数值分组、检测特定模式或均匀分配项目。
SQLite 的整除和取模（`%`）运算符是完成这些任务的基本工具 - 从对结果进行分页到将记录分类到各个桶（bucket）中。

### 工作原理

SQLite 遵循一个简单的规则：**当除法的两个操作数都是整数时，结果也是一个整数**，且小数部分会被截断（而不是四舍五入）。
对于正数，这有时被称为“向下取整除法”（floor division）。

取模运算符 `%` 返回整除后的**余数**。
将除法和取模结合起来可以得到完整的计算关系：

- `dividend = (quotient × divisor) + remainder`
- `17 / 5` → `3`（不是 3.4 - 小数部分被丢弃）
- `17 % 5` → `2`（因为 17 - (3 × 5) = 2）

这种截断行为非常重要：`7 / 4` 的结果是 `1`，而不是 `2`。
结果始终**向零截断**，因此 `-7 / 4` 的结果是 `-1`（而不是 -2）。

### 语法

```sql
-- 整除
SELECT a / b FROM some_table;

-- 取模（余数）
SELECT a % b FROM some_table;

-- 两者一起使用
SELECT a / b AS quotient, a % b AS remainder FROM some_table;
```

### 示例

```sql
-- 将 23 个项目按每组 5 个进行分配
SELECT 23 / 5 AS full_groups, 23 % 5 AS leftover;
-- 结果：full_groups = 4, leftover = 3

-- 检查一个数是否为偶数
SELECT 14 % 2 AS is_even_check;
-- 结果：0（表示 14 是偶数）

-- 将总分钟数转换为小时和分钟
SELECT total_minutes / 60 AS hours, total_minutes % 60 AS minutes
FROM activities;
-- 如果 total_minutes = 135 → hours = 2, minutes = 15

-- 负数的行为
SELECT -10 / 3 AS quotient, -10 % 3 AS remainder;
-- quotient = -3, remainder = -1
```

### 常见模式

| 模式 | 表达式 | 使用场景 |
| --- | --- | --- |
| 奇偶检查 | `value % 2` | 0 = 偶数，1 = 奇数 |
| 分组到桶 | `value / bucket_size` | 直方图分箱 |
| 循环分配 | `row_number % n` | 轮询分配（Round-robin） |
| 提取末位数 | `value % 10` | 获取数字的最后一位 |

### 你的任务

你有一个包含各种整数（包括零和负数）的 `numbers` 表，其中包含一列 `value`。
对于每个值，计算：

1. **quotient** - `value` 整除 `7` 的结果
2. **remainder** - `value` 除以 `7` 的余数

返回三列：`value`、`quotient` 和 `remainder`。
按 `value` 升序对结果进行排序。

### 预期结果

```markdown
value | quotient | remainder
------+----------+----------
  -10 |       -1 |        -3
    0 |        0 |         0
    3 |        0 |         3
    7 |        1 |         0
   15 |        2 |         1
   50 |        7 |         1
  100 |       14 |         2
```

### 解答

```sql
-- 对每个值，计算其除以 7 的商和余数
-- 返回列：value, quotient, remainder
-- 按 value 升序排序
SELECT
  value,
  value / 7 AS quotient,
  value % 7 AS remainder
FROM numbers
ORDER BY value ASC;
```
