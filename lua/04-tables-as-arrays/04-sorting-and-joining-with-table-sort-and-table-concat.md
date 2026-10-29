`table.sort` 会将数组中的元素按从小到大的顺序排列，而 `table.concat` 则将数组中的元素连接成一个字符串。
两者先后连用，可以将任意顺序的数组转换为一行排序后的文本：

```lua
local colors = {"red", "green", "blue"}
table.sort(colors)
print(table.concat(colors, " / "))
```

这会输出 `blue / green / red`。
`table.sort(colors)` 使用 `<` 比较元素，并在 `colors` 内部直接移动它们的位置。
这被称为就地排序（sorting in place）：该调用会直接修改传入的数组且不返回任何内容，因此没有已排序的副本可以存入变量中。
在该行之后，`colors[1]` 的值变为 `"blue"`。

`table.concat(colors, " / ")` 接受该数组和一个分隔符（放置在每对相邻元素之间的字符串），并返回一个字符串。
第一个元素之前或最后一个元素之后都不会添加任何内容，因此对于只有一个元素的数组，它仅返回该元素；对于空数组，则返回空字符串 `""`。

将示例粘贴在你的函数下方，并将其最后一行替换为 `print(table.concat(table.sort(colors), " / "))`。
在点击 Run 之前，先思考错误信息中会指出这两个函数中的哪一个，以及为什么。
然后再次删除这些行。

对于字符串，`<` 会从左到右逐字符进行比较，第一对不同的字符将决定其先后顺序。
每个字符都以数字形式存储，这些数字使得所有大写字母都排在所有小写字母之前，因此 `"Zoo" < "apple"` 为 true，且 `"Zoo"` 排在最前。
字符串中的数字也以同样的方式作为字符（而非数值）进行比较：`"10" < "9"` 为 true，因为 `"1"` 排在 `"9"` 之前，而根本不会去看 `"0"`。

编写 `sorted_list(words)`。
`words` 是一个由字母或数字组成的字符串数组，它可能为空。
对其进行排序，然后返回用分隔符 `", "`（逗号后跟一个空格）连接起来的单词。

### 解答

```lua
function sorted_list(words)
  table.sort(words)
  return table.concat(words, ", ")
end
```
