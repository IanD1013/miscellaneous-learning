模式验证（Schema validation）会在使用数据之前，检查其是否包含必填字段以及可接受的值。
解析 JSON 会返回 Python 值；但这并不能确定响应是否具有应用程序所期望的结构形态。

在本练习中，一个已经解析好的响应字典包含两个必填字段：`answer` 存放响应文本，`confidence` 存放 0 到 1 之间的数值评分。
这些是提供的测试固件值（fixture values）。
验证它们的数据结构形态并不能证明答案是正确的，也无法证明评分能否准确预测准确性。

字段检查可以使用你已经掌握的验证和字典操作：

```python
if not isinstance(data, dict):
    return None
text = data.get("answer")
if not isinstance(text, str):
    return None
```

先检查字典可以使查找操作更安全。
在未传入默认参数的情况下，`.get()` 在字段缺失时会返回 `None`，这将无法通过字符串检查。
空字符串的类型仍然是 `str`；请勿使用真值测试（truth test）将其拒绝。

对于数值类型，`isinstance(score, (int, float))` 可以接受这两种类型中的任意一种：元组提供了备选类型。
在此检查中，Python 还会将布尔值视为整数，因此需要显式排除 `isinstance(score, bool)`。
置信度必须是有限数值（finite），即既不是无穷大也不是 NaN（非数字），并且满足 `0 <= score <= 1`。
要求该链式比较为真也会同时排除这些非有限值。
在四舍五入之前验证原始分数：不能让刚好超出区间的数值因四舍五入而变成可接受的值。

### 构建验证后的结果

完成 `validate_answer(data)`。
只要字典、必填字段、类型或置信度区间未能通过这些检查，就返回 `None`。
否则，返回一个仅包含 `answer` 和 `confidence` 的新字典，并按此顺序排列。
保持文本不变，并使用 `round(score, 6)` 将置信度保留六位小数；这会返回一个数值，而不是固定宽度的文本。
仅选择这两个字段是一种投影（projection）操作：允许输入包含额外字段，但在结果中将它们忽略。
请保持输入的字典不变。

### 解答

```python
def validate_answer(data):
    if not isinstance(data, dict):
        return None
    text = data.get("answer")
    if not isinstance(text, str):
        return None
    score = data.get("confidence")
    if isinstance(score, bool) or not isinstance(score, (int, float)):
        return None
    if not 0 <= score <= 1:
        return None
    return {"answer": text, "confidence": round(score, 6)}
```
