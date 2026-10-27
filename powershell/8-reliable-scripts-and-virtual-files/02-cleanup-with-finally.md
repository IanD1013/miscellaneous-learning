`finally` 将清理操作集中放在 `try` 以及任何适用的 `catch` 之后。
无论操作成功、捕获到终止性失败，还是从任意块内部执行 `return` 退出时，它都会运行。
如果仅在成功读取后编写删除逻辑，就会遗漏失败路径。

以下函数读取一个临时虚拟文件并将其删除，即使读取操作提前返回：

```powershell
function Read-TemporaryText {
    Set-Content '/workspace/sample.txt' 'A' -NoNewline
    try {
        return (Get-Content '/workspace/sample.txt' -Raw)
    } catch {
        return $null
    } finally {
        if (Test-Path '/workspace/sample.txt') {
            Remove-Item '/workspace/sample.txt'
        }
    }
}
```

返回表达式在清理之前求值。
随后 `finally { ... }` 会在控制权离开函数之前运行，因此调用方会收到 `'A'`，而该文件已被删除。
`Test-Path` 返回一个布尔值，指示路径是否存在；保护条件使删除操作具备条件性。
`Remove-Item` 会删除该特定文件。
请保持清理操作静默执行：在 `finally` 中出现无修饰的裸字符串会将另一个成功输出值与预期结果一同输出。

临时文件的所有权决定了你可以删除哪个路径。
在此处，`sample.txt` 归本操作所有。
不相关的文必须保留，即使将其删除会让工作区看起来更整洁。

### 完成临时写入

使用 `try`、`catch` 和 `finally` 实现 `Invoke-TemporaryWrite($text, $fail)`。
`$text` 包含 0 到 40 个 ASCII 字母、数字或空格；`$fail` 为布尔值。

- 在 `/workspace/keep.txt` 中写入初始内容 `Keep`，不带换行符。
在清理过程中保留该文件。
- 在 `try` 内部，创建或覆盖预留的临时路径 `/workspace/temp.txt`，内容为 `Working`，不带换行符。
该预留路径下的任何先前内容均可被替换。
- 当 `$fail` 为 true 时，在创建临时文件后 throw `'Requested failure'`。
捕获该异常并记录状态 `'Error'` 以及文本 `$null`。
- 否则，将 `$text` 写入临时文件且不带换行符，使用 `Get-Content -Raw` 读取它，并记录状态 `'Ok'` 及读取到的文本。
将读取结果赋给一个变量，以免其变成额外的输出。
- 在 `finally` 中删除拥有的临时文件，并使用 `Test-Path` 进行保护性检查。

清理完成后，按顺序返回一个包含属性 `Status`、`Text`、`TemporaryExists` 和 `KeepText` 的 `[pscustomobject]`。
使用 `Test-Path` 和 `Get-Content -Raw` 从实际文件中读取最后两个属性。
选择 `'Ok'` 仅表示写入成功；这并不能证明临时文件已被删除。

### 解答

```powershell
function Invoke-TemporaryWrite {
    param($text, $fail)
    Set-Content '/workspace/keep.txt' 'Keep' -NoNewline
    $status = 'Error'
    $result = $null
    try {
        Set-Content '/workspace/temp.txt' 'Working' -NoNewline
        if ($fail) { throw 'Requested failure' }
        Set-Content '/workspace/temp.txt' $text -NoNewline
        # 空文件读取可能得到 $null，用 [string] 转换为空字符串
        $content = [string](Get-Content '/workspace/temp.txt' -Raw)
        $status = 'Ok'
        $result = $content
    } catch {
        $status = 'Error'
        $result = $null
    } finally {
        # 只删除本操作拥有的临时文件
        if (Test-Path '/workspace/temp.txt') {
            Remove-Item '/workspace/temp.txt'
        }
    }
    $keep = Get-Content '/workspace/keep.txt' -Raw
    return [pscustomobject]@{
        Status          = $status
        Text            = $result
        TemporaryExists = (Test-Path '/workspace/temp.txt')
        KeepText        = $keep
    }
}
```
