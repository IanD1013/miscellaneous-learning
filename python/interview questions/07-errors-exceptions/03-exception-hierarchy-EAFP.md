Python 中的每个异常都是一个对象，它的类位于一棵树中。
了解这棵树的形状能告诉你单个 `except` 子句实际会捕获什么，而了解 Pythonic 的风格（尝试执行操作，处理失败）能告诉你如何写出读起来清晰的代码，而不是用检查来守护每一步。

### BaseException / Exception 树

位于顶端的是 `BaseException`。
你编写的几乎所有代码都应该捕获它的子类 `Exception`，而不要直接捕获 `BaseException`。
原因在于它们之间存在的东西：`KeyboardInterrupt`（Ctrl-C）、`SystemExit`（由 `sys.exit()` 抛出）和 `GeneratorExit` 继承自 `BaseException`，但不继承自 `Exception`。
它们被有意放在 `Exception` 分支之外，这样普通的 `except Exception` 就不会吞掉你退出程序的尝试。

```python
issubclass(ValueError, Exception)        # True
issubclass(KeyboardInterrupt, Exception) # False
issubclass(KeyboardInterrupt, BaseException)  # True
```

所以 `except Exception:` 会捕获普通错误，而不去管 Ctrl-C。
`except BaseException:`（或裸 `except:`）甚至会捕获 Ctrl-C，这通常会困住一个试图终止卡住脚本的用户。

### 为什么裸 except 是一个陷阱

裸 `except:` 和 `except BaseException:` 完全相同。
它会隐藏所有错误，包括那些你从未打算处理的错误，让拼写错误看起来像正常的失败，并且可能阻止解释器关闭。
如果你确实需要一张宽泛的网，就捕获 `Exception`，并且至少把它记录下来。

```python
try:
    risky()
except Exception as err:   # 足够窄，能让 KeyboardInterrupt 通过
    log(err)
    raise                  # 记录后重新抛出，除非你真的能恢复
```

捕获与实际可能出错的情况相匹配的最窄类型。
`except (KeyError, IndexError):` 准确地说明了你的预期；`except Exception:` 则说明你放弃了。

### 常见的内置异常

这些异常经常出现，面试官会期望你能把一个操作对应到它抛出的错误。

```python
int("12a")        # ValueError：类型正确（str），值错误
1 + "2"           # TypeError：类型完全错误
{"a": 1}["b"]     # KeyError：缺失的 dict 键
[1, 2][5]         # IndexError：序列索引超出范围
"hi".len()        # AttributeError：没有这样的属性/方法
10 / 0            # ZeroDivisionError
next(iter([]))    # StopIteration：迭代器已耗尽
```

一个有用的关系：`KeyError` 和 `IndexError` 都继承自 `LookupError`，所以 `except LookupError:` 会同时捕获两者。
`ZeroDivisionError` 继承自 `ArithmeticError`。

### 捕获顺序很重要

Python 从上到下尝试 `except` 子句，并运行第一个类匹配的子句（包括子类）。
把具体类型放在通用类型之前，否则通用的那个会胜出，具体的块就会变成死代码。

```python
try:
    data["key"]
except Exception:      # 先匹配，所以下一个子句永远不会运行
    print("generic")
except KeyError:       # 不可达
    print("missing key")
```

把这两个子句的顺序反过来，`KeyError` 就会由它自己的分支处理。

### EAFP 与 LBYL

LBYL（"look before you leap"，三思而后行）先检查前置条件。
EAFP（"easier to ask forgiveness than permission"，请求原谅比请求许可更容易）直接执行操作并捕获失败。
Python 更偏好 EAFP：它通常更简短，并且避免了值在检查和使用之间发生变化的竞态（race）。

```python
# LBYL
if "name" in user and user["name"]:
    greet(user["name"])

# EAFP（更 Pythonic）
try:
    greet(user["name"])
except KeyError:
    pass
```

当成功路径是常见情况时，EAFP 表现出色，因为你不需要在每次调用时都付出检查的代价。
它还能在一个地方处理该操作可能抛出的所有失败模式。
权衡在于：只包裹可能失败的那一行，保持 `try` 体精简，并捕获具体的异常，这样你就不会隐藏无关的 bug。

```python
# 太宽泛：process() 中的拼写错误会被悄无声息地吞掉
try:
    value = config["timeout"]
    process(valeu)        # NameError 被下面的裸 except 隐藏了
except Exception:
    value = 30
```

让 `try` 只包含 `value = config["timeout"]` 并捕获 `KeyError`，那个隐藏的 bug 就会立即暴露出来。
