PSCustomObject 可以将相关的值按名称组织在一起。
在这里，`Label` 标识了一段文本，而 `Value` 标识了一个数字：

```powershell
$pair = [pscustomobject]@{
    Label = 'Blue'
    Value = 4
}
```

每个条目都会创建一个具名属性：即对象内部附加到一个值的名称。`Label` 包含 `'Blue'`；`Value` 包含 `4`。
与数组中的位置索引不同，这些名称可以清楚地告诉你正在读取的是哪个值。

`[pscustomobject]` 标记用于请求创建一个对象。
方括号需要包裹住名称 `pscustomobject`。`@{` 开始定义具名条目，闭合的 `}` 结束定义。
在内部，将属性名放在 `=` 的左侧，其值放在右侧。
这里的属性名前面没有 `$`；而作为值使用的变量仍然需要 `$`。
外层的 `$pair =` 将创建好的对象存储在一个变量中。

各个条目之间可以用换行符分隔（如上所示），也可以在单行中用分号分隔：

```powershell
$pair = [pscustomobject]@{ Label = 'Blue'; Value = 4 }
```

通过在对象变量后加上点号和属性名来读取属性：

```powershell
$pair.Label
$pair.Value
```

这些表达式分别输出 `Blue` 和 `4`。
点号用于选择单个属性的值；而单独使用 `$pair` 则会输出整个对象。

### 构建一个键值对

完成 `New-Pair`，使用其 `$label` 和 `$value` 参数来构建一个 PSCustomObject。
label 是一个由 1 到 12 个 ASCII 字母组成的非空单词；value 是一个 0 到 20 之间的整数。

首先使用提供的 label 创建 `Label`，然后使用提供的数字创建 `Value`。
请保持这些属性名称和顺序。
输出该对象一次，不要有任何其他输出。
如果将其存储在局部变量中，请在末尾仅返回该变量。
不要在函数中包含演示中的属性读取表达式。

### 解答

```powershell
function New-Pair {
    param($label, $value)
    # 按 Label、Value 的顺序创建对象并输出一次
    [pscustomobject]@{
        Label = $label
        Value = $value
    }
}
```
