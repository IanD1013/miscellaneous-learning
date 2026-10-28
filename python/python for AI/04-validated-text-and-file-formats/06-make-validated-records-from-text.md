验证流水线按顺序将数据传递给解析、检查和转换环节。
每个阶段仅在检查上一阶段未发生失败后，才接受其结果。
先进行过滤可能会掩盖格式错误的行：ID 为空并不能作为 CSV 字段多出的借口。

下方提供了上一课中已完成的解析器以供复用。
请将其复制到初始代码中未完成的 `clean_csv_records` 函数上方：

```python
import csv
import io

def read_csv_rows(text):
    with io.StringIO(text, newline="") as source:
        reader = csv.DictReader(source, strict=True)
        try:
            if reader.fieldnames != ["id", "text"]:
                return None
            rows = []
            for row in reader:
                if None in row or row["id"] is None or row["text"] is None:
                    return None
                rows.append({"id": row["id"], "text": row["text"]})
            return rows
        except csv.Error:
            return None
```

`read_csv_rows(text)` 使用了带引号行任务中的 CSV reader。
它严格要求按顺序包含表头 `id,text`，验证每行是否恰好有两个字段，并返回带有字符串值的字典列表。
若表头缺失或不同、字段缺失或多出，或者 strict reader 报告引号错误，它将返回 `None`。
带引号的逗号和换行符会保留在字段内部；实际的空行会被跳过。

小型流水线可以在使用辅助函数的成功结果之前检查其失败值：

```python
def count_csv_rows(text):
    rows = read_csv_rows(text)
    if rows is None:
        return None
    return len(rows)
```

显式的 `is None` 检查可将无效数据与 `[]`（表示没有数据行的成功解析）区分开来。
如果解析失败返回空列表，就会抹杀这种区别。

在遍历或显示时，Python 字典会保留键的插入顺序。
解析器在 `text` 之前插入了 `id`；在构建每条清理后的记录时请保持相同的顺序，以便其表示形式始终首先显示标识符。

### 完成转换

替换 `clean_csv_records(text)` 未完成的函数体。
调用解析器并保留其 `None` 失败结果。
否则，返回一个新的字典列表，其中键按 `id`、然后 `text` 的顺序插入：

- 去除每个 ID 周围的首尾空白字符，并丢弃去除空白后 ID 为空的行。
- 去除 text 周围的首尾空白字符，同时保留其大小写以及任何内部的逗号或换行符。
- 保留去除空白后 text 为空的行，并保持保留行的原有顺序。

仅有表头而没有数据行，或者所有有效行都被丢弃时，应返回 `[]`。
在过滤之前请验证整个 CSV；绝不要从格式错误的输入中返回部分记录。

### 解答

```python
import csv
import io

def read_csv_rows(text):
    with io.StringIO(text, newline="") as source:
        reader = csv.DictReader(source, strict=True)
        try:
            if reader.fieldnames != ["id", "text"]:
                return None
            rows = []
            for row in reader:
                if None in row or row["id"] is None or row["text"] is None:
                    return None
                rows.append({"id": row["id"], "text": row["text"]})
            return rows
        except csv.Error:
            return None

def clean_csv_records(text):
    rows = read_csv_rows(text)
    if rows is None:
        return None
    cleaned = []
    for row in rows:
        record_id = row["id"].strip()
        if record_id == "":
            continue
        cleaned.append({"id": record_id, "text": row["text"].strip()})
    return cleaned
```
