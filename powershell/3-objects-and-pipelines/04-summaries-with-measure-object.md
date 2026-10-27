`Measure-Object` 会将多条记录合并为一个汇总对象。
对于两条 `Value` 属性分别为 3 和 8 的记录，你可以同时请求获取它们的总和与计数：

```powershell
$records = @(
    [pscustomobject]@{ Value = 3 }
    [pscustomobject]@{ Value = 8 }
)
$summary = $records | Measure-Object -Property Value -Sum
$summary.Sum
$summary.Count
```

管道将两条记录传递给 `Measure-Object`。`-Property Value` 告诉该命令对每条记录测量哪个属性。`-Sum` 是一个请求求和的开关（switch）；它后面不需要跟数字。
该命令将 3 和 8 相加并生成一个汇总对象。
赋值操作将该对象捕获到 `$summary` 中。

`$summary.Sum` 读取总和，即 11。`$summary.Count` 读取被测量的数值数量，即 2。
这里的每条记录都有一个数值型的 `Value`，因此 Count 也是记录的数量。
即使值为零对 Sum 没有任何贡献，它仍然算作一个测量值。
对于空的 `$records` 数组，此测量将生成 Sum 为 0 且 Count 为 0。

上面的两个属性表达式输出了数字，以便你可以检查测量结果。
在你的函数内部，请将测量结果保存在变量中，并使用其属性来构建最终结果。
单独的一个 `$summary` 表达式也会输出中间对象。

### 构建汇总结果

完成 `Get-Summary`，它接收包含 0 到 6 个对象的数组 `$records`。
每个对象都有一个 `Value` 属性，其值为 0 到 20 之间的整数。
练习使用 `Measure-Object -Property Value -Sum` 测量这些记录。

精确输出一个包含以下属性且按此顺序排列的 `[pscustomobject]`：

- `Total`：所有 Value 属性的总和，从测量的 `.Sum` 中读取。
- `Count`：记录的数量，从测量的 `.Count` 中读取。

使用你已经掌握的对象字面量形式 `[pscustomobject]@{ ... }` 为结果赋予这些属性名称。
空输入仍必须生成此对象，且两个属性都设置为 0。
不要输出任何中间对象或数字。

### 解答

```powershell
function Get-Summary {
    param($records)
    # 将测量结果保存在变量中，避免输出中间对象
    $summary = $records | Measure-Object -Property Value -Sum
    [pscustomobject]@{
        Total = $summary.Sum
        Count = $summary.Count
    }
}
```
