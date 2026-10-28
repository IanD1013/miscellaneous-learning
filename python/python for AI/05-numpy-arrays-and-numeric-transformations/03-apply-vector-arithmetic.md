NumPy 算术运算会将操作应用于数组中的每个元素。
一维数值数组即向量：一个有序的数字序列。
乘法会缩放每个数字，而加法则会平移每个数字：

```python
import numpy as np

array = np.array([3, -1], dtype=float)
changed = array * 2 + 4
```

`changed.tolist()` 生成 `[10.0, 2.0]`。
乘法先于加法执行。
单个数字 `2` 和 `4` 是标量。
NumPy 使用广播机制（broadcasting）将每个标量应用于每个位置，而无需创建额外的维度。
此计算保留了数组的形状和顺序；空数组仍保持为空。
标量参数允许调用者为整个向量选择相同的缩放和平移量。

在构建数组之前验证输入，对列表元素和标量系数复用数组创建时的有限数检查。
`abs(value)` 可获取数值的大小（绝对值），因此 `abs(value) > 1000` 可以检测是否超出了任一边界。
即使列表为空，也要检查 `factor` 和 `offset`。
使用 `np.array(values, dtype=float)` 构建一个独立的数组，并根据其计算值构建返回的列表；覆盖原始列表中的元素会修改调用者的数据。

使用 `.tolist()` 转换计算后的数组，然后使用循环对每个浮点数应用 Python 内置的 `round(value, 6)`。
它的第二个参数指定保留六位小数；它不会生成格式化文本。
将任何舍入后的零替换为 `0.0`，以避免微小的负数保留为 `-0.0`。

### 缩放和平移列表

使用数组算术运算完成 `scale_values(values, factor, offset)`。

- 要求 `values` 必须是包含有限整数或浮点数的列表。
  要求 `factor` 和 `offset` 必须是有限数值标量。
  拒绝布尔值，包括列表内部的布尔值。
- 每个输入的数字必须在 `-1000` 到 `1000` 之间（包含边界）。
  对于任何无效输入，返回 `None`。
- 计算每个值乘以 `factor`，再加上 `offset`。
  计算得到的结果值可能会超出输入范围边界。
- 按输入顺序返回一个普通的浮点数列表，并按上述规则进行舍入。
  如果列表为空且标量有效，返回 `[]`。

### 解答

```python
import numpy as np

def _is_valid_number(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return False
    if not -float("inf") < value < float("inf"):
        return False
    return abs(value) <= 1000

def scale_values(values, factor, offset):
    if not isinstance(values, list):
        return None
    for value in values:
        if not _is_valid_number(value):
            return None
    if not _is_valid_number(factor) or not _is_valid_number(offset):
        return None
    array = np.array(values, dtype=float)
    changed = array * factor + offset
    result = []
    for value in changed.tolist():
        value = round(value, 6)
        if value == 0:
            value = 0.0
        result.append(value)
    return result
```
