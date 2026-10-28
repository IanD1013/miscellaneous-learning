`mean(axis=0)` 会对二维 NumPy 数组的行维度进行规约：它沿着每列向下合并数值，每列保留一个均值。
axis 就是被规约的维度。

```python
array = np.array([[2, 6], [4, 10]], dtype=float)
columns = array.mean(axis=0).tolist()
rows = array.mean(axis=1).tolist()
```

`columns` 的值为 `[3.0, 8.0]`：第一个均值使用 2 和 4 计算得出，第二个均值使用 6 和 10 计算得出。
`rows` 的值为 `[4.0, 7.0]`：`axis=1` 会合并每一行内的各个位置。
`axis=` 关键字用于选择该维度；它并不是用来选择特定的行或列。
如果不带 axis 参数，`mean()` 会将所有元素合并为一个单一数值。
`sum(axis=0)` 使用相同的按列分组方式，但只将数值相加而不除以元素个数。

在创建数组之前检查嵌套列表。
空的外层列表没有可以计算平均值的行，因此要在规约前进行处理。
包含空行的列表属于不同的形状，在此处视为无效。

对于每个数值分量，`abs(value)` 可以获取其绝对值大小，因此 `abs(value) > 1000` 可以检测出无论正负是否超出了本练习的限制。
为了检查数值的有限性，`-float("inf") < value < float("inf")` 要求该值严格介于负无穷和正无穷之间；这也会排除 NaN。
请先检查类型并排除布尔值。

### 实现 column\_means

在不修改输入的前提下完成 `column_means(rows)`：

- 要求外层为列表。
  当其为空时返回 `[]`。
- 否则，要求包含长度相等的非空行列表。
  每个分量必须是有限的 `int` 或 `float`（排除 `bool`），且绝对值大小最多为 1000。
  此界限属于本练习的限制。
  对于任何无效输入，返回 `None`。
- 练习使用 `mean(axis=0)` 进行规约，并按列顺序返回一个普通列表。
  使用 `.tolist()` 转换规约结果，然后通过循环对每个浮点型均值应用 Python 内置的 `round(value, 6)`。
  第二个参数指定保留六位小数。
  当四舍五入后的值等于零时（包括负零），返回 `0.0`。

### 解答

```python
import numpy as np

def column_means(rows):
    if not isinstance(rows, list):
        return None
    if len(rows) == 0:
        return []
    for row in rows:
        if not isinstance(row, list) or len(row) == 0 or len(row) != len(rows[0]):
            return None
        for value in row:
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                return None
            if not -float("inf") < value < float("inf") or abs(value) > 1000:
                return None
    means = np.array(rows, dtype=float).mean(axis=0).tolist()
    result = []
    for value in means:
        value = round(value, 6)
        if value == 0:
            value = 0.0
        result.append(value)
    return result
```
