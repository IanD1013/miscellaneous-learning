结果对齐（Result reconciliation）将每条返回的记录与其请求的 ID 进行匹配。
到达的位置顺序无法用于建立这种匹配关系：第二个请求的结果可能会最先到达。
每条记录的 `id` 标识该请求；其 `content` 包含返回的文本。
`ids` 列表提供了你期望在输出中呈现的顺序。

字典查找将匹配与排序分离开来。
对于已经过验证的记录，你可以将其内容存储在其 ID 下：

```python
lookup = {}
record = {"id": "segment-2", "content": "ready"}
lookup[record["id"]] = record["content"]
content = lookup.get("segment-1")
```

在这里，`lookup` 将 `"segment-2"` 映射到 `"ready"`。
最后一行会返回 `None`，因为 `"segment-1"` 没有对应的条目。
构建好查找字典后，遍历所请求的 ID 列表，即可按该顺序构建输出记录。
这样，缺失的条目也会在输出中占有明确的位置。
Python 字典会保留键插入时的顺序，包括显示其内容时也是如此。
构建每条输出记录时，请将 `"id"` 放在首位，`"content"` 放在第二位，以确保其字段顺序保持一致。

在向查找字典赋值之前，请检查是否存在重复的 ID：否则赋值会替换掉先前的 content 并掩盖重复项。
此外，还要检查每个结果 ID 是否属于请求的 ID 列表。
存在未知 ID 意味着提供的结果无法与该请求列表匹配。

### 对齐提供的记录

在不修改任何一个输入的前提下完成 `reconcile_results(ids, results)`。

- 两个参数都必须是列表。
  请求的 ID 必须是唯一的字符串。
- 每个 result 必须是一个字典，且仅包含 `"id"` 和 `"content"` 两个键，两者均存放字符串。
  空字符串是有效的 ID 和 content。
- 如果出现任何无效的形状或类型、重复的请求 ID 或结果 ID、或未知的结​​果 ID，均返回 `None`。
- 否则，按请求 ID 的顺序返回一个包含 `{"id": identifier, "content": content}` 字典的新列表，每条记录中键的插入顺序均为先 `"id"` 后 `"content"`。
  对于没有结果的请求 ID，使用 `None` 作为 content。
  两个空列表则生成 `[]`。

### 解答

```python
def reconcile_results(ids, results):
    if not isinstance(ids, list) or not isinstance(results, list):
        return None
    requested = {}
    for identifier in ids:
        if not isinstance(identifier, str) or identifier in requested:
            return None
        requested[identifier] = True
    lookup = {}
    for record in results:
        if not isinstance(record, dict) or len(record) != 2:
            return None
        if "id" not in record or "content" not in record:
            return None
        identifier = record["id"]
        content = record["content"]
        if not isinstance(identifier, str) or not isinstance(content, str):
            return None
        if identifier not in requested or identifier in lookup:
            return None
        lookup[identifier] = content
    ordered = []
    for identifier in ids:
        ordered.append({"id": identifier, "content": lookup.get(identifier)})
    return ordered
```
