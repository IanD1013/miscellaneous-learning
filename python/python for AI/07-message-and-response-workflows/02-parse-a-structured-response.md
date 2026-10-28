响应封套（response envelope）是保存响应数据的外层字典。
在所提供的这些 fixtures 中，`choices` 是候选响应的列表。
每个 choice 都是一个字典，其 `message` 字段包含另一个字典；该 message 的 `content` 字段则包含要提取的文本。

对于已知的有效 fixture，查找过程遵循以下层级结构：

```python
response = {"choices": [{"message": {"content": "Ready"}}]}
choices = response.get("choices")
first = choices[0]
message = first.get("message")
content = message.get("content")
```

在这里，`content` 的值变为 `"Ready"`。
列表索引用于选择第一个 choice，而字典查找用于选择指定名称的字段。
这些是具有特定形状的练习 fixtures，并不代表所有模型服务的响应都是如此。
输入已经是 Python 值；无需进行 JSON 解码。

未知的输入需要在这些步骤之间进行检查。
在调用 `.get()` 之前，检查外层值是否为字典。
在使用索引 `0` 之前，检查 `choices` 是否为非空列表。
然后，在读取相应字段之前，检查第一个 choice 及其 message 是否为字典。
`isinstance(value, dict)`、`isinstance(value, list)` 和 `isinstance(value, str)` 用于检测相关类型。
使用 `.get()` 读取缺失的键会得到 `None`。

空列表没有第一个 choice，但空字符串属于有效内容。
使用 `if not content` 进行判断会把 `""` 与缺失的内容一同拒绝；请改为检查其类型。

### 提取第一个 choice

实现 `extract_content(response)`。
当第一个 choice 的 content 为字符串时，原样返回该内容。
如果缺少任何必需字段、该路径上存在错误类型或 choices 列表为空，则返回 `None`。
仅检查第一个 choice，即使后面的 choice 包含有效文本也是如此。
允许每个字典层级包含额外字段，并保持输入不变。

### 解答

```python
def extract_content(response):
    if not isinstance(response, dict):
        return None
    choices = response.get("choices")
    if not isinstance(choices, list) or len(choices) == 0:
        return None
    first = choices[0]
    if not isinstance(first, dict):
        return None
    message = first.get("message")
    if not isinstance(message, dict):
        return None
    content = message.get("content")
    if not isinstance(content, str):
        return None
    return content
```
