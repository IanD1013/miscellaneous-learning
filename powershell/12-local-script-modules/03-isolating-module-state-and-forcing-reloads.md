在 `.psm1` 文件中使用 `$script:` 赋值的变量属于该模块的脚本作用域（script scope）。这种由模块拥有的脚本状态在其函数的多次调用之间仍然存在。调用方和另一个模块都可以各自拥有一个 `$script:count`，而不会共享该计数器的值。

例如，将以下内容保存在本地的 `remaining.psm1` 文件中：

```powershell
$script:remaining = 4
function Take-One {
    $script:remaining = $script:remaining - 1
    $script:remaining
}
Export-ModuleMember -Function Take-One
```

在执行 `Import-Module ./remaining.psm1` 后，两次调用 `Take-One` 分别返回 3 和 2。赋值操作更新了模块的变量，而最后的表达式输出了其当前值。每次调用时初始化的函数局部变量将会丢失该历史记录。如果在函数内部初始化 `$script:remaining`，也会导致每次调用时倒计时重新开始。

再次导入已加载的相同文件会复用其模块状态。`Import-Module -Force ./remaining.psm1` 会重新加载该文件并再次运行其顶层初始化，因此下一次调用 `Take-One` 将返回 3。重新加载此模块仍会保持调用方的变量以及另一个模块的状态相互独立。

### 完成计数器

编辑 `counter.psm1`。保留其顶层的 `$script:count=0` 初始化代码、公开函数 `Get-Next` 以及私有辅助函数 `Advance-Count`。使该辅助函数将模块的计数加 1，并准确输出该新的整数。`Get-Next` 必须调用该辅助函数并返回其输出。继续使用 `Export-ModuleMember -Function Get-Next` 仅导出 `Get-Next`。

第一次调用返回 1；后续调用依次返回 2、3 等。使用缓存的导入会继续该序列。强制重新加载则从 1 重新开始。即使调用方已经有一个名为 `count` 的变量，也要将所有计数器的修改保留在模块内部。所提供的 `other.psm1` 计数器仍必须独立地从 1 开始，且调用方不能直接调用 `Advance-Count`。避免从初始化或任一函数中产生多余的输出。

### 解答

counter.psm1

```powershell
$script:count=0
function Advance-Count { $script:count++; $script:count }
function Get-Next { Advance-Count }
Export-ModuleMember -Function Get-Next
```
