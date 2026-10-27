点源调用（Dot sourcing）会在调用方当前的作用域中运行辅助文件，使其定义的函数在当前作用域中可用。
在调用该辅助函数的代码前，加上一个点号、一个空格以及带引号的文件路径：

```powershell
. '/workspace/helpers.ps1'
$answer = Add-LocalOffset 4
```

在这里，该路径指定了所提供的虚拟辅助文件。
点号是一个调用运算符；它与带引号的路径是分开的。
仅仅将 `helpers.ps1` 与 `Main.ps1` 放在同一目录下并不会加载其定义。

提供的文件包含：

```powershell
$script:offset = 2
function Add-LocalOffset {
    param($value)
    $local:offset = 5
    $result = $value + $local:offset
    $local:offset = 9
    return $result
}
```

作用域决定了一个名称指向哪个变量。
**Script scope** 保存当前脚本执行期间的变量；`$script:offset` 显式选择了该作用域。
该文件顶部的赋值语句在文件运行时将其 offset 初始化为 `2`。

每次普通的函数调用都会为该次调用创建一个 **local scope**。
`$local:offset` 显式选择了该作用域中的变量，因此即使两者都以 `offset` 结尾，它与 `$script:offset` 也是完全不同的变量。
当传入参数 `4` 时，该辅助函数计算出 `9` 并存储在 `$result` 中。
随后它将其局部 offset 更改为 `9`，但后续的该赋值既不会重新计算已存储的结果，也不会修改脚本作用域的 offset。
第二次调用时，仍会从其自身的局部 offset 重新设置为 `5` 开始。

请将每次辅助函数调用的输出赋值给一个变量。
如果直接裸调用函数，会在报告之前将其数值作为额外的成功输出输出。
辅助函数内部的赋值是静默的，而其 `return` 会输出所存储的结果。

### 构建报告

在 `Main.ps1` 中完成 `Invoke-ScopedHelper($value)`。
在函数内部，使用 `. '/workspace/helpers.ps1'` 点源调用提供的文件，然后使用相同的参数调用两次 `Add-LocalOffset`。
请保持辅助文件不变。

返回一个 `[pscustomobject]`，其属性顺序如下：`First` 表示第一次调用的结果，`Second` 表示第二次调用的结果，`ScriptOffset` 表示在两次调用后从 `$script:offset` 读取的值。
两个结果都必须是输入值加上 `5`，且脚本 offset 必须保持为 `2`。
只输出此报告。

### 解答

```powershell
function Invoke-ScopedHelper {
    param($value)
    # 点源调用辅助文件，使其函数在当前作用域中可用
    . '/workspace/helpers.ps1'
    $first = Add-LocalOffset $value
    $second = Add-LocalOffset $value
    return [pscustomobject]@{
        First        = $first
        Second       = $second
        ScriptOffset = $script:offset
    }
}
```
