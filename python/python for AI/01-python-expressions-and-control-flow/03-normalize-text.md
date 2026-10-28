字符串方法是在字符串值上调用的操作。
在值与方法名之间加上点，然后加上圆括号即可调用它：

```python
text = '  READY  '
trimmed = text.strip()
small = 'READY'.lower()
changed = 'red blue'.replace(' ', '-')
```

引号用于包裹字符串文本；单引号和双引号均可。
在 `text.strip()` 中，空圆括号表示不需要任何参数。
`str.strip` 会移除两端的空白字符，包括空格、制表符和换行符。
在此处，`trimmed` 变为 `'READY'`。

`str.lower` 会生成小写文本，因此 `small` 变为 `'ready'`。
它也能处理 Unicode 字母：`'É'.lower()` 返回 `'é'`。
没有小写形式的字符则保持不变。

`str.replace` 接受要查找的文本及其替换文本，二者用逗号隔开。
在此处，`changed` 变为 `'red-blue'`。
每个匹配项都会被替换，因此两个相邻的空格会进行两次替换。

字符串是不可变（immutable）的：这些调用会返回结果，而不会改变原始字符串。
可以将每个结果保存在变量中，或者直接在其上调用下一个方法，如 `text.strip().lower()`。

使用字符串方法完成 `normalize_label(text)`。
按顺序在移除外部空白字符、转换为小写并将剩余的每个普通空格替换为 `'_'` 后返回字符串。
保留内部的制表符、换行符和其他内容。
空输入或仅包含空白字符的输入应返回 `''`。

### 解答

```python
def normalize_label(text):
    return text.strip().lower().replace(' ', '_')
```
