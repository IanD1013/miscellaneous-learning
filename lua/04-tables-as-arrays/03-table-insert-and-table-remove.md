`table.insert` 可以向数组中添加一个元素，而 `table.remove` 则可以取出一个元素。
这两个名称中的 `table` 是 Lua 内置的 table 函数集，而不是你自己定义的变量，因此你想要修改的数组需要作为第一个参数传入。
这两个函数都会直接修改该数组本身，并且都接受一个位置参数（即发生更改的索引）：

```lua
local letters = {"a", "b", "c", "d"}
local removed = table.remove(letters, 2)
table.insert(letters, 2, "x")
table.insert(letters, "e")
local last = table.remove(letters)
```

`table.remove(letters, 2)` 会将位置 2 处的 `"b"` 取出并返回它，因此 `removed` 的值为 `"b"`。
其后的元素会依次向前移动一位以填补空缺：`letters[2]` 现在是 `"c"`，`letters[3]` 是 `"d"`，而 `#letters` 变为 3。
当传入三个参数时，`table.insert` 会在值之前接收位置参数，因此 `table.insert(letters, 2, "x")` 会将 `"x"` 放在位置 2，并将 `"c"` 和 `"d"` 向后移动一位，结果为 `{"a", "x", "c", "d"}`。

如果省略位置参数，这两个函数都会在数组末尾进行操作。
`table.insert(letters, "e")` 会在最后一个元素之后添加 `"e"`。
`table.remove(letters)` 会移除最后一个元素（而不是第一个元素）并返回它：`last` 的值为 `"e"`，而 `letters` 恢复为 `{"a", "x", "c", "d"}`。

`table.remove` 会返回它移除的元素，但 `table.insert` 不返回任何值。
请将它单独作为一行调用；`letters = table.insert(letters, "e")` 会导致 `letters` 被赋值为 `nil`。

编写 `move_first_to_end(items)`。
`items` 是一个由字符串或数字组成的数组。
使用 `table.remove` 取出它的第一个元素，使用 `table.insert` 将该元素添加到末尾，然后返回 `items`：`{1, 2, 3}` 会变成 `{2, 3, 1}`。
只有一个元素的数组返回时保持不变，空数组同样如此，无需编写额外代码：对于空数组，`table.remove` 不会报错而是返回 `nil`，而在末尾插入该 `nil` 仍会使数组保持为空。

### 解答

```lua
function move_first_to_end(items)
  local first = table.remove(items, 1)
  table.insert(items, first)
  return items
end
```
