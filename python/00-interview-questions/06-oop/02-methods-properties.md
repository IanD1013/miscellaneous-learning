一个类可以包含三种方法，每一种接收的第一个参数都不同（或者没有）。
知道该选用哪一种是一个标准的面试考察点，因为你的选择表明了你是否理解 Python 如何绑定（bind）方法。
本课涵盖实例方法（instance method）、`@classmethod` 和 `cls`、`@staticmethod`，以及用于计算属性和带验证属性的 `@property`。

### 实例方法和 self

普通方法把 `self` 作为第一个参数。
`self` 是调用该方法的那个实例。
Python 会自动传入它：`obj.method()` 实际上就是 `Class.method(obj)`。

```python
class Counter:
    def __init__(self, start):
        self.value = start

    def increment(self):
        self.value += 1

c = Counter(0)
c.increment()
print(c.value)   # 1
```

`self` 只是一个命名惯例，而不是关键字，但每个面试官都期望你使用它。
关键在于实例是作为第一个参数被显式传入的，这就是为什么你在定义中写 `self`，而在调用时不写。

### @classmethod 和 cls

`@classmethod` 接收类本身作为第一个参数（按惯例命名为 `cls`），而不是实例。
常见用途是替代构造器（alternative constructor）：除了 `__init__` 之外构建实例的第二种方式。

```python
class Date:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    @classmethod
    def from_string(cls, text):
        year, month, day = (int(part) for part in text.split("-"))
        return cls(year, month, day)

d = Date.from_string("2026-06-13")
print(d.year)   # 2026
```

使用 `cls(...)` 而不是硬编码 `Date(...)` 对子类很重要：如果子类调用 `from_string`，`cls` 就是该子类，因此你会得到正确类型的实例。
你既可以在类上也可以在实例上调用类方法；两种情况下 `cls` 都是类。

### @staticmethod

`@staticmethod` 既不接收 `self` 也不接收 `cls`。
它是一个普通函数，出于组织代码的目的放在类里面，因为它与类相关，但不涉及实例或类的状态。

```python
class TempConverter:
    @staticmethod
    def c_to_f(celsius):
        return celsius * 9 / 5 + 32

print(TempConverter.c_to_f(100))   # 212.0
```

如果一个方法不使用 `self` 或 `cls`，它就适合改为 `@staticmethod`。
在代码审查中，明显的信号是方法体中从未引用 `self` 的方法。

### 用 @property 实现计算属性

`@property` 把一个方法变成只读属性。
调用者像访问数据一样访问它（`obj.area`），不需要括号，但在幕后运行的是一个方法。
用它来表示由其他属性推导出来的值。

```python
class Circle:
    def __init__(self, radius):
        self.radius = radius

    @property
    def area(self):
        return 3.14159 * self.radius ** 2

c = Circle(2)
print(c.area)   # 12.56636，没有括号
```

因为 `area` 在每次访问时都会重新计算，所以当 `radius` 改变时它会保持同步。
尝试给它赋值（`c.area = 5`）会抛出 `AttributeError`，除非你同时定义了 setter。

### 属性的 setter 与验证

用 `@<name>.setter` 添加一个 setter，以便在有人给该属性赋值时运行代码。
经典用途是验证输入。
把真实数据存储在一个名字不同的属性中（通常以下划线开头），这样属性就不会被遮蔽（shadow）。

```python
class Account:
    def __init__(self, balance):
        self.balance = balance        # 经过 setter

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, amount):
        if amount < 0:
            raise ValueError("balance cannot be negative")
        self._balance = amount

a = Account(100)
a.balance = 50      # 没问题
# a.balance = -1    # 抛出 ValueError
```

注意，`__init__` 给 `self.balance` 赋值，这会调用 setter，因此即使在构造期间也会执行验证。
底层存储属性是 `_balance`；如果 getter 返回的是 `self.balance`，它就会无限地调用自身（无限递归）。
