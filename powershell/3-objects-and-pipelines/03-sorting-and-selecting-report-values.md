Sort-Object 根据属性对对象进行排序。
随后带有 -ExpandProperty 的 Select-Object 会从每个对象中提取一个属性的值。
从两条记录开始：

```powershell
$records = @(
    [PSCustomObject]@{ Label = 'Oak'; Value = 12 }
    [PSCustomObject]@{ Label = 'Pine'; Value = 3 }
)
$records | Sort-Object -Property Value
```

`Sort-Object` 通过管道接收记录。`-Property` 是一个命名的命令参数：开头的连字符标记了参数名，而后面的参数 `Value` 则指定了用于排序的属性。
这些命令参数用空格跟在命令后面；它们与函数内部的 `param($records)` 声明是分开的。

默认排序规则为升序，最小值排在前面。
因为 `Value` 包含数字，所以 3 排在 12 前面。
输出结果是 Pine 对象后跟 Oak 对象，每个对象仍然同时包含 `Label` 和 `Value`。
排序只改变了它们的顺序，并没有移除记录。

要从该顺序中提取标签，请添加另一个命令：

```powershell
$records | Sort-Object -Property Value | Select-Object -ExpandProperty Label
```

`Select-Object` 接收排序后的对象。
它的 `-ExpandProperty` 参数以 `Label` 作为属性名，并为每个对象输出该属性的值。
输出结果是字符串 `Pine`，然后是字符串 `Oak`，而不是完整的对象。
请在提取前先进行排序：提取之后，这些字符串将不再包含可供排序的 `Value` 属性。

### 有序标签

完成接收 `$records` 的 `Get-OrderedLabels`。
练习使用 `Sort-Object -Property` 和 `Select-Object -ExpandProperty`，按 `Value` 升序输出每条记录的标签。
包含值为零的记录；无需进行过滤。
仅输出标签，不包含任何额外的诊断输出。

输入包含 0 到 6 条记录。
每条记录都有一个在 0 到 20 之间且唯一的整数 `Value`，以及 `Label` 中的非空 ASCII 单词。
本任务不涉及相等的排序值。
标签可能重复：每条记录保留一个输出值。
空输入不产生任何输出，一条记录产生一个字符串，多条记录产生多个字符串。

### 解答

```powershell
function Get-OrderedLabels {
    param($records)
    # 先按 Value 升序排序，再提取 Label 的值
    $records | Sort-Object -Property Value | Select-Object -ExpandProperty Label
}
```
