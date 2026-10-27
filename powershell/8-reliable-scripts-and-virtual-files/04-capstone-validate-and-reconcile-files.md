对账报告必须区分格式错误的行与没有引用匹配的有效键。
结合你练习过的字面量解析器、CSV 查找和失败清理：缺失的引用数据应包含在报告中，而导致终止的失败则会阻止生成成功的报告。

### 解析与对账

在 `Main.ps1` 中完成 `Invoke-FileReconciliation($lines, $csvText, $fail)`。
提供的两个辅助文件是只读的。
在你的函数内部，显式加载解析器并捕获其结果：

```powershell
. '/workspace/reconcile-helpers.ps1'
$parsed = Convert-LiteralFields $lines
```

点源（Dot sourcing）使辅助函数在当前作用域中可用。
`Convert-LiteralFields` 已经实现了字面量字段规则：正好有两个以 `|` 分隔的字段，且去除首尾空格后均非空。
它会修剪 `Key` 和 `Label` 的首尾空格，将 Label 内部的空格替换为 `_`，并返回 `Items` 以及 `Rejected`，保留每一行被拒绝的原始行。
请重用该结果，而不是重新解析。

`$lines` 包含 0 到 8 行 ASCII 文本行。
`$csvText` 包含 `Key,Reference` 表头以及 0 到 8 行格式规范的 CSV 行，其中包含 ASCII 单词键和文本引用；带引号的引用可能包含逗号。
使用 `ConvertFrom-Csv`，以便这些逗号保留在其字段中。

按顺序根据 CSV 行构建一个哈希表（hashtable）。
更新现有键可使最后一个重复的引用生效。
然后按解析项的原始顺序对其进行转换，保留重复的有效行。
使用 `ContainsKey` 来选择匹配的引用或精确字符串 `Unknown`。
未匹配的项仍然是有效的。

使用 `ConvertTo-Json -Compress` 序列化一份报告：先是 `Items`，然后是 `Rejected`。
每个 item 按顺序包含 `Key`、`Label`、`Reference`。
使用 `@(...)` 将两个报告属性都保持为数组，即使为空或仅包含一个值也是如此。
在赋值中捕获中间的成功输出，以确保你的函数仅返回其最终对象。

### 清理后完成

使用 `Set-Content -NoNewline` 将 `/workspace/keep.txt` 初始化为精确的 `Keep`；在此之后予以保留。
在 `try` 块内，创建 `/workspace/reconcile.tmp`。
如果布尔值 `$fail` 为 true，则在创建后执行 `throw`。
使用 `catch` 将 `Status` 设置为 `Error`，并将 `ReportJson` 设置为 `$null`；否则使用 `Ok` 和报告字符串。

在 `finally` 中仅删除属于你的临时文件，在删除前检查 `Test-Path`。
清理完成后，按以下顺序返回一个对象：`Status`、`ReportJson`、来自 `Test-Path` 的 `TemporaryExists`，以及来自 `Get-Content -Raw` 的 `KeepText`。
无论是成功还是失败，都必须确保临时文件不存在，且不相关的 keep 文件完好无损。

### 解答

```powershell
function Invoke-FileReconciliation {
    param($lines, $csvText, $fail)
    . '/workspace/reconcile-helpers.ps1'
    Set-Content '/workspace/keep.txt' 'Keep' -NoNewline
    $status = 'Error'
    $reportJson = $null
    try {
        Set-Content '/workspace/reconcile.tmp' 'Working' -NoNewline
        if ($fail) { throw 'Requested failure' }
        $parsed = Convert-LiteralFields $lines
        # 用 CSV 行构建查找表，重复键以最后一条为准
        $rows = @($csvText | ConvertFrom-Csv)
        $lookup = @{}
        foreach ($row in $rows) {
            $lookup[$row.Key] = $row.Reference
        }
        # 按解析项的原始顺序转换，未匹配的项使用 Unknown
        $items = @($parsed.Items | ForEach-Object {
            $reference = 'Unknown'
            if ($lookup.ContainsKey($_.Key)) {
                $reference = $lookup[$_.Key]
            }
            [pscustomobject]@{
                Key       = $_.Key
                Label     = $_.Label
                Reference = $reference
            }
        })
        $report = [pscustomobject]@{
            Items    = @($items)
            Rejected = @($parsed.Rejected)
        }
        $reportJson = $report | ConvertTo-Json -Compress
        $status = 'Ok'
    } catch {
        $status = 'Error'
        $reportJson = $null
    } finally {
        # 只删除属于本操作的临时文件
        if (Test-Path '/workspace/reconcile.tmp') {
            Remove-Item '/workspace/reconcile.tmp'
        }
    }
    $keep = Get-Content '/workspace/keep.txt' -Raw
    return [pscustomobject]@{
        Status          = $status
        ReportJson      = $reportJson
        TemporaryExists = (Test-Path '/workspace/reconcile.tmp')
        KeepText        = $keep
    }
}
```
