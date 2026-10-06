"Pythonic" 的代码使用的是这门语言设计时所围绕的那些模式，而不是用从其他语言带来的习惯去和它对着干。
面试官会用这些惯用法（idiom）来快速了解你对 Python 的熟悉程度。
它们与巧妙的技巧无关。
它们关乎的是写出更短、更清晰、更不容易出现差一错误（off by one bug）的代码。

### EAFP vs LBYL

处理可能会失败的事情有两种风格。
LBYL（Look Before You Leap，三思而后行）先进行检查。
EAFP（Easier to Ask Forgiveness than Permission，请求原谅比请求许可更容易）则直接尝试，然后处理失败。

```python
# LBYL
if "key" in d:
    value = d["key"]
else:
    value = None

# EAFP
try:
    value = d["key"]
except KeyError:
    value = None
```

Python 倾向于 EAFP。
LBYL 版本还有一个微妙的竞态问题：在 `in` 检查和查找之间，另一个线程可能会删除这个键。
EAFP 避免了这个空隙。
话虽如此，EAFP 并不总是最好的。
对于字典的默认值，`d.get("key")` 比两者都更简洁，而且在一大段代码外面包一个普通的 `try`/`except` 可能会掩盖 bug。

### 海象运算符

`:=` 在一个更大的表达式中完成赋值。
当你想在同一个地方使用一个值并对它进行测试时，它很有用，这样你就不用把它计算两次或重复写它。

```python
# 不用海象运算符的话，你要调用 input 两次，或者先存储再循环
while (line := input("> ")) != "quit":
    print(f"you said {line}")

data = [1, 2, 3, 4, 5]
if (n := len(data)) > 3:
    print(f"{n} items, that is a lot")
```

`:=` 是一个表达式，所以它有值；普通的 `=` 是一个语句，没有值。
在很多地方，你不能在顶层不加括号地写 `if x := 5`，而且你也不能把 `:=` 当作普通的独立赋值来使用。

### 元组解包与交换

Python 可以从一个可迭代对象中一次性给多个名字赋值。
经典的用法是在不使用临时变量的情况下交换两个变量。

```python
a, b = 1, 2
a, b = b, a        # 交换，现在 a == 2 且 b == 1

point = (3, 4)
x, y = point       # x == 3, y == 4
```

星号解包会把剩下的部分收集到一个列表中：

```python
first, *rest = [10, 20, 30, 40]
# first == 10, rest == [20, 30, 40]

head, *middle, tail = [1, 2, 3, 4, 5]
# head == 1, middle == [2, 3, 4], tail == 5
```

名字的数量必须与值的数量相匹配，否则你会得到一个 `ValueError`，除非有一个带星号的名字吸收了多余的值。

### enumerate 和 zip

当你需要索引时，使用 `enumerate`；当你同时遍历两个序列时，使用 `zip`。
用你自己维护的计数器去索引列表，是不 Pythonic 的写法。

```python
# 不 Pythonic
for i in range(len(names)):
    print(i, names[i])

# Pythonic
for i, name in enumerate(names):
    print(i, name)

# enumerate 接受一个起始值
for rank, name in enumerate(names, start=1):
    print(rank, name)

# zip 把它们配对；它在最短的输入处停止
for name, score in zip(names, scores):
    print(name, score)
```

`zip` 在最短的参数处停止，所以较长序列中多出来的元素会被静默丢弃。

### 用 in 检查成员关系

`in` 直接测试成员关系。
你不需要一个带标志变量的循环。

```python
if "apple" in fruits:
    print("found it")

# 对于字典，in 检查的是键
if "name" in person:
    print(person["name"])
```

对于列表，`in` 是线性扫描；对于 `set` 或 `dict` 的键查找，它很快。
为重复的成员检查选择 set，这本身就是一种 Pythonic 的做法。

### 真值检查

空容器、`0`、`0.0`、`""` 和 `None` 都是假值（falsy）。
所以要直接测试容器本身，而不是比较它的长度。

```python
items = []

# 不 Pythonic
if len(items) > 0:
    ...

# Pythonic
if items:
    ...

if not items:
    print("nothing here")
```

有一个陷阱：这对于"它是否为空"来说没问题，但如果你必须区分空列表和 `None`，就要用 `if items is not None`，因为两者都是假值，`if items:` 无法区分它们。

### with 语句

`with` 是使用必须被清理的资源（比如文件）时的惯用法。
它保证即使代码块抛出异常，清理操作也会执行。

```python
with open("data.txt") as f:
    contents = f.read()
# f 在这里会被自动关闭，即使 read() 抛出了异常

# 同时打开多个
with open("in.txt") as src, open("out.txt", "w") as dst:
    dst.write(src.read())
```

它取代了旧的模式，即先 `f = open(...)`，然后手动用 `try`/`finally` 来调用 `f.close()`。
一旦代码块退出，文件就会被关闭。

### 需要避免的常见反模式

- 用 `==` 与 `True`/`False` 比较：写 `if flag:`，而不是 `if flag == True:`。
- 检查 `if x == None`：使用 `if x is None`，因为 `None` 是一个单例。
- 在适合用 `enumerate` 或推导式的地方，用索引计数器来构建列表。
- 像 `def f(items=[])` 这样的可变默认参数，它会在多次调用之间被共享。使用 `None`，然后在函数内部创建列表。
