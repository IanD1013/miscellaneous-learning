`ConvertFrom-Csv` 将 CSV 文本读取为对象，并使用标头名称作为属性。
让它解析带引号的字段：引号内的逗号属于该值，而该字段内连续的两个双引号表示一个字面双引号。

```powershell
$text = "Label,Value`n" + '"A,B",2'
$rows = @($text | ConvertFrom-Csv)
$row = $rows[0]
$next = ([int]$row.Value) + 1
```

在这里，`$row.Label` 为 `A,B`。
如果按逗号拆分数据行，会将该标签拆成两部分。
`$row.Value` 是字符串 `2`：即使是数值字段，在 CSV 解析后仍保持为文本。
在相加之前使用 `[int]` 进行转换会使 `$next` 成为数字 `3`；直接与字符串相加可能会产生 `21`。
`@(...)` 捕获将解析出的行保持在数组中，包括在没有数据行的情况下。

`ConvertTo-Csv` 执行反向转换，先输出标头行，后跟数据行：

```powershell
$items = @([pscustomobject]@{ Label = $row.Label; ValuePlusOne = $next })
$lines = @($items | ConvertTo-Csv -NoTypeInformation)
```

`-NoTypeInformation` 省略了类型信息行，因此第一行包含列名。
构建每个输出对象时，先是 `Label`，后是 `ValuePlusOne`，以确立列顺序。
该转换会根据需要为字段加引号，并将嵌入的双引号转义为两个双引号。
使用 `@(...)` 捕获其输出的各行；这些行应包含在报告中，而不是单独输出。

### 构建报告

完成带有参数 `$csvText` 的 `Convert-CsvReport`。
输入包含标头 `Label,Value` 以及 0 到 8 个格式规范的 CSV 数据行。
Label 包含 1 到 20 个 ASCII 字母、数字、空格、逗号或双引号。
Value 是介于 0 到 20 之间的十进制整数。

使用 `ConvertFrom-Csv` 解析文本，转换每一行，并返回一个按顺序包含以下属性的对象：

- `Count`：数据行的数量。
- `Items`：一个对象数组，按属性顺序包含未更改的 `Label` 和等于转换后的值加一的数值型 `ValuePlusOne`。
保留输入行的顺序和重复项。
- `CsvLines`：使用 `ConvertTo-Csv -NoTypeInformation` 从 `Items` 生成的字符串数组，列按 `Label,ValuePlusOne` 顺序排列。

对于仅有标头的输入，返回 `Count` 为 0 以及两个空数组。
对于只有一行的情况，两个集合属性也请保持为数组。

### 解答

```powershell
function Convert-CsvReport {
    param($csvText)
    # 解析 CSV，Value 解析后是文本，相加前先转换为 [int]
    $rows = @($csvText | ConvertFrom-Csv)
    $items = @($rows | ForEach-Object {
        [pscustomobject]@{
            Label        = $_.Label
            ValuePlusOne = ([int]$_.Value) + 1
        }
    })
    $csvLines = @($items | ConvertTo-Csv -NoTypeInformation)
    return [pscustomobject]@{
        Count    = $items.Count
        Items    = @($items)
        CsvLines = @($csvLines)
    }
}
```
