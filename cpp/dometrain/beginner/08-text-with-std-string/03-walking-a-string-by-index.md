对文本的大多数操作都需要访问其中的每个字符，而字符数量并不是在编写代码时就能预先知道的。
`for` 循环从字符串本身获取该计数，其循环条件是阻止计数器越界访问到文本中不存在位置的唯一屏障。

```cpp
const int length = static_cast<int>(s.size());
for (int i = 0; i < length; ++i) {
    std::cout << s[i];
}
```

这会按顺序依次打印 `s` 的字符，每次循环打印一个。
计数器从 0 开始，每次循环前都会检查条件，之后 `++i` 会让计数器递增。
只要 `i < length` 成立，`i` 就处于 0 到 `length - 1` 之间，这恰好是文本所拥有的所有有效位置，因此在循环头部编写的这一条件，就保障了循环执行的每一次读取操作的安全性。
因此使用的是 `<` 而非 `<=`：如果多进行一次循环，读取操作就会落在 `size()` 的位置，而该位置根本不是文本的字符之一。

首先将长度存入 `const int` 可以使比较操作的两端都是 `int` 类型。
直接将计数器与 `s.size()` 进行比较最多只会产生一条警告，而这里的警告并不会阻止程序运行，因此类型转换让计数器和边界成为了相同类型的数字。
如果从长度中减去 1 则更加糟糕：对于空文本，`s.size() - 1` 是无符号减法，会产生一个巨大的数值，导致循环远远超出最后一个字符继续执行，而一旦发生这种情况，其后果是无法预测也无法依赖的。

`countCharacter(const std::string &text, char target)` 用于计算 `target` 在 `text` 中出现的次数。
使用 `for` 循环遍历字符串一次，从 `size()` 获取边界，以 `text[i]` 读取每个位置，并在每次 `text[i] == target` 时，为循环上方声明的总数加 1。
匹配是精确匹配，因此 `'A'` 不会匹配 `'a'`，`countCharacter("Abc", 'a')` 返回 0。
文本中从未出现的目标字符返回 0，空文本也返回 0。
这两种情况都不是拒绝处理：0 就是计数值，而且此函数无法拒绝查询。
请保持使用 `==` 进行比较，因为单个 `=` 是赋值而不是比较，且 `text` 是作为 `const` 引用传入的，因此编译器会报错拦截。

## 解答

```cpp
#include <string>

struct Solution {
    static int countCharacter(const std::string &text, char target) {
        // 逐个访问每个位置，遇到等于 target 的字符就加一
        int total = 0;
        const int length = static_cast<int>(text.size());
        for (int i = 0; i < length; ++i) {
            if (text[i] == target) {
                ++total;
            }
        }
        return total;
    }
};
```
