`Sync-Records` 必须仅在整个批次都有效之后才对文件进行协调（reconcile）。如果每接受一条记录就立即写入，在后续记录发生冲突时就会留下部分内容。请结合你之前练习过的管道暂存（pipeline staging）与受保护更新（guarded updates），将该决策封装在一个公共模块函数内。

### 完成模块

编辑 `reconcile.psm1` 中的 `Sync-Records`。其初始代码当前仅报告更改，而不会写入候选内容。保留提供的私有 `Convert-Records` 辅助函数，并且仅导出 `Sync-Records`。保持 `exercise-checks.ps1` 和 `data.txt` 为只读；该模块通过 `Set-Content` 更新虚拟文件。

`Sync-Records -Records $records -Path '/workspace/data.txt'` 接受一个实体化集合，包括空集合。`Path` 默认为 `/workspace/data.txt`。在去重之前，若输入记录超过 8 条则予以拒绝。对于此任务，传入的 `Key` 字段为字符串，传入的 `Value` 字段为整数。如果存在缺失字段、空键、长度超过 40 个字符的键、超出 0 到 8 范围的整数值或冲突的重复项，则拒绝整个批次。

辅助函数在 `process` 中绑定记录属性，在整个批次处理期间保留其查找表和集合。完全相同的重复键计为一个条目；值不同的重复键则抛出异常。它的 `end` 块仅在验证完成后返回 `Items` 和 `Count`。保持首次出现的顺序而不是进行排序：这可以使候选内容反映调用方的顺序，同时不允许重复项虚增计数。

### 写入前进行决策

使用 `ConvertTo-Json -InputObject @($staged.Items) -Compress` 序列化暂存的条目。数组包装器使 0 个、1 个和多个条目保持相同的 JSON 数组形态。每个条目依次包含 `Key` 和 `Value`，不含多余属性。使用 `Get-Content -Raw` 读取现有内容并比对完全一致的文本。写入操作必须使用 `-NoNewline`，以便后续相同的应用操作在比对时能够判定为相等。

只有内容不一致时才需要执行 `$PSCmdlet.ShouldProcess($Path, 'Replace content')`。在该保护分支内执行写入操作，然后将 `Changed` 标记为 true。调用方可以使用 `-WhatIf` 进行预览；跨越此模块边界时，需要显式传递它，例如 `Sync-Records -Records $records -WhatIf:$dry`，因为调用方局部的 `WhatIfPreference` 不会被继承。

恰好返回一个对象，字段按以下顺序排列：`Success`、`Changed`、`WouldChange`、`Count`。有效输入会将 `Success` 设为 true，并将 `Count` 设为唯一条目的数量。`WouldChange` 记录文本差异；`Changed` 记录实际的写入。内容相等（包括第二次执行相同的应用操作）会使两者都为 false。捕获常规故障，保留现有内容，并将所有三个标志均返回 false 且计数为 0。请对辅助函数的结果进行赋值接收，防止附带的输出混入公共结果中。

### 解答

reconcile.psm1

```powershell
function Convert-Records {
 [CmdletBinding()] param([Parameter(ValueFromPipelineByPropertyName=$true)][string]$Key,[Parameter(ValueFromPipelineByPropertyName=$true)]$Value)
 begin { $seen=@{}; $items=@() }
 process {
  if ($null -eq $Key -or $Key.Length -eq 0 -or $Key.Length -gt 40 -or $null -eq $Value -or $Value -lt 0 -or $Value -gt 8) { throw 'Invalid record' }
  if ($seen.ContainsKey($Key)) {
   if ($seen[$Key] -ne $Value) { throw 'Conflicting key' }
  } else { $seen[$Key]=$Value; $items += [pscustomobject]@{Key=$Key;Value=$Value} }
 }
 end { [pscustomobject]@{Items=@($items);Count=$items.Count} }
}
function Sync-Records {
 [CmdletBinding(SupportsShouldProcess=$true)] param($Records,[string]$Path='/workspace/data.txt')
 try {
  if (@($Records).Count -gt 8) { throw 'Too many records' }
  $staged=$Records | Convert-Records
  $text=ConvertTo-Json -InputObject @($staged.Items) -Compress
  $old=Get-Content $Path -Raw
  $would=$old -cne $text
  $changed=$false
  if ($would) {
   if ($PSCmdlet.ShouldProcess($Path, 'Replace content')) {
    # 校验全部通过之后才写入
    Set-Content $Path $text -NoNewline
    $changed=$true
   }
  }
  [pscustomobject]@{Success=$true;Changed=$changed;WouldChange=$would;Count=$staged.Count}
 } catch { [pscustomobject]@{Success=$false;Changed=$false;WouldChange=$false;Count=0} }
}
Export-ModuleMember -Function Sync-Records
```
