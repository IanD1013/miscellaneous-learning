Python 的 `for` 循环会将序列中的每个值赋给循环变量，并针对该值执行一次缩进的代码块。
此函数用于统计它访问了多少个值：

```python
def count_visits():
    visits = 0
    for number in range(3):
        visits += 1
    return visits
```

在 `for number in range(3):` 中，`in` 将变量与序列连接起来，冒号则开启循环体。
`range(3)` 依次提供整数 `0`、`1` 和 `2`。
`number` 是循环变量，有时也被称为归纳变量（induction variable）：Python 会在每次迭代时自动为其赋下一个值。
你不需要手动对其进行递增。

`range(stop)` 从零开始，且不包含 `stop`。
这使得它成为一个半开区间（half-open range）：包含起始值，排除终止值。
`range(0)` 不提供任何值，因此其循环体永远不会执行。

`visits` 是一个累加器（accumulator），即一个用于保存累计结果的变量。
请在循环之前对其进行初始化，以便先前的计算结果能够在每次迭代中保留下来。
在此处，`visits += 1` 意味着 `visits = visits + 1`。
额外的缩进使该更新操作成为循环的一部分。
`return` 与 `for` 对齐，因此它在所有迭代完成后才运行；该函数返回 `3`。

### 你的任务

针对非负整数 `stop` 完成 `sum_below(stop)`。
练习在 `range(stop)` 上使用 `for` 循环，将每个遍历到的整数累加到累加器中，然后返回总和。
如果没有可相加的值，则返回 `0`。

### 解答

```python
def sum_below(stop):
    total = 0
    for number in range(stop):
        total += number
    return total
```
