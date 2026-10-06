当你需要一个小型的"记录"类型，也就是一组具名字段时，Python 为你提供了几种选择，让你不必手写样板代码（boilerplate）。
`@dataclass` 为一个可变类生成那些管道性质的方法。
`enum.Enum` 定义一组固定的具名常量。
`NamedTuple` 和 `namedtuple` 为你提供一个带有具名字段的不可变（immutable）元组。
面试官会问到这些，因为它们能揭示你是否会选用合适的轻量级工具，而不是写一个完整的类，再手动实现 `__init__`、`__repr__` 和 `__eq__`。

### @dataclass 基础

`@dataclass` 装饰器会读取类级别的注解（annotation），并为你生成 `__init__`、`__repr__` 和 `__eq__`。
你把字段声明为带注解的属性。

```python
from dataclasses import dataclass

@dataclass
class Point:
    x: int
    y: int

p = Point(1, 2)
print(p)          # Point(x=1, y=2)   <- 生成的 __repr__
print(p == Point(1, 2))   # True       <- 生成的 __eq__ 比较字段值
```

如果没有 `@dataclass`，两个内容相同的独立对象比较时会不相等（默认的 `__eq__` 比较的是身份）。
生成的 `__eq__` 比较的是字段值组成的元组，而生成的 `__repr__` 会显示每一个字段。

注解是必需的。
一个没有注解的普通赋值会被当作普通的类属性，而不是 dataclass 字段，所以它不会成为 `__init__` 的参数。

### 默认值和 default\_factory

你可以给字段一个默认值，就像普通函数的默认值一样。
有默认值的字段必须放在没有默认值的字段之后，原因与普通函数参数相同。

```python
@dataclass
class User:
    name: str
    active: bool = True
```

陷阱在于可变的默认值。
你不能写 `tags: list = []`，因为这一个列表会被每个实例共享（与可变默认参数是同一个问题）。
dataclass 会在类定义时主动用一个 `ValueError` 拒绝这种写法。
请改用 `field(default_factory=...)`，它会为每个实例调用一次工厂函数。

```python
from dataclasses import dataclass, field

@dataclass
class Cart:
    items: list = field(default_factory=list)

a = Cart()
b = Cart()
a.items.append("apple")
print(a.items)   # ['apple']
print(b.items)   # []   <- 每个实例都得到了它自己的列表
```

### enum.Enum

`Enum` 是一组具名的常量成员。
每个成员都有一个 `.name`（标识符）和一个 `.value`（你赋的值）。
成员是单例（singleton），所以 `is` 比较是有效的。

```python
from enum import Enum

class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

print(Color.RED)         # Color.RED
print(Color.RED.name)    # 'RED'
print(Color.RED.value)   # 1
print(Color.RED is Color.RED)   # True
```

你可以迭代这个类，按定义顺序得到各个成员，也可以用调用语法按值查找成员，或者用下标按名称查找成员。

```python
list(Color)          # [<Color.RED: 1>, <Color.GREEN: 2>, <Color.BLUE: 3>]
Color(2)             # <Color.GREEN: 2>   （按值查找）
Color['GREEN']       # <Color.GREEN: 2>   （按名称查找）
```

当你不关心具体的值时，`auto()` 会为你分配它们，从 1 开始。

```python
from enum import Enum, auto

class State(Enum):
    PENDING = auto()   # 1
    ACTIVE = auto()    # 2
    CLOSED = auto()    # 3
```

### NamedTuple 和 namedtuple

具名元组（named tuple）是一个不可变的元组，它的各个位置同时也有名字。
它是一个真正的元组，所以它可以像元组一样解包、索引和比较，但 `.field` 访问比 `[0]` 更清晰。
有两种方式可以创建它。
较老的工厂函数是 `collections.namedtuple`；带类型的类形式是 `typing.NamedTuple`。

```python
from collections import namedtuple
Point = namedtuple("Point", ["x", "y"])

from typing import NamedTuple
class Point(NamedTuple):
    x: int
    y: int

p = Point(1, 2)
print(p.x, p[0])     # 1 1   （名称和索引都可以用）
print(tuple(p))      # (1, 2)
a, b = p             # 解包可以用，它是一个元组
```

因为它是一个元组，所以它是不可变的：`p.x = 5` 会抛出 `AttributeError`。
要得到一个修改过的副本，使用 `_replace`，它会返回一个新的具名元组。

```python
p2 = p._replace(x=99)   # Point(x=99, y=2)，p 没有改变
```

### 何时选用哪一个

- 带有行为或有很多字段的可变记录，并且你想要相等性比较和可读的 repr：`@dataclass`。
- 一组固定的、封闭的具名常量（状态、类别、选项）：`Enum`。
- 一个小型的不可变记录，尤其是你希望它表现得像元组（解包、从函数返回多个值）时：`NamedTuple`。

dataclass 不等于元组，并且默认是可变的；具名元组等于由其值组成的普通元组，并且不能被重新赋值。
