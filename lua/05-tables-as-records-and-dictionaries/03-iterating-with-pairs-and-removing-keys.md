要访问字典中的每个条目，可以使用 `pairs` 对其进行循环遍历：

```lua
local lengths = {cat = 3, horse = 5, ox = 2}
for key, value in pairs(lengths) do
  print(key, value)
end
```

该循环的写法与 `ipairs` 循环完全一致，只是在 `in` 后面使用了 `pairs(lengths)`。
在每次迭代中，`key` 保存 table 的一个键，`value` 保存该键对应的值，并且每个键都会且仅会出现一次。
控制台会为每个条目打印一行：

```bash
horse	5
cat	3
ox	2
```

你打印出的行顺序可能会有所不同。
`pairs` 不会按照键写入时的顺序进行遍历，而且下次点击 Run 时其顺序可能还会改变。
如果把 `pairs` 替换为 `ipairs`，则什么都不会打印：因为 `ipairs` 从索引位置 1 开始遍历，而 `lengths` 在位置 1 上没有任何内容。

要删除某个条目，可以将其设置为 `nil`：

```lua
lengths.horse = nil
print(lengths.horse)
```

这会打印 `nil`，此时上面的 `pairs` 循环将只会打印 `cat` 和 `ox` 对应的行。
只有 `nil` 才能真正删除一个条目。
如果改为存入 0 或 `false`，`horse` 仍然会保留在 table 中并持有该值，并且 `pairs` 仍会访问它。
当使用变量保存键时（例如循环内部的 `key`），请使用方括号语法：`lengths[key] = nil`。

在 `pairs` 循环运行期间，你可以删除条目，包括当前正在遍历的条目。
不过，在循环过程中切勿添加 table 中尚不存在的键：Lua 无法保证在此之后循环的行为。

编写函数 `keep_at_least(counts, minimum)`。
`counts` 是一个字典，其键为单词，值为整数（包含零和负数）；`minimum` 是一个整数。
使用 `pairs` 遍历 `counts`，删除所有值小于 `minimum` 的条目，并返回 `counts`。
值等于 `minimum` 的条目应予以保留。
如果所有条目都被删除，或者传入的 `counts` 本身为空，函数将返回一个空 table。

`pairs` 选取的顺序在这里没有任何影响。
每个条目都是通过将自身的值与 `minimum` 进行比较来决定保留还是删除，因此无论键以何种顺序出现，最终留下的条目都是相同的。

### 解答

```lua
function keep_at_least(counts, minimum)
  for key, value in pairs(counts) do
    if value < minimum then
      counts[key] = nil
    end
  end
  return counts
end
```
