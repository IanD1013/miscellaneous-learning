数值比较会在两个数字之间放置一个运算符，并检查它们之间的关系。
例如，`4 -eq 4` 用于检查这两个数字是否相等：

```powershell
4 -eq 4
3 -lt 4
4 -ge 4
```

每一行都会产生 true。`-eq` 表示等于（equal），`-lt` 表示小于（less than），`-ge` 表示大于或等于（greater than or equal）。
从左到右阅读：`3 -lt 4` 询问 3 是否小于 4。
前导连字符属于运算符的一部分；它并不执行减法操作。

更改第一个数字，观察每个测试在何时不再为 true。`3 -eq 4` 会产生 false，因为这两个数字不相同。`4 -lt 4` 会产生 false，因为相等的数字互不小于对方。`3 -ge 4` 会产生 false，因为 3 小于 4。
相等的情况符合 `-ge` 的条件，因此 `4 -ge 4` 会产生 true。

这些结果是布尔值（Boolean values），它们只有两种可能：true 和 false。
PowerShell 将这些值表示为 `$true` 和 `$false`。
美元符号是每个名称的一部分。
带引号的词（例如 `"true"`）是字符串；请直接让比较操作产生布尔值。

请将比较与赋值区分开来。`$number = 4` 将 4 存储在变量中。`$number -eq 4` 则在不改变其值的情况下检查该值。

比较操作也可以是函数的唯一输出：

```powershell
function Test-Equal {
    param($left, $right)
    $left -eq $right
}
```

最后一行比较这两个参数并输出其布尔结果。

### 检查最小值

使用 `$value` 和 `$minimum` 参数完成 `Test-Minimum`。
在本练习中，两个输入均为 0 到 20 之间的整数。
使用 `-ge` 精确输出一个布尔值：当值至少达到最小值（包括相等）时为 true，当值低于最小值时为 false。
请将上面示例中的表达式保留在函数外部，以免它们产生额外的输出。

### 解答

```powershell
function Test-Minimum {
    param($value, $minimum)
    # 比较结果即布尔值输出
    $value -ge $minimum
}
```
