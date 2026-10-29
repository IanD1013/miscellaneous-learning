数组的元素可以是记录（record）：将每条记录的大括号写在数组的大括号内部，这样每个元素就是一个带有命名字段的完整表（table）。
位于另一个表内部的表被称为嵌套表（nested table）。

```lua
local entries = {
  {name = "Lin", score = 12},
  {name = "Max", score = 40}
}
print(entries[2].score)
print(entries.score)
for _, entry in ipairs(entries) do
  print(entry.name, entry.score)
end
```

这段代码会打印 `40`，然后是 `nil`，接着在单独的一行中打印每条记录的姓名和分数。
在 `entries[2].score` 中，`entries[2]` 是第二个元素（即一条记录），而 `.score` 读取该记录的一个字段。
`entries.score` 省略了位置索引，因此它向数组本身请求名为 `score` 的字段。
该数组仅在位置 1 和 2 处有元素，因此读取结果为 `nil`。
在循环中，`entry` 在每次遍历时代表一个完整的元素，而 `entry.name` 和 `entry.score` 读取它的字段。
位置索引保存在 `_` 中，这是通常用于表示不使用的变量的命名习惯。

### 查找最高分

`name_with_max_score(entries)` 接收一个形如上述结构的记录数组，分数可能是负数。
它返回最高分记录的 `name`；当多条记录并列最高分时，返回最早出现的那条记录的姓名。

将目前为止最好的记录保存在一个局部变量 `best` 中，初始值为 `nil`，表示尚未处理任何记录。
在每次遍历时，如果 `best` 仍为 `nil`，或者当前元素的分数大于 `best` 中的分数，则该元素替换 `best`。
将 `nil` 检查（即 `best == nil`）放在 `or` 的左侧。
读取 `nil` 的字段会导致错误，并且 `or` 仅在其左侧为 `false` 或 `nil` 时才会读取其右侧，因此将检查放在左侧可以确保在 `best` 为 `nil` 时绝不会读取 `best.score`。
使用 `>` 比较分数。
如果使用 `>=`，具有相同分数的后续记录也会替换之前的记录，遇到平局时就会返回靠后的姓名。

相比之下，如果从一个凭空捏造的分数开始，当数组中没有任何分数大于该捏造分数时就会失败。
如果最高分从 0 开始且最佳姓名从 `nil` 开始，`name_with_max_score({{name = "Rex", score = -6}, {name = "Sol", score = -2}})` 将返回 `nil`：因为 -6 和 -2 都不大于 0，所以姓名永远不会被设置。
将 `best` 初始化为 `nil` 可以避免这种情况，因为第一个元素总会替换它。

循环结束后，返回 `best.name`。
空数组是例外：循环从不执行且 `best` 仍为 `nil`，此时应返回 `nil`。

### 解答

```lua
function name_with_max_score(entries)
  local best = nil
  for _, entry in ipairs(entries) do
    if best == nil or entry.score > best.score then
      best = entry
    end
  end
  if best == nil then
    return nil
  end
  return best.name
end
```
