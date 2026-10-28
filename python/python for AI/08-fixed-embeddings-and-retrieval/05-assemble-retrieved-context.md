检索到的上下文（Retrieved context）是由选定匹配项组装而成的文本。
上下文预算（budget）限制了可容纳的文本量；在这里，它使用 `len` 计算 Python Unicode 字符数，而不是模型 token 数。
例如，`len("🙂é")` 的结果是 `2`。

两个换行符用于分隔已包含的片段：

```python
parts = ["cat", "dog"]
context = "\n\n".join(parts)
length = len(context)  # 8
```

分隔符字符串的 `.join(parts)` 会将该分隔符置于各字符串之间，首个字符串之前或末尾字符串之后均不添加。
每个 `\n` 表示一个换行符，因此连接两个片段的长度为其各自长度之和再加上 2。

按匹配顺序包含完整的片段。
这是一种贪心前缀选择：如果下一个可用片段能够容纳，则接受它；一旦遇到第一个无法容纳的可用片段，便停止选择。
保持前缀可以保留选择顺序。
不要截断文本，也不要在后续匹配中寻找更短的片段来替代。
未知的标识符没有对应的片段，跳过即可，无需终止选择。

### 组装文本

实现 `assemble_context(matches, texts, budget)` 并返回组装后的字符串，且不得修改输入。

- `matches` 必须是非空字符串 ID 的列表。
  允许存在重复的 ID，每个出现的 ID 都会按顺序予以考虑。
- `texts` 必须是一个字典，其键为非空字符串 ID，值为字符串。
  请原样保留每个片段，包括空白字符。
  空字符串也是有效的片段。
- `budget` 必须是介于 `0` 到 `10000`（含）之间的整数。
  需显式拒绝布尔值：`isinstance(True, int)` 结果为 true。
- 在选择之前验证所有输入的结构与格式，包括匹配项未使用的字典条目。
  对于任何无效输入，返回 `None`。

已包含的空片段仍会占用一个位置。
因此，任何后续片段都需要其两个字符的分隔符。
预算为 0 时可以包含一个空的第一个片段，但不能包含非空文本。
当未包含任何内容时返回 `""`；这也代表单独包含一个空片段的情况。

### 解答

```python
def assemble_context(matches, texts, budget):
    if isinstance(budget, bool) or not isinstance(budget, int) or not 0 <= budget <= 10000:
        return None
    if not isinstance(matches, list) or not isinstance(texts, dict):
        return None
    for identifier in matches:
        if not isinstance(identifier, str) or not identifier:
            return None
    for identifier, text in texts.items():
        if not isinstance(identifier, str) or not identifier or not isinstance(text, str):
            return None
    snippets = []
    used = 0
    for identifier in matches:
        if identifier not in texts:
            continue
        snippet = texts[identifier]
        cost = len(snippet)
        if snippets:
            cost += 2
        if used + cost > budget:
            break
        snippets.append(snippet)
        used += cost
    return "\n\n".join(snippets)
```
