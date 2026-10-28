当代码可能在运行时失败时，Python 允许你把它包在 `try` 块中并处理这个失败，而不是让程序崩溃。
完整的语句有四种块，每一种都有特定的职责。
面试官会考察你是否知道 `else` 和 `finally` 究竟是用来做什么的、你是否捕获了正确的异常类型，以及 `except` 子句必须以怎样的顺序出现。

### 四种块及其职责

```python
try:
    # 可能抛出异常的代码
    result = risky()
except ValueError:
    # 仅当抛出了匹配的异常时运行
    result = None
else:
    # 仅当 try 块没有抛出任何异常时运行
    print("no error happened")
finally:
    # 无论如何都会运行
    print("cleaning up")
```

- `try`：被监视是否发生异常的代码。
- `except`：处理匹配的异常。你可以有多个。
- `else`：仅当 `try` 在没有异常的情况下结束时运行。如果抛出了任何异常，它就会被跳过。
- `finally`：无论如何都会运行，不管 `try` 是成功了、抛出了异常，还是提前返回了。

一个 `try` 至少需要一个 `except` 或一个 `finally`。
没有 `except` 就不能写 `else`。

### 为什么使用 else，而不是直接把代码放进 try

把成功路径的代码放在 `else` 中可以让 `try` 块保持精简，这样 `except` 只会捕获你本来想监视的那一行产生的错误。

```python
try:
    value = int(text)
except ValueError:
    print("bad input")
else:
    # 仅当 int(text) 成功时运行
    print(value * 2)
```

如果 `value * 2` 在 `try` 内部，那里发生的一个无关错误可能会被你为 `int()` 编写的 `except` 吞掉。
`else` 块让意图变得清晰。

### 捕获具体类型，并且顺序很重要

捕获你真正预期的最窄的异常类型。
裸 `except:`（或 `except Exception:`）会掩盖你没有预料到的 bug。

`except` 子句是从上到下检查的，第一个匹配的胜出。
所以具体的异常必须放在更通用的异常之前。
由于 `ValueError` 是 `Exception` 的子类，把 `Exception` 放在前面意味着 `ValueError` 永远不会被执行到。

```python
try:
    risky()
except Exception:      # 太宽泛，先捕获了所有异常
    print("general")
except ValueError:     # 不可达，ValueError 是一个 Exception
    print("value")
```

把顺序反过来，让具体的子句先运行：

```python
try:
    risky()
except ValueError:
    print("value")
except Exception:
    print("general")
```

### 用 as 获取实例

使用 `as` 把异常对象绑定到一个名字上，这样你就可以检查它。

```python
try:
    int("nope")
except ValueError as e:
    print(type(e).__name__)   # ValueError
    print(e)                  # invalid literal for int() with base 10: 'nope'
```

由 `as` 绑定的名字会在 `except` 块结束时被删除，所以之后你不能再使用它。
如果之后还需要它，就在块内把它赋值给另一个变量。

### 捕获类型元组

一个 `except` 子句可以通过把多个异常类型列在一个元组（tuple）中来同时处理它们。
括号是必需的。

```python
try:
    risky()
except (ValueError, TypeError) as e:
    print("bad value or type:", e)
```

这和写两个具有相同主体的独立 `except` 子句是一样的，只是更简短。

### finally 总是会运行

`finally` 会在退出 `try` 的每一条路径上运行，包括 `return`、`break` 或 `continue`，甚至在没有 `except` 匹配、异常正在向外传播时也会运行。

```python
def f():
    try:
        return "from try"
    finally:
        print("finally ran")

f()   # 打印 "finally ran"，然后返回 "from try"
```

最大的陷阱：如果 `finally` 自身执行了 `return`，它会覆盖 `try` 块中的 `return`。

```python
def g():
    try:
        return 1
    finally:
        return 2

g()   # 2，finally 的 return 胜出
```

因为 `finally` 即使在异常未被处理时也会运行，所以它是放置那些无论成功还是失败都必须执行的清理代码的地方。
