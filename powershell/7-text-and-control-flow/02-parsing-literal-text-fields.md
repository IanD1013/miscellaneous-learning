`Split`、`Trim` 和 `Replace` 允许你使用字面分隔符（即标记一个字段结束和下一个字段开始的字符）将一行文本转换为多个字段。
对于包含两个字段的有效行：

```powershell
$line = ' A | Blue Sky '
$parts = @($line.Split('|'))
$key = $parts[0].Trim()
$label = $parts[1].Trim().Replace(' ', '_')
```

点号会调用其前面字符串上的方法。
括号中包含其参数。
`.Split('|')` 会在每个字面量 `|` 处拆分字符串，生成 `' A '` 和 `' Blue Sky '`。
外层的 `@(...)` 将这些部分收集到一个数组中。
`.Trim()` 不需要参数，并返回去除了首尾边界空白字符的字符串；内部空格保持不变。
`.Replace(' ', '_')` 返回将每个空格替换为 `_` 后的字符串。
它的两个参数分别是要查找的文本及其替换内容。
这些方法都会返回新值，因此请将所需的结果赋值保存。
在此例中，`$key` 为 `'A'`，`$label` 为 `'Blue_Sky'`。

拆分也会保留空片段。
`'|x'` 会生成一个空字段，后跟 `'x'`；`'a||b'` 会生成三个字段。
在读取位置 0 和 1 之前，请先检查 `$parts.Count -eq 2`。
只有在此之后，才对这两个字段执行 trim。
`.Length` 属性用于计算字符串中的字符数，因此 `$key.Length -eq 0` 可以检测出在 trim 之后仍然为空的字段。
对 label 也要进行同样的检查。
仅包含空格不能构成有效字段。

使用这些字面量字符串方法完成 `Convert-LiteralFields($lines)`。
输入包含 0 到 8 个字符串，每个字符串最多包含 40 个 ASCII 字符。
字段包含 ASCII 字母、数字和空格，由 `|` 分隔。

返回一个包含以下属性的对象：

- `Count`：接受的行数。
- `Items`：对象数组，包含经过 trim 的 `Key`，以及经过 trim 且每个剩余空格都被替换为 `_` 的 `Label`。
保留重复项和输入顺序；`Key` 中的内部空格保持不变。
- `Rejected`：包含错误字段数量或在 trim 后字段为空的原始行，按输入顺序排列。

即使为空或仅包含一个元素，也请将 `Items` 和 `Rejected` 保持为数组。
为中间方法的结果赋值，以确保只有最终报告作为成功输出。

### 解答

```powershell
function Convert-LiteralFields {
    param($lines)
    $items = @()
    $rejected = @()
    foreach ($line in $lines) {
        $parts = @($line.Split('|'))
        if ($parts.Count -eq 2) {
            # 字段数量正确后才读取并 trim 两个字段
            $key = $parts[0].Trim()
            $label = $parts[1].Trim().Replace(' ', '_')
            if ($key.Length -eq 0 -or $label.Length -eq 0) {
                $rejected += $line
            } else {
                $items += [pscustomobject]@{ Key = $key; Label = $label }
            }
        } else {
            $rejected += $line
        }
    }
    return [pscustomobject]@{
        Count    = $items.Count
        Items    = @($items)
        Rejected = @($rejected)
    }
}
```
