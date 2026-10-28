Python 把函数当作普通的值来对待。
你可以把它们存储在变量中，传递给其他函数，也可以作为返回值返回。
`lambda` 是一种以内联方式编写的小型匿名函数（anonymous function），而若干内置函数（`sorted`、`min`、`max`、`map`、`filter`、`any`、`all`、`sum`）都接受一个函数作为参数，这样你就可以描述行为，而不必编写循环。
面试官通过这个主题来考察你是否理解"函数作为参数"到底是什么，以及什么时候推导式（comprehension）比 `map` 或 `filter` 更易读。

### Lambda 语法及其唯一限制

`lambda` 的形式是 `lambda params: expression`。
它没有名字，没有 `return`，也没有语句（statement）：只有一个表达式（expression），其值会被自动返回。

```python
square = lambda x: x * x
square(5)            # 25

add = lambda a, b: a + b
add(3, 4)            # 7
```

函数体必须是单个表达式。
你不能在 lambda 中放入赋值、`if`/`else` 语句、循环或 `try`。
条件*表达式*是可以的，因为它仍然是一个表达式：

```python
sign = lambda n: "neg" if n < 0 else "non-neg"
```

把 lambda 赋值给一个名字（`f = lambda x: ...`）是可行的，但通常不如 `def f(x): ...`，后者会在回溯信息（traceback）中给函数一个真正的名字。
当你需要一个一次性的函数作为参数时，lambda 才能大放异彩。

### 带 key 的 sorted、min、max

`sorted(iterable, key=...)` 返回一个新列表。
`key` 函数会对每个元素调用一次，其结果决定顺序；最终出现在列表中的是原始元素。
`reverse=True` 会反转顺序。

```python
words = ["banana", "kiwi", "fig"]
sorted(words, key=len)              # ['fig', 'kiwi', 'banana']
sorted(words, key=len, reverse=True)  # ['banana', 'kiwi', 'fig']
```

`min` 和 `max` 接受同样的 `key`。
它们返回的是产生最小或最大 key 的那个元素，而不是 key 本身：

```python
people = [("Ada", 36), ("Bob", 25)]
max(people, key=lambda p: p[1])     # ('Ada', 36)
```

一个常见的陷阱：`sorted` 返回一个列表，并且从不修改其参数，而 `list.sort()` 是原地排序并返回 `None`。
写 `x = my_list.sort()` 会让 `x` 变成 `None`。

要同时按两个条件排序，就从 key 中返回一个元组；元组会逐个位置进行比较：

```python
sorted(people, key=lambda p: (p[1], p[0]))   # 先按年龄，再按名字
```

### map 和 filter

`map(func, iterable)` 将 `func` 应用于每一项。
`filter(func, iterable)` 保留 `func` 返回真值（truthy）的那些项。
在 Python 3 中，两者返回的都是惰性迭代器（lazy iterator），而不是列表，所以你通常会用 `list()` 把它们包起来。

```python
nums = [1, 2, 3, 4]
list(map(lambda n: n * 10, nums))        # [10, 20, 30, 40]
list(filter(lambda n: n % 2 == 0, nums)) # [2, 4]
```

因为它们是迭代器，所以遍历一次之后就会被耗尽，并且没有长度：

```python
m = map(str, [1, 2])
list(m)   # ['1', '2']
list(m)   # []  已经被消费
```

`filter(None, iterable)` 是一种特殊形式，它会丢弃假值（falsy）项（`0`、`""`、`None`、空容器）。

### 为什么推导式通常更清晰

列表推导式（list comprehension）可以同时完成 `map` 和 `filter` 的工作，而且通常更易读，尤其是涉及 lambda 的时候。

```python
# map + filter
list(map(lambda n: n * 10, filter(lambda n: n % 2 == 0, nums)))
# 推导式，结果相同
[n * 10 for n in nums if n % 2 == 0]
```

主要在你已经有一个具名函数可以传入时（`map(str, nums)`）才使用 `map`/`filter`，这样可以避免 `lambda x: str(x)` 带来的冗余。

### any、all、sum

如果至少有一项为真值，`any(iterable)` 就是 `True`；如果每一项都为真值，`all(iterable)` 就是 `True`。
经典的陷阱是空的可迭代对象：`any([])` 是 `False`，而 `all([])` 是 `True`（因为没有任何东西不通过测试）。

```python
any(n > 3 for n in nums)   # True
all(n > 0 for n in nums)   # True
all([])                    # True
any([])                    # False
```

你传入一个生成器表达式（generator expression），这样值会被逐个测试，并且两者都会短路（short-circuit）：`any` 在遇到第一个真值时停止，`all` 在遇到第一个假值时停止。

`sum(iterable, start=0)` 从 `start` 开始把数字相加。
你可以用生成器表达式对变换后的视图求和：

```python
sum(n * n for n in nums)   # 30
sum([1.5, 2.5])            # 4.0
```

`sum` 拒绝字符串（`sum(["a", "b"])` 会抛出 `TypeError`）；对字符串请使用 `"".join(...)`。

### 函数作为参数

以上所有这些之所以可行，是因为函数只是一个对象。
你可以通过名字（不带括号）传递一个函数，并在之后调用它：

```python
def apply(func, value):
    return func(value)

apply(str.upper, "hi")     # 'HI'
apply(len, [1, 2, 3])      # 3
```

忘记 `func`（函数对象）和 `func()`（调用它）之间的区别是一个常见的 bug：`sorted(words, key=len)` 传递的是 `len`，而 `key=len()` 会尝试不带参数地调用 `len`，从而失败。
