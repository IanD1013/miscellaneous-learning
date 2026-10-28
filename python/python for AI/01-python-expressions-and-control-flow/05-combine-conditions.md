`and` 用于组合必须同时成立的条件；`or` 用于组合只要任一成立即可的备选条件。
与比较操作结合使用时，两者都会生成布尔值：

```python
value = 4
positive_small = value > 0 and value < 6
outside = value < 0 or value > 6
inside = not outside
```

这里 `positive_small` 为 `True`，`outside` 为 `False`。
`not` 会反转真值，因此 `inside` 为 `True`。
在条件之间放置 `and` 或 `or`；在要反转的条件之前放置 `not`。

之前的包装练习在其返回的列表中保留了缺失值。
现在来检查它们：Python 的 `None` 表示没有值，对应 JSON 的 `null`。
它与整数零不同。
`is` 用于检查对象标识；使用 `value is None` 来检查这种特定的缺失值，使用 `value is not None` 来检查其相反情况。

```python
value = None
positive = value is not None and value > 0
```

这将返回 `False`，而不会尝试执行会导致错误的 `None > 0`。
Python 从左到右计算 `and`，并在遇到第一个为假（false）的条件时停止。
这就是短路求值（short-circuit evaluation）：一旦剩余表达式无法改变结果，就会被跳过。
`or` 则在遇到第一个为真（true）的条件时停止。
保护条件（guard）必须放在数值比较之前。

### 你的任务

完成 `is_allowed(value, lower, upper)`。
`value` 是整数或 `None`；两个边界都是整数，且 `lower <= upper`。
对于 `None` 返回 `False`。
否则，仅当值在闭区间边界内时返回 `True`。
`>=` 表示大于或等于，`<=` 表示小于或等于，因此两个端点都属于该区间。
练习使用 `and` 连接保护条件和比较操作。

### 解答

```python
def is_allowed(value, lower, upper):
    return value is not None and value >= lower and value <= upper
```
