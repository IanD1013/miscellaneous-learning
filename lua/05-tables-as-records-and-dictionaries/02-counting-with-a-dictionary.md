对于 record，你在编写代码时就知道每个字段名称。
统计单词则不同：键就是单词本身，而且只有在程序运行时你才能知道有哪些单词。
方括号可以处理这种情况。
你曾将方括号与数字一起使用，例如 `words[2]`，而与字符串一起使用时，它们的工作方式相同：方括号内的任何值都会成为键。

```lua
local counts = {}
local word = "sun"
counts[word] = 1
print(counts.sun)
print(counts.word)
```

这将打印 `1`，然后是 `nil`。
`counts[word]` 会查看变量 `word` 内部的值，找到 `"sun"`，并将其用作键，因此它设置的条目与 `counts.sun` 读取的条目相同。
点号形式从不会去查找变量：`counts.word` 是 `counts["word"]` 的简写，即拼写为 w-o-r-d 的键，而该键下没有存储任何内容。
这种读取操作不会报错。
缺失的键读取结果为 `nil`，就像 record 中缺失的字段一样。

用于通过键查找值的 table 被称为字典（dictionary）。
在单词计数中，每个键都是一个单词，其值是该单词出现的次数。
一行代码即可完成计数：

```lua
counts[word] = (counts[word] or 0) + 1
```

当 `"sun"` 第一次出现时，`counts[word]` 为 `nil`，`nil or 0` 得到 0，该行代码会存入 1。
下一次遇到它时，读取结果为 1，`or` 保留 1，该行代码存入 2。
如果省略 `or 0`，第一个单词就会报错失败，因为 Lua 无法将 1 与 `nil` 相加。

编写 `count_words(words)`。
`words` 是一个由字母组成的单词数组。
创建一个空的 `counts` table，使用 `ipairs` 遍历 `words`，用上面那行代码统计每个单词，并返回 `counts`。
空数组会得到一个空 table，结果面板将其显示为 `[]`。
大小写很重要：`"Sky"` 和 `"sky"` 是不同的字符串，因此它们是不同的键。

`#` 对字典不起作用：`#counts` 为 0，因为 `#` 统计的是位置 1, 2, 3 及以后的项，而以单词为键的 table 没有这些项。
字典也不会保留单词输入的顺序，因此结果面板中列出的键的顺序可能与预期值不同。
只要键及其计数值匹配即可。

在将以下代码添加到函数 `end` 之后之前，先判断它们会打印什么，然后点击 Run 并查看控制台：

```lua
local counts = count_words({"sun", "rain", "sun"})
print(counts.sun)
print(counts.moon)
```

### 解答

```lua
function count_words(words)
  local counts = {}
  for _, word in ipairs(words) do
    counts[word] = (counts[word] or 0) + 1
  end
  return counts
end
```
