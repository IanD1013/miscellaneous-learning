字符串在 Python 中无处不在：文件路径、用户输入、日志行、字典中的键。
面试官很喜欢考字符串，因为它能暴露出你是否理解不可变性（immutability）、切片（slicing），以及该用哪个方法。
本课涵盖你需要烂熟于心的核心 `str` 操作。
（f-string 和格式化会在下一课讲解，所以这里不涉及。）

### 不可变性

`str` 是不可变的。
一旦创建，它的字符就不能被原地修改。
每一次"修改"实际上都会返回一个全新的字符串，而原字符串保持不变。

```python
s = "hello"
s[0] = "H"          # TypeError: 'str' object does not support item assignment
s = s.replace("h", "H")  # 这样可以：它返回一个新字符串
print(s)            # Hello
```

因为方法从不修改原字符串，忘记接收返回值是一个经典 bug：

```python
name = "  ada  "
name.strip()        # 返回值被丢弃了
print(repr(name))   # '  ada  '  （没有变化）
name = name.strip() # 接收返回值
print(repr(name))   # 'ada'
```

### 索引和切片

索引返回一个单字符的字符串。
负数索引从末尾开始计数。
切片使用 `s[start:stop:step]`，其中 `stop` 是不包含的，越界的边界会被截断（clamp），而不是抛出异常。

```python
s = "python"
print(s[0])      # p
print(s[-1])     # n
print(s[1:4])    # yth   （索引 1、2、3）
print(s[:3])     # pyt
print(s[::-1])   # nohtyp  （反转）
print(s[2:99])   # thon   （stop 被截断，不报错）
```

索引超出末尾会抛出 `IndexError`，但切片超出末尾不会。

### 常用方法

- `split()` 不带参数时，会按任意连续空白字符分割，并丢弃空字符串；带参数时，会按那个精确的分隔符分割。`rsplit` 从右边开始分割，和 `maxsplit` 搭配使用效果很好。
- `join` 从一个可迭代对象构建字符串：`sep.join(parts)`。分隔符就是你调用它的那个字符串。
- `strip`、`lstrip`、`rstrip` 移除开头和结尾的字符。不带参数时移除空白字符；带参数时移除该集合中的任意字符，而不是一个前缀。
- `replace(old, new)` 替换所有出现的地方（或者只替换前 `count` 个）。
- `find` 返回索引，找不到时返回 `-1`；`index` 做同样的事，但找不到时抛出 `ValueError`。
- `startswith` 和 `endswith` 接受一个由多个选项组成的元组。
- `in` 测试子字符串成员关系。

```python
print("a,b,,c".split(","))     # ['a', 'b', '', 'c']
print("  a b  c ".split())     # ['a', 'b', 'c']
print("-".join(["1", "2", "3"]))  # 1-2-3
print("xxhelloxx".strip("x"))  # hello
print("banana".find("z"))      # -1
print("file.py".endswith((".py", ".pyw")))  # True
print("ell" in "hello")        # True
```

一个常见陷阱：`strip("ab")` 把它的参数当作一组要从两端剥离的字符，所以 `"banana".strip("an")` 得到的是 `"b"`，而不是 `"banana"` 去掉一个字面量 `"an"`。

### 构建字符串：join 胜过在循环中使用 +

对字符串每做一次 `+=`，都会创建一个新字符串并复制到目前为止的所有内容，所以在循环中拼接是 O(n²) 的。
把各个片段收集起来，然后只 `join` 一次。

```python
# 慢：每次迭代都重建整个字符串
out = ""
for word in words:
    out += word

# 推荐：最后只分配一次
out = "".join(words)
```

### 多行字符串、原始字符串和转义

三引号可以跨越多行，并保留换行符。
原始字符串（`r"..."`）会关闭转义处理，这对 Windows 路径和正则表达式模式很方便。

```python
text = """line1
line2"""
print(len(text))        # 11  （换行符算作一个字符）

print("a\tb")           # a<TAB>b
print(r"a\tb")          # a\tb   （反斜杠-t 保持字面量）
print("C:\\new")        # C:\new
print(r"C:\new")        # C:\new
```

常见转义：`\n` 换行，`\t` 制表符，`\\` 字面量反斜杠，`\'` 和 `\"` 引号。

### str 与 repr

`str()`（`print` 使用的就是它）的目标是可读的形式；`repr()` 的目标是无歧义、通常可以往返还原（round-trippable）的形式。
对于字符串，`repr` 会加上引号并显示转义字符，这就是为什么调试时 `repr` 是更好的选择。

```python
s = "a\tb"
print(str(s))   # a<TAB>b
print(repr(s))  # 'a\tb'
print(s)        # a<TAB>b  （print 使用 str）
print([s])      # ['a\tb'] （容器用 repr 显示元素）
```

最后一行是面试官最爱的陷阱：打印列表时，元素是通过 `repr` 显示的，所以制表符会显示为 `\t`。
