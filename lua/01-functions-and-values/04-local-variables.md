函数可以在某一行计算出一个值，将其保存在一个名称下，并在随后的行中使用该名称。
这个名称就是一个局部变量：

```lua
function minutes_text(minutes)
  local seconds = minutes * 60
  return minutes .. " minutes is " .. seconds .. " seconds"
end
```

`local` 创建一个新变量，这里名为 `seconds`，而 `=` 为其赋值：Lua 计算右侧的表达式 `minutes * 60`，并将结果存储在左侧的名称下。
在 `return` 这一行中，`seconds` 代表存储的那个数字。
`..` 也可以拼接数字，将其数字写入文本中，因此 `minutes_text(3)` 返回 `3 minutes is 180 seconds`。

稍后你可以给变量赋予一个新值。
再次写下变量名和 `=`，但这次不要带 `local`，因为该变量已经存在：

```lua
local count = 2
local doubled = count * 2
count = count + 1
```

在 Lua 中，`=` 总是表示赋值；它绝不会检查两项是否相等。
如果当作数学来看，`count = count + 1` 永远不可能成立。
作为赋值语句，Lua 会用当前值 2 计算 `count + 1`，然后将 3 存回 `count` 中。
之后 `doubled` 仍然是 4：变量保存的是那一行计算出的值，而不是表达式本身。

局部变量仅存在于创建它的函数内部。
如果省略 `local`，`seconds = minutes * 60` 仍然可以运行，但 `seconds` 会变成一个全局变量：文件中的每个函数都可以读取和修改它，并且在函数返回后它依然保留其值。
在函数内部，请将每个新变量都声明为 `local`。

### 你的任务

编写 `rectangle_summary(width, height)`。
在两个局部变量中计算出面积（宽乘以高）和周长（宽与高之和的两倍），然后在一个字符串中返回这两者：`rectangle_summary(3, 4)` 返回 `area 12, perimeter 14`，其他尺寸则用各自的数字替换 12 和 14。
`width` 和 `height` 是整数且可以为 0；对它们进行乘法和加法运算会得到整数，拼接时为 `12` 而不是 `12.0`。

### 解答

```lua
function rectangle_summary(width, height)
  local area = width * height
  local perimeter = 2 * (width + height)
  return "area " .. area .. ", perimeter " .. perimeter
end
```
