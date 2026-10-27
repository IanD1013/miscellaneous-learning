`std::ostringstream` 是一个类似于 `std::cout` 的输出流，它写入自身所拥有的字符串而不是控制台。
每个 `<<` 都会追加数字、字符串或任何带有自定义 `operator<<` 的类型的格式化文本，而 `str()` 则返回到目前为止写入的所有内容：

```cpp
#include <sstream>

std::ostringstream out;
out << "retry " << 3 << " of " << 5;
std::string text = out.str();
```

`text` 的值为 `"retry 3 of 5"`。
流本身会对 int 进行格式化，因此不需要 `std::to_string`，也不需要 `+=`。

在项目之间添加分隔符时，关键在于你何时写入它。
如果在每个项目之后都写入 `"; "`，两个键值对的结果就会是 `"a=1; b=2; "`，这样就必须从字符串中截掉最后一个分隔符。
如果在除第一个项目之外的每个项目之前写入它，就完全不需要执行任何删除操作。

### 使用 std::istringstream 读取 int

来自同一头文件的 `std::istringstream` 则相反：`std::istringstream in(line);` 从 `line` 的副本中读取。
每个向 `int` 读取的 `in >> value` 都会跳过任意空白字符，读取可选的符号和数字，并在遇到第一个无法继续构成数字的字符时停止：

```cpp
std::istringstream in("  12 -3x");
int value = 0;
in >> value;
in >> value;
```

第一次读取存储了 12。
第二次读取存储了 -3 并停在 `x` 处，`x` 保留在流中。
第三次读取会在本应开始数字的地方遇到 `x`，从而设置流的 fail 状态。
读取一个超出 `int` 范围的数字也会设置该状态。
`int` 的范围是从 -2147483648 到 2147483647，因此 2147483648 会失败，-2147483649 也会失败。

在此运行环境中，当文本不以数字开头或数字超出 `int` 范围时，`std::stoi` 会终止程序。
而失败的 `>>` 不会终止任何东西：表达式 `in >> value` 在条件判断中求值为 false，因此你可以通过 `if (!(in >> value))` 来检查读取操作。
请保留内层括号。
`!in >> value` 虽然也能编译，但它会将 `!` 应用于流并将结果移位 `value`，因此不会读取任何内容。

### 异常文本或行尾

当一行仅包含由空白字符分隔的 `int` 且没有其他内容时，该行就是合规的。
一旦读取到达文本末尾，`in.eof()` 就会为 true；检查某行是否合规的一种极具诱惑的做法是：持续读取直到 `>>` 失败，然后探究它停止的原因：

```cpp
while (in >> value) {
    numbers.push_back(value);
}
return in.eof();
```

对于 `"12abc"`，这种做法是有效的：循环在 `abc` 处停止，`eof()` 为 false，该行被判定为异常。
但对于 `"2147483648"`，它会得出错误的结果。
读取操作会提取每一个数字字符，然后才发现该数字超出了范围，因此这一次读取既到达了文本末尾又失败了。
此时 `eof()` 为 true，该行就会被误报为合规。

因此，应在每次读取之前检查是否已到末尾，而不是在循环结束后检查一次。
`in >> std::ws` 会跳过空白字符，不读取其他任何内容。
如果在此之后 `in.eof()` 为 true，说明该行已无剩余字符，且此前的每个数字都已正确读取。
如果为 false，说明还有字符待读取，此时下一个 `in >> value` 必须成功。
如果该读取失败，则该行是异常的，即使该次读取同时也到达了末尾也是如此。

### 需要构建的内容

在 `streams.cpp` 中实现 `Solution` 的三个静态函数：

- `formatPairs(keys, values)`：将每个 `keys[i]` 和 `values[i]` 写作 `key=value` 并返回，键值对之间用 `"; "`（一个分号和一个空格）连接，且最后一个键值对之后没有任何内容：`{"a", "b"}` 和 `{1, 2}` 返回 `"a=1; b=2"`。
  请使用 `std::ostringstream` 构建它。
  当 `keys` 和 `values` 的大小不同时，返回 `""`。
- `parsesCleanly(line)`：当 `line` 合规时返回 `true`，否则返回 `false`。
  连续空格、负数以及完全没有数字的行都是合规的。
  一个单词、紧随数字后面的字母以及超出 `int` 范围的数字都是不合规的。
- `parseInts(line)`：当该行合规时按顺序返回所有数字；当不合规时返回一个空 vector。
  `"7 x 9"` 返回 `{}`，而不是在 `x` 之前读取的 7。
  没有数字的合规行也会返回 `{}`，而 `parsesCleanly` 就是区分这两种情况的调用。

请使用 `std::istringstream` 的 `>>` 读取每个数字，不要使用 `std::stoi` 或 `std::stoll`。
两个读取函数都需要相同的循环逻辑，因此使用一个用于填充 vector 并返回该行是否合规的 private static 辅助函数可以确保两者保持一致。

### 解答

```cpp
#include <sstream>
#include <string>
#include <vector>

struct Solution {
    static std::string formatPairs(const std::vector<std::string>& keys, const std::vector<int>& values) {
        if (keys.size() != values.size()) {
            return "";
        }
        std::ostringstream out;
        for (std::size_t i = 0; i < keys.size(); ++i) {
            if (i > 0) {
                out << "; ";  // 在除第一个之外的每一项前写入分隔符
            }
            out << keys[i] << '=' << values[i];
        }
        return out.str();
    }

    static bool parsesCleanly(const std::string& line) {
        std::vector<int> numbers;
        return readInts(line, numbers);
    }

    static std::vector<int> parseInts(const std::string& line) {
        std::vector<int> numbers;
        if (!readInts(line, numbers)) {
            return {};
        }
        return numbers;
    }

private:
    // 填充 numbers，并返回该行是否合规
    static bool readInts(const std::string& line, std::vector<int>& numbers) {
        std::istringstream in(line);
        while (true) {
            in >> std::ws;
            if (in.eof()) {
                return true;
            }
            int value = 0;
            if (!(in >> value)) {
                return false;
            }
            numbers.push_back(value);
        }
    }
};
```
