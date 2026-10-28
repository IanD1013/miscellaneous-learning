辅助函数（helper function）用于处理转换中的某个部分。
可以将其与调用它的函数定义在一起，然后传入所需的值：

```python
def trim_text(text):
    return text.strip()

def prepare_text(text):
    text = trim_text(text)
    return text.lower()
```

`prepare_text(" READY ")` 返回 `"ready"`。
调用 `trim_text(text)` 会将调用方的当前字符串作为参数传递给辅助函数。
辅助函数返回修剪后的字符串，赋值语句将其存储在 `prepare_text` 自己的 `text` 变量中。

每个函数都拥有局部作用域（local scope）：其形参和在其函数体内赋值的变量均属于该次函数调用。
上面的两个函数都使用了名称 `text`，但在一个函数中对其赋值并不会影响另一个函数的变量。
请通过参数和 `return` 来传递值；辅助函数不应依赖调用方内部的局部变量。
将两个函数定义置于同一缩进级别，每个函数体缩进在其 `def` 行下方。

记录循环可以为每个字符串复用同一个辅助函数：将 `record["text"]` 传递给辅助函数，并将其返回值存储在输出记录中。
构建一个单独的结果列表和单独的字典可以避免修改其他代码可能仍在使用的记录。
相反，如果直接对 `record["text"]` 赋值，则会更改输入的字典。

字典键保留其插入顺序。
编写 `{"id": identifier, "text": value}` 会在显示或迭代字典时将 ID 排在首位，从而使每条返回的记录具有一致的布局。

### 构建记录转换

起始代码包含两个未完成的函数。
请实现这两个函数：

- `normalize_text(text)` 接受一个字符串，并返回去除首尾空白字符且字母转换为小写的字符串。
  保留所有内部空白字符，包括重复的空格和制表符。
  空字符串或仅包含空白字符的文本应返回 `""`。
- `normalize_records(records)` 接受一个字典列表，字典中的 `"id"` 和 `"text"` 均为字符串值。
  返回一个字典列表，其中包含这两个键，并将 `"id"` 插入在 `"text"` 之前。
  原样保留每个 ID，并保持记录的输入顺序。
  使用与 `normalize_text` 相同的规则对每个文本进行规范化。
- 空记录列表返回 `[]`。

### 解答

```python
def normalize_text(text):
    return text.strip().lower()

def normalize_records(records):
    result = []
    for record in records:
        result.append({"id": record["id"], "text": normalize_text(record["text"])})
    return result
```
