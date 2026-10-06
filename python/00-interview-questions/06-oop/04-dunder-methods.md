Dunder 方法（"double underscore"，双下划线，比如 `__init__` 或 `__str__`）是 Python 代替你调用的钩子（hook）。
你很少直接调用它们。
相反，你写 `len(obj)`，Python 就调用 `obj.__len__()`；或者你写 `print(obj)`，Python 就会查找 `obj.__str__()`。
面试官喜欢考察这一块，因为这些名字看起来像魔法，但规则很简单：一个内置操作对应一个特定的 dunder 方法，如果你定义了这个方法，你就控制了它的行为。

### `__init__` vs `__new__`

`__init__` 是初始化方法（initializer）。
在它运行时，对象已经存在了；`self` 会交给你，你的工作是设置它的属性。
它必须返回 `None`。

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
```

`__new__` 是真正创建并返回新实例的构造方法（constructor）。
它在 `__init__` 之前运行。
对于日常的类，你永远不需要写 `__new__`；来自 `object` 的默认实现就够了。
只有在特殊情况下（不可变类型、单例、元编程）你才会用到它，这些超出了本课的范围。
关键事实：`__new__` 构建对象，`__init__` 配置对象。

### `__str__` vs `__repr__`

两者都为对象生成一个字符串，但它们面向不同的受众。

- `__str__` 是友好、可读的版本。
  它就是 `str(obj)` 和 `print(obj)` 显示的内容。
- `__repr__` 是无歧义、面向开发者的版本。
  它是 REPL 显示的内容，也是当对象位于被打印的容器中时出现的内容。
  惯例是，在可行的情况下，`repr` 应该看起来像能重新创建该对象的有效代码。

```python
class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y
    def __repr__(self):
        return f"Point({self.x}, {self.y})"
    def __str__(self):
        return f"({self.x}, {self.y})"

p = Point(1, 2)
print(p)        # (1, 2)        使用 __str__
print(str(p))   # (1, 2)        使用 __str__
print(repr(p))  # Point(1, 2)   使用 __repr__
print([p])      # [Point(1, 2)] 容器对其元素使用 __repr__
```

如果你只定义了 `__repr__`，那么 `str()` 会回退（fall back）到它，所以 `print(p)` 会显示 `Point(1, 2)`。
如果你只定义了 `__str__`，`repr()` 不会回退；它保持默认的 `<...object at 0x...>`。
这就是为什么通常的建议是：总是定义 `__repr__`，只有当你想要一个单独的面向用户的形式时才添加 `__str__`。

### `__eq__` 和 `__hash__` 的副作用

默认情况下，两个实例之间的 `==` 比较的是身份（identity）（与 `is` 的检查相同）。
定义 `__eq__` 来按值比较。

```python
class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y
    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)
```

这里有一个面试官很喜欢的陷阱：定义 `__eq__` 会把 `__hash__` 设为 `None`，这会使实例变得不可哈希（unhashable）。
你不能再把它们放进 `set` 或用作 `dict` 的键，并且 `hash(obj)` 会抛出 `TypeError`。
Python 这样做是因为两个比较结果相等的对象，其哈希值也应该相等，而它无法猜出你的哈希规则。
如果你需要对象可哈希，就自己定义 `__hash__`，通常基于相同的字段：

```python
    def __hash__(self):
        return hash((self.x, self.y))
```

### 用 `__len__` 和 `__bool__` 决定真值

`len(obj)` 调用 `obj.__len__()`，它必须返回一个非负整数。

真值判断（truthiness）使用一条回退链。
为了判断一个对象是否为真，Python 首先查找 `__bool__`；如果没有，就回退到 `__len__`（零表示假，非零表示真）；如果两者都不存在，该对象永远为真。

```python
class Bag:
    def __init__(self, items):
        self.items = items
    def __len__(self):
        return len(self.items)

bool(Bag([]))      # False  （没有 __bool__，所以 __len__ 返回 0）
bool(Bag([1, 2]))  # True   （__len__ 返回 2）
```

如果两者都定义了，真值检查时 `__bool__` 优先；只有在缺少 `__bool__` 时才会参考 `__len__`。

### 用 `__getitem__` 实现索引

`obj[key]` 调用 `obj.__getitem__(key)`。
在入门层面，这能让你的对象支持方括号访问。

```python
class Deck:
    def __init__(self, cards):
        self.cards = cards
    def __getitem__(self, index):
        return self.cards[index]

d = Deck(["A", "K", "Q"])
d[0]     # 'A'
d[-1]    # 'Q'
```

你收到的 `key` 就是方括号里的任何东西：一个整数、一个切片（slice），或者任何你选择支持的对象。
一个方便的副作用是，一个基于整数索引实现了 `__getitem__` 的对象，即使没有 `__iter__` 也会变成可迭代的（iterable），因为 Python 会依次调用 `obj[0]`、`obj[1]` 等等，直到遇到 `IndexError`。
