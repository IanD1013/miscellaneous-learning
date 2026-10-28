生成器（generator）是一种逐个产出值的函数，而不是预先把所有值都构建好再返回一个列表。
把一个普通函数变成生成器的标志是 `yield` 关键字。
任何包含 `yield` 的函数都会变成生成器函数：调用它并不会运行函数体，而是返回一个你可以迭代的生成器对象。
面试官会用生成器来检验你是否理解惰性求值（lazy evaluation）、暂停的状态，以及与列表相比在内存上的取舍。

### 调用生成器并不会运行它

当一个函数的函数体中有 `yield` 时，调用它会立即返回一个生成器对象。
此时还没有任何代码运行。

```python
def counter():
    print("starting")
    yield 1
    yield 2

g = counter()        # 还没有打印任何内容
print(type(g))       # <class 'generator'>
print(next(g))       # 打印 "starting"，然后是 1
print(next(g))       # 2
```

只有当你通过 `next()` 或 `for` 循环取值时，函数体才会运行。
第一次 `next(g)` 会运行到第一个 `yield` 并在那里暂停。

### 暂停与恢复会保留局部状态

每个 `yield` 都会把一个值交还给调用者，并把函数冻结在它当前所在的位置，包括局部变量以及在任何循环中的位置。
下一次请求会从紧接着那个 `yield` 之后的地方恢复执行。

```python
def gen():
    total = 0
    for n in (10, 20, 30):
        total += n
        yield total

print(list(gen()))   # [10, 30, 60]
```

`total` 能在多次 yield 之间保留下来，因为栈帧（frame）是被挂起了，而不是被销毁了。
这是它与普通函数的核心区别，普通函数一旦返回就会丢失它的局部变量。

### 生成器就是迭代器

生成器对象是它自己的迭代器。
它同时拥有 `__iter__`（返回自身）和 `__next__`，所以它可以直接用于 `for` 循环、`list()`、`sum()`、解包，以及任何其他消费可迭代对象的地方。
你不需要手写 `__iter__`/`__next__`；`yield` 会把两者都提供给你。

```python
def squares(n):
    for i in range(n):
        yield i * i

for s in squares(4):
    print(s, end=" ")   # 0 1 4 9
```

生成器只能被消费一次。
在你把它耗尽之后，再次迭代将不会产出任何东西；你必须再次调用生成器函数来获得一个新的生成器。

```python
g = squares(3)
print(list(g))   # [0, 1, 4]
print(list(g))   # []   已经被耗尽
```

### 迭代何时停止：StopIteration 和 return

当生成器的函数体执行完毕（执行到末尾）或遇到一个不带值的 `return` 时，生成器就结束了。
此时 `next()` 会抛出 `StopIteration`，`for` 循环会静默地捕获它。
在生成器内部，`return` 会提前结束迭代；`return` 上的值不会成为被产出的元素（它会落在 `StopIteration` 上，在这个层面上你很少会去读取它）。

```python
def up_to(limit):
    n = 0
    while n < limit:
        yield n
        n += 1
        if n == 2:
            return        # 提前停止，此后的值永远不会被产出

print(list(up_to(10)))    # [0, 1]
```

### 有限 vs 无界，以及为什么它能节省内存

生成器可以是无界的，因为它只在需要时才计算下一个值。
只要消费者停止索取，一个无限生成器就没有问题。

```python
def naturals():
    n = 0
    while True:
        yield n
        n += 1
```

它从不构建一个巨大的列表，所以无论你走多远，它使用的内存大致都是恒定的。
构建 `[i for i in range(10_000_000)]` 会一次性物化一千万个 int；而等价的生成器 `(i for i in range(10_000_000))` 一次只持有一个值。
当你要流式处理大量或无限制的数据、当你可能会提前停止，或者当你只是把这些值直接传给另一个消费者（比如 `sum()`）时，就选用生成器。
当你需要索引、求 len 或多次迭代时，就选用列表。
