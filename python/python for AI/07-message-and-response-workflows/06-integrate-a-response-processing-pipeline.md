JSONL 响应处理器即使在相邻行失败时也必须保留有用的记录。
结合逐行解析、schema 校验、重复项处理、结果对齐（reconciliation）以及有界批次（bounded batches）。
将物理行号与已接受记录的计数分开，以便调用者可以在原始文本中定位每个失败。

### 复用辅助函数

起始代码中仅包含 `process_responses`。
将以下已完成的辅助函数复制到其上方。
`make_batches` 用于验证大小并将记录切片为批次；`reconcile_results` 按提供的 ID 顺序返回记录。
在这里，两个列表都将只包含已接受的记录。
`reject_constant` 用于支持下面使用的严格 JSON 解析。

```python
import json

def reject_constant(value):
    raise ValueError("non-finite JSON constant")

def make_batches(records, batch_size):
    if not isinstance(batch_size, int) or isinstance(batch_size, bool):
        return None
    if batch_size < 1 or batch_size > 100:
        return None
    if not isinstance(records, list):
        return None
    batches = []
    for start in range(0, len(records), batch_size):
        batches.append(records[start:start + batch_size])
    return batches

def reconcile_results(ids, results):
    if not isinstance(ids, list) or not isinstance(results, list):
        return None
    requested = {}
    for identifier in ids:
        if not isinstance(identifier, str) or identifier in requested:
            return None
        requested[identifier] = True
    lookup = {}
    for record in results:
        if not isinstance(record, dict) or len(record) != 2:
            return None
        if "id" not in record or "content" not in record:
            return None
        identifier = record["id"]
        content = record["content"]
        if not isinstance(identifier, str) or not isinstance(content, str):
            return None
        if identifier not in requested or identifier in lookup:
            return None
        lookup[identifier] = content
    ordered = []
    for identifier in ids:
        ordered.append({"id": identifier, "content": lookup.get(identifier)})
    return ordered
```

对于每个非空行，在 `try` 中使用已确立的严格解码模式：

```python
record = json.loads(line, parse_constant=reject_constant)
json.dumps(record, allow_nan=False)
```

第一次调用会拒绝 `NaN`、`Infinity` 和 `-Infinity`。
第二次调用会检查解码后的值是否包含非有限数，包括像 `1e400` 这样的溢出。
捕获 `ValueError`，记录该行的行号，然后继续处理下一行。
仅靠解析并不能确立所需的对象结构。

使用来自 JSONL 解析练习的 JSONL 边界：字面量 LF（`\n`）结束一条物理记录，CRLF（`\r\n`）也能正常工作，因为多余的 CR 属于 JSON 空白字符。
使用 `text.split("\n")` 进行拆分以保留这些边界。
`splitlines()` 还会拆分 Unicode NEL (U+0085)、U+2028 和 U+2029；这些字符可能会出现在 JSON 字符串内部，且必须保留为其值的一部分。
空记录仍然占用一个物理行号。

Python 字典在显示或迭代时会保留插入顺序。
构建外部结果时，先放入 `"batches"`，后放入 `"invalid_lines"`。
批次内的每条记录必须先包含 `"id"`，后包含 `"content"`；提供的对齐辅助函数会构建该顺序，无论输入对象的键顺序如何。

### 完成处理器

实现具有以下行为的 `process_responses(text, batch_size)`：

- 当 `text` 不是字符串或 `batch_size` 不是 1 到 100（含）之间的整数时，返回 `None`。
  拒绝布尔值作为大小。
  即使文本为空，也要验证控制参数；`make_batches([], batch_size)` 可以用于检查大小。
- 按输入顺序处理由 LF 分隔的物理行，包括 CRLF 输入。
  在跳过 `.strip()` 为空的行之前，从 1 开始对每个物理行进行计数。
- 仅接受键严格为 `"id"` 和 `"content"` 且两者都持有字符串的解码字典。
  空字符串是有效的。
  精确保留字符串，包括空白字符。
- 一个 ID 只能被接受一次。
  将已接受 ID 的后续出现标记为无效，并保留第一条接受的记录。
  被拒绝的行不会保留其 ID。
- 按输入顺序将每个被拒绝的非空行行号放入 `invalid_lines` 中一次。
  每次拒绝后继续处理。
- 使用已接受 ID 的顺序对齐已接受的记录，然后对它们进行分批。
  每个批次最多包含 `batch_size` 条记录；保留最终的不完整批次，且不创建空批次。

返回一个字典，按插入顺序严格先包含 `"batches"`，随后包含 `"invalid_lines"`。
有效大小下的空文本或仅包含空白的文本返回 `{"batches": [], "invalid_lines": []}`。

### 解答

```python
import json

def reject_constant(value):
    raise ValueError("non-finite JSON constant")

def make_batches(records, batch_size):
    if not isinstance(batch_size, int) or isinstance(batch_size, bool):
        return None
    if batch_size < 1 or batch_size > 100:
        return None
    if not isinstance(records, list):
        return None
    batches = []
    for start in range(0, len(records), batch_size):
        batches.append(records[start:start + batch_size])
    return batches

def reconcile_results(ids, results):
    if not isinstance(ids, list) or not isinstance(results, list):
        return None
    requested = {}
    for identifier in ids:
        if not isinstance(identifier, str) or identifier in requested:
            return None
        requested[identifier] = True
    lookup = {}
    for record in results:
        if not isinstance(record, dict) or len(record) != 2:
            return None
        if "id" not in record or "content" not in record:
            return None
        identifier = record["id"]
        content = record["content"]
        if not isinstance(identifier, str) or not isinstance(content, str):
            return None
        if identifier not in requested or identifier in lookup:
            return None
        lookup[identifier] = content
    ordered = []
    for identifier in ids:
        ordered.append({"id": identifier, "content": lookup.get(identifier)})
    return ordered


def process_responses(text, batch_size):
    if not isinstance(text, str):
        return None
    if make_batches([], batch_size) is None:
        return None
    accepted = []
    seen = {}
    invalid_lines = []
    for line_number, line in enumerate(text.split("\n"), start=1):
        if not line.strip():
            continue
        try:
            record = json.loads(line, parse_constant=reject_constant)
            json.dumps(record, allow_nan=False)
        except ValueError:
            invalid_lines.append(line_number)
            continue
        if (
            not isinstance(record, dict)
            or len(record) != 2
            or "id" not in record
            or "content" not in record
            or not isinstance(record["id"], str)
            or not isinstance(record["content"], str)
            or record["id"] in seen
        ):
            invalid_lines.append(line_number)
            continue
        seen[record["id"]] = True
        accepted.append(record)
    ids = []
    for record in accepted:
        ids.append(record["id"])
    ordered = reconcile_results(ids, accepted)
    return {"batches": make_batches(ordered, batch_size), "invalid_lines": invalid_lines}
```
