**点积**（dot product）将两个向量中相对应位置的分量相乘，然后将这些乘积相加。
这里的向量是一个数字列表；每个数字都是一个分量，分量的数量就是它的维度。
对于 `[2, -1]` 和 `[3, 4]`，计算过程为 `2 * 3 + (-1) * 4`，结果为 `2`。

Python 的 `zip` 可以将对应的值成对提供：

```python
total = 0.0
for first, second in zip([2, -1], [3, 4]):
    total += first * second
```

`for` 后面的两个变量名在每次迭代时分别从每个列表中接收一个值：首先是 `2` 和 `3`，然后是 `-1` 和 `4`。
累加器的最终值为 `2.0`。
如果是两个空列表，循环不会执行任何操作，保持初始的 `0.0`。

`zip` 会在较短的输入结束时停止。
如果将 `[2, -1]` 与 `[3]` 配对，会静默忽略第二个分量并得出 `6.0`。
在相乘之前请检查长度是否相等；在本任务中，缺少分量会导致输入无效。

在累加完成后使用 `round(total, 6)` 将最终结果保留六位小数。
若先对每个乘积进行舍入可能会改变求和结果。
舍入后为零的结果必须返回为 `0.0`，包括原本可能会变成 `-0.0` 的微小负数结果。

### 你的任务

实现 `dot_product(left, right)`，且不得修改任何一个输入。

- 两个参数都必须是长度相等的列表，且各自包含 0 到 64 个分量。
- 每个分量都必须是有限的 `int` 或 `float`，绝对值最大为 1000。
  即使 Python 将布尔值视为整数，也请拒绝布尔值。
  检查 `-1000 <= value <= 1000` 还可以过滤掉非有限数值。
- 对于任何无效的容器、长度、分量类型或数值，严格返回 `None`。
- 否则，返回对应乘积之和，并保留六位小数。
  空输入以及舍入后为零的结果返回 `0.0`。

维度和分量的取值范围仅适用于本练习；它们并不是 Python 数值或向量本身的限制。

### 解答

```python
def dot_product(left, right):
    if not isinstance(left, list) or not isinstance(right, list):
        return None
    if len(left) != len(right) or len(left) > 64:
        return None
    for vector in [left, right]:
        for value in vector:
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                return None
            if not -1000 <= value <= 1000:
                return None
    total = 0.0
    for left_value, right_value in zip(left, right):
        total += left_value * right_value
    result = round(total, 6)
    if result == 0:
        return 0.0
    return result
```
