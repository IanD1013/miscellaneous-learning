`Where-Object` 保留满足条件的记录。
在这里，它保留 `Value` 至少为 10 的记录：

```powershell
$sample = @(
    [pscustomobject]@{ Label = 'Low'; Value = 4 }
    [pscustomobject]@{ Label = 'Mid'; Value = 10 }
)
$sample | Where-Object { $_.Value -ge 10 }
```

从 `Low` 开始。
它的 `Value` 是 4，因此与 10 的比较结果为 false，`Where-Object` 将其排除。
接下来是 `Mid`。
它的 `Value` 是 10，因此比较结果为 true，整条记录都会通过，包括其 `Label`。
熟悉的 `-ge` 包含等于。

`|` 字符将左侧表达式的对象发送给右侧的命令。
这就是管道（pipeline）。
在这里，它将 `$sample` 中的记录发送给 `Where-Object`，这是一个名为 cmdlet 的内置命令。
该命令接收具有可读取属性的对象，因此无需拆分文本。

大括号 `{ }` 包含对每条记录运行的条件。
该代码块被称为 scriptblock。
在它内部，`$_` 表示当前对象：先是 `Low`，然后是 `Mid`。
在 `foreach` 循环中，你会为每个项选择一个变量名；而 `Where-Object` 则提供 `$_`。`$_.Value` 中的点用于读取当前对象的 `Value` 属性。
这种 true-or-false 条件也称为谓词（predicate）。

### 筛选记录

在函数体中的 `param` 之后放置一个带有 `Where-Object` 的管道，以完成 `Get-Matches`。
使用 `$records` 作为输入，并将每条记录的 `Value` 与 `$minimum` 进行比较。

在本练习中，`$records` 是一个包含 0 到 6 个对象的数组。
每个对象的 `Label` 中都有一个非空 ASCII 单词，`Value` 中包含一个 0 到 20 的整数；`$minimum` 也是一个 0 到 20 的整数。

按原始顺序输出完整的匹配记录，且保持其属性不变。
空数组或没有匹配记录时不会产生任何对象。
与之前的函数输出一样，当你不进行赋值时管道会直接发出其结果；不要让额外的表达式出现在函数的输出中。
运行会将无输出显示为 `null`，单个匹配对象独立显示（标量），多个匹配对象则显示为集合。

### 解答

```powershell
function Get-Matches {
    param($records, $minimum)
    # 保留 Value 大于或等于 $minimum 的完整记录
    $records | Where-Object { $_.Value -ge $minimum }
}
```
