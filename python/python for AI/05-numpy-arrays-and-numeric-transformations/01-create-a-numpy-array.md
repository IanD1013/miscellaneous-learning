`numpy.array` 会创建一个所有元素共享同一种数据类型的数组。
Python 列表可以混合不同类型；对于数值计算，选择浮点型数组可以让诸如 `8` 这样的整数变为 `8.0`。

```python
import numpy as np

samples = np.array([8, 0.75], dtype=float)
plain_values = samples.tolist()
```

`as np` 为导入的 NumPy 模块赋予了更简短的名称 `np`；`np.array` 则调用了它的数组构造函数。
第一个参数提供数组的值。
`dtype` 代表数据类型（data type），关键字参数 `dtype=float` 指定了使用浮点型存储，即使所有输入都是整数也是如此。
如果不提供该参数，NumPy 会根据提供的值自行推断并选择类型。

`tolist()` 是在数组上调用的无参数方法。
在这里它会生成 `[8.0, 0.75]`：一个包含内置 Python 浮点数的普通 Python 列表，而不是 NumPy 数组或 NumPy 标量对象。

在构建数组之前请先进行验证。
`isinstance(value, (int, float))` 可以接受这两种数值类型之一；圆括号将允许的类型组合在一起。
请单独检查 `isinstance(value, bool)`，因为 Python 也会将布尔值视为整数。
NumPy 可以转换字符串和布尔值，但仅靠类型转换无法满足本任务的输入规则。

有限数（finite number）不包括正无穷、负无穷和 NaN（非数字）。
对于已经验证过的数值，请使用：

```python
finite = -float("inf") < value < float("inf")
```

`float("inf")` 会创建正无穷；前面的负号会创建负无穷。
链式比较要求两个不等式都成立。
对于任意无穷大或 NaN，该表达式都为 false。

为了安全构建，请独立于输入来构建结果。
直接替换输入列表中的元素会就地修改调用者的数据。
上面的数组和 `tolist()` 模式可以避免这些副作用；随后可以使用带有 `append` 的循环来构建归一化后的结果。

### 你的任务

完成 `as_float_values(values)`。
练习上面展示的 NumPy 浮点数组和 `tolist()` 模式。

- 接收一个仅包含有限整数或浮点数的列表，排除布尔值。
  对于任何其他容器或无效元素（包括字符串、`None` 和嵌套列表），返回 `None`。
- 按原始顺序返回一个普通的 Python 浮点数列表。
  输入为空时返回 `[]`。
- 保留有限浮点数值且不进行四舍五入。
  将带符号的零都转换为 `0.0`：在使用循环和 `append` 构建返回列表时，可以将等于零的值替换为 `0.0`。

### 解答

```python
import numpy as np

def as_float_values(values):
    if not isinstance(values, list):
        return None
    for value in values:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            return None
        if not -float("inf") < value < float("inf"):
            return None
    array = np.array(values, dtype=float)
    result = []
    for value in array.tolist():
        if value == 0:
            value = 0.0
        result.append(value)
    return result
```
