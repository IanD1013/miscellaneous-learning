任何 `.py` 文件都是一个模块（module）。
一个由模块组成的文件夹就是一个包（package）。
`import` 语句是你把名字从一个模块引入到另一个模块的方式，也是 Python 查找并运行那个文件的方式。
面试官会问这个话题，因为它能看出你是否理解输入 `import` 时实际发生了什么、为什么模块代码只运行一次，以及虚拟环境（virtual environment）如何防止一个项目的依赖破坏另一个项目的依赖。

### 导入形式

引入代码有三种常见方式。

```python
import math                 # 把模块对象绑定到名字 "math"
math.sqrt(9)                # 通过模块访问名字

from math import sqrt       # 只把 "sqrt" 绑定到当前命名空间
sqrt(9)                     # 直接使用，不需要 "math." 前缀

import numpy as np          # 别名：用更短的名字绑定模块
from math import pi as PI   # 给单个导入的名字起别名
```

`import math` 给你的是模块对象；你用点号访问它内部的内容。
`from math import sqrt` 把单个名字 `sqrt` 复制到你文件的命名空间（namespace）中，所以 `math` 本身并没有被定义。
`as` 会重命名你导入的任何东西，这样可以避免过长的名字和命名冲突。

一个常见陷阱：`from x import *` 会把所有公开名字都引入进来，并可能悄悄覆盖你已经定义的名字。
在交互式 shell 之外避免使用它。

### 模块和包

模块是单个文件。
包是把模块组织在一起的目录。
历史上，包需要一个 `__init__.py` 文件（可以为空）来把该目录标记为包；这个文件会在包第一次被导入时运行。

```
mypkg/
    __init__.py
    utils.py
    parsers.py
```

```python
import mypkg.utils          # 用点分路径导入子模块
from mypkg import parsers    # 按名字导入子模块
from mypkg.utils import clean
```

点分名字遵循文件夹结构。
`mypkg.utils` 表示 `mypkg` 包内的 `utils` 模块。

### if `__name__` == '`__main__`'

每个模块都有一个 `__name__` 变量。
当你用 `python file.py` 直接运行一个文件时，它的 `__name__` 被设置为字符串 `"__main__"`。
当同一个文件被另一个模块导入时，它的 `__name__` 则是该模块自己的名字。

```python
# greet.py
def hello():
    print("hi")

if __name__ == "__main__":
    hello()      # 仅在直接执行此文件时运行
```

运行 `python greet.py`，它会打印 `hi`。
在另一个文件中执行 `import greet`，`hello()` 不会被调用，因为 `__name__` 是 `"greet"`，而不是 `"__main__"`。
这个惯用法让一个文件既可以作为可导入的库，也可以作为可运行的脚本。

### 模块代码只运行一次

模块第一次被导入时，Python 会从上到下执行它的顶层代码，然后把模块对象缓存到 `sys.modules` 中。
之后对同一模块的导入会返回缓存的对象，而不会重新运行该文件。

```python
# config.py
print("loading config")
SETTINGS = {"debug": True}
```

```python
import config    # 打印 "loading config"
import config    # 什么都不打印；使用缓存
```

因此，模块级的副作用（side effect）（打印、打开文件、构建字典）在每个进程中只发生一次，无论你导入多少次。

### 模块搜索路径

当你写 `import foo` 时，Python 会按顺序查找 `sys.path` 中列出的目录，并使用第一个匹配项。
这个列表首先是正在运行的脚本所在的目录（在 REPL 中则是当前目录），然后是标准库，再然后是已安装的第三方包。

```python
import sys
print(sys.path)   # 按顺序搜索的目录列表
```

因为脚本自身的目录排在最前面，一个名为 `random.py` 的本地文件会遮蔽（shadow）标准库的 `random`。
用标准库模块的名字给自己的文件命名，是导致令人困惑的导入错误的经典原因。

### 虚拟环境和 pip

`pip` 从 PyPI 安装第三方包。
默认情况下，它会安装到当前活动 Python 的 site-packages 中，而这是该解释器上所有项目共享的。
虚拟环境为一个项目提供它自己独立的一套包，这样版本就不会冲突。

```bash
python -m venv .venv          # 在 .venv 文件夹中创建环境
source .venv/bin/activate     # 激活它（Windows：.venv\Scripts\activate）
pip install requests          # 只安装到这个环境中
pip freeze > requirements.txt # 记录确切版本
deactivate                    # 退出环境
```

当环境处于激活状态时，`python` 和 `pip` 指向这个隔离的副本，所以 `pip install` 不会影响其他项目或系统 Python。
`requirements.txt` 让其他人可以用 `pip install -r requirements.txt` 复现同一套包。
