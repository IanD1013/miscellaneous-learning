`sort_values` 会根据列的值对表格行进行排序。
列名列表指定了它们的优先级：第二列用于在第一列出现平局时进行裁决。
相对应的 `ascending` 列表设置了每个列的排序方向；`False` 将较大值排在前面，而 `True` 将较小值排在前面。

```python
rows = [{"name": "z", "priority": 2}, {"name": "a", "priority": 2}]
table = pd.DataFrame(rows, columns=["name", "priority"], dtype=object)
table["_order"] = list(range(len(rows)))
ordered = table.sort_values(
    ["priority", "name", "_order"],
    ascending=[False, True, True],
    kind="stable"
)
ordered = ordered.reset_index(drop=True)
```

这里的 `"a"` 排在 `"z"` 之前，因为它们的优先级相同。
`list(range(len(rows)))` 会生成从零开始的出现位置序号。
将该列表赋值给 `_order` 会添加一列，当其他列出现平局时，其升序值能够保留输入顺序。
`kind="stable"` 指定使用稳定排序算法，该算法在适用的情况下保留相等键之间的出现顺序。
对于这种多列排序，显式的 `_order` 列提供了最终的平局裁决依据。

排序会保留原始行标签，即索引（index）。
`reset_index(drop=True)` 会将其替换为从零开始的连续标签；`drop=True` 可以防止旧索引变成新的一列。
这只会更改标签，而不会改变已排好序的行顺序。

使用 `to_dict("records")` 获取字典列表。
使用 `id` 在 `score` 之前的字典字面量可以为这些字段指定插入顺序，从而使其表现形式保持一致。
使用 `int(value)` 获得普通的 Python 整数分数。
`dtype=object` 会保留传入的整数值，而不会通过浮点数存储进行转换。

为了安全起见，在构建表格之前，先将所选字段收集到新的字典中，正如参考实现所做的那样。
直接修改从 `records` 中获取的字典也会更改调用者的数据。

### 任务

使用 pandas 完成 `rank_table(records)`：

- 接收一个包含字符串 `id` 和整数 `score` 的字典列表。
  空字符串、负分和零均为有效值。
  布尔类型的分数无效。
- 若外部值或记录无效、缺少必需字段或字段类型不正确，则返回 `None`。
  忽略多余字段。
- 按 `score` 降序、然后按 `id` 升序、最后按出现顺序排序。
  即使输入顺序相反也要应用此排序规则；保留重复行。
- 返回仅包含 `id` 和 `score` 的普通字典，其中包含整数分数。
  若输入为空，则返回 `[]`。

### 解答

```python
import pandas as pd

def rank_table(records):
    if not isinstance(records, list):
        return None
    rows = []
    for record in records:
        if not isinstance(record, dict):
            return None
        if "id" not in record or "score" not in record:
            return None
        if not isinstance(record["id"], str):
            return None
        if isinstance(record["score"], bool) or not isinstance(record["score"], int):
            return None
        rows.append({"id": record["id"], "score": record["score"]})
    table = pd.DataFrame(rows, columns=["id", "score"], dtype=object)
    table["_order"] = list(range(len(rows)))
    ordered = table.sort_values(
        ["score", "id", "_order"],
        ascending=[False, True, True],
        kind="stable"
    )
    ordered = ordered.reset_index(drop=True)
    result = []
    for row in ordered.to_dict("records"):
        result.append({"id": row["id"], "score": int(row["score"])})
    return result
```
