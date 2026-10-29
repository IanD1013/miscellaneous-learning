`ipairs` 允许 `for` 循环按顺序遍历数组。
在每次遍历中，循环都会获取两样东西：索引（数组中的位置）以及存储在该位置的值。

```lua
local colors = {"red", "green", "blue"}
for i, color in ipairs(colors) do
  print(i, color)
end
```

这会打印三行：`1` 对应 `red`，`2` 对应 `green`，`3` 对应 `blue`。
你可以自由选择变量名 `i` 和 `color`，但它们的顺序是固定的：第一个变量始终获取索引，第二个变量获取值。
`in` 将它们与要遍历的数组 `ipairs(colors)` 分隔开。
循环从索引 1 开始，到最后一个元素后停止，因此它用一行代码就完成了 `for i = 1, #colors do` 加上 `local color = colors[i]` 这两行代码所做的事情。
如果数组为空，循环体则一次也不会执行。

通常循环体只需要值。
省略第一个变量名并不会跳过索引：`for color in ipairs(colors)` 会将 1、2 和 3 赋值给 `color`，而根本不会读取颜色。
因此，请同时写出这两个变量名，并将未使用的索引命名为 `_`。
它是一个普通的变量名，Lua 程序员习惯用它来标记代码中被忽略的变量。

`break` 可以提前终止循环。
Lua 会跳过当前遍历的剩余部分，不再进行后续遍历，并从循环的 `end` 之后的第一行继续执行。
它只会跳出循环，绝不会退出函数：

```lua
local scores = {7, 3, 12, 5}
for _, score in ipairs(scores) do
  if score > 10 then
    break
  end
  print(score)
end
print("after the loop")
```

控制台会显示 `7`、`3`，然后是 `after the loop`。
`break` 位于 `if` 内部，但 `if` 不是循环，因此被终止的是 `for`：12 绝不会被打印，5 也绝不会被执行到。

编写 `sum_until_zero(numbers)`。
`numbers` 是一个整数数组，其中的数字可以为负数。
返回第一个 0 之前的所有元素之和。
如果没有 0，则返回所有元素之和；空数组返回 0。
使用 `ipairs` 遍历数组，将总和保存在初始值为 0 的局部变量 `total` 中，并在值为 0 时使用 `break` 跳出循环。
将 `return total` 放在循环的 `end` 之后，这样无论是因为 `break` 终止了循环，还是所有元素已遍历完毕，它都会执行。

### 解答

```lua
function sum_until_zero(numbers)
  local total = 0
  for _, number in ipairs(numbers) do
    if number == 0 then
      break
    end
    total = total + number
  end
  return total
end
```
