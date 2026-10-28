捕获错误只是故事的一半。
另一半是发出错误信号：当你的代码遇到它无法处理的情况时，它应该 `raise` 一个异常，让调用方知道这件事。
面试官会考察这个话题，因为它的机制很简单，但需要真正的判断力。
他们想看到你会抛出正确的类型、附带有用的信息、在包装错误时保留原始原因，并且知道什么时候用内置异常就够了，什么时候自定义类型才值得存在。

### raise 和裸 re-raise

`raise` 语句会抛出一个异常。
你通常抛出的是一个实例，而且几乎总是会传入一条描述出了什么问题的消息。

```python
def withdraw(balance, amount):
    if amount > balance:
        raise ValueError(f"cannot withdraw {amount} from {balance}")
    return balance - amount
```

在 `except` 块内部，裸 `raise`（不带参数）会重新抛出（re-raise）当前正在处理的异常，并保留它原始的回溯（traceback）。
这就是你检查或记录一个错误后，再让它继续向外传播的方式。

```python
try:
    risky()
except ValueError:
    # 做一些事情，然后让它原样继续传播
    raise
```

在没有任何活动异常的地方使用裸 `raise` 会抛出 `RuntimeError: No active exception to re-raise`。
而按名字重新抛出（`raise ValueError(...)`）会创建一个新的异常并替换回溯，所以当你的意思是"就是这个错误，继续传播"时，优先使用裸 `raise`。

### 带消息抛出

向异常传入一个字符串会设置它的 `args`，并且这就是 `str(exc)` 返回的内容。
消息是给阅读回溯的人看的，所以要写得具体。

```python
try:
    raise ValueError("port must be positive")
except ValueError as exc:
    print(str(exc))   # port must be positive
    print(exc.args)   # ('port must be positive',)
```

你抛出类时要带括号，`raise ValueError("...")`。
写 `raise ValueError`（不带括号）也可以，因为 Python 会不带参数地帮你实例化它，但这样就没有消息了。

### 定义自定义异常

自定义异常就是一个继承自 `Exception`（或更具体的内置异常）的类。
最简定义完全不需要类体。

```python
class ConfigError(Exception):
    """Raised when configuration is invalid."""

raise ConfigError("missing database url")
```

继承 `Exception`，而不是 `BaseException`。
`BaseException` 是 `KeyboardInterrupt` 和 `SystemExit` 的父类，而普通的 `except Exception` 有意不应该捕获它们。
捕获一个自定义类型也会捕获它的子类，所以一个小型的层次结构（一个基类 `AppError` 加上具体的子类）可以让调用方选择宽泛地或精确地捕获。

### 为自定义异常添加属性

真实的异常通常携带结构化数据，而不只是一个字符串。
定义 `__init__`，保存这些字段，并把一条可读的消息传给基类。

```python
class ValidationError(Exception):
    def __init__(self, field, value):
        super().__init__(f"invalid value for {field}: {value!r}")
        self.field = field
        self.value = value

try:
    raise ValidationError("age", -5)
except ValidationError as exc:
    print(exc.field)   # age
    print(exc.value)   # -5
```

调用 `super().__init__(message)` 正是让 `str(exc)` 和回溯显示你的消息的关键。
忘了它，异常打印出来就没有任何细节。

### 使用 raise ... from ... 进行异常链（exception chaining）

当你捕获一个错误并抛出另一个错误时，`raise NewError(...) from original` 会把原始异常记录为 `__cause__`，并且回溯会显示 "The above exception was the direct cause of the following exception"。
这让根本问题保持可见，而不是把它隐藏起来。

```python
def load(path):
    try:
        return open(path).read()
    except OSError as exc:
        raise ConfigError(f"cannot read {path}") from exc
```

即使没有 `from`，当你在 `except` 块中抛出异常时，Python 也会自动设置 `__context__`，并且回溯会显示 "During handling of the above exception, another exception occurred"。
使用显式的 `from exc` 来标记一个有意的原因，或者在原始异常只是噪音时使用 `from None` 来抑制异常链。

### 什么时候创建你自己的异常类型

当调用方需要捕获你的特定失败而不捕获无关的失败时，或者当内置异常无法描述这个问题时，就使用自定义异常。
错误的函数参数是 `ValueError`；缺失的键是 `KeyError`；合适的时候就复用它们。
当失败是你业务领域的一部分，并且你希望调用方按照它自己的方式处理时，就创造 `PaymentDeclined` 或 `RateLimitExceeded`。
不要为每个错误都创建一个新类型；一个你从不单独捕获的自定义异常只会增加噪音而没有价值。
