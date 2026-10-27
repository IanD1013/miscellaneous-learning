`Import-Module` 用于加载脚本模块，即包含可复用函数的 `.psm1` 文件。使用提供的 `tools.psm1`，最小的调用序列为：

```powershell
Import-Module -Name ./tools.psm1
$version = Get-Version
```

这里的 `-Name` 接收显式模块路径。本练习在虚拟目录 `/workspace` 中运行，因此 `./tools.psm1` 指向 `/workspace/tools.psm1`。即使该文件位于 `main.ps1` 旁边，也不会自动加载。在调用其函数之前必须先将其导入。提供的模块使 `Get-Version` 可用并初始返回 `1`；请保持其提供的脚手架不变。

普通的重复导入会复用已加载的模块，并不会重新读取修改后的源码。如果文件被重写使得 `Get-Version` 返回 `8`，另一次普通导入仍然会使已加载的函数返回 `1`。此时文件内容与已加载的定义并不一致。

要加载更改后的定义，请先移除已加载的模块，然后再导入其路径：

```powershell
Remove-Module -Name tools
Import-Module -Name ./tools.psm1
$version = Get-Version
```

移除时使用模块名称 `tools`（不带扩展名）。它会卸载模块的命令，但不会删除文件。随后的导入会读取当前文件。本练习中的这些操作均针对本地虚拟脚本模块。

### 完成导入序列

在 `main.ps1` 中，在 `Invoke-Exercise` 内的每个空白处添加显式导入：在第一次调用 `Get-Version` 之前，以及在第二次调用之前。保留现有的选项处理和结果构建逻辑。

- 在没有选项的情况下，两次调用均返回 `1`。
- `Change` 会将提供的 `$Inputs.Source` 写入虚拟模块文件中。若没有 `Remove`，第二次调用必须保持已加载的值不变。
- `Remove` 会在两次调用之间卸载 `tools`。当与 `Change` 结合使用时，第二次导入必须使用替换后的函数，包括返回 `0` 的替换函数。
- `Missing` 会尝试导入一个不存在的文件。保持现有的失败结果：`Success` 为 false，`First` 保持为 `1`，而 `Second` 为 null。

仅返回现有的结果对象。保持两次函数调用均赋值给各自的变量，以避免它们的值成为额外的输出。

### 解答

```powershell
function Invoke-Exercise($Inputs, $Options) {
 try {
  # 第一次调用之前导入模块
  Import-Module -Name ./tools.psm1
  $first = Get-Version
  if ($Options.Change) { Set-Content ./tools.psm1 $Inputs.Source -NoNewline }
  if ($Options.Remove) { Remove-Module -Name tools }
  if ($Options.Missing) { Import-Module -Name ./missing.psm1 }
  # 第二次调用之前再次导入：未移除时复用缓存，移除后读取新文件
  Import-Module -Name ./tools.psm1
  $second = Get-Version
  [pscustomobject]@{Success=$true;First=$first;Second=$second}
 } catch { [pscustomobject]@{Success=$false;First=$first;Second=$null} }
}
```
