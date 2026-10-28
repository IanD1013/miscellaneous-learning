列表推导式（list comprehension）和生成器表达式（generator expression）看起来几乎一模一样，但它们的行为却大不相同。
列表推导式会立即在内存中构建出整个列表。
生成器表达式不会预先构建任何东西；它交给你一个惰性对象，在你索取时逐个产出值。
知道何时选择哪一个是一个常见的面试考察点，因为选错的话，要么会浪费内存，要么会破坏那些期望得到真正列表的代码。
本节课涵盖语法上的差异、惰性求值与立即求值（lazy versus eager evaluation）、生成器在内存和短路（short-circuiting）上的优势、把生成器表达式作为唯一函数参数传递时的规则，以及如何在两者之间做出选择。

### 语法：方括号 vs 圆括号

唯一可见的差异就是括号。
方括号 `[]` 得到的是列表推导式。
圆括号 `()` 得到的是生成器表达式。

```python
squares_list = [n * n for n in range(5)]   # [0, 1, 4, 9, 16]
squares_gen = (n * n for n in range(5))     # <generator object ...>
```

列表版本是一个已经完成的列表。
生成器版本是一个还没有计算任何东西的生成器对象。
打印它显示的是类似 `<generator object <genexpr> at 0x...>` 的内容，而不是那些值。

### 惰性求值 vs 立即求值

列表推导式会立即运行整个循环并存储每一个结果。
生成器表达式只有在你取值时才运行循环体，每次 `next()` 调用取一个（这正是 `for` 循环在底层所做的事情）。

```python
def loud(n):
    print(f"making {n}")
    return n

gen = (loud(n) for n in range(3))   # 还没有打印任何内容
print("created")
first = next(gen)                   # 现在打印 "making 0"
```

因为工作被推迟了，生成器可以描述一个无限或巨大的序列，而永远不需要真正构建它。
生成器也是单次遍历的：一旦你消费了它，它就空了。
第二次迭代它不会产出任何东西。

```python
gen = (n for n in range(3))
print(list(gen))   # [0, 1, 2]
print(list(gen))   # []  生成器已经被耗尽
```

### 内存与短路

列表推导式会为每一个元素分配空间。
生成器只持有它的当前状态，所以无论序列有多长，它都保持很小。
对生成器调用 `sys.getsizeof` 返回一个很小的常数；对一个大列表调用则会返回一个很大的数字。

更大的优势在于短路。
像 `any`、`all`、`next` 和 `in` 这样的函数一旦得到答案就会停止。
把生成器传给它们，答案之后的工作就永远不会发生。

```python
nums = range(1, 10_000_000)
# 在第一个匹配处停止，不构建任何东西
has_big = any(n > 5 for n in nums)
```

如果你写的是 `any([n > 5 for n in nums])`，列表推导式会先构建全部一千万个布尔值，然后 `any` 再去扫描它们。
生成器版本只检查一个值就停止了。

### 把生成器表达式作为唯一参数传递

当生成器表达式是函数调用的唯一参数时，你不需要再加一对括号。
调用的括号同时充当了生成器的括号。

```python
total = sum(n * n for n in range(5))     # 没问题，不需要额外的括号
count = len(x for x in data)             # TypeError: generators have no len()
```

但如果调用中还有其他参数，生成器表达式就必须用它自己的括号包起来，否则 Python 会抛出 `SyntaxError`。

```python
import math
math.hypot(x for x in pts)               # 没有内层括号时会 SyntaxError
math.hypot(*(x for x in pts))            # 这里必须显式加括号
```

注意 `len()` 完全不能用于生成器，因为生成器事先并不知道自己的长度。
当你需要计数时，使用列表，或者 `sum(1 for _ in gen)`。

### 如何选择

当你只会消费这些值一次，并把它们直接传给某个会进行迭代的东西时，使用生成器表达式：`sum`、`any`、`all`、`max`、`min`、`join`、`for` 循环。
它能节省内存，并且可以短路。

当你需要一个真正的列表时，使用列表推导式：你要对它进行索引、对它循环不止一次、检查它的 `len`、对它切片，或者把它返回给调用者保存。
在这些场景下选用生成器，只会迫使你之后再额外调用一次 `list(...)`。

```python
names = ", ".join(name.title() for name in raw)   # 生成器表达式，只消费一次
evens = [n for n in data if n % 2 == 0]            # 列表，会被复用和索引
```
