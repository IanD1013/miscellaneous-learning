将 `if` 放在 `foreach` 内部，分别决定要输出哪些数字：

```powershell
function Show-LargeNumbers {
    foreach ($number in @(9, 2, 6)) {
        if ($number -ge 6) {
            $number
        }
    }
}
```

这会保留 9 和 6（包括等于阈值的值），并丢弃 2。
只有当条件为真时，单独的 `$number` 才会产生输出。
每次迭代都会访问下一个输入值，因此匹配的数字会保持其原始顺序。

运行（Run）会根据函数产生的值的数量来显示输出：不包含输出表达式的函数体显示 `null`；仅包含 `9` 的函数体显示 `9`；包含 `9` 然后是 `6` 的函数体显示 `[9,6]`。

完成带有参数 `$values` 和 `$minimum` 的 `Get-FilteredValues`。
练习结合使用 `foreach`、`if` 和数值比较运算符 `-ge`，以输出每个大于或等于所提供最小值的数字。
按输入顺序输出数字本身，不要将它们相加。
不要产生任何其他输出。

`$values` 包含 0 到 6 个介于 0 到 20 之间的整数，`$minimum` 是一个介于 0 到 20 之间的整数。
空输入或没有匹配数字的输入不得产生任何输出。

### 解答

```powershell
function Get-FilteredValues {
    param($values, $minimum)
    foreach ($value in $values) {
        if ($value -ge $minimum) {
            # 只有满足条件的数字才会输出，并保持输入顺序
            $value
        }
    }
}
```
