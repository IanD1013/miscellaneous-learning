`else` 附加到其正上方的 `if` 上，并处理该 `if` 拒绝的情况：

```cpp
bool stored = true;
std::string state;
if (stored) {
    state = "has contents";
} else {
    state = "nothing stored";
}
```

这两个主体是互斥的分支。
条件只求值一次，一个主体运行，另一个就不会运行，无论哪种情况，`state` 最终都会保存某个值。
在 `else` 之后紧接着写另一个 `if`，这一对就会扩展为一个链：

```cpp
int count = 3;
std::string size;
if (count < 1) {
    size = "none";
} else if (count < 4) {
    size = "a few";
} else {
    size = "many";
}
```

链式结构自上而下进行测试，并且最先匹配的获胜。
一旦某个条件成立，其对应的主体就会运行，并且其下方的每个条件都会被跳过而不进行求值。
这就是为什么较低的分支只需要声明自己的上限：`count < 4` 永远不会遇到小于 1 的值，因为上面的分支已经捕获了这些值。
因此，顺序也是逻辑的一部分。
如果将 `count < 4` 放在最前面，0 就会进入该分支，导致原本为 0 准备的分支根本不会运行。

彼此之间没有 `else` 的独立 `if` 语句具有不同的形式。
每个条件都会被测试，像 0 这样的值可能会满足其中的两个条件，而后运行的主体将覆盖较早主体所存储的值。
末尾的 `else` 不需要自带任何条件，因为它不需要；它会捕获链中剩余的所有情况。
如果以另一个 `else if` 结尾，那么不符合任何条件的输入将保持变量原有的值。

### 需求

- 完成 `digitBandLabel`，它接收一个名为 `value` 的 `int` 并返回一个 `std::string`。
- 任何小于 0 的值返回 `negative`。
- 0 到 9 返回 `one digit`。
- 10 到 99 返回 `two digits`。
- 100 及以上返回 `three or more digits`。
- 每个标签必须与所写的完全一致：全小写、单空格、无多余字符。
- 在捕获该值的分支内将区间文本赋值给初始代码中的 `label`，并在最后统一返回 `label`，而不是在分支内部直接返回。
- 这四个区间是一个链的分支，因此你的代码中必须出现 `else`。
  四个都会写入 `label` 的独立 `if` 语句会让 5 匹配两个区间，而最终保留下来的将是第二次赋值。

### 解答

```cpp
#include <string>

struct Solution {
    static std::string digitBandLabel(int value) {
        // 先测试区间的最低边界，并在匹配的分支中设置 label
        std::string label = "negative";
        if (value < 0) {
            label = "negative";
        } else if (value < 10) {
            label = "one digit";
        } else if (value < 100) {
            label = "two digits";
        } else {
            label = "three or more digits";
        }
        return label;
    }
};
```
