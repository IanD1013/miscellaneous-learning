JSONL 在每一行存储一个单独的 JSON 值。
在这里，每个非空行都必须包含一个完整的对象。
请独立解析各行，这样受损的记录就不会导致其后的有效记录被丢弃。

`text.split("\n")` 仅在字面 LF 换行符处进行拆分。
在此处它们定义了物理行；CRLF 结尾同样有效，因为剩余的 `\r` 属于 JSON 空白字符。
JSON 字符串内部字面的 Unicode NEL (U+0085)、行分隔符 (U+2028) 和段落分隔符 (U+2029) 仍属于这些字符串的一部分，从而保留了它们的内容以及后续的行号。
`enumerate(lines, start=1)` 将每一行与其位置配对，从 1 开始：

```python
text = '{}\n \nbad'
for line_number, line in enumerate(text.split("\n"), start=1):
    if line.strip():
        print(line_number, line)
```

这会打印编号为 1 和 3 的非空行。
两个循环变量分别接收编号和行内容。
`line.strip()` 去除周围的空白字符；空结果表示该行为空白行。
在跳过空白行之前对原始行进行编号，这样错误就能指向输入中的实际物理位置。

### 验证每条记录

Python 默认的 JSON 解码器接受 `NaN`、`Infinity` 和 `-Infinity`。
可以通过向 `parse_constant` 传递一个辅助函数来拒绝这些常量：

```python
import json

def reject_constant(value):
    raise ValueError("non-finite JSON constant")

record = json.loads('{"score": 4}', parse_constant=reject_constant)
json.dumps(record, allow_nan=False)
```

传递不带括号的辅助函数名称：当解码器遇到这些常量之一时便会调用它。
`raise ValueError(...)` 会以可被捕获的错误终止解码。
最后的 `json.dumps` 调用会检查已解析值中任意位置的非有限数字。
`allow_nan=False` 使序列化在遇到它们时引发 `ValueError` 而不是将它们写入。
丢弃其返回的字符串；保留 `record`。

第二次检查还会捕获诸如 `1e400` 这样解码为无穷大的数字。
解码时的 `ValueError` 可能表示格式错误的 JSON，或者此运行时无法表示的数字（包括被拒绝的整数转换）。
将这两种情况都作为无效行处理。
将这两个调用都放在每行的 `try` 块内，捕获 `ValueError`，并继续处理后面的行。

解析完成后，`isinstance(record, dict)` 用于检查外层值是否为对象。
在此处，数组、字符串、数字、布尔值和 `null` 都是无效的根节点。
有效的对象可以包含嵌套列表和对象，但其中的所有数字都必须是有限且可表示的。

将接受的对象收集到 `records` 中，并将无效的非空行行号收集到 `errors` 中。
返回 `{"records": records, "errors": errors}`，按此顺序插入外层字典的键：先是 `records`，然后是 `errors`。
这样可以确保结果在显示或迭代时具有一致的顺序。
保持两个列表与输入顺序一致，并保留每个解析对象的键顺序。
空文本或完全由空白组成的文本将产生两个空列表。

### 你的任务

使用循环和上述的逐行验证逻辑来实现 `parse_jsonl(text)`。

### 解答

```python
import json

def reject_constant(value):
    raise ValueError("non-finite JSON constant")

def parse_jsonl(text):
    records = []
    errors = []
    for line_number, line in enumerate(text.split("\n"), start=1):
        if not line.strip():
            continue
        try:
            record = json.loads(line, parse_constant=reject_constant)
            json.dumps(record, allow_nan=False)
        except ValueError:
            errors.append(line_number)
            continue
        if isinstance(record, dict):
            records.append(record)
        else:
            errors.append(line_number)
    return {"records": records, "errors": errors}
```
