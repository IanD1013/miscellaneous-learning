Python 中的函数调用比许多语言都更灵活。
你可以按位置或按名字传递实参，把多余的实参收集到 `*args` 和 `**kwargs` 中，强制某些参数只能用关键字传递（keyword-only）或只能按位置传递（positional-only），并用 `*` 和 `**` 把一个可迭代对象（iterable）或映射（mapping）展开到调用中。
面试官会考察这一点，因为这些规则看起来很简单，直到你把它们混在一起使用，而 Python 把实参绑定到形参的顺序会让人感到意外。

### 位置实参 vs 关键字实参

实参要么按位置传递（从左到右匹配），要么按关键字传递（按参数名匹配）。
你可以在一次调用中混用它们，但每个位置实参都必须出现在任何关键字实参之前。

```python
def greet(name, greeting):
    return f"{greeting}, {name}"

greet("Ada", "Hello")            # 都是位置实参
greet("Ada", greeting="Hello")   # 一个位置实参，一个关键字实参
greet(greeting="Hello", name="Ada")  # 都是关键字实参，顺序随意
```

写成 `greet(name="Ada", "Hello")` 是 `SyntaxError`：位置实参不能跟在关键字实参之后。
把同一个参数传两次（一次按位置，一次按关键字）会引发 `TypeError: got multiple values for argument`。

### 默认值

带默认值的参数会变成可选的。
默认值只在 `def` 运行时求值一次，而不是在每次调用时求值。
在签名中，带默认值的参数必须放在不带默认值的参数之后。

```python
def power(base, exp=2):
    return base ** exp

power(3)      # 9，使用默认值
power(3, 3)   # 27
```

### \*args 和 \*\*kwargs

`*args` 把多余的位置实参收集到一个 tuple 中。
`**kwargs` 把多余的关键字实参收集到一个 dict 中。
这些名字只是约定俗成；真正起作用的是 `*` 和 `**`。

```python
def record(*args, **kwargs):
    return args, kwargs

record(1, 2, x=3)   # ((1, 2), {'x': 3})
```

你可以要求一些普通参数，同时仍然接受额外的实参：

```python
def log(level, *messages, **fields):
    return level, messages, fields

log("INFO", "started", "ok", user="ada")
# ('INFO', ('started', 'ok'), {'user': 'ada'})
```

在包装函数（wrapper）内部，用 `*args, **kwargs` 同时转发两者，就能原封不动地传递所有内容：

```python
def trace(func, *args, **kwargs):
    return func(*args, **kwargs)
```

### 仅限关键字参数（在 \* 之后）

任何列在单独的 `*`（或 `*args`）之后的参数都只能按关键字传递，永远不能按位置传递。
这让调用处具有自解释性，并防止调用者意外地按位置传递一个标志参数。

```python
def connect(host, *, timeout=10, retries=3):
    return host, timeout, retries

connect("db", timeout=5)   # 没问题
connect("db", 5)           # TypeError: takes 1 positional argument but 2 were given
```

### 仅限位置参数（在 / 之前）

任何列在 `/` 之前的参数都只能按位置传递，永远不能按名字传递（在 Python 3.8 中加入）。
当参数名是一个你不希望调用者依赖的实现细节时，就会使用它。

```python
def divide(a, b, /):
    return a / b

divide(10, 2)        # 5.0
divide(a=10, b=2)    # TypeError: got some positional-only arguments passed as keyword
```

签名中的完整顺序是：仅限位置参数，然后是 `/`，然后是普通参数，然后是 `*`（或 `*args`），然后是仅限关键字参数，最后是 `**kwargs`。

### 在调用处解包

`*` 和 `**` 在调用时同样有效。
`*iterable` 把其中的元素展开为位置实参；`**mapping` 把其中的键值对展开为关键字实参。
`**` 映射的键必须是与参数名匹配的字符串。

```python
def point(x, y, z):
    return (x, y, z)

coords = [1, 2, 3]
point(*coords)              # (1, 2, 3)

data = {"x": 1, "y": 2, "z": 3}
point(**data)               # (1, 2, 3)
```

你可以把它们组合起来并混入字面量：`point(1, *[2], **{"z": 3})`。
一个常见的 bug 是解包一个键与参数不匹配的映射，这会引发 `TypeError: got an unexpected keyword argument`。
解包出的位置元素太少或太多，会引发一个关于实参数量的 `TypeError`。
