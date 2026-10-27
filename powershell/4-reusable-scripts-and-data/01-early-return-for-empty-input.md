提前 `return` 可以在条件表明无需计算结果时立即结束函数。
请将此检查放在计算之前：

```powershell
function Get-CountPlusOne {
    param($values)
    if ($values.Count -eq 0) { return $null }
    $values.Count + 1
}
```

我们熟悉的 `if` 会检查数组的 `Count` 是否等于 0。
其大括号内包含针对空输入的操作。`return $null` 会立即结束当前函数，因此对于空数组，最后一行永远不会执行。`$null` 是 PowerShell 中表示无结果的值。
美元符号是其名称的一部分；它不是文本 `'null'`。

如果有两个元素，条件为 false，函数输出 `3`。
如果没有元素，则不产生任何值。
这种检查被称为 guard（保护条件）：它处理无法进行计算的情况，将剩余的代码留给其他输入。

对于求平均值，空数组保护条件还可以防止除以零。
一旦确定数组非空，就可以复用度量摘要：

```powershell
$values = @(2, 5)
$summary = $values | Measure-Object -Sum
$summary.Sum / $summary.Count
```

这里的 `Sum` 是 `7`，`Count` 是 `2`。`/` 运算符将它们相除得到 `3.5`。
在经过空数组保护条件检查之后，该计数不可能为零。
将摘要赋值给变量可以避免它出现在函数的输出中；最后的裸表达式则会输出平均值。

return 不会清除之前的输出。
在保护条件之前的裸数字或字符串仍然会作为结果的一部分输出，即使函数稍后返回了 `$null` 也是如此。

### 计算平均值

完成 `Get-Average`，保留 `param($values)`。
输入是一个包含 0 到 6 个整数的数组，每个整数的范围为 0 到 20。

- 练习在进行任何输出或除法之前，针对空数组提前 `return $null`。
- 对于非空输入，仅输出其算术平均值，包括小数。使用 `Measure-Object -Sum` 来计算它。

包含 0 的非空数组的平均值为 0。
将 `$null` 保留给不存在平均值的空数组。

### 解答

```powershell
function Get-Average {
    param($values)
    # 保护条件：空数组没有平均值
    if ($values.Count -eq 0) { return $null }
    $summary = $values | Measure-Object -Sum
    $summary.Sum / $summary.Count
}
```
