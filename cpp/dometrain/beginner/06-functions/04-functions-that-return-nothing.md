有些函数不需要返回任何内容。
在返回类型的位置写上 `void` 正好表达了这层含义，并且编译器也会严格按此执行。

```cpp
static void printTimes(int count) {
    if (count <= 0) {
        return;
    }
    std::cout << count << " times\n";
}
```

`static void` 就像 `static int` 一样开启函数定义，其中 `void` 代表该函数不需要使用的返回类型。
在函数内部，`return;` 关键字后面不带任何内容，仅表示直接退出。
执行到闭合大括号时也会以相同的方式结束函数，因此 `void` 函数体完全不需要 `return`。
这种形式的函数调用是为了其副作用（effect）：它的调用本身就是一条独立的语句，不能放在 `=` 的右侧或输出链中，因为没有任何值会返回来替代它。
`printTimes` 所实现的效果，完全是通过 `std::cout` 来完成的。

初始代码中的 `printLabelledValue` 声明了两个参数，第一个是标签，第二个是 `int`，其函数体需要由你来编写：标签，然后是一个冒号，接着是一个空格，然后是数值，最后是 `"\n"`。
该辅助函数会根据其输出的单行内容进行评分，因此标签 `Total` 与数值 12 输出到控制台时必须为 `Total: 12`。
`printLabelledPair(int first, int second)` 会调用它两次，依次为 `first` 传入 `First`，为 `second` 传入 `Second`。
对于 7 和 4，控制台最终应显示：

```makefile
First: 7
Second: 4
```

捕获的输出会逐字符进行比对，因此 `First` 和 `Second` 中的大写字母、冒号以及其后的单个空格都很关键。
第一行末尾的 `"\n"` 是让 `Second` 换到下一行的关键。
最后一个值后面的换行符在两份文本比对前会被裁剪（trim），它本身并不起决定作用，但以相同的方式编写每一行是确保第一行格式正确的最稳妥方式。
一对零和一个负数也按完全相同的布局打印。
`printLabelledValue` 应保留在 `struct Solution` 之外，即初始代码放置它的文件顶部。
有一项评分调用会直接通过该独立名称访问辅助函数，如果将其定义藏在结构体内部将无法响应调用，从而导致报错指向你正在编辑的文件之外的某一行。
运行器自带 `main` 函数并从那里启动每个测试用例，因此本文件绝不能声明 `main`。

## 解答

```cpp
#include <iostream>
#include <string>

static void printLabelledValue(std::string label, int value) {
    // 输出一行：标签、冒号、空格、数值，最后换行
    std::cout << label << ": " << value << "\n";
}

struct Solution {
    static void printLabelledPair(int first, int second) {
        // 先为第一个值调用辅助函数，再为第二个值调用一次
        printLabelledValue("First", first);
        printLabelledValue("Second", second);
    }
};
```
