当 PowerShell 绑定调用时，类型化参数会将其对应的实参转换为其声明的类型。
在参数名前放置 `[int]` 可以在函数体使用该值之前请求将其转换为整数：

```powershell
function Increase-Integer {
    param([int]$first)
    return ($first + 1)
}
Increase-Integer -first '08'
```

该调用返回数字 `9`。
实参最初是文本，但在函数内部 `$first` 包含整数 `8`。
命名实参仍然通过名称来选择参数；其类型声明控制着转换。
传入数字 `8` 会产生相同的结果。

你还可以选择在函数内部的哪个位置进行转换：

```powershell
function Convert-IntegerText {
    param($text)
    $number = [int]$text
    return $number
}
Convert-IntegerText -text '014'
```

`[int]$text` 是一种显式类型转换，即将值转换为所请求类型的表达式。
此处的转换发生在赋值执行时，而不是在绑定实参时。
结果是数字 `14`；文本中的前导零不会改变其十进制值。

请在进行算术运算之前确定好转换时机。
如果左侧是文本，`'4' + '9'` 会将字符串拼接为 `'49'`。
转换后，`4 + 9` 则会将数字相加得到 `13`。
像 `'four'` 这样的文本无法转换为整数：类型化参数会在绑定期间失败，而显式类型转换则会在该表达式执行时失败。

### 相加数值字段

使用两个类型化参数 `[int]$first` 和 `[int]$second` 完成 `Add-NumericFields`。
将它们的数值和作为一个数字返回。
每个实参都是一个整数或十进制整数文本，并且两者可以混合搭配使用这两种形式。
前导零和零都是有效的。
输入均为较小的非负值；格式错误的文本以及超出整数转换范围的值不在本次任务考虑范围内。
请将中间计算保存在赋值语句中，以免输出多余的结果。

### 解答

```powershell
function Add-NumericFields {
    param([int]$first, [int]$second)
    # 类型化参数已把文本转换为整数，因此这里是数值相加
    $sum = $first + $second
    return $sum
}
```
