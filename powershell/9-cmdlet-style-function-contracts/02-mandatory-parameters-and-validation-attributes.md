参数属性可以在高级函数执行其主体之前拒绝参数。将它们放在 `param` 中参数类型的前面，并配合函数上的 `[CmdletBinding()]` 一起使用：

```powershell
function Get-Limit {
    [CmdletBinding()]
    param([Parameter(Mandatory=$true)][ValidateRange(1,8)][int]$Count)
    return $Count
}
Get-Limit -Count 8
```

这将返回 `8`。`[Parameter(Mandatory=$true)]` 要求调用者必须提供 `Count`；`[ValidateRange(1,8)]` 接受两个端点值，并拒绝小于 1 或大于 8 的值。将整数设为必选并不会限定其允许的范围。如果传入 `-Count 9`，在执行到 `return $Count` 之前验证就会失败。

在字符串参数上使用 `[ValidateSet('Keep','Drop')]` 可以使其仅接受这两个选项。匹配不区分大小写，因此 `'kEeP'` 会被接受，无需重写调用者的文本。诸如 `$Mode='Keep'` 之类的默认值会在省略该参数时提供值。`[ValidateNotNullOrEmpty()]` 会拒绝 null 和空字符串；当调用者必须同时提供该参数时，请将其与 `Mandatory` 结合使用。它不需要修剪（trimming）或拒绝仅包含空格的字符串。

### 完成 Get-Validated

在 `main.ps1` 中的现有参数上添加验证属性：

- `Count` 是一个 1 到 8（包含两端）之间的必选整数。必须拒绝零、负整数和 9。
- `Mode` 接受 `Keep` 或 `Drop`（不区分大小写），默认值为 `Keep`。
- `Name` 是一个必选的非空字符串。传入的名称最多为 40 个字符；请保留其文本。

保持 `RootCount` 作为函数体内的第一条语句。它会递增传入的计数器且不输出任何结果。成功的调用会执行它一次，然后返回现有的对象：`Name` 保持不变，当 `Mode` 为 `Keep` 时 `Value` 为 `Count`，为 `Drop` 时 `Value` 为 `0`。不要输出额外的值。

被拒绝的参数必须保持该计数器不变。验证失败会在此处终止 helper 调用，从而允许传入的调用者的 `catch` 返回 `Success=false` 和 `Result=null`。请保持该调用者不变；若在 `RootCount` 之后添加检查，则只有在函数体已经运行后才会拒绝输入。

### 解答

```powershell
function Get-Validated {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true)][ValidateRange(1,8)][int]$Count,
        [ValidateSet('Keep','Drop')][string]$Mode='Keep',
        [Parameter(Mandatory=$true)][ValidateNotNullOrEmpty()][string]$Name
    )
    RootCount
    if ($Mode -eq 'Drop') { return [pscustomobject]@{ Name=$Name; Value=0 } }
    return [pscustomobject]@{ Name=$Name; Value=$Count }
}
```
