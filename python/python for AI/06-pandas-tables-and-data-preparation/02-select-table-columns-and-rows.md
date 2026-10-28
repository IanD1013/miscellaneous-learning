`table.loc[rows, columns]` 可以同时选择行和指定的列。
布尔掩码（boolean mask）是一个由 `True` 和 `False` 值组成的 Series，每行对应一个值；`.loc` 会保留标记为 `True` 的行。

```python
import pandas as pd

table = pd.DataFrame(
    [{"label": "p", "size": 1}, {"label": "q", "size": 4}],
    columns=["label", "size"],
    dtype=object,
)
mask = table["size"] >= 4
chosen = table.loc[mask, ["label"]]
```

`table["size"]` 会将一列作为 Series 检索出来。
将其与 `4` 进行比较会比较其中的每个值，第一行生成 `False`，第二行生成 `True`。
在 `.loc[...]` 内部，逗号将行选择与列选择分隔开。
列表 `["label"]` 保留仅包含该列的表格，因此 `chosen.to_dict("records")` 返回 `[{"label": "q"}]`。
筛选操作会保留行的原始顺序。

显式指定 `columns` 也可以让空表具有列名。
`dtype=object` 保留了 Python 整数值，而不会将它们转换为浮点数（浮点数可能会导致大数值计数丢失精度）。

一种安全的构建模式是在构建表格之前将验证过的值收集到新的字典中，然后使用 `to_dict("records")` 转换筛选后的表格。
就地修改输入字典或清空输入列表也会更改调用者的数据。
在构建输出字典时，编写 `{"id": identifier, "count": int(value)}` 可以将计数保持为 Python 整数，并在 `count` 之前插入 `id`。
Python 字典会保留插入顺序，因此它们的表示形式遵循该键顺序。

### 筛选匹配的记录

使用计数比较和 `.loc` 完成 `select_table_records(records, minimum)`。

- `records` 必须是一个字典列表。
  每个字典必须包含字符串类型的 `id` 和整数类型的 `count`。
  空字符串是有效的。
  忽略额外的字段。
- `minimum` 必须是一个整数。
  在这两个整数类型的字段中都要排除布尔值：Python 中的 `isinstance(True, int)` 为 true。
  小数和 `None` 均无效。
  负数计数和负数阈值有效。
- 如果任何输入无效，即使该记录本会被过滤掉，也应返回 `None`。
  在筛选前进行验证。
- 保留计数大于或等于 `minimum` 的记录。
  返回仅包含 `id` 然后是 `count` 的普通字典，保留输入顺序和重复的 id。
  对于空输入或没有匹配项的情况，返回 `[]`。

### 解答

```python
import pandas as pd

def select_table_records(records, minimum):
    if isinstance(minimum, bool) or not isinstance(minimum, int):
        return None
    if not isinstance(records, list):
        return None
    rows = []
    for record in records:
        if not isinstance(record, dict):
            return None
        if "id" not in record or "count" not in record:
            return None
        if not isinstance(record["id"], str):
            return None
        if isinstance(record["count"], bool) or not isinstance(record["count"], int):
            return None
        rows.append({"id": record["id"], "count": record["count"]})
    table = pd.DataFrame(rows, columns=["id", "count"], dtype=object)
    mask = table["count"] >= minimum
    chosen = table.loc[mask, ["id", "count"]]
    result = []
    for row in chosen.to_dict("records"):
        result.append({"id": row["id"], "count": int(row["count"])})
    return result
```
