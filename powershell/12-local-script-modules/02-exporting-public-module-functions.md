`Export-ModuleMember -Function` 用于选择调用方在导入脚本模块后可以使用的函数。将其放在 `.psm1` 文件内，并列出确切的公共函数名称。未包含在该列表中的辅助函数（helper）仍可供模块内部的函数使用：

```powershell
function Get-Trimmed([string]$Text) { $Text.Trim() }
function Get-Label([string]$Text) { Get-Trimmed $Text }
Export-ModuleMember -Function Get-Label
```

导入此模块后，调用方可以运行 `Get-Label ' ready '` 并收到 `ready`。直接从调用方调用 `Get-Trimmed` 则会失败。导出控制的是模块外部的可见性；它不会移除辅助函数，也不会阻止公共函数使用它。如果没有显式的导出声明，脚本模块默认会公开其所有函数，包括辅助函数。

### 完成 tools.psm1

修改 `Get-Normalized($Values)`，针对每个输入字符串使用所提供的私有 `Format-Value` 辅助函数。该辅助函数会修剪周围的空白字符并将文本转换为小写。保留输入顺序、重复项和空字符串。

恰好输出一个包含 `Items` 和 `Count` 的对象。无论输入是零个、一个还是多个值，`Items` 都必须保持为数组：空输入生成 `Items=@()` 和 `Count=0`；一个输入生成一个单元素数组和 `Count=1`。将每个辅助函数的结果捕获到集合中，以避免它也成为公共函数的单独输出。

保持 `Get-NormalizedCount($Values)` 返回输入值的数量。使用 `Export-ModuleMember -Function Get-Normalized,Get-NormalizedCount` 导出这两个公共函数，使 `Format-Value` 保持私有。这两个公共名称在以小写形式调用时也必须正常工作。仅编辑 `tools.psm1`；`exercise-checks.ps1` 中提供的调用方代码保持不变。

### 解答

tools.psm1

```powershell
function Format-Value([string]$Value) { $Value.Trim().ToLower() }
function Get-Normalized($Values) {
    $items=@()
    foreach ($value in $Values) { $items += Format-Value $value }
    [pscustomobject]@{Items=@($items);Count=$items.Count}
}
function Get-NormalizedCount($Values) { @($Values).Count }
Export-ModuleMember -Function Get-Normalized,Get-NormalizedCount
```
