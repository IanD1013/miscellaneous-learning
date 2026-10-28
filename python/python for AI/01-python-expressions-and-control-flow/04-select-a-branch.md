`if` 语句用于选择一个分支，即当其条件为真时要运行的代码块。
比较运算提供了条件：`value < 0` 测试某个值是否小于零，而 `value == 0` 测试是否相等。
使用 `==` 进行比较；单个 `=` 用于赋值。

以下是在三个数值范围之间进行有序选择的示例：

```python
def describe_range(number):
    if number < 10:
        return 'small'
    elif number < 20:
        return 'medium'
    else:
        return 'large'
```

每个分支头部都以冒号结尾。
在函数内部，`if`、`elif` 和 `else` 所在行保持对齐。
它们的主体部分会进一步缩进一级，在此处增加了四个空格。
Python 使用缩进来对语句进行分组，而不是使用花括号。

Python 会首先检查 `if` 条件。
`elif` 表示仅在先前的条件为假时才尝试的另一个条件。
第一个为真的条件会选择其主体运行，并跳过其余备选分支。
对于 `5`，两个比较条件都为真，但只有第一个分支会运行。
`else` 没有条件：它用于处理先前每个条件都为假的值。
每个 `return` 也会结束函数的执行。

针对整数输入完成 `classify_sign(value)`。
练习使用 `if`/`elif`/`else` 链，在小于零时返回 `'negative'`，为零时返回 `'zero'`，大于零时返回 `'positive'`。
直接与零进行比较，以便相同的规则适用于较小和较大的整数。

### 解答

```python
def classify_sign(value):
    if value < 0:
        return 'negative'
    elif value == 0:
        return 'zero'
    else:
        return 'positive'
```
