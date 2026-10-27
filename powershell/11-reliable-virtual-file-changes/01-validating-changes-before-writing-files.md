暂存更改（staged change）是指在文件被修改之前保留在内存中的完整候选内容。应在内存中验证整批内容：如果最后一行校验失败，立即写入第一行已接受的内容将会损坏旧文件。

写入操作应位于可能拒绝候选内容的操作之后：

```powershell
$before = Get-Content '/workspace/data.txt' -Raw
try {
    $desired = Convert-Lines -Lines $Lines
} catch {
    return [pscustomobject]@{
        Success=$false; Changed=$false
        WouldChange=$false; Content=$before
    }
}
if ($before -cne $desired) {
    Set-Content '/workspace/data.txt' $desired -NoNewline
}
```

`Get-Content -Raw` 将整个文本读取为一个字符串。`Set-Content` 会替换它；`-NoNewline` 可防止末尾出现多余的换行符。`-cne` 区分大小写地比较字符串，因此已存在的 `A` 与期望的 `a` 是不同的。这些路径指的是练习的虚拟工作区，每次运行都会提供全新的初始文件内容。

在 `main.ps1` 中完成 `Set-ValidatedContent`，保留所提供的 `Convert-Lines` 辅助函数。它最多接受八行。每一行必须为非 null，在去除首尾空格前最多 40 个字符，在去除首尾空格后不能为空。它会去除首尾空格，转换为小写，并用 `|` 连接各行，同时保留原有顺序。空批次将生成空文本。该辅助函数在输入被拒绝时会抛出异常；请在执行任何写入操作之前调用它，以便即使最后一行无效，现有文本也能保持完全不变。

返回一个包含以下属性的对象：

- `Success`：批次被接受时为 true，批次被拒绝时为 false。
- `WouldChange`：当接受的候选文本与原始文本不同时为 true；被拒绝时为 false。
- `Changed`：仅当本次调用实际替换了不同的文件内容时为 true。已接受且已经匹配的文件无需写入。
- `Content`：成功时为最终生成的文件文本，被拒绝时为原始文本。

将 `Changed` 初始值设为 false，并在写入后对其进行设置。仅在报告中声明更改不能代替对文件的实际修改。请将中间值保存在变量中：单独的表达式会产生额外的成功输出，即使稍后的 `return` 会输出报告也是如此。请保持其他提供的文件不变。

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
function Set-ValidatedContent {
 param($Lines)
 $path = '/workspace/data.txt'
 $before = Get-Content $path -Raw
 try {
  # 先在内存中验证整批内容，再决定是否写入
  $desired = Convert-Lines -Lines $Lines
 } catch {
  return [pscustomobject]@{ Success=$false; Changed=$false; WouldChange=$false; Content=$before }
 }
 $wouldChange = $before -cne $desired
 $changed = $false
 if ($wouldChange) {
  Set-Content $path $desired -NoNewline
  $changed = $true
 }
 return [pscustomobject]@{ Success=$true; Changed=$changed; WouldChange=$wouldChange; Content=$desired }
}
```
