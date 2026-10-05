Python 把文本和二进制数据保存在两种独立的类型中，面试官很喜欢考察你是否理解它们的区别。
`str` 保存文本：一个 Unicode 码点（code point）序列。
`bytes` 保存原始二进制：一个由 0 到 255 的整数组成的序列。
它们不能互换，而且 Python 3 拒绝悄悄地混用它们。
知道边界在哪里，以及如何跨越它，就是这个主题的全部内容。

### str 是文本，bytes 是二进制

`str` 是一个不可变（immutable）的 Unicode 字符序列。
`bytes` 对象是一个不可变的小整数序列（每个都在 0 到 255 之间）。
你用 `b` 前缀来写 bytes 字面量。

```python
text = "héllo"        # str，5 个字符
raw = b"hello"        # bytes，5 个字节
print(type(text), type(raw))   # <class 'str'> <class 'bytes'>
print(raw[0])                  # 104  （一个 int，而不是 'h'）
```

对 `bytes` 做索引得到的是一个 `int`，而不是单字节的 `bytes`。
然而切片得到的仍然是 `bytes`。
bytes 字面量中只能直接包含 ASCII 字符；其他任何字符都必须使用像 `\x80` 这样的转义。

### bytearray 是可变的"表亲"

`bytes` 是不可变的。
`bytearray` 是可变版本：思路相同，但你可以原地修改字节。

```python
buf = bytearray(b"abc")
buf[0] = 65          # 'A' 对应的 int
print(buf)           # bytearray(b'Abc')
```

### encode 和 decode 跨越边界

要把文本变成字节，你需要 `encode()`。
要把字节变回文本，你需要 `decode()`。
在 Python 3 中两者都默认使用 UTF-8。

```python
s = "café"
data = s.encode()          # 等同于 s.encode("utf-8")
print(data)                # b'caf\xc3\xa9'
print(s.decode)            # AttributeError: str 没有 decode
back = data.decode()       # "café"
```

记住方向：`str.encode()` 产生 `bytes`，`bytes.decode()` 产生 `str`。
`str` 没有 `decode`，`bytes` 没有 `encode`，因为它们各自已经处在自己的那一侧。

### UTF-8 和多字节字符

UTF-8 将每个 ASCII 字符编码为一个字节，但 ASCII 之外的字符需要两个、三个或四个字节。
这意味着文本的 `len()` 和它的 UTF-8 字节的 `len()` 可能不同。

```python
s = "café"
print(len(s))              # 4  （四个字符）
print(len(s.encode()))     # 5  （é 在 UTF-8 中占两个字节）

emoji = "🦊"
print(len(emoji))          # 1  （一个码点）
print(len(emoji.encode())) # 4  （UTF-8 中占四个字节）
```

对 `str` 调用 `len()` 计算的是字符（码点）数。
对 `bytes` 调用 `len()` 计算的是字节数。
把两者混为一谈是一个经典 bug。

### UnicodeDecodeError

如果你尝试 `decode()` 在所选编码中无效的字节，Python 会抛出 `UnicodeDecodeError`。
当字节是用一种编码产生的，而你却用另一种编码去解码时，这种情况很常见。

```python
data = "café".encode("utf-8")    # b'caf\xc3\xa9'
data.decode("ascii")             # UnicodeDecodeError: 字节 0xc3 不在 ASCII 中
```

你可以用 `errors` 参数来缓和这种情况：`decode("ascii", errors="replace")` 会用一个占位字符替换，而 `errors="ignore"` 会丢弃有问题的字节。
默认值是 `errors="strict"`，它会抛出异常。

### 为什么在写入磁盘或网络前要先编码

文件和网络套接字（socket）传输的是字节，而不是 Python 文本对象。
在文本离开你的程序之前，它必须被编码为字节；当字节到达时，它们必须被解码回文本。
如果双方对编码的看法不一致，你就会得到乱码（mojibake）或 `UnicodeDecodeError`。
约定使用 UTF-8 是安全的默认选择。

### ord 和 chr

`ord()` 接收单个字符并返回它的整数 Unicode 码点。
`chr()` 做相反的事，把码点转回单字符的字符串。

```python
print(ord("A"))      # 65
print(chr(65))       # 'A'
print(ord("€"))      # 8364
print(chr(8364))     # '€'
```

它们操作的是码点，而不是字节。
`ord("A")` 是码点 65；它恰好也是 'A' 的单个 UTF-8 字节，这只是 ASCII 的巧合，并不是适用于每个字符的规则。
