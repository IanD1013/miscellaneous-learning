### CROSS JOIN

CROSS JOIN 会生成两个表的笛卡尔积（Cartesian product），即将第一个表中的每一行与第二个表中的每一行进行组合。
与其他 JOIN 不同，它不需要匹配条件。

### 何时使用 CROSS JOIN

当需要生成所有可能的组合时，CROSS JOIN 非常有用：

- 产品变体（尺寸 × 颜色）
- 排班组合（员工 × 班次）
- 测试数据生成
- 矩阵样式报告

### 基本语法

```sql
-- 显式 CROSS JOIN 语法
SELECT *
FROM table1
CROSS JOIN table2;

-- 隐式语法（逗号写法）
SELECT *
FROM table1, table2;
```

### 理解笛卡尔积

如果表 A 有 3 行，表 B 有 4 行，则 CROSS JOIN 会生成 3 × 4 = 12 行。

```sql
-- 示例：尺寸和颜色的所有组合
SELECT sizes.name, colors.name
FROM sizes
CROSS JOIN colors;
```

| 结果行数计算公式 |
| --- |
| rows\_table1 × rows\_table2 |

### 你的任务

你正在构建一个产品目录系统。
请为产品变体生成所有可能的尺寸与颜色组合。

编写一个查询，返回：

- `size_name`：来自 sizes 表的尺寸名称
- `color_name`：来自 colors 表的颜色名称

返回所有可能的组合，以便目录显示每个变体选项。

### 预期输出列

| size\_name | color\_name |
| --- | --- |
| Small | Red |
| Small | Blue |
| ... | ... |

### 解答

```sql
-- 生成所有尺寸与颜色的组合
-- 使用 CROSS JOIN 创建笛卡尔积
SELECT 
    sizes.name AS size_name,
    colors.name AS color_name
FROM sizes
CROSS JOIN colors;
```
