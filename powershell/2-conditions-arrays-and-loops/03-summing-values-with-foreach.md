`foreach` 循环会对集合中的每个元素运行相同的代码块。
下面这个简短的示例将两个值相加：

```powershell
$values = @(2, 5)
$total = 0
foreach ($value in $values) {
    $total = $total + $value
}
$total
```

`foreach` 后面的圆括号包含 `$value in $values`。
在这里，`$values` 是要遍历的集合，`in` 将其与 `$value` 分开，`$value` 是保存当前元素的循环变量。
PowerShell 将第一个元素放入 `$value`，运行 `{` 和 `}` 之间的代码，然后对下一个元素重复此操作。
该代码就是循环体；它的每次运行都是一次迭代（iteration）。

`$total` 是一个累加器（accumulator），即用于保存跨迭代累积结果的变量。
在循环之前将其设置为零，以便有一个初始值。
在第一次迭代中，`$value` 为 2，因此 `$total = $total + $value` 存储 2。
在第二次迭代中，`$value` 为 5，相同的赋值操作将存储 7。
如果将 `$total = 0` 移入循环体内部，则每次都会丢弃之前的总和。

赋值操作会更新累加器而不会产生输出。
在闭合大括号之后的最后一个单独的 `$total` 会输出一次 7。
如果将该表达式放入循环体内部，也会输出中间的总和。
对于空集合，循环体运行零次，最终表达式将输出初始值零。

### 完成 Get-Sum

保留提供的 `Get-Sum` 函数及其 `$values` 参数。
通过累加每个元素的总和来练习 `foreach`，然后在循环结束后仅输出最终完成的总和。
在本练习中，`$values` 包含零到六个整数，每个整数介于 0 到 20 之间。
处理空数组、单个元素以及多个元素；零值不会增加总和。
空数组必须输出 0。

### 解答

```powershell
function Get-Sum {
    param($values)
    # 累加器在循环之前初始化为零
    $total = 0
    foreach ($value in $values) {
        $total = $total + $value
    }
    # 循环结束后仅输出一次最终总和
    $total
}
```
