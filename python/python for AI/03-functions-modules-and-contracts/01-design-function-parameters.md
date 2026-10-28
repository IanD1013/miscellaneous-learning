默认参数允许调用方在常规选项已足够时省略该值。
在函数定义中，将 `=value` 放在参数名称后：

```python
def label(text, prefix="item: "):
    return prefix + text

label("notes")
label("notes", "file: ")
label("notes", prefix="file: ")
```

`text` 是必填参数；`prefix` 具有默认字符串 `"item: "`。
必填参数位于带有默认值的参数之前。
第一次调用返回 `"item: notes"`。
第二次调用使用位置参数：值从左到右匹配参数。
第三次调用使用关键字参数：`prefix=` 指定接收该值的参数。
这两次自定义调用均返回 `"file: notes"`。
在调用中，`name=value` 提供一个实参；在定义中，它设置默认值。
位置参数必须放在关键字参数之前。

`+` 运算符按顺序连接字符串，并保留其空格和大小写。
字符串默认值是不可变（immutable）的，这意味着其内容无法被就地修改。
在某次调用中使用自定义参数不会替换后续调用的默认值。

### 完成格式化程序

完成 `format_pair(left, right, separator="/")`。
所有三个输入都是字符串。
返回一个字符串，依次包含 `left`、`separator` 和 `right`。
保留提供的默认值，以便调用方可以省略第三个参数，或者通过位置或关键字提供它。

精确保留输入内容，包括空格和空字符串。
文本规范化（normalization）会改变此函数的返回约定（即对其输入的承诺结果）。
每次调用都必须使用其自身的参数，与之前的调用无关。

### 解答

```python
def format_pair(left, right, separator="/"):
    return left + separator + right
```
