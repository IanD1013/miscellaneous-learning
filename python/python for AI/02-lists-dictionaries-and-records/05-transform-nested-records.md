在嵌套记录中，每个列表项都是一个具有自身字段的字典。
循环会遍历列表项；随后通过键查找读取当前字典中的字段：

```python
rows = [{'label': '  Draft  ', 'pages': 4}]
labels = []
for row in rows:
    labels.append({'label': row['label'].strip()})
```

`row` 每次指向一个字典。
`row['label']` 读取该字典的字符串，而 `.strip()` 返回去除了首尾空白字符的字符串。
大括号在每次迭代时都会创建一个全新的输出字典。
其 `'label'` 键是明确指定的，因此 `pages` 字段永远不会进入输出。
循环结束后，`labels` 为 `[{'label': 'Draft'}]`；`rows` 仍然包含原始文本和这两个字段。

以这种方式选择字段可以让输出具有比输入更小的结构（shape）。
复制整个字典会保留不需要的字段。
追加原始字典并更新它则会更改调用者的数据。
为每条记录构建一个单独的字典可以避免这种副作用。

Python 字典会保留键的插入顺序。
在字典字面量中，字段是按从左到右的顺序插入的：在迭代或显示字典时，`{'label': 'Draft', 'pages': 4}` 会将 `label` 置于 `pages` 之前。
指定明确的字段顺序可以让每条输出记录都具有一致的结构，而无论输入的键顺序如何。

### 任务

完成 `select_fields(records)`。
每个输入字典都具有字符串类型的 `id` 和 `text` 字段，并且可能还包含其他字段。

返回一个列表，其中每个输入记录对应一个字典，且字典中仅包含 `id` 和 `text`（严格按照此顺序插入）。
保持 `id` 不变，并仅去除 `text` 的首尾空白字符。
保持记录在输入中出现的顺序，并保留具有重复 ID 的记录。
空输入返回 `[]`。

### 解答

```python
def select_fields(records):
    result = []
    for record in records:
        result.append({"id": record["id"], "text": record["text"].strip()})
    return result
```
