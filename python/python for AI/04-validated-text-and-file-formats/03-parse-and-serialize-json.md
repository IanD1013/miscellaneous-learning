`json.loads(text)` 将 JSON 文本解析为 Python 值；`json.dumps(value)` 将这些值重新序列化为文本。
在使用这两个函数之前，请先导入 `json`：

```python
import json

record = json.loads('{"ready": true, "note": null}')
text = json.dumps(record)
```

解析后的记录是一个包含 `True` 和 `None` 的字典。
JSON 在键和字符串中使用双引号，并采用拼写 `true`、`false` 和 `null`。
数组会转换为列表。
序列化会恢复 JSON 的拼写，而不是使用 Python 的字典表示形式。

普通序列化遵循字典的插入顺序。
而以下选项可以控制输出：

```python
text = json.dumps(record, sort_keys=True,
                  separators=(",", ":"), ensure_ascii=False,
                  allow_nan=False)
```

`sort_keys=True` 会对每个字典中的键进行排序，包括嵌套的字典。
`separators=(",", ":")` 提供了项之间的逗号以及键与值之间的冒号，且不添加额外的空格。
`ensure_ascii=False` 会保留诸如 `é` 等字符，而不是将它们转换为 ASCII 转义序列。
必需的转义仍会保留，字符串值中的空格也会保持原样。

### 拒绝无效数字

此任务仅接受有限数字：既不能是无穷大（infinity），也不能是 NaN（表示“非数字”的特殊值）。
Python 的默认解码器接受非 JSON 常量 `NaN`、`Infinity` 和 `-Infinity`。
向其提供此辅助函数以拒绝它们：

```python
def reject_constant(value):
    raise ValueError("non-finite JSON constant")

record = json.loads('{"count": 3}', parse_constant=reject_constant)
```

`parse_constant` 接收不带括号的函数名称。
当解码器遇到这些常量之一时就会调用该函数；`raise ValueError(...)` 会因抛出错误而停止解析。

序列化选项 `allow_nan=False` 是第二重防护：对于解析数据中任何位置出现的非有限浮点数，它都会引发 `ValueError`。
它能捕获像 `1e400` 这样有效的数字文本，这些文本因超出浮点表示范围而变为无穷大。
当运行时拒绝数字的表示时，整数转换也可能引发 `ValueError`。
这些失败并不意味着 JSON 语法畸形。

畸形的 JSON 会引发 `json.JSONDecodeError`，它是 `ValueError` 的一种子类。
将解析和序列化放在 `try` 块中，并处理 `except ValueError:`，以便针对所有这些情况返回相同的失败值。

### 你的任务

使用上述辅助函数和选项实现 `normalize_json(text)`。
在根层级仅接受 JSON 对象，包括 `{}`；使用 `isinstance(value, dict)` 检查解析后的值。
允许嵌套对象和数组。
返回紧凑、排序后的 JSON 字符串；对于畸形输入、被拒绝的数字或任何其他根类型，返回 `None`。
即使解析成功，也必须拒绝数组、字符串、数字、布尔值或 `null` 作为根的情况。

[Python JSON 参考](https://docs.python.org/3.13/library/json.html)

### 解答

```python
import json

def reject_constant(value):
    raise ValueError("non-finite JSON constant")

def normalize_json(text):
    try:
        value = json.loads(text, parse_constant=reject_constant)
        if not isinstance(value, dict):
            return None
        return json.dumps(value, sort_keys=True, separators=(",", ":"),
                          ensure_ascii=False, allow_nan=False)
    except ValueError:
        return None
```
