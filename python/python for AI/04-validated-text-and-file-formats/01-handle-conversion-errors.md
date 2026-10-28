`try` 和 `except ValueError` 允许你从失败的整数转换中恢复，而无需将所有错误都视为转换失败。
在整数验证练习中，提供的 `_observe_limit` 调用者已经捕获了 `ValueError`，并报告了 `validate_limit` 是正常返回还是抛出了异常。
你在那里编写了验证保护逻辑和 `raise`；而在这里，你需要自己编写异常处理程序。
将可能失败的操作放在 `try` 内部：

```python
try:
    value = int("17", 10)
except ValueError:
    value = None
```

`int` 是一个内置可调用对象：无需 import。
它的第一个参数是要转换的文本；`10` 指定了十进制基数。
在这里转换成功，因此 `value` 变为 `17`，Python 会跳过 `except` 块。
如果将 `"17"` 替换为 `"seventeen"`，`int` 会抛出 `ValueError`。
Python 会中断 `try` 块并运行匹配的处理程序，将 `value` 设置为 `None`。

冒号表示这两个代码块的开始。
缩进它们的主体，并将 `except` 与 `try` 对齐。
明确指定 `ValueError` 可以保持处理程序的针对性；不相关的异常会继续传递给调用者。
尽量保持受保护块的精简，以便处理程序仅作用于你打算从中恢复的转换操作。

十进制整数文本可以包含首尾的空白字符、可选的 `+` 或 `-` 符号、前导零以及数字之间单个的 `_` 字符。
Unicode 十进制数字同样有效：`int("１２", 10)` 会返回 `12`。
你不需要自己去除空白字符。
空文本、仅包含正负号、类似 `"2.5"` 的小数以及单词都会导致转换失败。

即使拼写有效，也仍然可能抛出 `ValueError`：当前运行时将十进制字符串转换限制为 4,300 个数字（不包含符号和 `_` 字符）。
由 4,300 个 1 组成的字符串可以成功转换；而 4,301 个 1 则会超出限制。
请通过相同的异常分支来处理这种失败。

### 解析整数

完成 `parse_integer(text)`，其输入始终为字符串。
在 `try` 中使用 `int(text, 10)`，并在成功时返回该整数。
捕获 `ValueError`，并在转换失败时返回 `None`。
零和负整数都是有效结果，因此在失败时返回 `0` 将无法区分二者。

### 解答

```python
def parse_integer(text):
    try:
        return int(text, 10)
    except ValueError:
        return None
```
