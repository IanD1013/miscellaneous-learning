当你使用像 `x` 这样的名字时，Python 会去哪里查找它？
答案是一个固定的搜索顺序，而闭包（closure）就是内部函数持续使用创建它的那个函数中的名字时所发生的情况。
面试官喜欢考察这个主题，因为这些规则说起来很简单，但在循环中会产生令人意外的结果，而且读取一个名字和给它赋值之间的区别，几乎会让每个人一开始都栽跟头。

### LEGB 规则

当你引用一个名字时，Python 会按以下顺序搜索四个作用域（scope），并在找到第一个匹配时停止：

- **L**ocal（局部）：在当前函数内部赋值的名字。
- **E**nclosing（外层）：在包裹当前函数的任何函数中的名字。
- **G**lobal（全局）：模块顶层的名字。
- **B**uilt-in（内置）：像 `len`、`print`、`range` 这样始终存在的名字。

```python
x = "global"

def outer():
    x = "enclosing"
    def inner():
        return x          # 在外层作用域中找到
    return inner()

print(outer())            # enclosing
```

查找关注的是名字在哪里被找到，而不是值从哪里来。
如果 `inner` 有自己的 `x = ...`，那么这个局部变量会胜出。

### 读取 vs 赋值：UnboundLocalError 陷阱

一个只读取某个名字的函数可以看到全局变量。
但如果一个函数在其函数体的任何地方对某个名字赋值，Python 就会把这个名字视为整个函数的局部变量，即使是在赋值之前的那些行上也是如此。

```python
count = 0

def bump():
    count = count + 1     # UnboundLocalError
    return count
```

因为 `count` 在 `bump` 中被赋值，所以它是局部变量，于是 `count + 1` 读取的是一个尚未被设置的局部变量。
这是最常见的面试“为什么这段代码会崩溃”问题之一。

### global 和 nonlocal

`global name` 告诉 Python，对 `name` 的赋值应该重新绑定（rebind）模块级变量，而不是创建一个局部变量。
`nonlocal name` 对最近的外层函数的变量做同样的事情。
如果只是读取，两者都不需要。

```python
count = 0

def bump():
    global count
    count += 1            # 重新绑定模块级的 count

def make_counter():
    n = 0
    def step():
        nonlocal n
        n += 1
        return n
    return step
```

`nonlocal` 要求这个名字已经存在于某个外层函数作用域中；它无法触及全局作用域，也无法创建新变量。

### 什么是闭包

闭包是一个被返回（或以其他方式比定义它的那次调用存活得更久）的内部函数，同时它仍然引用着外层作用域中的名字。
只要内部函数还活着，这些外层变量就会一直存活。

```python
def multiplier(factor):
    def mul(n):
        return n * factor   # factor 来自外层作用域
    return mul

double = multiplier(2)
print(double(5))            # 10
```

每次调用 `multiplier` 都会创建一个新的 `factor`，因此 `multiplier(2)` 和 `multiplier(3)` 返回的是相互独立的函数。

### 闭包捕获的是变量，而不是值

闭包捕获的是变量本身，而不是内部函数定义时该变量值的快照。
如果被捕获的变量之后发生了变化，闭包会看到新的值。

```python
def make():
    x = 1
    def show():
        return x
    x = 99
    return show

print(make()())             # 99，而不是 1
```

### 延迟绑定（late-binding）循环陷阱

在循环中使用闭包是一个经典错误。
循环中创建的每个函数都捕获同一个循环变量，并且它们在循环结束后都会读取它的最终值。

```python
funcs = [lambda: i for i in range(3)]
print([f() for f in funcs])   # [2, 2, 2]，而不是 [0, 1, 2]
```

这三个 lambda 都闭包引用了同一个变量 `i`，而循环结束后它的值是 `2`。
修复方法是把当前值绑定为默认参数，默认参数会在 lambda 定义时立即求值：

```python
funcs = [lambda i=i: i for i in range(3)]
print([f() for f in funcs])   # [0, 1, 2]
```

`for` 循环不会创建新的作用域，所以循环变量会泄漏出去并被共享。
默认参数技巧在定义时捕获值，从而完全避开了共享变量的问题。
