`while` 循环在每次进入循环体执行之前检查其条件。
对于基于索引的扫描，条件检查应位于读取数组之前，这样空数组就永远不会访问索引 0：

```powershell
$values = @(3, -2, 5, -1, 8)
$index = 0
while ($index -lt $values.Count) {
    $value = $values[$index]
    $index = $index + 1
    if ($value -eq -1) { break }
    if ($value -eq -2) { continue }
    $value
}
```

这会输出 `3` 和 `5`。
该条件允许从 0 到 `Count - 1` 的索引。
在最后一个可用元素之后，索引等于 `Count`，下一次条件检查为 false。
这是扫描的正常终止方式：到达数组末尾。

这两个分支改变了扫描的进行方式。
`break` 会立即退出当前 `while` 循环，因此 `-1` 充当了停止哨兵（stop sentinel），即标记有效输入结束的值。
后面的 `8` 永远不会被读取。
`continue` 会跳过当前循环体中的剩余部分并返回条件检查处。
在进入任何分支之前递增索引，意味着跳过 `-2` 不会使循环永远卡在同一个元素上。

### 构建扫描报告

使用 `while` 循环完成 `Read-UntilStop($values)`。
输入是一个包含 0 到 8 个整数的数组，整数范围从 `-2` 到 `20`。
按原始顺序保留非负值，包括 0 和重复值。
忽略 `-2`；遇到第一个 `-1` 时停止，既不要保留它，也不要处理它后面的任何内容。
如果不存在哨兵值，则扫描所有可用元素。

返回一个包含 `Count`（保留的元素数量）和 `Values`（这些值的数组）的 `[pscustomobject]`。
对初始集合使用 `@()`，对其报告属性使用 `@($items)`，以便空结果和单元素结果保持数组形式。
示例中输出单个值是为了演示控制流；你的函数应该累积这些值，并且仅输出其完成后的报告。

### 解答

```powershell
function Read-UntilStop {
    param($values)
    $items = @()
    $index = 0
    while ($index -lt $values.Count) {
        $value = $values[$index]
        # 先递增索引，这样 continue 不会卡在同一个元素上
        $index = $index + 1
        if ($value -eq -1) { break }
        if ($value -eq -2) { continue }
        $items += $value
    }
    return [pscustomobject]@{
        Count  = $items.Count
        Values = @($items)
    }
}
```
