`[Parameter(ValueFromPipelineByPropertyName=$true)]` 会将记录属性绑定到同名参数。按值绑定将输入对象作为一个值传入；按属性绑定则从该对象中获取匹配的字段。在这里，`Value` 和 `Factor` 是声明的字段，且它们的名称匹配时不区分大小写。

此函数从每个传入的记录中输出 `Value` 字段：

```powershell
function Get-RecordValue {
    [CmdletBinding()]
    param(
        [Parameter(ValueFromPipelineByPropertyName=$true)]
        [int]$Value
    )
    process { $Value }
}
[pscustomobject]@{ Value = 3 } | Get-RecordValue
```

结果为 `3`。绑定发生在为该记录运行 `process` 之前，因此该代码块读取的是参数，而不是自行提取属性。

可选参数的默认值会分别应用于每个输入。在 `Get-Scaled` 中，包含 `Factor = 8` 的记录后面跟着一个不包含 `Factor` 的记录时，将分别使用因子 `8` 和 `2`。缺失的属性不会保留上一条记录的因子。显式指定的命名参数具有更高的优先级：`$Inputs | Get-Scaled -Factor 4` 会对每条记录都使用 `4`，即使记录本身包含 `Factor`。

### 完成 Get-Scaled

将占位符 `Scaled` 的值替换为绑定参数的乘积。保留两个属性绑定属性（property-binding attributes），并在 `process` 中只输出一个对象，该对象包含 `Value`、生效的 `Factor` 以及 `Scaled`。

包装函数接受零到八条记录。每条记录都需要一个介于 0 到 8 之间的整数 `Value`；可选的 `Factor` 和 `Options.Factor` 使用相同的范围。保留其对缺失 `Value` 或无效值的拒绝行为。它将结果收集在 `Items` 中，保留顺序和重复项，并以数组形式呈现空、单个和多个结果。辅助函数中多余的裸表达式（bare expressions）将会变成多余的项。

### 解答

```powershell
function Get-Scaled {
 [CmdletBinding()] param([Parameter(ValueFromPipelineByPropertyName=$true)][ValidateRange(0,8)][int]$Value,[Parameter(ValueFromPipelineByPropertyName=$true)][ValidateRange(0,8)][int]$Factor=2)
 process { [pscustomobject]@{Value=$Value;Factor=$Factor;Scaled=$Value * $Factor} }
}
function Invoke-Exercise {
 param($Inputs,$Options)
 try {
  if (@($Inputs).Count -gt 8) { throw 'limit' }
  foreach ($record in $Inputs) { if ($null -eq $record.Value) { throw 'value' } }
  if ($null -ne $Options.Factor) { $items=@($Inputs | Get-Scaled -Factor $Options.Factor) }
  else { $items=@($Inputs | Get-Scaled) }
  [pscustomobject]@{Items=@($items)}
 } catch { [pscustomobject]@{Rejected=$true} }
}
```
