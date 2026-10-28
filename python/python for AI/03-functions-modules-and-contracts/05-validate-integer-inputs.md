`isinstance(value, int)` 检查某个值是否为整数，并返回 `True` 或 `False`。
在对可能是字符串或 `None` 的输入进行数值运算之前，请使用类型检查：

```python
def double_integer(value):
    if not isinstance(value, int):
        raise ValueError("an integer is required")
    return value * 2
```

`isinstance` 的第二个参数是要检查的类型；`int` 代表 Python 的整数类型。
当检查失败时，`not` 会使条件为真。
`raise` 会通过异常来终止函数执行，异常是一种中断正常执行的错误。
`ValueError("an integer is required")` 会创建该错误，并附带一条解释被拒绝输入的消息。
将 `raise` 放在无效分支内；只有在检查成功时才会执行到 return。

这里有一个需要注意的细节：`isinstance(True, int)` 的结果也是 `True`，因为 Python 将布尔值视为一种整数。
`isinstance(value, bool)` 可以识别布尔值，以便你明确地拒绝它们。
在比较边界范围之前请先检查类型：类似 `"8"` 这样的字符串无法使用 `<` 与整数进行比较。
看起来像数字的字符串仍然是字符串。

### 你的任务

完成 `validate_limit(value)`。
仅接受 1 到 100 之间的整数（包含两个端点），并原样返回接受的值。
排除 `True` 和 `False`。
拒绝浮点数（例如 `1.5` 和 `7.0`）、字符串、`None`、零、负整数以及大于 100 的整数。
对于每个被拒绝的输入，抛出 `ValueError` 并附带完全一致的提示信息：`limit must be an integer from 1 to 100`。
不要将无效输入转换为整数。

已编写完成的 `_observe_limit(value)` 调用方会记录 `["returned", value]` 或 `["raised", message]`。
它会为你处理抛出的 `ValueError`，因此如果返回错误字符串，反而会被记录为返回的值。
`_whole_float_limit()` 会使用 `7.0` 调用该调用方。
请保持这两个已完成的辅助函数不变，仅实现 `validate_limit`。

### 解答

```python
def validate_limit(value):
    if type(value) is not int or value < 1 or value > 100:
        raise ValueError("limit must be an integer from 1 to 100")
    return value


def _whole_float_limit():
    return _observe_limit(7.0)

def _observe_limit(value):
    try:
        return ["returned", validate_limit(value)]
    except ValueError as error:
        return ["raised", str(error)]
```
