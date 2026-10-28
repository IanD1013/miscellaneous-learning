`groupby` 会将具有相同值的行归入一个组。
聚合操作会将每个组的值规约为一个结果。
要累加每个 label 的计数：

```python
rows = [
    {"label": "b", "count": 6},
    {"label": "b", "count": 4},
]
table = pd.DataFrame(rows, dtype=object)
grouped = table.groupby("label", as_index=False).agg({"count": "sum"})
```

`"label"` 指定了分组列：两行都属于 `"b"` 组。
`agg` 用于选择聚合方式。
它的字典将列 `"count"` 映射到操作 `"sum"`，因此 `grouped` 只有一行，label 为 `"b"`，count 为 `10`。
如果使用 `"count"` 作为操作，则会统计非缺失值的数量并返回 `2`；列名本身并不会决定所执行的操作。

`as_index=False` 会将分组标签保留为一列，而不是作为行标签（索引），因此 `grouped.to_dict("records")` 在每个字典中都会包含这两个字段。
`dtype=object` 将输入值存储为 Python 对象，从而在此处保留了 Python 的整数算术特性。
在构建返回的记录时，对每个总和使用 `int` 以显式保证其为 Python 整数类型。

一种安全的构建模式是在创建表之前，先构建仅包含 `"label"` 和 `"count"` 的新行。
直接修改原始字典或对输入列表进行就地（in-place）排序会改变调用者可能仍需要的数据。
参考解答构建了独立的行和独立的结果。

实现 `sum_by_label(records)` 并练习这种 pandas 分组技巧。
返回一个仅包含 `"label"` 和 `"count"` 的字典列表，每个不同的 label 对应一项，并计算计数的总和。
使用显式的排序键（sorting key）按 label 字母升序对结果进行排序。
负数计数是有效的，并且需要保留总和为零的分组。

在创建表之前进行验证。
`records` 必须是一个列表；每个记录必须是一个字典，且包含字符串类型的 `"label"` 和整数类型的 `"count"`。
空字符串是有效的 label。
即使 Python 将布尔值视为整数，也要拒绝布尔值作为 count。
忽略多余的字段。
如果有任何必需的字段或容器无效（包括缺失字段），则返回 `None`。
对于空列表，在分组前直接返回 `[]`，因为它没有任何列。

### 解答

```python
import pandas as pd

def sum_by_label(records):
    if not isinstance(records, list):
        return None
    rows = []
    for record in records:
        if not isinstance(record, dict):
            return None
        if "label" not in record or "count" not in record:
            return None
        if not isinstance(record["label"], str):
            return None
        if isinstance(record["count"], bool) or not isinstance(record["count"], int):
            return None
        rows.append({"label": record["label"], "count": record["count"]})
    if len(rows) == 0:
        return []
    table = pd.DataFrame(rows, dtype=object)
    grouped = table.groupby("label", as_index=False).agg({"count": "sum"})
    result = []
    for row in grouped.to_dict("records"):
        result.append({"label": row["label"], "count": int(row["count"])})
    return sorted(result, key=lambda item: item["label"])
```
