函数可以使用由其调用者提供的值。
为函数所需的每个值添加一个参数（parameter，即命名的输入变量）：

```powershell
function Join-Text {
    param($label, $number)
    "$label $number"
}

Join-Text 'Page' 6
```

这会生成 `Page 6`。`param` 语句位于函数内部，在使用其输入的语句之前。
圆括号 `(` 和 `)` 包裹参数列表，逗号 `,` 分隔两个参数。
每个参数名称都以 `$` 开头，就像你之前使用过的变量一样。
将下一条语句放在 `param(...)` 之后的单独一行中。

参数值（argument，实参）是在调用中提供的值。
在 `Join-Text 'Page' 6` 中，每个位置参数按顺序匹配一个形参：`'Page'` 传给 `$label`，`6` 传给 `$number`。
调用函数时，请使用空格分隔实参；用逗号分隔的圆括号属于参数声明。
后续调用可以传入不同的值，而无需更改函数体。

双引号允许插值（interpolation）：PowerShell 会将变量的值插入到字符串中。
在 `"$label $number"` 中，空格保留为字面文本。
单引号则相反，会保留内容的字面形式：`'$label $number'` 会直接输出变量名称，包括美元符号。`'Page'` 两边的单引号是合适的，因为该参数是固定的文本。

使用现有的 `$label` 和 `$count` 参数完成 `Format-Label`。
生成一个包含标签、一个空格、一个冒号、一个空格以及计数的字符串。
在 `"$label : $count"` 中，空格和冒号保留为字面文本，而变量提供它们的值。
仅输出该字符串。

在本练习中，标签是一个由 1 到 12 个英文字母（A-Z 或 a-z）组成的非空单词，计数是 0 到 20 之间的整数。
无需进行输入验证。
类似于 `Format-Label 'Boxes' 3` 的调用必须生成 `Boxes : 3`。

### 解答

```powershell
function Format-Label {
    param($label, $count)
    # 双引号字符串会插入变量的值
    "$label : $count"
}
```
