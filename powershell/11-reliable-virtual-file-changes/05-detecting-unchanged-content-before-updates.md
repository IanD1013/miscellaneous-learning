幂等更新只将内容更新为目标值一次；重复相同的请求将使其保持不变。在请求写入权限之前，将暂存文本与当前的原始文本进行比较：

```powershell
$current = 'A'
$desired = 'a'
$wouldChange = $current -cne $desired
```

`-cne` 对字符串进行区分大小写的比较，因此该表达式为 true。普通的 `-ne` 会将这些值视为相等，并保留大写内容。请将文件与规范化后的候选内容进行比较，而不是比较原始输入行。

在 `main.ps1` 中完成 `Set-DesiredContent($Lines)`。保留提供的 `Convert-Lines` 辅助函数以及现有的 `[CmdletBinding(SupportsShouldProcess=$true)]` 声明。仅操作位于 `'/workspace/data.txt'` 的现有虚拟文件。

使用 `Get-Content $Path -Raw` 读取其当前文本，并使用 `$desired = Convert-Lines -Lines $Lines` 获取辅助函数的输出。该辅助函数接受 0 到 8 个字符串，修剪（trim）前每个字符串最多 40 个字符。它会拒绝 null 或仅包含空白字符的行，修剪并转换为小写每个接受的行，保留顺序和重复项，并用 `'|'` 连接它们。空数组将生成空文本。

转换成功后，使用区分大小写的比较计算 `WouldChange`。将 `Changed` 初始化为 `$false`。仅当文本存在差异时调用 `$PSCmdlet.ShouldProcess($Path, 'Replace content')`，并且仅在它返回 true 时才执行写入。使用 `Set-Content $Path $desired -NoNewline`；添加换行符会导致下一次原始比较出现差异。仅在写入后将 `Changed` 设置为 `$true`。

返回一个包含以下字段的 `[pscustomobject]`：

- `Success`：对于有效输入为 `$true`，包括未更改的内容和预览。
- `Changed`：指示本次调用是否写入了文件。
- `WouldChange`：指示写入前当前文本与目标文本是否不同。
- `Content`：有效输入的目标文本。

捕获转换失败，保持文件不变，并返回 `Success`、`Changed` 和 `WouldChange` 均为 `$false`，其中 `Content` 保留原始文本。捕获中间表达式，使函数仅输出其结果对象。

使用 `-WhatIf` 时，存在差异的内容仍会报告 `WouldChange=$true` 以及预期的 `Content`，而 `Changed=$false` 且文件保持不变。重复该预览仍会发现差异。在实际更新后，重复请求会将两个变更字段都报告为 `$false`。

### 解答

```powershell
function Convert-Lines($Lines) {
 if (@($Lines).Count -gt 8) { throw 'Too many lines' }
 $staged = @()
 foreach ($line in $Lines) {
  if ($null -eq $line -or $line.Length -gt 40 -or $line.Trim().Length -eq 0) { throw 'Invalid line' }
  $staged += $line.Trim().ToLower()
 }
 return ($staged -join '|')
}
function Set-DesiredContent {
 [CmdletBinding(SupportsShouldProcess=$true)] param($Lines)
 $path = '/workspace/data.txt'
 $before = Get-Content $path -Raw
 try {
  $desired = Convert-Lines -Lines $Lines
 } catch {
  return [pscustomobject]@{ Success=$false; Changed=$false; WouldChange=$false; Content=$before }
 }
 $wouldChange = $before -cne $desired
 $changed = $false
 if ($wouldChange) {
  # 只有内容不同才请求权限，-WhatIf 时 ShouldProcess 返回 $false
  if ($PSCmdlet.ShouldProcess($path, 'Replace content')) {
   Set-Content $path $desired -NoNewline
   $changed = $true
  }
 }
 return [pscustomobject]@{ Success=$true; Changed=$changed; WouldChange=$wouldChange; Content=$desired }
}
```
