`[CmdletBinding(SupportsShouldProcess=$true)]` 为高级函数提供了一个名为 `-WhatIf` 的开关参数。保持 `SupportsShouldProcess` 设置为常量 `$true`；调用者在调用函数时选择是否启用预览模式。函数本身仍然会运行，因此请将更改文件的操作放置在 `ShouldProcess` 防护语句中：

```powershell
function Set-Text {
    [CmdletBinding(SupportsShouldProcess=$true)]
    param($Path, $Content)

    if ($PSCmdlet.ShouldProcess($Path, 'Replace content')) {
        Set-Content $Path $Content -NoNewline
    }
}
```

`$PSCmdlet.ShouldProcess($Path, 'Replace content')` 会请求对该目标执行指定操作的权限。常规调用会使该方法返回 `$true` 并进入写入分支。在带有 `-WhatIf` 参数时，它会描述拟执行的操作并返回 `$false`。该宿主描述与函数的成功输出是分开的。未受保护的写入操作仍将执行：仅添加属性并不能保护文件状态。

例如，`Set-Text -Path '/workspace/data.txt' -Content 'b' -WhatIf` 会预览替换操作。显式使用 `-WhatIf:$false` 可以实际执行该操作。这些路径指向浏览器工作区中的虚拟文本文件。

### 完成预览结果

在 `main.ps1` 中实现 `Set-PreviewContent -Lines $Lines`，并保留所提供的 `Convert-Lines` 辅助函数。使用 `Get-Content $Path -Raw` 读取 `/workspace/data.txt`，然后在请求权限或写入之前捕获辅助函数生成的候选内容。该辅助函数接受空列表，拒绝超过 8 行的输入，并拒绝 null 行、长度超过 40 个字符的行或仅包含空白字符的行。它会修剪有效行、将其转换为小写并使用 `|` 进行连接。

使用 `-cne` 比较现有内容与候选文本。仅在内容不同时才需要调用 `ShouldProcess`。使用该调用保护替换操作，并使用 `Set-Content $Path $desired -NoNewline`，以确保不会添加尾随换行符。

返回且仅返回一个包含以下属性的对象：

- `Success`: 当转换成功时为 `$true`，包括预览模式或内容未发生更改的情况。
- `WouldChange`: 经过验证的候选文本是否与现有内容不同。
- `Changed`: 仅在受保护的写入操作实际执行后才为 `$true`。
- `Content`: 成功时的候选文本，即使在预览模式下也是如此。

在进入防护检查或写入操作之前捕获转换失败。此时返回 `Success=$false`、两个更改标志均为 `$false`，并将原始内容作为 `Content` 返回；同时保留原文件。请捕获中间值而不是将其输出。重复预览必须保持原文件不变，并继续报告相同的候选内容。

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

function Set-PreviewContent {
    [CmdletBinding(SupportsShouldProcess=$true)] 
    param($Lines)
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
