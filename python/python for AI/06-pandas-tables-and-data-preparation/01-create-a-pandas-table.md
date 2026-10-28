`pandas.DataFrame` 可以将行字典转换为表格：字典的键标识列，每个字典提供一行。
`import pandas as pd` 中的别名让你可以使用 `pd.DataFrame` 来调用同一个构造函数。

```python
import pandas as pd

row = [{"label": "sample", "size": 4}]
table = pd.DataFrame(rows, columns=["label", "size"], dtype=object)
table = table.astype(object)
records = table.to_dict("records")
```

`columns=` 提供列名及其顺序。
在没有行可以推断列时，它还可以为输入为空的情况提供显式的 schema（即表格声明的列）。
指定了这些列名后，即使 `rows = []` 仍然会创建一个包含 `label` 和 `size` 列的表格。

`dtype=object` 存储 Python 对象（包括 Python 整数），而不是将计数限定为固定宽度的数值类型。
`astype(object)` 返回一个转换为该存储类型的表格；将其重新赋值可保留转换后的表格。
它不会将任意值转换为整数。
`to_dict("records")` 选择 records 方向：一个字典列表，每行一个字典，键按照列的顺序排列。
空表格会生成 `[]`。
在构建最终字典时，`int(row["size"])` 会将数值字段转换为普通的 Python 整数。

一种安全的构建模式是收集仅包含所选字段的全新字典，然后从该列表中构建 DataFrame。
这可以让调用者的记录保持可用以供复用。
原地从原始字典中删除多余的键会产生修改调用者数据的副作用。

### 构建表格

完成 `make_table(records)` 以返回一个普通行字典列表。
练习上面展示的 DataFrame 构建方法。

- 接收一个字典列表。
  每个字典必须包含字符串类型的 `id`，以及排除布尔值的整数类型的 `count`。
  对于任何无效输入，返回 `None`。
  空字符串、零和负数计数都是有效的。
- 每个返回的字典必须仅包含 `id` 和 `count`；忽略多余的字段。
- 按输入顺序返回行，键的顺序为 `id`、`count`，且计数需为普通 Python 整数。
  空列表返回 `[]`。

### 解答

```python
import pandas as pd

def make_table(records):
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
    table = table.astype(object)
    result = []
    for row in table.to_dict("records"):
        result.append({"id": row["id"], "count": int(row["count"])})
    return result
```
