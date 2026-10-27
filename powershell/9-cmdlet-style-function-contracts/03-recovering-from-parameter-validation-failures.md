验证失败可能在函数执行其主体中的第一条语句之前发生。在调用方中用 `try` 包裹辅助函数的调用：被拒绝的辅助函数内部的 `catch` 无法运行，因为参数绑定已阻止该主体启动。

例如，此调用使用了提供的 `Test-Validated` 辅助函数：

```powershell
try {
    $item = Test-Validated -Count 0 -Name 'sample'
    $item
} catch {
    'Rejected'
}
```

`Count` 必须在 1 到 8 之间，因此调用在验证期间失败。在此练习环境中，该失败会终止调用并将控制权转移给调用方的 `catch`。该代码片段输出 `Rejected`；将计数改为 1 则可完成赋值并输出辅助函数的记录。该赋值捕获了辅助函数的输出，使其不会在调用方决定返回什么之前逸出。

### 构建调用方

在 `main.ps1` 中完成 `Invoke-Checked`。它接收一个包含 `Count`、`Name` 以及可选的 `Missing` 标志的 options 记录。`Mode` 也可能出现在输入中；此辅助函数不使用它。

- 在 `try` 内部，使用 `-Count $Options.Count` 调用一次 `Test-Validated`。当 `$Options.Missing` 为 true 时，完全省略 `-Name`。否则，同时传入 `-Name $Options.Name`。
- 该辅助函数需要这两个参数，接受 1 到 8 之间的计数，并拒绝空名称。让它的参数验证来决定调用是否成功。
- 捕获返回的记录，并返回一个包含 `Success=$true` 且 `Value` 保存该记录的 `[pscustomobject]`。在 `catch` 中，返回一个包含 `Success=$false` 和 `Value=$null` 的记录。

提供的 `Invoke-Exercise` 会重置主体计数器并报告 `{ Result, Before, After }`。成功执行的辅助函数主体会将其递增一次，从而得到 `Before=0` 和 `After=1`。被拒绝的参数会使两者都保持为 0，因为主体从未启动。请保持提供的辅助函数和计数器不变，不要进行任何文件写入，也不要在结果之外输出任何诊断字符串。

### 解答

```powershell
function Invoke-Checked {
    param([object]$Options)
    try {
        # 参数验证失败会在函数体启动前终止调用，直接进入 catch
        if ($Options.Missing) { $item = Test-Validated -Count $Options.Count }
        else { $item = Test-Validated -Count $Options.Count -Name $Options.Name }
        return [pscustomobject]@{ Success=$true; Value=$item }
    } catch {
        return [pscustomobject]@{ Success=$false; Value=$null }
    }
}
```
