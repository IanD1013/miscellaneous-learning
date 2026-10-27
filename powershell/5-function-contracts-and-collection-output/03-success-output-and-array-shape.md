在 PowerShell 函数中，每个未被赋值的表达式都会作为其成功输出（success output）的一部分，即调用方接收到的值。
`return` 会结束函数，但在此之前生成的输出仍会传递给调用方。
赋值操作可以让你保留中间值而不将其输出：

```powershell
function Get-Values {
    $label = 'ready'
    4
    9
}
$captured = @(Get-Values)
[pscustomobject]@{ Count = $captured.Count; Values = $captured }
```

`Get-Values` 输出两个数字。
被赋值的文本保留在局部作用域内。
如果将 `$label = 'ready'` 替换为单独的表达式 `'ready'`，则会添加第三个值。
那段多余的文本就是附带输出（incidental output）：即在执行其他操作时输出、却意外成为结果一部分的值。
对另一个函数的裸调用（bare call）也会传播该函数的成功输出。
如果你需要运行某个辅助函数但丢弃其返回值，可以对该调用进行赋值：`$null = Get-Values`。

如果不使用数组捕获，将函数的输出进行赋值时，如果没有值会得到 `$null`，单个值会得到标量，多个值则会得到数组。
数组子表达式 `@(...)` 在这三种情况下都会将输出收集到一个数组中。
在此例中，`$captured = @(Get-Values)` 捕获了辅助函数的输出；`@($values)` 对变量中已持有的值应用相同的规则。
空输出会变成 `@()`，单个值会变成单元素数组。

该示例输出了一个包含所捕获数组的对象。
该对象起到了封包（envelope）的作用：其 `Values` 属性将集合保留在单个结果中。
如果直接输出数组本身，其元素会再次展开为独立的成功输出值。
这种封包方式允许调用方对空值、单个值以及多个值使用相同的属性。

### 构建集合结果

完善带有既有 `param($values)` 的 `Get-ValueCollection`。
输入是一个包含 0 到 8 个整数（范围为 0 到 20，允许重复）的数组。
返回一个包含 `Count` 以及随后的 `Values` 的对象：

- `Count` 为输入值的数量。
- `Values` 始终是一个数组，按原始顺序包含每个输入值，包括重复项。
- 空输入产生 `Count = 0` 和 `Values = @()`。

请保持对中间操作进行赋值，以确保该对象是函数唯一的成功输出。

### 解答

```powershell
function Get-ValueCollection {
    param($values)
    # 用 @(...) 保证空输入或单个值时仍是数组
    $items = @($values)
    return [pscustomobject]@{
        Count  = $items.Count
        Values = @($items)
    }
}
```
