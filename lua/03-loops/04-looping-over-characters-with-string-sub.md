`#` 是长度运算符：把它放在由普通英文字母和空格组成的字符串前面，你就可以得到它的长度，即其中包含的字符数。
`string.sub` 接受一个字符串、一个起始位置和一个结束位置，并将从起始位置到结束位置的字符（两者均包含在内）作为新字符串返回。
位置从 1 开始计数，因此最后一个字符的位置等于字符串的长度。

```lua
local word = "spoon"
print(#word)
print(string.sub(word, 1, 1))
print(string.sub(word, 2, 3))
print(string.sub(word, 2))
```

这会打印出 `5`、`s`、`po` 和 `poon`。
传入相同的起始和结束位置会返回单个字符。
如果不传入结束位置，`string.sub` 会一直截取到字符串末尾，这就是为什么最后一行打印的是 `poon` 而不是 `p`。

`word:sub(2, 2)` 是 `string.sub(word, 2, 2)` 的简写形式。
冒号会将其前面的字符串作为第一个参数传入，因此括号内只需要包含位置参数。
这里必须使用冒号。
如果使用点号，`word.sub(2, 2)` 在调用时就会遗漏 `word`，导致 `sub` 根本接收不到 `"spoon"`：它会返回一个空字符串且不会报错，而 `print(word.sub(2, 2))` 则会输出一行空白。

从 1 到字符串长度的数值型 `for` 循环可以按顺序读取每个字符：

```lua
local word = "spoon"
for i = 1, #word do
  print(word:sub(i, i))
end
```

这会打印出这五个字母，每行一个。
对于空字符串 `""`，其长度为 0，因此循环从 1 到 0 运行，其循环体一次都不会执行。

`==` 会将大写字母和小写字母视为不同的字符：`"B" == "b"` 的结果是 `false`。
`string.lower(s)` 返回 `s` 的小写副本，而 `string.upper(s)` 返回大写副本。
两者也都可以使用冒号形式调用：

```lua
local name = "Lua"
print(string.upper(name))
print(name:lower())
print(name)
```

这会打印出 `LUA`、`lua` 和 `Lua`：每次调用都返回了一个新的字符串，而 `name` 本身保持不变。
单独写一行 `name:lower()` 不会产生任何实际效果，因此请使用它返回的副本。

### 忽略大小写统计字母数量

编写函数 `count_letter(text, letter)`。
`text` 包含字母和空格，可能为空字符串；`letter` 为单个字母（小写或大写）。
返回在忽略大小写的情况下，`text` 中有多少个字符是该字母：`count_letter("Banana", "b")` 返回 `1`，`count_letter("AAA", "a")` 返回 `3`，对于空的 `text` 则返回 `0`。

遍历从 1 到 `#text` 的每个位置，将该位置上的字符与 `letter` 进行比较，并累加匹配项。
比较前先将两边都转为小写：`letter`，以及从 `text` 中读取的每个字符。
将两者都转为大写也同样可行。

### 解答

```lua
function count_letter(text, letter)
  local count = 0
  local target = letter:lower()
  for i = 1, #text do
    if text:sub(i, i):lower() == target then
      count = count + 1
    end
  end
  return count
end
```
