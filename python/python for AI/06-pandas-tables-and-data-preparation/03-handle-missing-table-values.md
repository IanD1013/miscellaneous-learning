`isna()` 用于识别 pandas 列中的缺失值，而 `fillna(value)` 则用于替换它们。
显式的 `None` 表示计数不可用；0 则表示已知计数为零。
空字符串仍然是字符串，而不是缺失的计数。

```python
import pandas as pd

sample = pd.DataFrame({"count": [None, -4, 0]}, dtype=object)
missing = sample["count"].isna()
sample["count"] = sample["count"].fillna(0).astype(object)
```

选取 `sample["count"]` 会返回一个 Series，即该列的值。
调用 `isna()` 会返回一个布尔型 Series：第一个值为 `True`，其余两个值为 `False`。
调用 `fillna(0)` 会生成替换值，同时保持 `-4` 和 `0` 不变。
将结果重新赋值给 `sample["count"]` 会更新该列；仅调用该方法而不赋值则不会更新表格。

在构建此表格时使用 `dtype=object`，这样与 `None` 并存的整数就能保留其整数值，而不会变成浮点数值。
大整数在转换为浮点数时可能会丢失精度。
在 `fillna(0)` 后链式调用 `.astype(object)` 可以使填充后的列保持为 object 存储类型。
在执行 `to_dict("records")` 后，构建每个输出记录时使用 `int(row["count"])` 以返回普通的 Python 整数。
在转换前请先验证计数：因为 `int` 也会接受本任务所拒绝的值。

在构建表格之前先构建投影行是一种安全的方法：对这些行进行编辑不会影响调用者的数据。
对原始记录进行就地（in-place）修改会产生副作用。

### 你的任务

使用 pandas 表格和 `fillna(0)` 完成 `fill_missing_counts(records)`。

- 接收一个字典列表。
  每条记录必须同时包含 `"id"` 和 `"count"`。
  id 必须是字符串，包括空字符串。
  计数必须是整数（布尔值除外），或者显式的 `None`（JSON 的 `null`）。
  负整数是合法的。
- 如果任何输入违反了这些规则，则返回 `None`。
  请单独检查键是否存在：即使允许显式的 null，缺失 `"count"` 键也是无效的。
- 返回一个新的字典列表，其中仅包含 `"id"` 和 `"count"`，保持该键顺序和原始行顺序。
  忽略多余的字段。
  将缺失的计数替换为整数 0，并保留所有既有的整数。
- 如果输入为空列表，则返回 `[]`。

### 解答

```python
import pandas as pd

def fill_missing_counts(records):
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
        count = record["count"]
        if count is not None and (isinstance(count, bool) or not isinstance(count, int)):
            return None
        rows.append({"id": record["id"], "count": count})
    table = pd.DataFrame(rows, columns=["id", "count"], dtype=object)
    table["count"] = table["count"].fillna(0).astype(object)
    result = []
    for row in table.to_dict("records"):
        result.append({"id": row["id"], "count": int(row["count"])})
    return result
```
