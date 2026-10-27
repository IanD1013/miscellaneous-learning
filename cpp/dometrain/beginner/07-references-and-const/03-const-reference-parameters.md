形如 `const std::string &text` 的参数让函数可以读取调用者的字符串，并在执行过程中同时完成两项独立的工作：

```cpp
static std::string shout(const std::string &text) {
    return text + "!";
}
```

`&` 将 `text` 绑定到调用者自己的字符串上，因此无论该字符串有多长，都不会进行拷贝。
`const` 则取消了通过该名称进行写入的权限：在该函数体中执行 `text = "other";` 无法通过编译。
结合在一起，它们保证了“不拷贝”且“不修改”，这就是为什么常量引用参数是函数仅用于读取字符串时的默认选择。
其通用形式为 `const T &name`，其中 `T` 是函数仅读取而从不写入的任意类型。

去掉 `const`，它就会变回函数可以通过其进行赋值的普通引用。
在这里这种形式被规则（而非编译器）所禁止：运行器传入的值是以字面量形式提供的，非 const 引用需要绑定到一个已声明的变量上，否则编译报错会出现在运行测试的文件中，而不是你的代码文件中。

`joinWithFallback` 接收 `label`、`value` 和 `fallback`（均声明为 `const std::string &`），并返回由它们拼接而成的 `std::string`：

- 结果由 label 开始，接着是一个冒号和一个空格 `": "`，然后是 value。
- 空的 `value` 会被替换为 fallback：`"size"`、`""`、`"unknown"` 返回 `size: unknown`。
- “空”严格指 `value == ""`。
  `"0"` 和单个空格都包含一个字符，因此它们都会原封不动地传递到结果中。
- 允许空的 label，此时结果直接以分隔符开头，例如 `: 12`。
- 禁止使用 `.empty()` 和 `.size()`。
  同时也禁止使用传值拷贝的写法（`std::string label`、`std::string value` 和 `std::string fallback`）以及去掉 const 的写法（`std::string &label`、`std::string &value` 和 `std::string &fallback`）：所有三个参数都必须保持初始代码中声明的 `const std::string &` 形式。

## 解答

```cpp
#include <string>

struct Solution {
    static std::string joinWithFallback(const std::string &label, const std::string &value, const std::string &fallback) {
        // 只有当 value 是空字符串时才改用 fallback
        if (value == "") {
            return label + ": " + fallback;
        }
        return label + ": " + value;
    }
};
```
