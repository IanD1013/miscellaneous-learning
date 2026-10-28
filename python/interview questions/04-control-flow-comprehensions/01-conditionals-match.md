分支是程序决定下一步做什么的方式。
Python 让语法保持精简：一个 `if`、任意数量的 `elif` 子句，以及一个可选的 `else`。
在此之上，还有用于内联选择值的条件表达式（conditional expression），以及用于匹配数据结构形状的 `match` 语句（3.10 中新增）。
本课涵盖这四者，以及面试官喜欢追问的陷阱。

### if / elif / else

条件不一定要是真正的 `bool`。
Python 会测试你给它的任何东西的*真值性*（truthiness）。
第一个条件为真值的分支会执行，其余分支被跳过。
`else` 只在没有任何条件匹配时才会执行。

```python
x = 0
if x:
    print("truthy")
elif x is None:
    print("none")
else:
    print("falsy")   # 打印这一行：0 是假值
```

永远只有一个分支会执行。
一旦某个条件匹配，Python 就不会再求值剩下的 `elif` 测试。

### 由真值性驱动的条件

空容器、`0`、`0.0`、`""` 和 `None` 都是假值（falsy）。
其他一切（非空容器、任何非零数字）都是真值（truthy）。
这就是为什么惯用的判空写法是 `if items:`，而不是 `if len(items) > 0:`。

一个常见陷阱：`if x == None` 能用，但不够惯用，而且遇到自定义的 `__eq__` 时可能出现异常行为；应该使用 `if x is None`。
另外，`0`、`0.0` 和 `False` 都是假值，所以 `if value:` 无法区分"缺失"和"数字零"。
当零是一个有效值时，应测试 `if value is not None`。

### 条件表达式

`A if cond else B` 在 `cond` 为真值时求值为 `A`，否则为 `B`。
它是一个表达式，所以会产生一个值，你可以把它赋值给变量或作为参数传递。
条件位于中间，这会让来自其他语言的人感到意外。

```python
n = 7
label = "even" if n % 2 == 0 else "odd"
print(label)          # odd
```

只有被选中的那一侧会被求值，所以未使用的分支永远不会执行。
让它们保持为单一、可读的选择；把很多个串联起来会很难读，这种情况应该用 `if/elif`。

### 嵌套条件和提前返回

深度嵌套的 `if` 块很难理解。
提前返回的守卫子句（guard clause）可以把逻辑扁平化，并在一开始就处理边界情况。
每个 `return` 都会立即退出函数，所以一旦某个分支返回，后面的代码行就不会执行。

```python
def describe(n):
    if n < 0:
        return "negative"
    if n == 0:
        return "zero"
    return "positive"
```

### match：字面量模式和捕获模式

`match` 会把一个主体（subject）与一系列 `case` 模式进行比较，并执行第一个匹配的模式。
模式中的裸名称是一个*捕获模式*（capture pattern）：它总是匹配，并把主体绑定到该名称上。
要与一个常量值进行匹配，请使用字面量（literal）。

```python
def http(status):
    match status:
        case 200:
            return "OK"
        case 404:
            return "Not Found"
        case other:           # 捕获：绑定上面没有匹配到的任何值
            return f"Unknown {other}"
```

因为裸名称是捕获而不是比较，所以 `case x:` 并不意味着"如果主体等于 x"。
要匹配某个变量的值，你必须对它加以限定（例如 `case Status.OK:` 或 `case obj.attr:`），否则它会被当作一个新的绑定。

### match：通配符 \_

`_` 是通配符（wildcard）。
它匹配任何东西，但不绑定任何东西，这使它成为放在末尾的惯用"默认"分支。
与 `if` 中的 `else` 不同，`match` 不要求有最后一个分支；如果没有任何匹配，该语句就什么也不做。

### match：序列模式、映射模式和类模式

模式可以匹配数据的形状，而不仅仅是值。
序列模式（sequence pattern）可以解构列表和元组（并且可以使用 `*rest`）。
映射模式（mapping pattern）匹配字典中选定的键，并忽略多余的键。
类模式（class pattern）匹配一个实例，并且可以提取出属性。

```python
def handle(event):
    match event:
        case ("move", x, y):           # 序列模式，绑定 x 和 y
            return f"move to {x},{y}"
        case {"type": "click", "id": i}:  # 映射模式，忽略多余的键
            return f"click {i}"
        case [first, *rest]:           # 绑定第一个元素和剩余部分
            return f"{first} then {rest}"
        case _:
            return "?"
```

序列模式不会匹配 `str`，即使字符串是可迭代的；字符串被当作单个值，而不是一个可以解构的序列。
只要列出的键存在，映射模式就会匹配，不管还有没有其他键。
像 `Point(x=0, y=y)` 这样的类模式在一个分支中同时混合了字面量匹配和捕获。
