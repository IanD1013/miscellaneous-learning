JSON 将值存储为文本。
例如，`'{"Label":"A","Value":2}'` 包含描述具有两个属性的对象的文本。
外层的单引号使其成为 PowerShell 字符串。
在该字符串内部，JSON 使用 `{}` 包裹对象，使用双引号包裹属性名和字符串值，在每个名称和值之间使用冒号，并在属性之间使用逗号。
数字 `2` 没有引号，因此它表示数字而非文本。

在读取其属性之前，请将该文本转换为 PowerShell 对象。
这个可运行的示例读取一条记录，构建一个更新后的对象，并将其转换回 JSON：

```powershell
$json = '{"Name":"Ash","Count":3}'
$record = $json | ConvertFrom-Json
$updated = [pscustomobject]@{
    Name = $record.Name
    Count = $record.Count + 2
}
$updated | ConvertTo-Json -Compress
```

第一个管道将字符串传递给 `ConvertFrom-Json`，它会将 JSON 文本解析为对象。
赋值操作将该对象存储在 `$record` 中而不将其输出。`$record.Name` 读取 `Ash`；`$record.Count` 读取数字 `3`，它可以参与算术运算。
我们熟悉的 `[pscustomobject]@{ ... }` 构建了一个新对象，保留名称并将计数设置为 `5`。
其属性定义使用 PowerShell 语法：`=` 和不带引号的属性名。

最后一个管道将该更新后的对象传递给 `ConvertTo-Json`，它会生成 JSON 文本。`-Compress` 省略了可选的空白字符，例如缩进和换行符。
结果是 `{"Name":"Ash","Count":5}`。
在函数内部，请将此转换保留为输出表达式；多余的裸表达式也会成为函数的输出。

JSON 也可以描述列表。
方括号包围其元素：`[]` 为空列表，而 `[{"Label":"A","Value":2}]` 包含一个对象。
在 PowerShell 的 `@(...)` 中捕获解析后的列表项，以确保即使只有零个或一个元素时也能保持为数组：

```powershell
$empty = @('[]' | ConvertFrom-Json)
$one = @('[{"Label":"A","Value":2}]' | ConvertFrom-Json)
```

`$empty.Count` 为 `0`；`$one.Count` 为 `1`，且 `$one[0].Value` 为 `2`。

### 更新一条记录

完成 `Update-JsonValue($json)`。
其输入是单个对象的有效 JSON：`Label` 是包含 1 到 12 个字母的 ASCII 单词，`Value` 是 0 到 20 之间的整数。

使用 `ConvertFrom-Json` 读取它，构建一个标签保持不变且值增加 1 的新对象，并使用 `ConvertTo-Json -Compress` 仅输出更新后的 JSON 文本。
在新对象中将 `Label` 放在 `Value` 之前，以确保此报告具有稳定的文本格式。
例如，`{"Label":"A","Value":2}` 必须精确生成 `{"Label":"A","Value":3}`。

### 解答

```powershell
function Update-JsonValue {
    param($json)
    $record = $json | ConvertFrom-Json
    # Label 保持不变，Value 加 1
    $updated = [pscustomobject]@{
        Label = $record.Label
        Value = $record.Value + 1
    }
    $updated | ConvertTo-Json -Compress
}
```
