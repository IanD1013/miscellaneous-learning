### PostgreSQL 中的 ENUM 类型

ENUM 类型定义了一组静态且有序的值。
它们非常适合那些只应包含特定预定义值（例如状态、类别或优先级）的列。

### 创建 ENUM 类型

```sql
CREATE TYPE mood AS ENUM ('sad', 'neutral', 'happy');
CREATE TYPE priority AS ENUM ('low', 'medium', 'high', 'critical');
```

### 为什么使用 ENUM 类型？

- **类型安全**：只能存储有效的值
- **存储效率高**：无论值的长度如何，仅占用 4 字节
- **内置排序**：值按定义顺序排序，而不是按字母顺序
- **自文档化**：有效值在模式（schema）中已定义

### ENUM 排序

ENUM 值按照它们在定义中的位置排序，而不是按字母顺序：

```sql
CREATE TYPE size AS ENUM ('small', 'medium', 'large');

-- 根据定义顺序，'small' < 'medium' < 'large'
-- 这使得可以进行如下比较：WHERE size > 'small'
```

### 常见使用场景

| 使用场景 | 示例 ENUM |
| --- | --- |
| 订单状态 | 'pending', 'processing', 'shipped', 'delivered' |
| 优先级 | 'low', 'medium', 'high', 'critical' |
| 用户角色 | 'guest', 'member', 'admin' |
| 星期几 | 'monday', 'tuesday', ... 'sunday' |

### 你的任务

创建一个名为 `order_status` 的 ENUM 类型，并严格按以下顺序包含这些值：

1. `pending`
2. `processing`
3. `shipped`
4. `delivered`
5. `cancelled`

顺序非常重要，因为它决定了值之间相互比较的方式。

### 预期结果

```sql
CREATE TYPE order_status AS ENUM ('pending', 'processing', 'shipped', 'delivered', 'cancelled');
```

### 解答

```sql
-- 创建 order_status ENUM 类型
-- 值依次为：pending, processing, shipped, delivered, cancelled
CREATE TYPE order_status AS ENUM ('pending', 'processing', 'shipped', 'delivered', 'cancelled');
```
