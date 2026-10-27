成员资格运算符用于判断集合中是否包含某个值。
使用 `-in` 时将值放在前面，使用 `-contains` 时将集合放在前面：

```powershell
'A' -in @('A', 'B')
@('A', 'B') -contains 'A'
```

两个表达式的结果都是 `True`。
如果在交换运算符的同时没有交换操作数，判断的问题就会改变。
即使集合中多次包含该值，这些运算符也只产生一个布尔值结果。
它们默认的字符串比较是忽略大小写的，因此 `'a'` 也会匹配 `'A'`。

当需要让标签匹配通配符模式时，请使用 `-like`：

```powershell
'Alpha' -like 'Al*'
'Al' -like 'Al*'
'Beta' -like 'Al*'
```

结果分别为 `True`、`True` 和 `False`。
通配符 `*` 匹配零个或多个字符；其他字符必须与它们在文本中的位置相匹配。
带引号的模式（例如 `'Al*'`）将星号保留在传递给 `-like` 的字符串内。
如果不加星号，整个标签必须与该模式完全匹配。
`-like` 默认同样忽略大小写。

一条记录必须同时通过两项检查。
该布尔逻辑与运算使用 `-and` 来要求两个结果均为真：

```powershell
('A' -in @('A', 'B')) -and ('Alpha' -like 'Al*')
```

括号使每个比较保持独立完整。
标签匹配无法弥补类别不在允许列表中的缺失。

### 过滤记录

完成 `Select-AllowedLabels($records, $allowed, $pattern)`。
每条记录都包含 `Category` 和 `Label` 属性。
使用上述不区分大小写的比较方式，当某条记录的类别存在于 `$allowed` 中且其标签匹配 `$pattern` 时，保留该记录。

返回一个包含 `Count`（保留的数量）和 `Items`（保留的原始记录数组）的对象。
保留原始顺序和重复记录。
`$allowed` 中的重复条目不会导致记录重复。
任一输入集合都可能为空；当没有任何记录符合条件时，返回 `Count = 0` 以及空的 `Items` 数组。
使用 `@(...)` 捕获保留的项，以确保在仅有一条匹配项时 `Items` 仍为数组。
仅输出此报告对象。

### 解答

```powershell
function Select-AllowedLabels {
    param($records, $allowed, $pattern)
    # 类别必须在允许列表中，且标签必须匹配通配符模式
    $kept = @($records | Where-Object {
        ($_.Category -in $allowed) -and ($_.Label -like $pattern)
    })
    return [pscustomobject]@{
        Count = $kept.Count
        Items = @($kept)
    }
}
```
