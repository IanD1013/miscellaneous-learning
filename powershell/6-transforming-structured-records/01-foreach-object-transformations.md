`ForEach-Object` 会对通过管道传入的每个对象运行一次转换 scriptblock（花括号内的代码）。
使用它根据当前记录构建新记录：

```powershell
$items = @($records | ForEach-Object {
    [pscustomobject]@{
        Label = $_.Label
        Doubled = $_.Value * 2
    }
})
```

在 `ForEach-Object { ... }` 内部，`$_` 表示当前的输入对象。
每次遍历都会读取该对象的属性，并输出一个包含 `Label` 和 `Doubled` 的新对象。
仅选择 `Value` 会生成现有值；构造 `[pscustomobject]` 则能让你保留一个属性的同时计算另一个属性。

scriptblock 的输出会作为管道的输出。
一个单独的 `$_.Value` 表达式会在输出新对象的同时多输出一个值。
请将计算保持在属性值或赋值语句中，以确保每个输入恰好产生一个对象。
即使值为零，也仍然需要生成转换后的记录。

外层的 `@(...)` 会将这些对象捕获为一个数组，即使没有记录或只有一条记录也是如此。
然后你可以使用 `$items.Count` 来统计转换后的记录数。
在构造报告对象时，将其 `Items` 属性设置为 `@($items)`，以确保该属性始终保持为数组。

使用 `ForEach-Object` 完成 `Convert-RecordValues($records)`。
返回一个包含 `Count` 和 `Items` 的对象。
每个项目必须包含保持不变的原始 `Label` 以及等于 `Value * 2` 的 `Doubled`。
保留输入顺序和重复记录。
空输入应返回值为 `0` 的 `Count` 和一个空的 `Items` 数组。
输入记录已包含数值型的 `Value` 属性；无需进行文本转换或标签清理。

### 解答

```powershell
function Convert-RecordValues {
    param($records)
    # 每条输入记录恰好生成一个新对象
    $items = @($records | ForEach-Object {
        [pscustomobject]@{
            Label   = $_.Label
            Doubled = $_.Value * 2
        }
    })
    return [pscustomobject]@{
        Count = $items.Count
        Items = @($items)
    }
}
```
