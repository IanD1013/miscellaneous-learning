赋值 `other = record` 只是为同一个字典赋予了另一个名称。
这就是别名机制（aliasing）：通过任何一个名称所做的更改都会影响同一个对象。
你在字典更新中使用的 `dict.copy` 方法会创建一个独立的外部字典，但它是一个浅拷贝（shallow copy）：嵌套对象仍然是共享的。

```python
original = {"labels": ["draft"]}
changed = original.copy()
changed["labels"].append("checked")
```

现在两个字典都包含 `["draft", "checked"]`。
`original.copy()` 调用了字典不带参数的 `copy` 方法。
它复制了字典的条目，因此 `changed["labels"]` 仍然引用原始列表。
执行 append 操作会更改该共享列表；仅复制外部字典并没有将其分离开来。

要获得一个独立的列表，请使用 `list.copy`：

```python
labels = ["draft"]
separate = labels.copy()
separate.append("checked")
```

此时 `labels` 仍为 `["draft"]`，而 `separate` 变为 `["draft", "checked"]`。
点号用于选择列表的方法，空括号用于调用它。
这也是一个浅拷贝，但此处的元素是字符串，因此对于追加操作来说，一个独立的列表已经足够了。
对于嵌套记录，在编辑复制后的列表之前，需要将其赋值给复制后的字典。

字典会保留键的插入顺序，这使得迭代和显示的记录保持一致。
字典的副本也会保留该顺序；替换现有条目（例如 `tags`）会将其键保留在相同的位置。

### 任务

完成 `update_tags(record, tag)`。
该记录包含一个字符串类型的 `id` 和一个字符串列表类型的 `tags`；`tag` 是一个字符串。

- 以 `[original, updated]` 的形式返回两条记录。
  第一条记录包含原始输入值；第二条记录具有相同的 `id`，其 `tags` 列表包含现有的标签并随后追加 `tag`。
- 即使列表为空或已经包含该标签，也要进行追加。
  保持现有标签的顺序不变。
- 在返回的两个字典中都保留输入记录的键插入顺序。
  如果输入中 `tags` 在 `id` 之前，那么在两个输出中它也必须在 `id` 之前。

### 解答

```python
def update_tags(record, tag):
    updated = dict(record)
    updated["tags"] = record["tags"] + [tag]
    return [record, updated]
```
