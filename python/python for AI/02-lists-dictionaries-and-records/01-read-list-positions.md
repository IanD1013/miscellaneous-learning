列表（list）按顺序保存各个值。
列表字面量将逗号分隔的元素放在方括号之间；`[]` 会创建一个空列表。
在此之前，给出的单元素返回列表用于保存参数，给出的双元素返回列表用于将两个计算出的输出组合在一起。
这些前置内容将列表用作返回容器。
现在你可以读取单个位置并对元素计数了：

```python
values = ["alpha", "beta"]
first = values[0]
count = len(values)
empty = []
```

`values` 后面的方括号用于选择一个元素。
方括号内的数字是其索引（index），即位置编号。
Python 使用从零开始的索引：`values[0]` 是 `"alpha"`，而 `values[1]` 是 `"beta"`。
该赋值操作读取了该元素但并未将其移除。
当你只需要一个值时，读取是一种安全的方法；就地（in place）修改列表同时也会改变调用方所持有的列表。

`len(values)` 将该列表传入并调用内置的 `len` 函数，返回其元素数量，此处为 `2`。
对于 `empty`，`len(empty)` 为 `0`。
空列表不存在位置零，因此读取 `empty[0]` 会引发 `IndexError`。
在访问元素之前请先检查长度；`len(values) == 0` 是用于空列表情况的判断条件。

已编写完成的 `_observe_first(values)` 辅助函数会调用你的函数，并将其结果放入一个单元素列表中。
例如，在你的函数正常工作后：

```python
_observe_first(["label", 4])  # 返回 ["label"]
_observe_first([[2, 3], 0])  # 返回 [[2, 3]]
```

在第二次调用中，第一个元素本身就是一个列表。
辅助函数的外层方括号包含了这整个元素；它们不会将其扁平化，也不会将其转换为文本。
请保持此辅助函数不变，仅实现 `first_or_none(values)`。
你的函数返回元素本身；辅助函数则提供包含它的外层列表。

完成 `first_or_none(values)`。
输入是一个包含数字、字符串、布尔值、`None` 或其他列表的列表：

- 当列表为空时返回 `None`。
- 否则，原样返回其第一个元素，即使该元素为 `0`、`False` 或 `None`。

使用长度来判断是否存在第一个位置。
存储在那里的值并不能用来判断列表是否为空。

### 解答

```python
def first_or_none(values):
    if len(values) == 0:
        return None
    return values[0]

def _observe_first(values):
    return [first_or_none(values)]
```
