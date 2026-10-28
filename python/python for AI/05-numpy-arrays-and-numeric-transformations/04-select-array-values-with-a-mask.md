数组比较会分别检查每个元素。
其结果是一个布尔掩码（boolean mask）：一个由 `True` 和 `False` 组成的数组，用于标记保留哪些位置。

```python
array = np.array([1, 6, 4], dtype=float)
mask = array > 3
selected = array[mask]
selected.tolist()
```

这里的 `mask` 包含 `[False, True, True]`。
标量 `3` 会与每个元素进行比较，因此掩码的长度与 `array` 相同。
在 `array[mask]` 中，方括号会选出对应掩码位置为 `True` 的元素。
结果包含按原始顺序排列的 `[6.0, 4.0]`。
`.tolist()` 将该选出的数组转换为普通的 Python 列表。
与 `if` 条件中的单次比较不同，此比较会针对每个位置生成一个判断。

复用数组创建时的数值验证逻辑：在转换前检查是否为 `int` 或 `float`，排除 `bool`，并应用 `-float("inf") < value < float("inf")`。
列表元素和阈值都需要检查。
NumPy 可以转换像 `"2"` 这样的数字字符串，因此仅仅完成转换并不能验证原始输入的有效性。

请基于选出的数组构建结果，而不是从调用者的列表中删除元素。
就地（in place）删除元素会更改调用者可能仍需要使用的数据。

### 筛选大于阈值的元素

使用 NumPy 比较和掩码索引完成 `select_above(values, threshold)`。

- 接收一个由有限整数或浮点数组成的列表以及一个有限数值阈值。
  对于任何其他容器、无效元素或无效阈值，返回 `None`。
  在此处布尔值属于无效数字。
- 仅保留严格大于 `threshold` 的值。
  不包含等于的情况。
  保留输入顺序以及每个符合条件的重复项。
- 返回一个普通的浮点数列表。
  输入为空或没有符合条件的值时返回 `[]`。
- 保留有限浮点数值且不进行四舍五入，包括极小的非零值。
  将筛选出的所有零归一化为 `0.0`：将选出的值复制到返回列表中时，如果值等于零则追加 `0.0`，否则追加原值。

### 解答

```python
import numpy as np

def _is_finite_number(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return False
    return -float("inf") < value < float("inf")

def select_above(values, threshold):
    if not isinstance(values, list) or not _is_finite_number(threshold):
        return None
    for value in values:
        if not _is_finite_number(value):
            return None
    array = np.array(values, dtype=float)
    selected = array[array > threshold]
    result = []
    for value in selected.tolist():
        if value == 0:
            result.append(0.0)
        else:
            result.append(value)
    return result
```
