通过结合你练习过的解析、过滤、排序和投影操作，根据 JSON 记录构建一份报告。
在排序完成之前保留这些记录：一旦你展开了 `Label`，用于排序的数值型 `Value` 就会丢失。

### 构建报告

补全 `Get-JsonReport`，保留 `param($json, $minimum)`。`$json` 参数是包含 0 到 6 条记录的有效 JSON 数组。
每条记录都有一个非空 ASCII 单词作为 `Label`，以及一个取值在 0 到 20 之间的唯一整数 `Value`。`$minimum` 是一个取值在 0 到 20 之间的整数。
Label 可能会重复；保留每个匹配记录的 label。
Value 绝不会出现重复值，并且不需要进行输入验证。

从输入逐步处理以生成报告：

- 使用 `ConvertFrom-Json` 解析 `$json`，并通过 `@(...)` 捕获记录，包括空输入或仅单条记录输入的情况。
- 使用 `Where-Object` 保留 `Value` 至少为 `$minimum` 的记录。等于该值的记录也属于结果。
- 使用 `Sort-Object` 按数值型 `Value` 升序对保留的记录进行排序，然后使用 `Select-Object -ExpandProperty` 提取 `Label`。使用 `@(...)` 捕获这些 label，以确保在零个或一个结果时仍能构成数组。
- 构建一个首个属性为 `Count`、第二个属性为 `Labels` 的 `[pscustomobject]` 报告。从匹配的 label（而非原始记录）中读取 `.Count`。
- 使用 `ConvertTo-Json -Compress` 序列化报告，并仅输出该结果。将中间结果保存在变量中，以免它们增加函数的输出。

在本练习中，输出格式是固定的紧凑 JSON：`Count` 为数字且位于 `Labels` 之前，`Labels` 始终是一个数组。
单个匹配项需要一个包含单个 label 的数组；空输入或没有匹配项时需要精确输出 `{"Count":0,"Labels":[]}`。
请勿包含任何额外输出。

### 解答

```powershell
function Get-JsonReport {
    param($json, $minimum)
    # 用 @(...) 保证空输入或单条记录时仍是数组
    $records = @($json | ConvertFrom-Json)
    # 先过滤，再按数值型 Value 排序，最后提取 Label
    $labels = @(
        $records |
            Where-Object { $_.Value -ge $minimum } |
            Sort-Object -Property Value |
            Select-Object -ExpandProperty Label
    )
    $report = [pscustomobject]@{
        Count  = $labels.Count
        Labels = $labels
    }
    $report | ConvertTo-Json -Compress
}
```
