`[CmdletBinding()]` 用于标记高级函数声明。将其直接放置在 `param(...)` 之前。`[switch]` 参数为调用者提供了一个选项，他们只需指定该参数名称即可启用它，而无需提供单独的实参：

```powershell
function Get-EmptyOption {
    [CmdletBinding()]
    param([switch]$IncludeEmpty)
    return [bool]$IncludeEmpty
}

Get-EmptyOption                       # False
Get-EmptyOption -IncludeEmpty         # True
Get-EmptyOption -IncludeEmpty:$false  # False
```

省略该 switch 会使其值为 false。仅指定其名称会将其设为 true。`-IncludeEmpty:$false` 中的冒号为指定的 switch 附加了显式的 false 值。最后那次调用仍然提供了该参数，因此仅检查是否提供了该参数会错误地启用该选项。请使用 `$IncludeEmpty` 作为条件；`[bool]$IncludeEmpty` 表示与布尔结果相同的值。

初始代码中的 `Get-Selected` 通过 `-Values` 接收一个数组，并接受可选的 `-IncludeEmpty` switch。例如，`Get-Selected -Values @('', 'red') -IncludeEmpty` 通过名称传递了这两个参数。`-Values` 接收其后的数组实参，而 `-IncludeEmpty` 则启用该选项。这些都是普通的函数调用；这些值作为一个数组整体传入。

### 仅在请求时保留空字符串

更新 `main.ps1` 中的 `Get-Selected`，保留其高级声明和参数类型。它应返回一个包含以下内容的对象：

- `Values`：按原始顺序排列的已选值，包括重复项。当 switch 为 false 时，仅移除空字符串（`''`）。当 switch 为 true 时，保留所有值。
- `Included`：switch 的布尔值，即使输入数组为空也是如此。

对于空结果和单值结果，保持 `Values` 具有数组形态。初始代码中的 `@($selected)` 已经处理了这一点。在累加选定内容时不要输出中间值：循环内多余的裸表达式将成为函数的额外输出。

提供的 `Invoke-Exercise` 会在省略 switch、启用 switch 或显式为 false 的情况下调用你的函数。系统会使用多个输入调用你的函数，并比较返回的每个对象。

### 解答

```powershell
function Get-Selected {
    [CmdletBinding()]
    param([object[]]$Values=@(), [switch]$IncludeEmpty)
    $selected=@()
    foreach ($value in $Values) {
        # switch 为 true 时保留所有值，否则只移除空字符串
        if ($IncludeEmpty -or $value -ne '') { $selected += $value }
    }
    return [pscustomobject]@{ Values=@($selected); Included=[bool]$IncludeEmpty }
}
```
