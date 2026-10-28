`table.merge(lookup, ...)` 通过匹配键列来合并行。
`.merge` 之前的表为左表；传入的参数为右表。
在这里，`code` 将每一行连接到其描述：

```python
import pandas as pd

table = pd.DataFrame(
    [{"code": "p"}, {"code": "q"}],
    columns=["code"], dtype=object
)
lookup = pd.DataFrame(
    [{"code": "p", "text": "Present"}],
    columns=["code", "text"], dtype=object
)
joined = table.merge(
    lookup, on="code", how="left",
    sort=False, validate="many_to_one"
)
```

`on="code"` 指定了要在两个表中进行匹配的列。
`how="left"` 保留所有左表行，包括没有匹配项且获得缺失 `text` 值的 `q`。
内连接会丢弃该行。
`sort=False` 避免对键进行排序；这种左合并会保留左表行的出现顺序。

一对一连接在两侧都具有唯一的键。
多对一连接允许多个左表行共享同一个键，但每个右表键必须仅标识一行。
`validate="many_to_one"` 会检查右侧的唯一性，如果检查失败则引发错误。
如果不进行该检查，对于 `p` 的两个右表行将为每个左表 `p` 生成两个合并后的行。
即使描述完全相同也会导致行数倍增。

在构造每个 DataFrame 时提供 `columns=[...]`，这样即使输入为空，它也仍然具有所需的列。
`dtype=object` 确保这些列即使在为空时也适用于 Python 字符串值。
使用 `joined.to_dict("records")` 获取行字典，然后通过循环仅构建所需的输出字段。
使用 `pd.isna(value)` 检测缺失的合并文本并将其替换为 Python 的 `None`；空字符串是有效文本，而不是缺失值。

一种安全的方法是为每个表构造投影行。
直接就地修改原始记录或标签字典会产生副作用。

### 合并标签

使用 pandas 基于 `label_id` 进行左合并来完成 `join_labels(records, labels)`。

- 两个参数都必须是字典列表。
  每条记录需要字符串类型的 `id` 和 `label_id`；每个标签需要字符串类型的 `label_id` 和 `text`。
  空字符串有效。
  忽略多余字段。
- 若存在任何无效的容器、行、缺失的必填字段或非字符串的必填值，均返回 `None`。
  在合并之前检查标签 ID 是否唯一，即使 `records` 为空也是如此。
  任何重复的查找键都是无效的，包括文本完全相同的重复项。
- 返回一个普通字典列表，按此字段顺序仅包含 `id` 和 `label`。
  保留记录的出现顺序和重复记录。
  将 `label` 设置为匹配的 `text`，若未匹配则设为 `None`。
  标签为空会导致每条记录都无法匹配；验证通过后，若记录为空则返回 `[]`。

### 解答

```python
import pandas as pd

def join_labels(records, labels):
    if not isinstance(records, list) or not isinstance(labels, list):
        return None
    record_rows = []
    for record in records:
        if not isinstance(record, dict):
            return None
        if "id" not in record or "label_id" not in record:
            return None
        if not isinstance(record["id"], str) or not isinstance(record["label_id"], str):
            return None
        record_rows.append({"id": record["id"], "label_id": record["label_id"]})
    label_rows = []
    seen = set()
    for label in labels:
        if not isinstance(label, dict):
            return None
        if "label_id" not in label or "text" not in label:
            return None
        if not isinstance(label["label_id"], str) or not isinstance(label["text"], str):
            return None
        if label["label_id"] in seen:
            return None
        seen.add(label["label_id"])
        label_rows.append({"label_id": label["label_id"], "text": label["text"]})
    table = pd.DataFrame(record_rows, columns=["id", "label_id"], dtype=object)
    lookup = pd.DataFrame(label_rows, columns=["label_id", "text"], dtype=object)
    joined = table.merge(
        lookup, on="label_id", how="left",
        sort=False, validate="many_to_one"
    )
    result = []
    for row in joined.to_dict("records"):
        text = row["text"]
        result.append({"id": row["id"], "label": None if pd.isna(text) else text})
    return result
```
