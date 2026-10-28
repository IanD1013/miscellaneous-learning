捕获被拒绝的转换并不能撤销早前的写入。辅助函数可能会接受第一条记录但拒绝最后一条记录，因此请将转换后的行保留在内存中，直到每个辅助函数调用都成功为止。原始行验证检查了你打算写入的文本；而在这里，替换文本必须首先由一个可能会失败的辅助函数计算得出。

使用结构化的失败策略：将常规拒绝转换为单个结果对象，同时保留原始文件。在转换前捕获原始文本，并对辅助函数的输出进行赋值，以避免其作为额外的结果逸出：

```powershell
$before = Get-Content '/workspace/data.txt' -Raw
try {
    $converted = Convert-Record -Value $record.Value
    $row = $record.Key + ':' + $converted
} catch {
    return [pscustomobject]@{ Success=$false; Changed=$false; Content=$before }
}
```

具名 `-Value` 调用在其函数体运行之前会先触发辅助函数的 `[ValidateRange(0,8)]` 检查。被拒绝的值会将控制权转移到 `catch`；有效值则返回输入值加一。该代码片段处理单条记录。你的函数必须在提交任何内容之前保护整个转换过程。

在 `main.ps1` 中完成 `Invoke-Transform`，并保持 `Convert-Record` 不变。仅读取和替换虚拟文件 `/workspace/data.txt`。

- 接受 0 到 8 条记录。每条记录包含一个最多 40 个字符的非空字符串 `Key` 和一个 0 到 8 之间的整数 `Value`。在不进行写入的情况下，拒绝记录过多、字段缺失、无效键以及超出该范围的值。
- 为每条记录暂存一行 `Key:convertedValue`，保留顺序和重复的键。使用 `-join '|'` 连接各行；空输入产生空文本。
- 使用 `-cne` 将候选文本与原始文本进行比较。仅在两者不同时，使用 `Set-Content` 和 `-NoNewline` 进行一次提交，以避免添加末尾换行符。
- 恰好返回一个包含 `Success`、`Changed` 和 `Content` 的对象。成功时报告候选内容以及它是否不同；失败时报告 `$false`、`$false` 和原始文本。每次调用时启动一个新的暂存集合，以便重复成功的转换时报告无更改。

### 解答

```powershell
function Convert-Record {
    [CmdletBinding()] 
    param(
        [Parameter(Mandatory=$true)][ValidateRange(0,8)][int]$Value
    )
    return ($Value + 1)
}

function Invoke-Transform($Records) {
    $path = '/workspace/data.txt'
    $before = Get-Content $path -Raw

    try {
        if (@($Records).Count -gt 8) { throw 'Too many records' }
        # 每次调用都从新的暂存集合开始
        $rows = @()
        foreach ($record in $Records) {
            if ($null -eq $record.Key -or $record.Key.Length -eq 0 -or $record.Key.Length -gt 40 -or $null -eq $record.Value) { throw 'Invalid record' }
            $converted = Convert-Record -Value $record.Value
            $rows += ($record.Key + ':' + $converted)
        }
        $desired = $rows -join '|'
    } catch {
        return [pscustomobject]@{ Success=$false; Changed=$false; Content=$before }
    }
    $changed = $false
    if ($before -cne $desired) {
        Set-Content $path $desired -NoNewline
        $changed = $true
    }
    return [pscustomobject]@{ Success=$true; Changed=$changed; Content=$desired }
}
```
