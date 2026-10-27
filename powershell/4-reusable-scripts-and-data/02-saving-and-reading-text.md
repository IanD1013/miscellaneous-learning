`Set-Content` 将文本保存到文件中，而 `Get-Content` 则将其读回。
下面这两个命令会保存一行内容，然后再将其读取出来：

```powershell
Set-Content -Path ./text.txt -Value 'first line' -NoNewline
Get-Content -Path ./text.txt -Raw
```

结果为 `first line`。`-Path` 指定了文件位置；`./` 表示当前虚拟工作区，因此 `./text.txt` 指代那里的一个文件。
课程文件位于浏览器的虚拟工作区中，与您计算机上的文件是相互隔离的。

`-Value` 提供了要保存的文本。`Set-Content` 会替换任何先前的内容：在相同路径下保存 `second line` 只会留下 `second line`，而不是将其追加到 `first line` 之后。`-NoNewline` 可防止该命令在末尾添加行尾符。
它不会删除文本中已有的换行符。
如果没有此参数，保存 `first line` 时还会在其后添加一个换行符。

`Get-Content` 通常会按行读取。`-Raw` 会将整个文件作为一个字符串读取，并保留其换行符。
当结果必须保留完整文本（包括空格和末尾换行符）时，请使用该参数。

在函数内部，将读取结果赋值给一个变量，这样读取操作就不会输出多余的值：

```powershell
$saved = Get-Content -Path ./text.txt -Raw
```

然后使用你已经掌握的对象构造方式，在属性中返回该字符串：

```powershell
[pscustomobject]@{ Text = $saved }
```

该对象应为函数的唯一输出。
在函数体其他位置单独写一个 `$saved` 会添加另一个输出值。

### 保存并读取提供的文本

完成接收 `$text` 的 `Save-Text`。
练习使用 `Set-Content` 将其保存到 `./text.txt`（替换任何先前的内容），然后使用 `Get-Content` 将其读取出来。
输出一个包含单个属性 `Text` 的 PSCustomObject，该属性包含完全一致的已保存字符串。

输入是一个 0 到 60 个字符的 ASCII 字符串，可能包含空格和可选的 LF 换行符。
请完整保留所有内容，包括末尾的任何 LF。
对于空输入，`Text` 必须包含空字符串。

### 解答

```powershell
function Save-Text {
    param($text)
    # 保存文本，替换任何先前的内容，且不添加行尾符
    Set-Content -Path ./text.txt -Value $text -NoNewline
    # 将整个文件作为一个字符串读回
    $saved = Get-Content -Path ./text.txt -Raw
    [pscustomobject]@{ Text = $saved }
}
```
