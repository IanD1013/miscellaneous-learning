对 `$script:FormatMode` 的临时更改会影响后续的函数调用，除非你恢复进入函数时的原始值。状态恢复意味着即使操作成功返回，也要将该共享设置恢复为其捕获的值。如果将其直接重置为 `'Plain'`，则会覆盖调用方原有的 `'Lower'` 或 `'Mixed'` 设置。

在修改设置之前先将其捕获：

```powershell
function Get-TemporaryMode {
    $saved = $script:FormatMode
    try {
        $script:FormatMode = 'Upper'
        return $script:FormatMode
    } finally {
        $script:FormatMode = $saved
    }
}
```

return 表达式在临时模式处于激活状态时捕获 `'Upper'`。`finally` 中的赋值操作会在调用方恢复执行之前恢复脚本变量。因此，返回的值与调用后的设置描述的是不同的时刻。对于可能抛出异常的工作，应使用相同的结构设计：在 `catch` 中放置结构化的失败结果，在 `finally` 中进行状态恢复。如果在局部使用 `$FormatMode` 赋值，则只会更改一个不同的变量。

### 实现转换逻辑

在 `main.ps1` 中，添加 `Convert-Lines($Lines)` 并完成 `Invoke-WithSetting($Lines)`：

- `Convert-Lines` 接受空集合或最多八个字符串。若超过八行、包含 null 行、某行在修剪前超过 40 个字符、或某行修剪后的文本为空，则抛出异常以拒绝。对于有效输入，对每一行使用 `.Trim().ToLower()`，并按输入顺序使用 `-join '|'` 连接后返回结果。空输入生成 `''`。
- `Invoke-WithSetting` 捕获传入的脚本模式，临时将其设置为 `'Upper'`，然后调用 `Convert-Lines -Lines $Lines`。成功时，返回一个 `[pscustomobject]`，包含 `Success=$true`、使用 `.ToUpper()` 转换后的文本 `Content`，以及 `Mode='Upper'`。空输入也是成功的且包含空内容（包括提前返回的情况）。
- 捕获转换失败并返回一个对象，包含 `Success=$false`、`Content=''` 以及 `Mode='Upper'`。丢弃任何部分内容。
- 在两种路径下的 `finally` 中恢复捕获的模式。仅输出结果对象；将辅助输出赋值给变量，并确保清理代码中不包含无赋值的裸表达式（bare expressions）。保持 `data.txt` 不变。

### 解答

```powershell
$script:FormatMode = 'Plain'
function Convert-Lines($Lines) {
 if (@($Lines).Count -gt 8) { throw 'Too many lines' }
 $staged = @()
 foreach ($line in $Lines) {
  if ($null -eq $line -or $line.Length -gt 40 -or $line.Trim().Length -eq 0) { throw 'Invalid line' }
  $staged += $line.Trim().ToLower()
 }
 return ($staged -join '|')
}
function Invoke-WithSetting($Lines) {
 # 修改设置之前先捕获调用方的原始值
 $saved = $script:FormatMode
 try {
  $script:FormatMode = 'Upper'
  $converted = Convert-Lines -Lines $Lines
  return [pscustomobject]@{ Success=$true; Content=$converted.ToUpper(); Mode='Upper' }
 } catch {
  return [pscustomobject]@{ Success=$false; Content=''; Mode='Upper' }
 } finally {
  # 成功、失败和提前返回都会恢复原始模式
  $script:FormatMode = $saved
 }
}
```
