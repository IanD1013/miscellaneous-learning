消息有效负载（message payload）将文本及其用途关联在一起。
在此工作流程中，每条消息都是一个字典：`role` 用于标识消息的类型，而 `content` 则包含其文本。
角色 `system` 标记指令；`user` 标记伴随这些指令的请求。

```python
message = {"role": "user", "content": "Describe the result."}
```

这将创建包含两个字符串字段的一条消息记录。
字段名称和角色值必须完全一致：如果将请求放入名为 `text` 的字段中，就会产生不同的数据结构。
列表用于按顺序保存多条消息。
在此，系统消息必须在先，用户消息在后，以便它们的位置能够保留预期的“指令/请求”顺序。
这是本练习有效负载所需的两个角色。
Python 字典会保留键的插入顺序：上面的字面量在 `content` 之前插入了 `role`，因此迭代和显示时都会遵循该顺序。
在每条消息中都保持这种字段顺序，以便有效负载始终在其文本之前展示其用途。

在构建记录之前，请先验证文本。
在调用 `.strip()` 之前，请使用熟悉的 `isinstance(value, str)` 进行检查。
去除操作（stripping）会移除首尾空格；它会保留单词、内部间距、大小写和 Unicode 字符。
在去除首尾空格后检查字符串是否为空：单独的制表符或换行符不包含任何可用内容。

### 构建消息对

完成 `build_messages(system_text, user_text)`：

- 如果任一参数不是字符串，或者任一去除首尾空格后的字符串为空，则返回 `None`。
- 否则，返回一个恰好包含两个字典的列表，每个字典的键按照 `role`、然后是 `content` 的顺序插入。
  第一个字典的 `role` 为 `"system"`，`content` 为去除首尾空格后的 `system_text`；第二个字典的 `role` 为 `"user"`，`content` 为去除首尾空格后的 `user_text`。

只要有一条消息无效，就必须拒绝整对消息；不要返回部分列表。

### 解答

```python
def build_messages(system_text, user_text):
    if not isinstance(system_text, str) or not isinstance(user_text, str):
        return None
    system_text = system_text.strip()
    user_text = user_text.strip()
    if system_text == "" or user_text == "":
        return None
    return [
        {"role": "system", "content": system_text},
        {"role": "user", "content": user_text},
    ]
```
