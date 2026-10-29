`table.sort(words)` 使用 `<` 来比较元素，这会将小写单词按字母顺序排列。
对于任何其他排序方式，请传入第二个参数：一个比较函数，用于决定两个元素中哪一个排在前面。
下面这个函数会将单词按字母逆序排列：

```lua
local words = {"fig", "apple", "kiwi"}
table.sort(words, function(a, b)
  return a > b
end)
print(table.concat(words, ", "))
```

这会打印出 `kiwi, fig, apple`。
在调用内部编写的 `function(a, b) ... end` 会在此处直接创建一个没有名字的函数，而 `end` 后面的 `)` 则闭合了 `table.sort` 的调用。
在排序过程中，`table.sort` 每次比较两个单词时都会调用你的函数，将其中一个作为 `a`，另一个作为 `b`。
当 `a` 必须排在 `b` 前面时，函数返回 `true`，否则返回 `false`。
它不会返回排在前面的单词。
在这里，当 `a` 在字母表中的顺序靠后时，`a > b` 为 true，因此字母靠后的单词会移动到前面。

函数也是一个值，就像数字或字符串一样，所以你也可以把它存储在变量中并传递该变量：

```lua
local later_first = function(a, b)
  return a > b
end
table.sort(words, later_first)
```

注意在那里写 `later_first` 时不要加括号。
`table.sort(words, later_first())` 会在 `table.sort` 开始之前立即调用该函数，且没有传入任何参数，因此 `a` 和 `b` 都是 `nil`，调用会失败并报错 `attempt to compare two nil values`。

按长度排序会遇到平局的情况。
`function(a, b) return #a < #b end` 会将 `"fig"` 排在 `"kiwi"` 前面，但对于 `"bb"` 和 `"aa"`，无论以哪种顺序比较它都会返回 `false`，因为没有哪个单词更短。
两个都不必排在前面的元素构成平局，而 `table.sort` 对平局元素不做任何保证：它可能会交换它们，也可能保持原样。
对于 `{"bb", "aa"}`，它会保持 `"bb"` 在前。
当平局的顺序很重要时，由比较函数来决定：当长度不同时比较长度，当长度相等时用 `<` 比较单词。
函数内部的 `if` 语句可以选择返回哪种比较结果。

编写 `sort_by_length(words)`。
`words` 是一个由小写单词组成的数组。
使用 `table.sort` 和一个比较函数对其进行排序，最短的单词排在最前，相同长度的单词按字母顺序排列，然后返回 `words`。

### 解答

```lua
function sort_by_length(words)
  table.sort(words, function(a, b)
    if #a ~= #b then
      return #a < #b
    end
    return a < b
  end)
  return words
end
```
