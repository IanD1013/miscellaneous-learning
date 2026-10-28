检索阈值（retrieval threshold）是结果必须达到的最低相似度得分。
应用该阈值时应包含边界值：得分等于阈值的结果予以保留。
然后取前 k 个（top k），即按排名顺序排列的前 `k` 个合格结果。
请求五个结果并不要求在仅有两个合格时也返回五个。

筛选步骤可以使用普通循环，随后进行切片：

```python
scores = [0.9, 0.6, 0.2]
selected = []
for score in scores:
    if score >= 0.6:
        selected.append(score)
first_two = selected[:2]
```

`selected` 包含 `[0.9, 0.6]`。
过滤决定资格；切片限制数量。
切片会保留原有顺序，并在列表长度小于其上限时安全地返回较少的项。

提供的 `rank_embeddings(query, records)` 已经返回包含 `id` 和 `score` 的字典，按得分降序排序，平局时按 ID 升序排序。
得分四舍五入保留六位小数；将这些返回的得分与阈值进行比较。
请保持提供的两个辅助函数不变。

该辅助函数还负责输入验证。
查询必须是一个非零列表，包含 1 到 64 个数值分量，每个分量在 -1000 到 1000 之间（含边界），布尔值除外。
极小的非零向量也是有效的。
`records` 必须是一个字典列表，每个字典包含 `id` 和 `vector`，且 ID 为非空字符串。
允许包含额外字段。
格式错误的记录会导致排序返回 `None`；不可用的向量会被跳过，包括零向量、无效分量或维度不匹配。
有效的空记录列表将返回 `[]`。

### 完成筛选逻辑

在不更改输入的前提下实现 `retrieve_matches(query, records, k, threshold)`：

- 仅接受 `k` 为 0 到 100 之间（含边界）的整数，布尔值除外。
- 仅接受 `threshold` 为 -1 到 1 之间（含边界）的有限整数或浮点数，布尔值除外。
  对于无效的控制参数返回 `None`。
- 调用排序辅助函数并传递其 `None` 结果，即使 `k` 为零也是如此。
  请求零个结果并不能免除对无效查询或记录数据的检查。
- 收集 `score >= threshold` 的排序项，然后使用切片返回前 `k` 个。
  保留辅助函数的顺序和结果字典。
  无匹配项的有效输入，或 `k` 等于零时，返回 `[]`。

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
```
