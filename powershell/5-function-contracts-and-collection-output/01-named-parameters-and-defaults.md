命名参数通过参数名称来指定参数，因此你可以按照最易读的顺序来传递参数。
当调用者可以省略某个参数时，在 `param` 中为该参数提供一个默认表达式：

```powershell
function Add-Offset {
    param($value, $offset = 2)
    $value + $offset
}

Add-Offset -offset 3 -value 4
Add-Offset 4
```

第一次调用返回 `7`。
即便声明中先列出 `$value`，`-offset` 也会将 `3` 赋值给 `$offset`，且 `-value` 会将 `4` 赋值给 `$value`。
第二次调用是位置参数调用：`4` 传递给第一个参数。
由于未提供偏移量，因此 `$offset` 使用其默认表达式 `2`，结果为 `6`。

传递零与省略参数不同。
`Add-Offset 4 0` 返回 `4`：传入的 `0` 会替换默认值。
使用 `if ($offset)` 检查会将零视为 false，并可能错误地替换为 `2`。
请将默认值放在参数声明中，以便仅在省略该参数时才应用默认值。

在 `main.ps1` 中完成 `Get-AdjustedValue`，保留 `param($value, $offset = 2)`。
返回一个数值：传入的值加上偏移量。
本练习中两个参数的输入均为 `0` 到 `20` 之间的整数。

提供的调用代码会将两次调用收集到一个包含 `Named` 和 `Positional` 属性的对象中。
无论偏移量是被省略还是显式传入零，这两个属性都必须包含相同的和。
你的辅助函数返回该数字；提供的代码会创建报告。

### 解答

```powershell
function Get-AdjustedValue {
    param($value, $offset = 2)
    # 默认值只在省略参数时生效，显式传入的 0 会替换默认值
    return $value + $offset
}
```
