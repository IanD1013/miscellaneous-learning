`begin`、`process` 和 `end` 允许管道函数保持运行累计总和，而无需为每条记录返回部分结果：

```powershell
function Get-NumberSum {
    [CmdletBinding()]
    param([Parameter(ValueFromPipeline=$true)][int]$Number)
    begin { $sum = 0 }
    process { $sum += $Number }
    end { [pscustomobject]@{ Sum = $sum } }
}
@(2, 5) | Get-NumberSum
```

这会返回一个具有 `Sum = 7` 的对象。`begin` 在记录到达之前运行一次。PowerShell 在为该记录运行 `process` 之前，将每个传入的值绑定到 `$Number`。所有这三个块共享调用的变量，因此 `$sum` 能够在各记录之间保留。在 `process` 内部初始化它将会丢弃之前的累计总和。`end` 在输入完成后运行一次，即使管道为空也会运行：`@() | Get-NumberSum` 返回 `Sum = 0`。新的调用将以全新的状态开始。

属性名绑定遵循相同的生命周期。在 `Get-KeyTotals` 中，每条记录在 `process` 运行之前提供新的 `$Key` 和 `$Value` 值。请保持赋值静默，并仅在 `end` 中输出汇总；多余的裸表达式（bare expression）会变成另一个结果。现有的 `foreach` 按保存的顺序收集分组，而 `@($groups)` 保证 `Groups` 是一个包含零个、一个或多个条目的数组。

### 完成聚合

修复 `main.ps1` 中的 `Get-KeyTotals`。保留其类型化、属性绑定的参数、生命周期计数器以及提供的 `Invoke-Exercise(Inputs, Options)` 包装函数。

- `Inputs` 包含零到八条记录。每条记录都有一个长度为 1 到 40 个字符的非空字符串 `Key`，以及一个介于 0 到 8 之间（含两端）的整数 `Value`。
- 返回一个汇总，其中 `Count` 统计每条记录，`Total` 对每个值求和（包括 0）。空输入将两者均返回为 0。
- `Groups` 包含带有 `Key`、`Count` 和 `Total` 的对象。将每个键转换为小写，合并变得相同的键，并按首次出现的顺序保留分组。空输入产生空数组；单条记录产生一个分组。
- 如果没有 `Options.Repeat`，包装函数将返回 `Summary`、`Begins`、`Processes` 和 `Ends`。如果设置了 `Repeat = $true`，它将返回 `First` 和一个空输入的 `Second`，再加上合并后的计数器。每次调用都会贡献一个 begin、一个 end 以及每条记录对应的一个 process。第二个汇总不得包含来自第一个汇总的任何状态。

包装函数已经处理了被拒绝的输入。请专注于在整个生命周期中累加值。

### 解答

```powershell
function Get-KeyTotals {
    [CmdletBinding()] 
    param(
        [Parameter(ValueFromPipelineByPropertyName=$true)]
        [ValidateNotNullOrEmpty()]
        [string]$Key='unused',

        [Parameter(ValueFromPipelineByPropertyName=$true)]
        [ValidateRange(0,8)]
        [int]$Value
    )
    begin { 
        $totals=@{}
        $keys=@()
        $count=0
        $total=0
        $script:Begins++
    }
    process {
        $script:Processes++
        $keyName=$Key.ToLower()

        if (-not $totals.ContainsKey($keyName)) { 
            $totals[$keyName]=[pscustomobject]@{Key=$keyName;Count=0;Total=0}
            $keys += $keyName 
        }
        $totals[$keyName].Count++
        $totals[$keyName].Total += $Value
        $count++; 
        $total += $Value
    }
    end { 
        $script:Ends++
        $groups=@(foreach ($keyName in $keys) { $totals[$keyName] })
        [pscustomobject]@{Count=$count;Total=$total;Groups=@($groups)} 
    }
}

function Invoke-Exercise {
    param($Inputs,$Options)
    $script:Begins=0
    $script:Processes=0
    $script:Ends=0

    try {
        if (@($Inputs).Count -gt 8) { 
            throw 'limit' 
        }
        foreach ($record in $Inputs) {
            if ($null -eq $record.Key -or $record.Key.Length -gt 40 -or $null -eq $record.Value) { 
                throw 'record' 
            } 
        }
        $summary=$Inputs | Get-KeyTotals
        if ($Options.Repeat) { 
            $second=@() | Get-KeyTotals
            [pscustomobject]@{
                First=$summary
                Second=$second
                Begins=$script:Begins
                Processes=$script:Processes
                Ends=$script:Ends
            } 
        }
        else { 
            [pscustomobject]@{
                Summary=$summary
                Begins=$script:Begins
                Processes=$script:Processes
                Ends=$script:Ends
            } 
        }
    } catch { 
        [pscustomobject]@{
            Rejected=$true
            Processes=$script:Processes
        } 
    }
}
```
