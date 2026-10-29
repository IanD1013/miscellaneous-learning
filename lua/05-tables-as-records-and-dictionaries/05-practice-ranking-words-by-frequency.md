`rank_words(words)` 接收一个单词数组，并返回一个字符串数组：每个不同的单词只出现一次，按出现频率从高到低排序。
`words` 中的每个元素都是由字母组成的单词，空的 `words` 返回空数组。
出现次数相同的单词按字母顺序排列，大写字母优先。
这正是两个字符串使用 `<` 比较时的顺序，因为所有大写字母都在小写字母之前：`"Oak" < "ash"` 为 true。
`"Oak"` 和 `"oak"` 是两个不同的单词。

直接对 `words` 进行排序会按拼写排列单词，而 `table.sort` 从不检查每个单词出现的次数。
因此需要先进行计数，使用一个将每个单词映射到其出现次数的字典。

### 从计数到排名

`pairs` 遍历字典，提供每个单词及其计数。
将每一项作为一条记录存储在一个新数组 `records` 中。
如果循环变量命名为 `word` 和 `count`，每次循环可以用一行代码添加记录：

```lua
table.insert(records, {word = word, count = count})
```

在大括号内，每个 `=` 左侧的名称是字段名，右侧的值可以是任何变量或表达式，这里是同名的循环变量。
`records` 数组还不是最终答案：`pairs` 访问键的顺序是不固定的，并且两次 Run 之间的顺序可能会发生变化。

使用 `table.sort` 和一个比较函数对这些记录进行排序。
该函数接收两条记录，因此可以直接从中读取 `a.count` 和 `b.count`。
当计数不同时，计数较大的记录排在前面。
当计数相等时，使用 `<` 比较 `a.word` 和 `b.word`。

第二个比较正是使结果保持固定的关键。
没有它，代码就无法决定出现次数相同的单词排在何处：它们最初是 `pairs` 给出的顺序，而 `table.sort` 也可以随意重新排列并列的元素。
使用相同的单词，这样的解决方案可能会在一次 Run 中得到正确的排名，而在下一次 Run 中得到错误的排名。

最后，使用 `ipairs` 遍历排序后的记录，并将每个 `record.word` 收集到你要返回的数组中。

### 解答

```lua
function rank_words(words)
  local counts = {}
  for _, word in ipairs(words) do
    counts[word] = (counts[word] or 0) + 1
  end

  local records = {}
  for word, count in pairs(counts) do
    table.insert(records, {word = word, count = count})
  end

  table.sort(records, function(a, b)
    if a.count ~= b.count then
      return a.count > b.count
    end
    return a.word < b.word
  end)

  local ranked = {}
  for _, record in ipairs(records) do
    table.insert(ranked, record.word)
  end
  return ranked
end
```
