哈希表（hashtable）将值存储在键（key）下，因此无需再次扫描源数据即可查找记录。
从一个空表开始，使用方括号来写入和读取条目：

```powershell
$lookup = @{}
$lookup['A'] = 3
$key = 'A'
$lookup.ContainsKey($key)
$lookup[$key]
```

`@{}` 用于创建空的哈希表。
索引赋值将 `3` 存储在 `'A'` 下；`$lookup[$key]` 读取该值。
`ContainsKey` 是一个方法，即在表上调用的操作。
它的括号包含键参数，`.ContainsKey($key)` 返回 `$true` 或 `$false` 以指示条目是否存在。
上面最后两行分别输出 `True` 和 `3`。

更新键会替换现有的值。
在上述示例之后赋值 `$lookup['a'] = 9` 会替换 `3`，因为这些字符串键不区分大小写：`'A'` 和 `'a'` 标识的是同一个条目。
按源记录的原始顺序处理它们，以确保以最后一条记录为准。

请将检查键是否存在与存储的值分开。
即使键存在，`if ($lookup[$key])` 也会将零视为 false。
将 `ContainsKey` 的结果存储在变量中，然后仅当该结果为 true 时才读取该值。
赋值操作可以避免这些中间值泄漏到成功输出中。

### 解析请求的键

完成带有参数 `$records` 和 `$keys` 的 `Resolve-KeyValues`。
每个集合包含零到八个项。
每条源记录都包含 `Key`（长度为一到十二个字符的 ASCII 字母数字字符串）和 `Value`（零到二十之间的整数）。
查询键具有相同的字符串格式。

构建查找表，然后按照调用者的顺序遍历 `$keys`。
为每个查询生成一个对象，依次包含属性 `Key`、`Value` 和 `Found`。
保留查询的大小写拼写以及重复的查询。
缺失的键获取 `Value = -1` 和 `Found = $false`。

返回一个包含 `Count` 和 `Results` 的对象。
将结果对象累加到数组中；使用 `Results = @($results)` 确保对于空结果、单个结果还是多个结果都保持为数组。
空查询返回 `Count = 0` 和 `Results = []`。
由查询列表决定结果顺序，而不是通过枚举表来决定。

### 解答

```powershell
function Resolve-KeyValues {
    param($records, $keys)
    # 先构建查找表，重复键以最后一条记录为准
    $lookup = @{}
    foreach ($record in $records) {
        $lookup[$record.Key] = $record.Value
    }
    # 按调用者提供的查询顺序生成结果
    $results = @()
    foreach ($key in $keys) {
        $found = $lookup.ContainsKey($key)
        $value = -1
        if ($found) {
            $value = $lookup[$key]
        }
        $results += [pscustomobject]@{
            Key   = $key
            Value = $value
            Found = $found
        }
    }
    return [pscustomobject]@{
        Count   = $results.Count
        Results = @($results)
    }
}
```
