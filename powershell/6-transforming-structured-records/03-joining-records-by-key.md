查找连接（lookup join）通过匹配键，将参考集合（reference collection）中的数据附加到每个输入记录中。
完成带有参数 `$records` 和 `$reference` 的 `Join-ReferenceValues`，使每条记录保留其 `Key` 和 `Value`，并获得一个 `Label`。

先构建参考哈希表（hashtable），然后遍历输入记录。
为已存在的键赋值会替换其先前的值：

```powershell
$lookup = @{}
$lookup['A'] = 'First'
$lookup['a'] = 'Last'
$label = 'Unknown'
if ($lookup.ContainsKey('A')) {
    $label = $lookup['A']
}
```

这里 `$label` 的值变为 `'Last'`。
哈希表的字符串键不区分大小写，因此 `'A'` 和 `'a'` 共享同一个条目。
对于参考集合，重复键的策略是后者覆盖前者（last-wins）：按提供的顺序处理条目，每次将 `$entry.Label` 赋值给 `$lookup[$entry.Key]`。
在连接任何记录之前，先完成这些赋值。

对于每个输入行，初始值设为 `'Unknown'`。
在检索标签之前，使用 `ContainsKey` 来确定其是否存在。
未匹配的记录仍会生成一个输出行。
在 `ForEach-Object` 内部，`$_` 表示该输入行；发出一个包含 `Key`、`Value` 和 `Label` 的新 `[pscustomobject]`。
使用 `$items = @($records | ForEach-Object { ... })` 捕获转换结果，以确保空结果和单行结果仍保持为数组。

返回一个包含 `Count = $items.Count` 和 `Items = @($items)` 的 `[pscustomobject]`。
将中间值保留在赋值中；多余的裸表达式会在报告旁添加额外的成功输出。

### 保留输入行

保留它们的原始顺序和拼写，包括重复的行。
只有参考条目会折叠到查找表中：具有相同键的两个输入行仍然需要两个输出行。
因此，空的参考集合会将每个输入行标记为 `'Unknown'`；空的输入将返回 `Count` 为零和空的 `Items` 数组。
输入已经是带有字母数字键、数值和参考标签的记录对象；无需进行文本解析。

### 解答

```powershell
function Join-ReferenceValues {
    param($records, $reference)
    # 先构建参考哈希表，重复键后者覆盖前者
    $lookup = @{}
    foreach ($entry in $reference) {
        $lookup[$entry.Key] = $entry.Label
    }
    # 未匹配的记录标签为 Unknown，但仍保留输出行
    $items = @($records | ForEach-Object {
        $label = 'Unknown'
        if ($lookup.ContainsKey($_.Key)) {
            $label = $lookup[$_.Key]
        }
        [pscustomobject]@{
            Key   = $_.Key
            Value = $_.Value
            Label = $label
        }
    })
    return [pscustomobject]@{
        Count = $items.Count
        Items = @($items)
    }
}
```
