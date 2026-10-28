`with` 会在缩进代码块执行期间保持文件打开状态，并在该代码块结束时将其关闭。
上下文管理器（context manager）是负责管理这种设置和清理操作的对象；由 `open` 返回的文件对象支持此特性。

```python
with open("/tmp/hopfa-ch4-unicode.txt", encoding="utf-8") as source:
    text = source.read()
```

`open` 接收一个路径，默认以读取文本的方式打开。
关键字参数 `encoding="utf-8"` 告诉 Python 如何将文件的字节解码为字符，包括希腊字母和 emoji 表情符号。
`as source` 为打开的文件命名。
冒号表示代码块的开始，缩进则标记了可以使用该文件的语句。
`source.read()` 将所有文本读取为一个字符串。
空文件会产生 `""`。

代码块结束后，文件会被关闭，但 `text` 依然可用。
代码块内部的 `return` 也会在调用者接收到返回值之前触发清理操作。
如果读取过程中引发异常，清理操作同样会执行。

打开一个不存在或无法访问的路径可能会引发 `OSError`，这是操作系统故障（例如文件访问错误）的异常。
将文件操作放在 `try` 内部，并使用 `except OSError:` 返回失败值。
保持该异常处理程序的针对性，以便让无关的编程错误保持可见。

### 读取提供的文件

使用 `with open(..., encoding="utf-8")` 完成 `read_text(path)`。
返回完整的字符串，保留空格、Unicode 字符和换行符。
当打开或读取引发 `OSError` 时返回 `None`；空字符串表示成功读取了一个空文件。

函数上方的设置提供了固定的虚拟文件：`hopfa-ch4-empty.txt` 为空，`hopfa-ch4-unicode.txt` 包含 `Καλημέρα 🌱`，而 `hopfa-ch4-lines.txt` 包含 `first\nsecond\n`。
这些路径位于 `/tmp/` 下；`hopfa-ch4-missing.txt` 不存在。
请保持该设置不变，并读取传递给函数的路径。

### 解答

```python
import os

with open("/tmp/hopfa-ch4-empty.txt", "w", encoding="utf-8") as fixture:
    fixture.write("")
with open("/tmp/hopfa-ch4-unicode.txt", "w", encoding="utf-8") as fixture:
    fixture.write("Καλημέρα 🌱")
with open("/tmp/hopfa-ch4-lines.txt", "w", encoding="utf-8", newline="") as fixture:
    fixture.write("first\nsecond\n")
if os.path.exists("/tmp/hopfa-ch4-missing.txt"):
    os.remove("/tmp/hopfa-ch4-missing.txt")

def read_text(path):
    try:
        with open(path, encoding="utf-8") as source:
            return source.read()
    except OSError:
        return None
```
