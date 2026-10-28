Python 的卖点是"自带电池"（batteries included）。
成为一名高效的初级开发者，很大一部分在于知道哪块电池已经存在，这样你就不会重复造轮子。
本课快速浏览面试官期望你会用到的高价值标准库模块：`collections`、`datetime`、`os` 和 `sys`、`random`，以及 `math`。
最后以一个在面试中经常出现的认知点收尾：全局解释器锁（Global Interpreter Lock，GIL），以及为什么线程不能让 CPU 密集型（CPU-bound）的 Python 代码变快。

### collections：defaultdict、Counter、deque

`collections` 增加了一些容器类型，帮你省去常见的样板代码。

`defaultdict` 使用一个工厂函数自动构建缺失的值，这样你就不用再写 `if key not in d` 这样的保护判断。

```python
from collections import defaultdict

groups = defaultdict(list)
for name in ["amy", "al", "bob"]:
    groups[name[0]].append(name)   # 第一次访问时不会抛出 KeyError
print(groups)   # defaultdict(<class 'list'>, {'a': ['amy', 'al'], 'b': ['bob']})
```

工厂函数在调用时不带任何参数。
`defaultdict(int)` 让缺失的键从 `0` 开始，这让计数变成一行代码。
注意，仅仅读取一个缺失的键就会把它插入进去，这可能会让你感到意外。

`Counter` 是一个专为计数而构建的 dict 子类。
它可以对任何可迭代对象计数，并提供 `.most_common()`。

```python
from collections import Counter

c = Counter("mississippi")
print(c["s"])              # 4
print(c.most_common(1))    # [('i', 4)]
print(c["z"])              # 0  （缺失的键返回 0，不会报错）
```

`deque` 是一个双端队列（double-ended queue），在两端都能快速追加和弹出。
`list.pop(0)` 是 O(n)，因为它要移动每个元素；`deque.popleft()` 是 O(1)。

```python
from collections import deque

q = deque([1, 2, 3])
q.appendleft(0)   # deque([0, 1, 2, 3])
q.popleft()       # 0，很快
```

### datetime 基础

`datetime` 处理日期和时间。
两个 `datetime` 对象相减会得到一个 `timedelta`。

```python
from datetime import datetime, timedelta

start = datetime(2026, 1, 1, 9, 0)
later = start + timedelta(hours=2, minutes=30)
gap = later - start
print(gap)             # 2:30:00
print(gap.total_seconds())  # 9000.0
```

`datetime.now()` 给出本地时间；`datetime.utcnow()` 在 3.12 中已被弃用，推荐改用 `datetime.now(timezone.utc)`。

### os、sys：环境与参数

`os.environ` 是环境变量的一个类 dict 视图。
`os.getenv("NAME", default)` 安全地读取单个环境变量。
`sys.argv` 是命令行参数列表，其中 `sys.argv[0]` 是脚本名，真正的参数从索引 1 开始。

```python
import os, sys

port = os.getenv("PORT", "8000")   # 未设置时使用默认值
print(sys.argv[0])                 # 脚本路径
```

### random 和 math

`random` 提供伪随机值：`random.randint(a, b)` 包含两端，`random.choice(seq)` 选取一个元素，`random.shuffle(lst)` 原地打乱并返回 `None`。

```python
import random
random.seed(0)            # 相同的种子产生可复现的输出
print(random.randint(1, 6))
```

`math` 包含浮点数学：`math.sqrt`、`math.floor`、`math.ceil`、`math.pi` 和 `math.inf`。
像 `//` 和 `%` 这样的整数运算不需要 `math`。

### GIL（认知）

CPython 有一个全局解释器锁：同一时间只有一个线程执行 Python 字节码。
所以启动多个线程来处理数字计算并不能加速 CPU 密集型工作；这些线程是轮流执行，而不是并行运行。
线程对于 I/O 密集型（IO-bound）工作（网络调用、磁盘、等待）仍然有帮助，因为线程在等待时会释放 GIL，让另一个线程运行。
当你确实需要并行的 CPU 工作时，标准答案是 `multiprocessing`，它使用独立的进程，每个进程都有自己的解释器和自己的 GIL。
