通过从一个新的空列表开始，并添加满足条件的每个值，来构建一个筛选后的列表。
`append` 会将一个元素添加到列表末尾：

```python
selected = []
selected.append(8)
selected.append(3)
```

`selected` 现在包含 `[8, 3]`。
句点调用该列表上的 `append`，括号中包含要添加的元素。
该调用会修改列表并返回 `None`，因此请将其作为独立语句使用，而不是将其返回值赋值给 `selected`。

要直接访问列表中的元素，请编写 `for value in values:`。
每次迭代都会按列表的原有顺序将下一个元素赋给 `value`。
在循环内部放置一个 `if` 来决定追加哪些元素。
比较操作 `value >= 0` 表示大于或等于零，因此零也符合条件。

一种安全的方法是在函数内部、循环之前用 `[]` 创建一个单独的结果列表。
向该列表追加元素可以保持调用者的输入不受修改；就地修改输入可能会影响仍在使用该输入的代码。
在遇到符合条件的元素时追加它们；重复的值仍保持为单独的元素。
在循环结束后返回结果，包括在没有要添加的元素时。

### 练习

完成针对整数列表的 `keep_nonnegative(values)`。
返回一个包含所有非负值的列表，并保留其原始顺序和重复项。
空输入以及仅包含负值的输入必须返回 `[]`。

### 解答

```python
def keep_nonnegative(values):
    result = []
    for value in values:
        if value >= 0:
            result.append(value)
    return result
```
