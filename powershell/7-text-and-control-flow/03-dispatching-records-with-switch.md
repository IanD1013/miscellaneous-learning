`switch` 通过将某个值与字面量标签进行比较来选择匹配的子句。
将类别放在圆括号中，并将每个标签对应的语句放在花括号中：

```powershell
$category = 'high'
$value = 0
switch ($category) {
    'Low' { $value = 1; break }
    'High' { $value = 3; break }
    default { $value = 0 }
}
$value
```

这会输出 `3`。
普通的字面量匹配是不区分大小写的，因此 `'high'` 会匹配 `'High'`。
带引号的标签是完整字符串；它们不会执行通配符匹配。
当没有标签匹配时，default 分支将运行，从而为未知的类别赋予一个确定的值。

匹配的子句不会自动终止 switch。
如果两个标签都匹配，两个子句都会执行。
`break` 会在赋值后退出当前的 switch，防止后续匹配的子句继续运行。
分号用于分隔这两条语句；将它们写在不同行也同样有效。
在 `foreach` 中，这个 `break` 会结束 switch，循环仍会继续访问下一个类别。

像 `$value = 3` 这样的赋值操作是静默的（不会产生输出）。
上面最后的 `$value` 会输出结果以便查看。
在你编写的函数中，请保持每次分发的静默，改为将赋值追加到数组中。
子句中孤立的值（bare value）会成为多余的函数输出，与最终报告混在一起。

### 构建类别报告

使用 `foreach` 完成 `Get-CategoryValues($categories)`，每次对一个类别应用 `switch ($category)`。
输入包含 0 到 8 个 ASCII 字母数字单词。
将 `Low` 映射为 `1`，`High` 映射为 `3`，其他所有单词映射为 `0`，并保留输入顺序和重复项。

从一个空的 values 数组开始，每次迭代追加一个赋好的数字。
只返回一个包含 `Count` 和 `Values` 属性的 `[pscustomobject]`（按此顺序）。
`Count` 是值的数量。
使用 `@($values)` 保持 `Values` 为数组，包括空输入时为空数组，单个类别时为单元素数组。

### 解答

```powershell
function Get-CategoryValues {
    param($categories)
    $values = @()
    foreach ($category in $categories) {
        $value = 0
        # switch 默认不区分大小写，break 防止继续匹配后续子句
        switch ($category) {
            'Low' { $value = 1; break }
            'High' { $value = 3; break }
            default { $value = 0 }
        }
        $values += $value
    }
    return [pscustomobject]@{
        Count  = $values.Count
        Values = @($values)
    }
}
```
