一个 `if` 语句使用一个条件（即 true 或 false 的测试）来选择运行哪段代码。
其 true 分支是 `if` 后面的代码块。
其 false 分支是 `else` 后面的代码块。
每次调用只会运行其中一个分支。

```powershell
function Get-Category {
    param($value)
    if ($value -ge 5) {
        'High'
    } else {
        'Low'
    }
}
```

`if` 语句位于函数体内部，在 `param($value)` 之后。`if` 后面的圆括号 `(` 和 `)` 包裹着条件。
在这里，`$value -ge 5` 使用了你之前练习过的比较操作符：`-ge` 表示大于或等于。
每对大括号 `{` 和 `}` 包裹一段代码块。
第一个代码块属于 `if`；`else` 引入第二个代码块，并且自身不需要条件。

当 `$value` 等于 6 时，比较结果为 true，因此函数输出 `High` 并跳过 `else` 块。
当值为 4 时，比较结果为 false，因此它跳过第一个代码块并输出 `Low`。
当值正好是 5 时，比较结果为 true，因为 `-ge` 包含相等的情况。
所选代码块中的单引号字符串会作为函数的输出提供。
圆括号内的比较仅用于选择分支，而不会向该输出中添加布尔值。

### 对数字进行分类

使用 `if` 和 `else` 完成 `Get-Category`，将阈值设为 **10**（而不是示例中的 5）。
参数 `$value` 是一个介于 0 到 20 之间（含 0 和 20）的整数。

- 当 `$value` 大于或等于 10 时，准确输出 `High`。
- 当 `$value` 小于 10 时，准确输出 `Low`。
- 仅生成所选标签，不要有多余的输出。

### 解答

```powershell
function Get-Category {
    param($value)
    if ($value -ge 10) {
        'High'
    } else {
        'Low'
    }
}
```
