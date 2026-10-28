固定 embedding 是用于表示某个条目的给定数值向量。
按照与查询向量（query vector）的余弦相似度对这些向量进行排序：得分较高的排在前面。
四舍五入后相同的得分也需要保持一致的顺序，以便每次检索时结果不会重新排列。

每个输入记录都是一个字典，例如 `{'id': 'note-a', 'vector': [1, 0]}`。
其 `id` 用于标识该条目；其 `vector` 保存 embedding。
每个结果仅包含 `id` 和 `score`，其中 `score` 是四舍五入后的相似度。
Python 字典保留键的插入顺序，这也决定了它们的显示表现形式。
构造每个结果时，将 `id` 放在第一位，`score` 放在第二位，如 `{'id': 'note-a', 'score': 1.0}`，这样每一行都会在得分之前显示其标识符。

提供的 `cosine_similarity(left, right)` 辅助函数在通过 `math.hypot` 计算向量大小之前，会先用每个非零向量的最大绝对值分量对其进行缩放。
然后它计算归一化点积并保留六位小数。
请保持该函数不变。
对于无效向量，它返回 `None`：任一参数必须是包含 1 到 64 个分量的列表，两个长度必须匹配，且分量必须是 -1000 到 1000（包含）之间的有限整数或浮点数，布尔值除外。
向量必须至少包含一个非零分量；极小的非零值也是有效的。
调用 `cosine_similarity(query, query)` 可以在没有任何记录的情况下验证查询向量。

为了实现稳定排序，先按四舍五入后的得分降序排列，再按 ID 升序排列。
升序元组键可以同时表示这两个方向：

```python
scored = [{'id': 'b', 'score': 0.8}, {'id': 'a', 'score': 0.8}]
ordered = sorted(scored, key=lambda item: (-item['score'], item['id']))
```

对得分取反可以使较高的得分排在前面；元组的第二个值用于解决得分相同的情况。
`sorted` 会返回一个新列表，因此将得分存入一个单独的列表并对该列表进行排序，可以避免重新排列调用者的记录。
当两个键值都匹配时，Python 的稳定排序会保留原有的出现顺序。
因此，重复的 ID 仍然会保留为独立的行，包括相同的得分/ID 对。

### 对记录进行排序

完成 `rank_embeddings(query, records)`。
如果查询无效、`records` 的值不是列表，或者任何记录不是包含 `id` 和 `vector` 的字典，则返回 `None`。
ID 必须是非空字符串；无效的 ID 也会导致整个调用返回 `None`。

忽略那些向量无效、全为零或维度错误的记录。
返回剩余的字典，其键按 `id` 后接 `score` 的顺序插入，并按照上述得分和 ID 规则进行排序。
空记录或没有可用向量的记录应返回 `[]`。

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
```
