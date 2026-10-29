只有当条件为 true 时，`if` 语句才会运行一段代码。
加上 `elseif` 和 `else`，它就可以在多段代码中恰好运行其中一段。
下面这个函数会根据数字的正负符号返回对应的英文单词：

```lua
function sign_word(n)
  if n < 0 then
    return "negative"
  elseif n == 0 then
    return "zero"
  else
    return "positive"
  end
end
```

- `if` 后面紧跟一个条件，这里是比较操作 `n < 0`，然后是单词 `then`。
`then` 之后直到下一个 `elseif`、`else` 或 `end` 之间的代码行，就是该条件的**分支**（branch）。
- `elseif` 会添加另一个条件，该条件拥有自己的 `then` 以及自己的分支。
你可以根据需要添加任意多个 `elseif`。
- `else` 不需要任何条件。
当它前面的所有条件都不为 true 时，就会运行它的分支。
- 最后一个分支后面的单个 `end` 用于结束整个语句。
下一行的 `end` 则用于结束该函数。

Lua 会从上到下依次测试各个条件，并运行第一个为 true 的条件所对应的分支。
其下方的所有分支都会被跳过，即使其中某些分支的条件也为 true。
分支内部的 `return` 会立即结束函数，并将该值作为结果返回。

请将 `elseif` 写成一个词。
带有空格的 `else if` 表示一个 `else` 分支中又开启了第二个独立的 `if`，而那个 `if` 需要有它自己对应的 `end`。

### 当多个条件同时为 true 时

在接下来的任务中，你需要将分数转换为等级字母：90 分及以上为 A，60 分及以上为 D。
对于 95 分，`score >= 90` 为 true，`score >= 60` 也为 true。
如果把 `score >= 60` 的判断放在前面，95 分就会在那里停下并得到 D。
因此，应该先测试最高的阈值，然后依次向下。
一旦所有 90 分及以上的分数都已返回，后续的 `score >= 80` 就只会遇到低于 90 的分数，因此不需要额外再检查 `score < 90`。

### 等级字母

编写函数 `letter_grade(score)`，其中 `score` 是一个 0 到 100 之间的整数。
以单字符字符串的形式返回等级：

- 90 分或以上：`"A"`
- 80 到 89 分：`"B"`
- 70 到 79 分：`"C"`
- 60 到 69 分：`"D"`
- 60 分以下：`"F"`

使用一个 `if` 语句，分别为 B、C 和 D 设置 `elseif` 分支，并为 F 设置一个 `else` 分支。

### 解答

```lua
function letter_grade(score)
  if score >= 90 then
    return "A"
  elseif score >= 80 then
    return "B"
  elseif score >= 70 then
    return "C"
  elseif score >= 60 then
    return "D"
  else
    return "F"
  end
end
```
