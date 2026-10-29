数值型 for 循环会针对范围内的每个数字各运行一次相同的代码行。
以下代码会依次输出 1、2、3：

```lua
for i = 1, 3 do
  print(i)
end
```

`for` 开始循环，而 `i` 是**循环变量**。
`=` 之后是它的起始值和结束值，用逗号隔开。
Lua 将 `i` 设为 1 并运行**循环体**（即 `do` 与 `end` 之间的代码行），然后给 `i` 加 1 并再次运行循环体。
一旦 `i` 超过 3，循环就会停止，因此 3 本身是包含在内的：循环体会以 `i` 为 3 的状态运行，而下一个值 4 会结束循环。

在另一个逗号后的第三个数字是**步长**（step），即每次**循环迭代**（运行一次循环体）后添加到 `i` 的增量。
如果省略不写（如上所示），步长默认为 1。
负数步长会使循环递减：

```lua
for i = 3, 1, -1 do
  print(i)
end
```

这将输出 3、2 和 1。
如果去掉 `-1`，它将什么都不输出。
因为此时步长为 1，起始值 3 已经超过了 1，循环体运行零次。

`i` 仅存在于循环内部（即 `do` 和 `end` 之间），你在循环体内声明的任何 `local` 变量也是如此。
累加总和（running total）必须在每次迭代中持续存在并在循环结束后依然保留，因此要在 `for` 上方声明它：

```lua
local total = 0
for i = 1, 4 do
  total = total + i
end
print(total)
```

`total` 初始为 0，每次迭代都会把当前的 `i` 加到上面，`print` 会显示 `10`。
如果把 `local total = 0` 移到循环体内部，它会在每次迭代时都运行，导致总和每次都重新从 0 开始。

### 计算范围累加和

编写 `sum_range(first, last, step)`。
它使用一个从 `first` 到 `last`、步长为 `step` 的 for 循环，累加循环变量所取的每一个值，并返回该和。
`step` 可以为负数，但绝不会为 0（Lua 会将步长为 0 视为错误）。
如果循环从未进入该范围，累加和为 0。

通过测试后，在函数下方添加 `print(sum_range(1, 10, 4))` 和 `print(sum_range(1, 10, -4))`。
自己先算出这两个数字，然后点击 Run 进行对比。

### 解答

```lua
function sum_range(first, last, step)
  local total = 0
  for i = first, last, step do
    total = total + i
  end
  return total
end
```
