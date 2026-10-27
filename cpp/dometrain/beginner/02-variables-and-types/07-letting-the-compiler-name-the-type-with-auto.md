编译器可以为你指定变量的类型。
在原本写类型的地方写上 `auto`，类型就会从初始化表达式中推导得出：

```cpp
auto count = 3;
std::string label = "beta";
auto name = label;
```

`count` 的类型是 `int`，因为 `3` 是一个整数字面量；`name` 是 `std::string`，因为 `label` 本身就是该类型。
类型在编译时确定并固定到变量上，之后任何操作都无法改变它。
由于类型是从初始化表达式读取的，因此没有初始化表达式的 `auto` 会让编译器无从推导，从而导致文件无法编译。

### 推导结果与预期不符的情况

`auto` 遵循的是初始化表达式，而不是你对变量的预设意图。
双引号中的文本会被推导为 `const char *`（即字符串字面量底层的类型），而不是 `std::string`，因此这些声明会导致拼接它们的语句报错：

```cpp
auto opener = "[";
auto closer = "]";
auto pair = opener + closer;
```

字符与整数相加会被推导为 `int`，因为该算术运算产生的是一个数值。
这两种情况的修复方法相同：在需要特定类型的地方明确写出该类型。

### 拼接三个部分

`labelWithShiftedChar` 返回 `label`，后接一个冒号，再接一个字符（其字符编码为 `code + shift`）。
当输入为 `alpha`、97 和 1 时，结果为 `alpha:b`。
结果中不应包含任何空格。
`shift` 可以为正数、零或负数，且每个评测用例中偏移后的编码都会对应一个可打印的数字或字母。
允许 label 为空，因此在前面没有任何内容的情况下输入 48 和 5 会得到 `:5`，并且 label 中的多字节文本会原样保留。
你的文件中必须至少有一个声明使用 `auto` 编写，拼接后的文本适合使用 `auto`，因为其初始化表达式已经确定了类型。
偏移后的字符则相反，应明确写为 `char`：`code + shift` 会被推导为 `int`，而 `std::string` 和 `int` 之间没有定义 `+` 运算符，因此在此处使用 `auto` 会导致拼接操作无法编译。

### 解答

```cpp
#include <string>

struct Solution {
    static std::string labelWithShiftedChar(const std::string &label, char code, int shift) {
        // 构建答案：label，分隔符，然后是偏移后的字符
        auto prefix = label + ":";
        char shifted = code + shift;
        return prefix + shifted;
    }
};
```
