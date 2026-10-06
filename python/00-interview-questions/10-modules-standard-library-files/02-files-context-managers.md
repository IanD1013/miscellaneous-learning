读写文件是初级开发者遇到的第一批真正的 I/O 任务之一。
语言给了你 `open()`，但面试官关心的是：你是否用 `with` 确定性地关闭文件、是否选择了正确的模式和编码，以及是否使用标准库（`pathlib`、`json`、`csv`）而不是手动解析。

### open() 及其模式

`open(path, mode, encoding=...)` 返回一个文件对象（file object）。
模式字符串控制你能做什么：

```python
open("data.txt", "r")   # 读（默认），文件必须存在
open("data.txt", "w")   # 写，先把文件截断为空
open("data.txt", "a")   # 追加，写入的内容追加到末尾
open("data.txt", "x")   # 独占创建，如果文件已存在则抛出 FileExistsError
open("img.png", "rb")   # 二进制读，你得到的是 bytes，而不是 str
```

文本模式（默认）给你 `str`，并使用某种编码对字节进行解码。
二进制模式（`b`）给你原始的 `bytes`，不做任何解码。
两者不能混用：把 `str` 写入二进制文件会抛出 `TypeError`，把 `bytes` 写入文本文件也一样。
加上 `+`（例如 `"r+"`）会以既可读又可写的方式打开。

### 为什么 with 是正确的方式

每个打开的文件都占用一个操作系统资源。
如果你忘了关闭它，你写入的数据可能停留在缓冲区里而永远到不了磁盘，而且在某些平台上文件会一直被锁定。
`with` 语句会在代码块结束时自动关闭文件，即使块内抛出了异常也是如此。

```python
with open("notes.txt", "w", encoding="utf-8") as f:
    f.write("hello\n")
# f 在这里已关闭，有保证，即使出错也是如此
```

手动的替代方式需要一个 `try`/`finally` 才能写对，而这正是 `with` 替你做的事情。
代码块结束后，文件被关闭；从已关闭的文件读取会抛出 `ValueError`。

### 读取：四种方式

- `f.read()` 把整个文件作为单个字符串返回（二进制模式下是 bytes）。
- `f.readline()` 返回一行，包括末尾的 `"\n"`，到达文件末尾时返回 `""`。
- `f.readlines()` 返回所有行组成的列表，每行都保留其 `"\n"`。
- 迭代文件（`for line in f:`）一次产出一行，几乎不占内存，所以它是处理大文件的正确选择。

换行符会保留在每一行上，所以人们经常调用 `line.strip()` 或 `line.rstrip("\n")` 来去掉它。

### 编码很重要

文本文件在磁盘上是字节；编码（encoding）决定这些字节如何映射为字符。
默认编码依赖于平台，所以始终传入 `encoding="utf-8"`，让你的代码在任何地方表现一致。
用错误的编码读取文件会抛出 `UnicodeDecodeError`，或者悄悄产生错误的字符。

### pathlib 基础

`pathlib.Path` 是处理路径的现代方式。
`/` 运算符以与操作系统无关的方式拼接各部分，而 `Path` 拥有能替代许多文件操作的方法。

```python
from pathlib import Path

p = Path("data") / "report.txt"   # 拼接为 data/report.txt
p.exists()                        # 如果路径存在则为 True
p.name                            # "report.txt"
p.suffix                          # ".txt"

text = Path("config.txt").read_text(encoding="utf-8")   # 一次调用完成打开、读取、关闭
Path("out.txt").write_text("done\n", encoding="utf-8")  # 一次调用完成打开、写入、关闭
```

`read_text` 和 `write_text` 会替你打开、执行 I/O 并关闭，所以单次读或写不需要 `with`。

### 标准库中的 JSON 和 CSV

不要手动解析这些格式。
`json` 模块在 Python 对象和 JSON 文本之间进行转换：

```python
import json

with open("config.json", encoding="utf-8") as f:
    data = json.load(f)        # 从文件读取 JSON 到 dict/list

json.dumps({"a": 1})           # 返回一个 str：'{"a": 1}'
json.loads('{"a": 1}')         # 把 str 解析为 {"a": 1}
```

`json.load`/`json.dump` 处理文件对象；`json.loads`/`json.dumps` 处理字符串（注意末尾的 `s` 代表 "string"）。
JSON 的键总是字符串，所以一个带整数键的 Python dict 读回来时键会变成字符串。

`csv` 模块读写逗号分隔的行。
打开文件时传入 `newline=""`，这样模块才能正确处理行尾：

```python
import csv

with open("people.csv", newline="", encoding="utf-8") as f:
    for row in csv.reader(f):
        print(row)             # 每一行都是字符串列表

with open("out.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["name", "age"])
```

`csv.reader` 把每个字段都作为字符串产出，即使是数字也一样，所以 `"42"` 不会自己变成 `42`。
`csv.DictReader` 则把每一行作为以表头行为键的 dict 给出，而不是列表。
