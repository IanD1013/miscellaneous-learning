计数必须先存在，然后才能对其进行递增，而在 `std::map<std::string, int>` 中，下标操作正是创建该项并将其初始值设为 0 的机制。
在下标前加上前缀 `++` 可以在一个表达式中同时完成这两项工作，而它们的发生顺序正是这一惯用法的核心：

```cpp
#include <map>
#include <string>

std::map<std::string, int> counts;
++counts["ant"];   // 条目被创建并保存 0，然后增加到 1
++counts["ant"];   // 增加到 2
```

下标操作会访问 `ant` 对应的条目，并在首次请求时创建它，而 `++` 会给找到的值加一。
因此，初次出现时会在无需编写额外判断的情况下留下计数 1，之后的每次出现都会再加一。

`++` 放在哪一边决定了表达式本身的值。
写在前面时，`++counts[word]` 是自增后的计数值，因此 `if (++counts[word] == 2)` 恰好在将某个单词的计数从 1 提升到 2 的那一次遍历中为 true。
写在后面时，`counts[word]++` 是自增前的计数值，同样的比较会延迟一次触发，并且对于只出现两次的单词根本不会触发。

给定 `{"ant", "bee", "ant", "cow"}`，有一个单词出现了两次，答案为 1。
这就是 `countRepeatedWords(const std::vector<std::string> &words)` 作为 `int` 返回的内容，即至少出现两次的不同单词的数量。
出现五次的单词同样只贡献 1，因此比较条件是 `== 2` 而不是 `>= 2`，因为每个单词只有一次遍历能将其计数从 1 提升到 2。
在循环外部声明 `std::map<`，这既是它应该在的位置，也是所需标记所在的位置。
如果在循环内部声明，map 将在每次循环时被清空，导致每个单词看起来都像是初次出现。
这些单词无需预先排序或分组，因为无论它们出现在 vector 的哪个位置，每个单词都能找到自己的条目；出于类似的原因，使用 `std::count(` 重新扫描也是被禁止的：因为已经在进行计数了。
不包含单词的 vector 返回 0，单词各不相同的 vector 也同样返回 0。

## 解答

```cpp
#include <map>
#include <string>
#include <vector>

struct Solution {
    static int countRepeatedWords(const std::vector<std::string> &words) {
        // 为每个单词计数，计数刚好变成 2 时答案加一
        std::map<std::string, int> counts;
        int repeated = 0;
        for (const std::string &word : words) {
            if (++counts[word] == 2) {
                ++repeated;
            }
        }
        return repeated;
    }
};
```
