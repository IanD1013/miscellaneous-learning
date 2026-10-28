归一化一个数值行可以在保持其方向的同时，使其模（或长度）等于 1。
行的模是其各个分量平方和的平方根。
将每个分量除以该模即可得到一个单位行。
零向量的所有分量均为零，模也为零，因此需要单独处理以避免除以零。

对于一维数组，使用提供的导入别名编写的 `numpy.linalg.norm`（即 `np.linalg.norm`）可以计算该模。
首先对行进行缩放：直接平方原始分量可能会导致极小值丢失变为零，或者使极大值溢出。
除以绝对值最大的分量可以将缩放后的分量保持在 -1 到 1 之间，同时不会改变方向。

```python
row = [2.0, -2.0]
scale = 0.0
for value in row:
    scale = max(scale, abs(value))
scaled = []
for value in row:
    scaled.append(value / scale)
array = np.array(scaled, dtype=float)
magnitude = np.linalg.norm(array).tolist()
unit_row = (array / magnitude).tolist()
```

`abs(value)` 在计算缩放比例时去除了符号：`abs(-2.0)` 为 `2.0`。
`max(scale, abs(value))` 会选择两个参数中的较大者，因此该循环会找到绝对值最大的分量。
在这里，缩放后的行为 `[1.0, -1.0]`，其模约为 `1.414214`，其单位分量约为 `0.707107` 和 `-0.707107`。
数组除法会将除数应用于每个分量。
`.tolist()` 将 NumPy 的模转换为普通标量，并将最终数组转换为普通列表。
对于零行，`scale` 保持为零；跳过两次除法并直接生成零即可。

在进行算术运算之前，复用数组创建时的有限数检查：接受 `int` 或 `float`，拒绝 `bool`，并要求 `-float("inf") < value < float("inf")`。
使用 `append` 构建单独的输出列表；直接就地修改分量也会改变调用者的行。

### 你的任务

通过逐行缩放和 `np.linalg.norm` 来完成 `normalize_rows(rows)` 作为练习。
使用普通循环和 `append` 来构建列表。

- 接受一个列表的列表，其具有相等且为正的行宽，并且分量为有限整数或浮点数。
  对于布尔值、其他分量类型、非列表行、非列表的外层输入、不规则行（长短不一的行）以及宽度为零的行，通过返回 `None` 来拒绝。
- 外层列表为空时返回 `[]`。
  在计算任何行之前，先验证完整输入。
- 归一化每个非零行，包括极小和极大的有限值。
  将零行保持为 `0.0` 的列表。
- 按原始行和分量顺序返回普通列表。
- 对每个归一化后的分量应用内置的 `round(value, 6)`。
  如果四舍五入后的值等于零，则追加 `0.0`，以确保结果中绝不包含 `-0.0`。
  保留六位小数是四舍五入规则，并不要求显示末尾的零。

### 解答

```python
import numpy as np

def normalize_rows(rows):
    if not isinstance(rows, list):
        return None
    for row in rows:
        if not isinstance(row, list) or len(row) == 0 or len(row) != len(rows[0]):
            return None
        for value in row:
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                return None
            if not -float("inf") < value < float("inf"):
                return None
    result = []
    for row in rows:
        scale = 0.0
        for value in row:
            scale = max(scale, abs(value))
        if scale == 0:
            result.append([0.0] * len(row))
            continue
        scaled = []
        for value in row:
            scaled.append(value / scale)
        array = np.array(scaled, dtype=float)
        magnitude = np.linalg.norm(array).tolist()
        unit_row = []
        for value in (array / magnitude).tolist():
            value = round(value, 6)
            if value == 0:
                value = 0.0
            unit_row.append(value)
        result.append(unit_row)
    return result
```
