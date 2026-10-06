类（class）定义了一种新类型：它把其对象将共享的数据和行为打包在一起。
调用类会创建一个实例（instance）：一个拥有自己状态的具体对象。
本课涵盖如何定义类、`__init__` 和 `self` 的作用、实例属性（instance attribute）与类属性（class attribute）的区别、共享可变类属性陷阱，以及在使用层面上属性查找是如何工作的。
掌握好这些，大多数其他面向对象特性都会变得更容易。

### 定义类并创建实例

使用 `class` 定义类，并像调用函数一样调用类来创建实例。

```python
class Dog:
    def __init__(self, name):
        self.name = name

d = Dog("Rex")      # 创建一个实例
print(d.name)       # Rex
print(type(d))      # <class '__main__.Dog'>
print(isinstance(d, Dog))  # True
```

`Dog(...)` 构建一个新对象，在它上面运行 `__init__`，然后把这个对象返回。
每次调用都会产生一个独立的实例。

### `__init__` 和 self

`__init__` 是初始化方法（initializer）。
Python 会在新对象创建之后立即自动调用它，并把新对象作为第一个参数传入。
按照惯例，第一个参数命名为 `self`。

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

p = Point(3, 4)
print(p.x, p.y)   # 3 4
```

你永远不需要自己传入 `self`。
`Point(3, 4)` 在幕后会变成 `Point.__init__(p, 3, 4)`。
在任何方法内部，`self` 指向调用该方法的那个实例。
`self` 只是约定俗成的名字，而不是关键字，但请始终使用它。

`__init__` 并不创建对象，并且除了 `None` 之外不能返回任何东西。
从 `__init__` 返回一个值会抛出 `TypeError`。

### 实例属性 vs 类属性

通过 `self` 赋值的属性属于那一个实例。
在类体中、任何方法之外赋值的属性是类属性，由所有实例共享。

```python
class Counter:
    kind = "counter"        # 类属性，共享
    def __init__(self):
        self.count = 0      # 实例属性，每个对象各自一份

a = Counter()
b = Counter()
a.count += 1
print(a.count, b.count)   # 1 0   相互独立
print(a.kind, b.kind)     # counter counter   相同的值
```

当你读取 `a.kind` 时，Python 先检查实例，没有找到，然后检查类并找到了它。
因此，所有实例看到的都是同一个类属性，直到其中某个实例遮蔽（shadow）了它。

### 在实例上设置属性 vs 在类上设置属性

赋值 `obj.attr = value` 总是在实例上创建或更新属性，即使存在同名的类属性也是如此。
它不会改变类属性，而是只对那一个对象隐藏了类属性。

```python
class Robot:
    legs = 2

r1 = Robot()
r2 = Robot()
r1.legs = 4          # 只在 r1 上创建一个实例属性
print(r1.legs)       # 4   实例优先于类
print(r2.legs)       # 2   仍然看到的是类属性
print(Robot.legs)    # 2   类属性没有改变
```

要为所有实例改变这个值，就在类上赋值：`Robot.legs = 6`。
之后，每个没有遮蔽 `legs` 的实例都会读到 6。

### 共享可变类属性陷阱

类属性是共享的。
如果它是一个可变对象（比如列表），并且你通过某个实例修改（mutate）了它，那么每个实例都会看到这个变化，因为它们都指向同一个对象。

```python
class Team:
    members = []        # 一个由所有实例共享的列表
    def add(self, name):
        self.members.append(name)   # 修改共享的列表

t1 = Team()
t2 = Team()
t1.add("Ada")
print(t2.members)   # ['Ada']   t2 也看到了
```

`self.members.append(...)` 并没有对 `self` 赋值，它修改的是在类上找到的那个对象。
解决方法是在 `__init__` 中给每个实例一个属于自己的列表。

```python
class Team:
    def __init__(self):
        self.members = []   # 每个实例一个新列表
```

注意，重新绑定（rebinding，`self.members = [...]`）会创建一个实例属性，从而避开这个陷阱，但对共享对象进行原地修改则不会。

### 实例的 `__dict__`

对象把自己的属性存储在一个名为 `__dict__` 的字典中。
类属性不会被复制到其中；只有在实例上设置的属性才会出现在那里。

```python
class Box:
    color = "red"          # 类属性
    def __init__(self, size):
        self.size = size    # 实例属性

b = Box(10)
print(b.__dict__)      # {'size': 10}   这里没有 'color'
b.color = "blue"       # 现在遮蔽了类属性
print(b.__dict__)      # {'size': 10, 'color': 'blue'}
```

属性查找会先读取实例的 `__dict__`，然后回退到类。
写入 `b.color = ...` 会在实例的 `__dict__` 中添加一个键，这就是为什么它会遮蔽类属性，而不是改变类属性。
