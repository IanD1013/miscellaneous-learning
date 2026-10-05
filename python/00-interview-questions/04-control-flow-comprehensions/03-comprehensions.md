推导式（comprehension）在单个表达式中从一个已有的可迭代对象（iterable）构建一个新集合。
Python 有三种：列表、集合和字典推导式。
还有生成器表达式（generator expression），它是惰性的（lazy）兄弟，一次产生一个值，而不是预先构建出整个集合。

面试官喜欢考推导式，因为它们能看出你是否理解迭代、过滤，以及立即求值（eager evaluation）和惰性求值（lazy evaluation）之间的区别。
陷阱集中在嵌套循环的顺序、过滤子句，以及在你想要一个列表时意外构建出一个生成器。

### 三种集合推导式

形状是相同的：一个输出表达式、一个或多个 `for` 子句，以及可选的 `if` 过滤器。
只有外围的括号和输出表达式会变化。

```python
nums = [1, 2, 3, 4]

squares = [n * n for n in nums]        # 列表   -> [1, 4, 9, 16]
unique = {n % 2 for n in nums}         # 集合   -> {0, 1}
table = {n: n * n for n in nums}       # 字典   -> {1: 1, 2: 4, 3: 9, 4: 16}
```

列表推导式使用 `[]`，集合推导式使用带单个值的 `{}`，字典推导式使用带 `key: value` 对的 `{}`。
注意 `{x for x in ...}` 是集合推导式，而 `{k: v for ...}` 是字典推导式。
没有元组推导式：`(x for x in nums)` 是一个生成器表达式，而不是元组。

### 过滤（if）子句

`for` 子句之后的 `if` 只保留通过测试的元素。
它做过滤；它不做转换。

```python
evens = [n for n in range(10) if n % 2 == 0]   # [0, 2, 4, 6, 8]
```

这个末尾的 `if` 不能带 `else`。
如果你需要在两个值之间选择，那就是放在输出位置上的条件表达式（conditional expression），它总是产生一个值：

```python
labels = ["even" if n % 2 == 0 else "odd" for n in range(4)]
# ['even', 'odd', 'even', 'odd']
```

所以末尾的 `if` 把元素过滤掉，而前面的 `... if ... else ...` 为每个元素选择一个值。

### 多个 for 子句与嵌套循环

你可以串联多个 `for` 子句。
它们从左到右读取，顺序与你编写嵌套 `for` 循环的顺序相同，所以最左边的循环是外层循环。

```python
pairs = [(x, y) for x in [1, 2] for y in ["a", "b"]]
# [(1, 'a'), (1, 'b'), (2, 'a'), (2, 'b')]
```

`x` 循环是外层，`y` 是内层，完全等同于：

```python
pairs = []
for x in [1, 2]:
    for y in ["a", "b"]:
        pairs.append((x, y))
```

后面的 `for` 子句可以依赖前面的子句，这就是你展平（flatten）嵌套结构的方式：

```python
matrix = [[1, 2], [3, 4]]
flat = [item for row in matrix for item in row]   # [1, 2, 3, 4]
```

不要把它和嵌套推导式（nested comprehension）混淆，嵌套推导式是把一整个推导式放在输出位置上。
下面这个转置了一个矩阵：

```python
matrix = [[1, 2, 3], [4, 5, 6]]
transposed = [[row[i] for row in matrix] for i in range(3)]
# [[1, 4], [2, 5], [3, 6]]
```

这里内层的 `[row[i] for row in matrix]` 对每个 `i` 运行一次。

### 为什么用推导式而不是在循环中 append

推导式用一个表达式表达"构建一个由这些东西组成的列表"。
与创建一个空列表然后在循环中调用 `.append` 相比，它更短，不会在构建过程中把一个构建了一半的列表泄漏到作用域中，并且循环变量不会泄漏到外围作用域（在 Python 3 中，推导式有自己的作用域）。
它通常也更快，因为 append 是在内部处理的，而不是通过重复的属性查找。
只有当循环体需要单个表达式无法容纳的语句时，才使用循环中的 `append`，比如 `try`/`except` 或带副作用的分支。

### 生成器表达式：惰性的兄弟

把方括号换成圆括号，你就得到一个生成器表达式。
它不构建集合。
它在你迭代时按需产生值，所以它占用很少的内存，并且可以短路（short-circuit）。

```python
gen = (n * n for n in range(1_000_000))   # 还没有计算任何东西
print(next(gen))                          # 0
print(any(n > 100 for n in range(50)))    # True，在 n == 11 时提前停止
```

当生成器表达式是函数的唯一参数时，你可以省略多余的圆括号：`sum(x * x for x in nums)` 是没问题的。
生成器是一次性的；一旦耗尽，它就不再产生任何值。
当你需要多次使用结果，或者需要索引或 `len` 时，使用列表推导式；当你只遍历一次，或者把它传给 `sum`、`any`、`all`、`max` 或 `min` 时，使用生成器表达式。
