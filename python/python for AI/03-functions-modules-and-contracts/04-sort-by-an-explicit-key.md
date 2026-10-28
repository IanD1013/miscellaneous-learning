`sorted(values)` 会按升序（从小到大）返回一个新列表。
原列表保持其原有顺序：

```python
values = [8, 2, 5]
ordered = sorted(values)
```

`ordered` 为 `[2, 5, 8]`；`values` 仍为 `[8, 2, 5]`。
添加关键字参数 `reverse=True` 会选择降序，因此最大值排在最前面。

对于字典，可以使用 `key=` 来选择用于比较的字段。
它的参数是一个函数，该函数接收一个列表元素并返回该元素的排序值：

```python
rows = [{"rank": 3}, {"rank": 1}]
ordered = sorted(rows, key=lambda row: row["rank"])
```

这里的 `ordered` 为 `[{"rank": 1}, {"rank": 3}]`。
结果包含完整的字典，而不仅仅是它们的 rank。
`lambda row: row["rank"]` 创建了一个小型函数：`row` 是它的参数，冒号将该参数与表达式隔开，表达式的值会自动返回。
lambda 内部不应包含 `return` 语句。
将此函数传递给 `key=` 会让 `sorted` 为每一行调用它；你不需要在那里自行调用它。

元组（tuple）使用逗号将多个值按固定顺序组合在一起，通常包裹在圆括号内。
类似于 `lambda row: (row["score"], row["id"])` 的多部分键会先比较 score，在 score 相同时再比较 ID。
元组中的第一个位置具有优先级。
这会特意对相同分数的记录按 ID 重新排序。

仅使用分数的键表现则有所不同：Python 的排序是稳定的（stable），这意味着相同键的元素会保留其输入时的顺序。
在设置 `reverse=True` 时也是如此。
如果具有相同分数的 ID `"z"` 和 `"a"` 依序传入，它们将保持该顺序。

直接就地（in-place）重新排序调用者的列表会改变其他代码所看到的内容。
建议使用 `sorted` 单独构建排好序的列表，并在不修改字典字段的情况下读取它们。
新列表仍然包含相同的字典，因此修改其中一个字典也会影响调用者的记录。

### 对记录进行排序

完成 `sort_records(records)`。
每个输入的字典都有一个整数类型的 `"score"` 和一个字符串类型的 `"id"`。
练习上面介绍的 `sorted` 和 lambda 模式，或者使用到目前为止学过的 Python 概念来实现等效的方法。

- 返回一个包含所有输入记录及其字段值的列表，按分数从高到低排序。
- 分数相同时保留输入顺序。
- 正确处理空列表、零分以及负分。

### 解答

```python
def sort_records(records):
    return sorted(records, key=lambda record: record["score"], reverse=True)
```
