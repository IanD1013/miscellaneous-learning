`throw 'Invalid value'` 会引发终止性错误：正常执行会停止，外层的 `catch` 可以处理它。
辅助函数可以拒绝某个值，而无需决定其调用方应返回什么报告：

```powershell
function Get-Nonnegative {
    param($value)
    if ($value -lt 0) { throw 'Invalid value' }
    return $value
}

try {
    $number = Get-Nonnegative -1
    'Accepted'
} catch {
    'Rejected'
}
```

`try { ... }` 块包围了可能失败的操作。
当传入 `-1` 时，辅助函数永远不会执行到 `return $value`；执行流程会转移到 `catch { ... }`，因此仅会产生 `Rejected`。
将参数改为 `0`，赋值就会完成，产生 `Accepted`，并且 catch 块会被跳过。
这种无类型的 `catch` 可以处理来自 try 块的终止性错误，而无需检查其具体细节。

请将成功报告保留在 `try` 内部且在调用辅助函数之后。
如果辅助函数失败，则绝不能产生该报告。
捕获失败也不会清除在此之前产生的成功输出：单纯的累加值或诊断字符串仍会传递给调用方。
计算时请使用赋值操作，并且仅在整个输入都被接受后才输出辅助函数的总和。

### 构建校验总和

完成接收 `$values` 的 `Get-CheckedTotal`。
添加一个辅助函数来累加整数，并在遇到负值时立即使用 `throw 'Invalid value'`。
在 `try` 内部调用该辅助函数，捕获其总和，并使用 `catch` 生成失败报告。

恰好返回一个 `[pscustomobject]`，其属性顺序如下：

- 所有值均被接受：`Status = 'Ok'`，`Total` 等于它们的总和。
- 存在任何负值：`Status = 'Invalid'`，`Total = $null`。
丢弃任何部分累加的总和。

空数组可被接受且总和为 `0`；零也是有效值。
除了预期的结果外，保持两个函数体内没有任何其他输出，以确保返回的报告不会附加多余的数字或文本。

### 解答

```powershell
function Get-ValuesTotal {
    param($values)
    $total = 0
    foreach ($value in $values) {
        # 遇到负值立即拒绝，丢弃部分累加的总和
        if ($value -lt 0) { throw 'Invalid value' }
        $total += $value
    }
    return $total
}

function Get-CheckedTotal {
    param($values)
    try {
        $total = Get-ValuesTotal $values
        return [pscustomobject]@{ Status = 'Ok'; Total = $total }
    } catch {
        return [pscustomobject]@{ Status = 'Invalid'; Total = $null }
    }
}
```
