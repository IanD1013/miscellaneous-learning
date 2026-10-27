`Group-Object -Property Category` 会将具有相同类别的记录收集到一个分组对象中。
在决定每个汇总应包含什么内容之前，你可以先检查这些分组：

```powershell
$records = @(
    [pscustomobject]@{ Category = 'B'; Value = 3 }
    [pscustomobject]@{ Category = 'B'; Value = 6 }
)
$records | Group-Object -Property Category | ForEach-Object {
    $measure = $_.Group | Measure-Object -Property Value -Sum
    [pscustomobject]@{      Category = $_.Name
        Count = $_.Count
        Total = $measure.Sum
    }
}
```

在此 `ForEach-Object` 内部，`$_` 是一个分组对象，而不是单条原始记录。
它的 `.Name` 是共享的类别，`.Count` 是成员记录的数量，而 `.Group` 则包含这些记录。
此处的组计数为 2，总和为 9。
重复的值仍然属于单独的记录，并且必须分别计入。

`Measure-Object -Property Value -Sum` 从当前分组的每个成员中读取 `Value`。
它返回一个度量对象；`.Sum` 用于检索数值总和。
将该对象赋值给 `$measure` 可以防止它出现在成功输出中。
如果在此处度量 `$records`，则会为每个类别计算出相同的总计。

完成带有参数 `$records` 的 `Get-CategorySummary`，以返回一个具有以下属性的对象：

- `Count`：类别汇总的数量。
- `Groups`：包含 `Category`、成员 `Count` 和 `Total` 的对象数组，按此属性顺序排列。

使用 `Sort-Object -Property Category` 对完成的汇总进行排序，以便报告按类别明确升序排列。
在读取其计数之前，使用 `@(...)` 捕获管道结果。
使用 `@($groups)` 保持 `Groups` 为数组值：空输入需要 `[]`，单个类别需要单元素数组，多个类别需要多元素数组。
仅输出完成的报告。

输入包含最多八条记录，具有拼写一致的 ASCII 类别词和较小的非负整数值。
空输入返回 `Count = 0` 以及空的 `Groups` 数组；值为零的记录仍算作其类别中的一个成员。

### 解答

```powershell
function Get-CategorySummary {
    param($records)
    # 先分组汇总，再按 Category 升序排序
    $groups = @($records | Group-Object -Property Category | ForEach-Object {
        $measure = $_.Group | Measure-Object -Property Value -Sum
        [pscustomobject]@{
            Category = $_.Name
            Count    = $_.Count
            Total    = $measure.Sum
        }
    } | Sort-Object -Property Category)
    return [pscustomobject]@{
        Count  = $groups.Count
        Groups = @($groups)
    }
}
```
