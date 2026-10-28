数组的 `shape` 记录了沿每个维度的元素数量。
一维（扁平）数组只有一个维度；将其重塑为行则会给它两个维度。
`reshape` 在保持元素内容和顺序不变的同时改变其排列结构。

```python
import numpy as np

flat = np.array([8, 3, 6, 1], dtype=float)
rows = flat.reshape((2, 2))
```

这里的 `flat.shape` 是 `(4,)`，这是一个单元素元组，其末尾的逗号用于将其与带括号的普通数字区分开来。
`rows.shape` 是 `(2, 2)`：两行，每行包含两个值。
`reshape((2, 2))` 中的内层括号将请求的维度组合为一个元组；外层括号用于调用该方法。
两个数组的 `size` 都等于 `4`。
读取 `.shape` 和 `.size` 时无需调用它们：它们是属性，而不是方法。

我们熟知的 `np.array(..., dtype=float)` 用于提供浮点元素，而 `rows.tolist()` 则将结果转换为普通的 Python 嵌套列表。
重塑操作既不会填充也不会丢弃元素。
请求维度的乘积必须等于原始的 `size`。
对于扁平输入和所选的宽度，`len(values) % width` 可用于检查是否有余数；只有余数为零时才允许拆分为 `len(values) // width` 个完整的行。
在进行上述任一计算之前先验证宽度，以避免零作为除数。

空输入仍然具有有效的形状。
当宽度为 `3` 时，请求 `(0, 3)`：0 行 3 列使用 0 个元素。
其 `.tolist()` 的结果是 `[]`。

对于宽度检查，`isinstance(width, int)` 也会接受布尔值，因为 Python 将 `bool` 视为 `int` 的子类。
可以使用 `isinstance(width, bool)` 排除它们。
像 `2.0` 这样的浮点数即使其值是整数，它仍然是浮点数；不要将其转换为整数以使其通过验证。
提供的 `_whole_float_width()` 是一个已完成的调用方示例，它会将 `2.0` 传递给你的函数。
你只需实现 `reshape_rows`。

在调用 `.tolist()` 之后，使用普通的循环和 `append` 构建清洗后的行。
写入这些输出行可以避免对调用方的列表进行就地修改。

### 重塑为行

使用 NumPy 数组和 `reshape` 完成 `reshape_rows(values, width)`。

- 除非 `values` 是一个由有限整数或浮点数组成的列表，否则返回 `None`。
  拒绝布尔元素。
  复用数组创建时的数值检查：`float("inf")` 表示正无穷，而 `-float("inf") < value < float("inf")` 仅接受有限数值。
- 要求 `width` 必须是 `1` 到 `100`（含两端）之间的整数。
  拒绝将布尔值、字符串和浮点数作为宽度，即使该浮点数的值为整数。
- 当输入长度不能被宽度整除时，返回 `None`。
  即使对于空列表，也要验证这些条件。
- 返回包含浮点数的普通行列表，保持输入顺序。
  保留有限浮点数值且不进行四舍五入；将带符号的零（无论是正零还是负零）统一替换为 `0.0`。

### 解答

```python
import numpy as np

def reshape_rows(values, width):
    if not isinstance(values, list):
        return None
    for value in values:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            return None
        if not -float("inf") < value < float("inf"):
            return None
    if isinstance(width, bool) or not isinstance(width, int):
        return None
    if width < 1 or width > 100:
        return None
    if len(values) % width != 0:
        return None
    array = np.array(values, dtype=float).reshape(-1, width)
    rows = []
    for row in array.tolist():
        cleaned = []
        for value in row:
            if value == 0:
                value = 0.0
            cleaned.append(value)
        rows.append(cleaned)
    return rows

def _whole_float_width():
    return reshape_rows([], 2.0)
```
