管道组合通过将一个函数的成功输出作为下一个函数的输入来连接各个函数。在这里，规范化在聚合看到每条记录之前对其进行更改：

```powershell
$records = @([pscustomobject]@{ Key = 'UP'; Value = 2 })
$records | Convert-Normalized | Get-KeyTotals
```

`Convert-Normalized` 发出一个带有小写 `Key` 和原始 `Value` 的记录。`Get-KeyTotals` 通过 `[Parameter(ValueFromPipelineByPropertyName=$true)]` 绑定这些属性。因此，所发出对象上的名称和值是函数间连接的一部分。将记录格式化为文本将会破坏这一契约。

在这个浏览器宿主环境中，每个上游阶段执行完毕并且其全部输出被收集后，下一个阶段才会接收它。原生 PowerShell 通常在记录可用时在各阶段之间流式传输记录。这些练习演示了记录转换和生命周期计数；它们并不演示原生流式传输、交错的阶段执行或流式传输过程中的资源使用。

每个裸表达式都会产生成功输出。例如在 `process` 内部的一个字符串 `'normalizing'` 会成为下游的另一个输入。稍后的 `return` 不会移除已经发出的成功输出；`return` 之后的代码不会运行。从 normalizer 为每条记录恰好发出一个 `[pscustomobject]`，且不包含诊断文本。不要将这些记录收集到一个嵌套数组中。普通的数组输出会展开为单独的管道值。

在起始代码中完成 `Convert-Normalized`，以便每次 `process` 调用在应用 `$Key.ToLower()` 的同时保留 `$Value`。在 `Invoke-Summary` 中保持提供的组合：

```powershell
$Records | Convert-Normalized | Get-KeyTotals
```

调用方使用 `Invoke-Summary -Records $Inputs`。保持其他函数及其验证完整不变。输入最多包含八条记录；每条记录都有一个长度最多为 40 个字符的非空字符串 `Key` 以及一个介于 0 到 8 之间的整数 `Value`。被拒绝的绑定会终止调用并到达外部 `catch`，后者返回 `{Rejected=$true; Processes=...}`。

对于接受的输入，`Get-KeyTotals` 在 `begin` 中初始化一次，在 `process` 中对每条规范化记录更新一次，并在 `end` 中发出一个汇总摘要。其 `Count` 包括重复项，`Total` 对每个值求和，而 `Groups` 按首次出现的顺序包含小写键，每个都包含 `Key`、`Count` 和 `Total`。`@($groups)` 属性使 `Groups` 在为空、单个和多个分组时都保持为数组。

`Invoke-Exercise(Inputs, Options)` 返回 `Summary`、`Begins`、`Processes` 和 `Ends`；`Options` 未被使用。空输入仍会返回零值摘要，其中 `Groups=[]`、`Begins=1`、`Processes=0` 且 `Ends=1`。对于任何接受的输入，两个生命周期计数器都保持为 1，且 `Processes` 等于记录计数。

### 解答

```powershell
function Convert-Normalized {
 [CmdletBinding()] param([Parameter(ValueFromPipelineByPropertyName=$true)][ValidateNotNullOrEmpty()][string]$Key='unused',[Parameter(ValueFromPipelineByPropertyName=$true)][ValidateRange(0,8)][int]$Value)
 process { [pscustomobject]@{Key=$Key.ToLower();Value=$Value} }
}
function Invoke-Summary {
 param($Records)
 $Records | Convert-Normalized | Get-KeyTotals
}
function Get-KeyTotals {
 [CmdletBinding()] param([Parameter(ValueFromPipelineByPropertyName=$true)][ValidateNotNullOrEmpty()][string]$Key='unused',[Parameter(ValueFromPipelineByPropertyName=$true)][ValidateRange(0,8)][int]$Value)
 begin { $totals=@{}; $keys=@(); $count=0; $total=0; $script:Begins++ }
 process {
  $script:Processes++; $keyName=$Key.ToLower()
  if (-not $totals.ContainsKey($keyName)) { $totals[$keyName]=[pscustomobject]@{Key=$keyName;Count=0;Total=0}; $keys+= $keyName }
  $totals[$keyName].Count++; $totals[$keyName].Total+= $Value
  $count++; $total+= $Value
 }
 end { $script:Ends++; $groups=@(foreach ($keyName in $keys) { $totals[$keyName] }); [pscustomobject]@{Count=$count;Total=$total;Groups=@($groups)} }
}
function Invoke-Exercise {
 param($Inputs,$Options)
 $script:Begins=0; $script:Processes=0; $script:Ends=0
 try {
  if (@($Inputs).Count -gt 8) { throw 'limit' }
  foreach ($record in $Inputs) { if ($null -eq $record.Key -or $record.Key.Length -gt 40 -or $null -eq $record.Value) { throw 'record' } }
  $summary=Invoke-Summary -Records $Inputs
  [pscustomobject]@{Summary=$summary;Begins=$script:Begins;Processes=$script:Processes;Ends=$script:Ends}
 } catch { [pscustomobject]@{Rejected=$true;Processes=$script:Processes} }
}
```
