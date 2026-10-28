`csv.DictReader` 将 CSV 记录读取为字典，使用第一条记录作为表头：即列名列表。
逗号用于分隔字段，但双引号可以包裹包含逗号或换行符的字段。
如果直接按逗号拆分或分别处理每个物理行，将会破坏这些字段。

```python
import csv
import io

sample = 'topic,note\nformat,"comma, inside"\n'
with io.StringIO(sample, newline="") as source:
    reader = csv.DictReader(source, strict=True)
    for row in reader:
        print(row["note"])
```

这会打印出 `comma, inside`。
`io.StringIO` 使字符串可以像文本文件一样被读取，而无需打开磁盘文件。
命名参数 `newline=""` 让换行符保持原样传递给 CSV 解析器。
`with ... as source:` 代码块在结束时会关闭流，即使在提前 return 时也是如此。

`csv.DictReader(source, strict=True)` 用于创建 reader。
命名参数 `strict=True` 使其在遇到解析错误（例如未闭合的带引号字段）时抛出 `csv.Error`。
使用 `except csv.Error:` 可以处理该特定失败情况。
解析操作发生在读取表头或遍历记录时，因此这两个操作都应放在 `try` 内部。

读取 `reader.fieldnames` 可以获取作为列表的表头。
在收集行之前验证该列表：除非你进行检查，否则解析器会接受重复或意外的列名。
然后对 `reader` 进行循环，为每条数据记录生成一个字典；所有字段值都保持为字符串。

成功解析并不保证字段数量正确。
在默认设置下，多余的字段会出现在字典键 `None` 下，因此 `None in row` 可以检测到它们。
缺失的字段其值为 `None`；通过测试 `row["text"] is None` 可以将其与合法的空字符串 `""` 区分开来。
以这种方式检查每个必需的字段。
记录之间的完全空白物理行会被 reader 忽略。
引号内的换行符仍属于该字段的一部分。

Python 字典在显示或迭代时会保留键的插入顺序。
在返回的每条记录中保持相同的键顺序，可以使这两列保持一致的顺序。

### 读取双列记录

使用基于 StringIO 的 DictReader 实现 `read_csv_rows(text)`。
要求表头列表必须严格按顺序等于 `["id", "text"]`。
返回一个字典列表，每个字典恰好包含这两个按插入顺序排列的键：先是 `"id"`，然后是 `"text"`。
保留记录顺序和字段内容，包括空字符串。
ID 也保持为字符串。

如果表头缺失或不匹配、存在任何缺失或多余字段、或抛出 `csv.Error`，则返回 `None`。
有效的表头且无数据记录时返回 `[]`。
发生失败后不要返回部分收集的行。

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
```
