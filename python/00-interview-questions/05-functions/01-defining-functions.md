函数（function）把一段行为封装在一个名字后面。
你用 `def` 定义函数，给它参数，并使用 `return` 把一个值交还给调用者。
本课涵盖 `def` 的工作方式、当你不返回任何东西时会发生什么、默认参数值（default argument values）的行为（包括 Python 中最著名的那个陷阱）、文档字符串（docstring），以及函数是可以被四处传递的普通对象这一事实。

### def 和 return

`def` 创建一个函数对象，并把它绑定到一个名字上。
`return` 结束调用并送回一个值。

```python
def add(a, b):
    return a + b

result = add(2, 3)  # 5
```

一个函数可以有多个 `return` 语句。
最先到达的那个会立即结束调用。
到达的 `return` 之后的代码不会运行。

### 隐式返回 None

如果函数一直执行到末尾都没有遇到 `return`，或者执行了一个不带值的裸 `return`，它就返回 `None`。

```python
def greet(name):
    print(f"Hello, {name}")

x = greet("Ada")   # 打印问候语
print(x)           # None
```

当人们在函数内部 `print`，却期望拿回结果时，这一点会让他们犯错。
`print` 本身也返回 `None`，所以 `y = print("hi")` 会把 `None` 绑定到 `y`。

### 默认参数值

参数可以声明一个默认值，在调用者省略该实参时使用。

```python
def power(base, exp=2):
    return base ** exp

power(5)      # 25，exp 默认为 2
power(5, 3)   # 125
```

带默认值的参数必须放在不带默认值的参数之后，否则就是 `SyntaxError`。

### 可变默认参数陷阱

默认值只在 `def` 运行时求值一次（ONCE），而不是在每次调用时求值。
如果默认值是像 list 或 dict 这样的可变（mutable）对象，那么每一次依赖默认值的调用都会共享同一个对象。

```python
def append_to(item, acc=[]):
    acc.append(item)
    return acc

print(append_to(1))   # [1]
print(append_to(2))   # [1, 2]  同一个（SAME）list 一直存在
```

修复方法是标准惯用法：默认设为 `None`，并在函数内部构建一个新对象。

```python
def append_to(item, acc=None):
    if acc is None:
        acc = []
    acc.append(item)
    return acc
```

这适用于 list、dict、set 以及任何其他可变的默认值。
像数字、字符串、tuple 和 `None` 这样的不可变（immutable）默认值是安全的，因为它们无法被原地修改。

### 文档字符串和 help()

作为函数体第一条语句的字符串字面量会成为它的文档字符串（docstring）。
它存储在 `func.__doc__` 上，并由 `help(func)` 显示。

```python
def area(radius):
    """Return the area of a circle with the given radius."""
    return 3.14159 * radius ** 2

print(area.__doc__)   # Return the area of a circle with the given radius.
```

文档字符串是文档，而不是注释：`# comment` 在编译时就被丢弃，但文档字符串在运行时仍然附着在对象上。

### 函数是一等对象（first-class objects）

函数是一个值。
你可以把它赋给另一个名字，把它存进 list 或 dict，并把它传给其他函数。

```python
def shout(text):
    return text.upper()

f = shout            # 把另一个名字绑定到同一个函数
print(f("hi"))       # HI

def apply(func, value):
    return func(value)

print(apply(shout, "go"))   # GO
```

注意 `shout`（函数对象）和 `shout("hi")`（运行它的一次调用）之间的区别。
传入 `shout()` 而不是 `shout`，传递的是返回值，而不是函数。

### 提前返回

一旦知道答案就用 `return` 离开函数，能让代码保持扁平并避免深层嵌套。

```python
def first_even(numbers):
    for n in numbers:
        if n % 2 == 0:
            return n
    return None   # 没有匹配项
```

一旦任何 `return` 运行，函数就会停止，即使是在循环内部。
