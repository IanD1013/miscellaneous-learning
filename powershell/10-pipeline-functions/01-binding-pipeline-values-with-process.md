`[Parameter(ValueFromPipeline=$true)]` 允许按值将传入的管道值绑定到参数。将处理逻辑放在 `process` 中，以便每个记录都获得各自的转换：

```powershell
function Get-ValueRecord {
    [CmdletBinding()]
    param([Parameter(ValueFromPipeline=$true)][ValidateRange(0,8)][int]$Value)
    process { [pscustomobject]@{ Value = $Value } }
}
```

`[CmdletBinding()]` 启用了高级参数声明。`[int]` 声明了参数类型；`[ValidateRange(0,8)]` 将接受的整数限制在该闭区间范围内。这些是练习的边界限制，而不是整数类型本身的限制。本任务使用整数输入，因此无需做类型转换选择。

对于 `2, 5 | Get-ValueRecord`，绑定会分别为每个输入提供 `$Value`，并且 `process` 会发出两个对象。单独的对象表达式会生成成功输出；额外的诊断表达式则会变成额外的输出结果。`Get-ValueRecord -Value 5` 会直接绑定命名参数并运行一次 `process`。空管道不会提供任何记录，因此会运行零次 `process`。仅仅声明管道参数并不会使普通函数体中的代码对每个输入都重复执行。

### 完成 Get-Doubled

将初始代码中 `process` 块里的占位符 `Doubled=0` 替换为当前 `$Value` 的两倍。对每个输入发出一个包含原始 `Value` 及其 `Doubled` 值的对象，保持原有顺序和重复项。

提供的 `begin` 和 `end` 块在每次调用时都会将计数器递增一次，包括空管道的情况；`process` 计数器记录每个已处理的值。请保持这些计数器和 `Invoke-Exercise` 完好无损。包装器使用 `@(...)` 收集输出，为零个、一个或多个项保留数组，并将其与计数器一起在 `Items` 中报告。

最多接受八个整数，每个整数范围为 0 到 8。当 `Direct` 为 true 时，恰好需要一个输入。包装器对于无效输入会返回 `Rejected` 以及当前的 `Processes` 计数；在本练习中，参数验证将终止辅助调用。空管道将返回一个空的 `Items` 数组。

### 解答

```powershell
function Get-Doubled {
 [CmdletBinding()] param([Parameter(ValueFromPipeline=$true)][ValidateRange(0,8)][int]$Value)
 begin { $script:Begins++ }
 process { $script:Processes++; [pscustomobject]@{Value=$Value;Doubled=$Value * 2} }
 end { $script:Ends++ }
}
function Invoke-Exercise {
 param($Inputs,$Options)
 $script:Begins=0; $script:Processes=0; $script:Ends=0
 try {
  if (@($Inputs).Count -gt 8) { throw 'limit' }
  if ($Options.Direct) { if (@($Inputs).Count -ne 1) { throw 'direct' }; $items=@(Get-Doubled -Value $Inputs[0]) }
  else { $items=@($Inputs | Get-Doubled) }
  [pscustomobject]@{Items=@($items);Begins=$script:Begins;Processes=$script:Processes;Ends=$script:Ends}
 } catch { [pscustomobject]@{Rejected=$true;Processes=$script:Processes} }
}
```
