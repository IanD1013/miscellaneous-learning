检索准备将你已经编写的辅助函数连接起来：验证语料库、筛选排序后的匹配项、组装它们的文本，并构建消息有效负载（payload）。
所选的 ID 与组装的上下文描述了不同的决策。
一个匹配项可以通过相似度阈值，即使其文本超出了上下文预算限制。

### 连接辅助函数

每个语料库记录包含用于标识记录的 `id`、作为上下文包含的 `text`，以及用于与查询进行比较的 `vector`。
为 `retrieve_matches` 构建一个 `id`/`vector` 记录列表，并为 `assemble_context` 构建一个 ID 到文本的字典映射。
这两种转换都不应修改调用方的数据。

`retrieve_matches(query, records, k, threshold)` 使用 `rank_embeddings` 将分数从高到低排序，如果分数相同则按 ID 升序决胜。
它保留大于或等于阈值的分数，并最多选择 `k` 条记录。
在调用 `assemble_context(identifiers, texts, budget)` 之前，按该顺序提取它们的 ID。

上下文辅助函数包含完整的片段，片段之间用 `"\n\n"` 分隔，分隔符的字符也计入预算。
它会在遇到第一个导致超出预算的片段时停止。
即使组装提前停止，也要保留每一个已选出的 ID。
在结果中保持组装后的上下文不变。

### 完成工作流

使用提供的辅助函数实现 `prepare_retrieval(query, corpus, k, threshold, budget, question)`。
不要修改它们的代码。
如果输入无效或辅助函数执行失败，则返回 `None`：

- `corpus` 必须是包含 `id`、`text` 和 `vector` 的字典列表；允许包含额外字段。
  ID 必须是非空字符串，且在整个语料库中唯一。
  文本必须是字符串，包括可能为空字符串。
- 查询和记录向量必须是非零长度且维度匹配的列表，维度范围为 1 到 64。
  每个分量必须是 -1000 到 1000 之间的整数或浮点数（排除布尔值）。
  使用 `cosine_similarity(query, record['vector'])` 检查每条记录：无效的向量将导致拒绝整个语料库，即使仅做排序会跳过该记录。
- `k` 必须是 0 到 100 之间的整数；`threshold` 是 -1 到 1 之间的整数或浮点数；`budget` 是 0 到 10000 之间的整数。
  布尔值属于无效控制参数。
  即使语料库为空或 `k == 0`，这些检查以及查询验证依然适用。
- `question` 必须是一个经过 `.strip()` 后依然非空的字符串。

系统文本必须严格以 `"Answer using only the supplied context."` 开头。
当上下文非空时，追加两个换行符和上下文；否则仅使用指导语本身。
将此文本和经过 strip 处理的问题传递给 `build_messages`。
该辅助函数会去除两条消息内容的外层空白字符，因此系统消息可能会丢失尾部的上下文空白，而返回的上下文仍保留它。

返回一个按以下顺序插入键的字典：`ids`、`context`、`messages`。
消息按系统、用户的顺序排列，每个消息的 `role` 都在 `content` 之前。
此函数使用固定向量准备数据；它不会调用模型。

### 解答

```python
# 提供的辅助函数，请保持不变。
import math


def cosine_similarity(left, right):
    if not isinstance(left, list) or not isinstance(right, list):
        return None
    if len(left) != len(right) or not 1 <= len(left) <= 64:
        return None
    unit_vectors = []
    for vector in [left, right]:
        scale = 0.0
        for value in vector:
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                return None
            if not -1000 <= value <= 1000:
                return None
            scale = max(scale, abs(value))
        if scale == 0:
            return None
        scaled = []
        magnitude = 0.0
        for value in vector:
            component = value / scale
            scaled.append(component)
            magnitude = math.hypot(magnitude, component)
        unit = []
        for component in scaled:
            unit.append(component / magnitude)
        unit_vectors.append(unit)
    score = 0.0
    for left_value, right_value in zip(unit_vectors[0], unit_vectors[1]):
        score += left_value * right_value
    result = round(score, 6)
    if result == 0:
        return 0.0
    return result

def rank_embeddings(query, records):
    if cosine_similarity(query, query) is None:
        return None
    if not isinstance(records, list):
        return None
    scored = []
    for record in records:
        if not isinstance(record, dict) or 'id' not in record or 'vector' not in record:
            return None
        if not isinstance(record['id'], str) or not record['id']:
            return None
        score = cosine_similarity(query, record['vector'])
        if score is not None:
            scored.append({'id': record['id'], 'score': score})
    return sorted(scored, key=lambda item: (-item['score'], item['id']))

def retrieve_matches(query, records, k, threshold):
    if isinstance(k, bool) or not isinstance(k, int) or not 0 <= k <= 100:
        return None
    if isinstance(threshold, bool) or not isinstance(threshold, (int, float)):
        return None
    if not -1 <= threshold <= 1:
        return None
    ranked = rank_embeddings(query, records)
    if ranked is None:
        return None
    matches = []
    for item in ranked:
        if item['score'] >= threshold:
            matches.append(item)
    return matches[:k]

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
    return '\n\n'.join(snippets)

def build_messages(system_text, user_text):
    if not isinstance(system_text, str) or not isinstance(user_text, str):
        return None
    system_text = system_text.strip()
    user_text = user_text.strip()
    if not system_text or not user_text:
        return None
    return [{"role": "system", "content": system_text}, {"role": "user", "content": user_text}]

def prepare_retrieval(query, corpus, k, threshold, budget, question):
    if not isinstance(corpus, list):
        return None
    texts = {}
    for record in corpus:
        if not isinstance(record, dict):
            return None
        if 'id' not in record or 'text' not in record or 'vector' not in record:
            return None
        identifier = record['id']
        if not isinstance(identifier, str) or not identifier or identifier in texts:
            return None
        if not isinstance(record['text'], str):
            return None
        if cosine_similarity(query, record['vector']) is None:
            return None
        texts[identifier] = record['text']
    if not isinstance(question, str) or not question.strip():
        return None
    matches = retrieve_matches(query, corpus, k, threshold)
    if matches is None:
        return None
    ids = []
    for match in matches:
        ids.append(match['id'])
    context = assemble_context(ids, texts, budget)
    if context is None:
        return None
    system_text = "Answer using only the supplied context."
    if context:
        system_text += "\n\n" + context
    messages = build_messages(system_text, question.strip())
    if messages is None:
        return None
    return {"ids": ids, "context": context, "messages": messages}
```
