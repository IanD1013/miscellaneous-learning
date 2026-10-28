字典（`dict`）通过键（key）来存储值：键是用于查找这些值的名称。
与列表的索引位置不同，这里的键是一个字符串。

```python
counts = {"short": 2, "long": 0}
current = counts["short"]
counts["short"] = 5
counts["medium"] = 1
```

花括号用于界定字典；每个冒号用于分隔键及其对应的值，逗号用于分隔不同的条目。
`{}` 是一个空字典。
在赋值之前，通过 `["short"]` 读取会返回 `2`。
在 `=` 的左侧，方括号用于指定要替换或添加的键。
最终的字典为 `{'short': 5, 'long': 0, 'medium': 1}`。
字典在显示或遍历时会保留插入顺序：替换已有键的值会保留其原有位置，而添加新键则会将其排在最后。
在这里，`short` 依然排在第一位，而 `medium` 出现在最后。

使用方括号读取不存在的键会引发 `KeyError`。
当键不存在时，`counts.get("absent", 0)` 会返回第二个参数 `0`；若键已存在，则返回其存储的值，包括 0。
这种查找操作不会添加新条目。
`"long" in counts` 返回 `True`，因为 `in` 检查的是键，而不是值。

为了避免修改调用方可能仍需要的数据，可以先使用这种复制模式：

```python
updated = counts.copy()
```

以 `counts.copy()` 形式调用的 `dict.copy` 方法会返回一个浅拷贝：一个包含相同条目的全新外层字典。
在 `updated` 中替换某个整数计数不会改变 `counts`。
相反，若直接对 `counts` 进行赋值，则会就地修改调用方的字典。

### 递增一个计数

完成 `increment_count(counts, key)`。
输入包含字符串键和非负整数计数；`key` 是一个字符串。
返回一个字典，其中该键的计数加一，若原先不存在则从零开始计数。
保留所有其他条目及其输入的键顺序。
已存在的键必须保持其位置；新添加的键必须排在最后。
输入为空字典的情况也必须能够正常处理。

### 解答

```python
def increment_count(counts, key):
    updated = dict(counts)
    updated[key] = updated.get(key, 0) + 1
    return updated
```
