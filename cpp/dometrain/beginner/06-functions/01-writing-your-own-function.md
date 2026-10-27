函数定义由四个部分组成，并且它们按固定顺序出现：返回值的类型、函数名、括号中的参数列表，以及花括号中的函数体。

```cpp
static int rangeWidth(int low, int high) {
    int width = high - low;
    return width;
}
```

最前面的 `int` 是返回类型，因此函数体内的每个 `return` 都必须产生一个 `int`。
`rangeWidth` 是函数名。
`(int low, int high)` 是参数列表：包含两个参数，每个参数都写成类型后跟名称的形式，并用逗号隔开。
花括号 `{` 和 `}` 包裹着函数体，而 `return width;` 会在此处立即结束函数并将该值返回。
写在任何花括号外部的定义前面的 `static`（如 `rangeWidth`）将该名称的作用域限制在其所在的文件内。
而在 `struct Solution` 内的 `totalSeconds` 上的 `static` 则是该关键字的另一项职责：它标记了一个无需预先构建任何实例即可运行的函数，这也是运行器能够启动它的原因。

你可以自行选择参数名称。
`low` 和 `high` 是仅在 `rangeWidth` 运行期间存在的变量，外部代码无法知晓它们的名称。
参数列表中的顺序决定了传入的值赋给哪个名称：运行器会按照从左到右的顺序将持有的值填充到各个参数中。
重命名这两个参数，函数的行为依然相同；但如果颠倒它们的顺序，减法运算的方向就会搞错。

请填写 `totalSeconds`。
它接收 `(int minutes, int seconds)` 并返回一个 `int`，将这两个值合并为总秒数：将分钟数乘以 60 并加上秒数。
2 和 30 得出 150，0 和 45 得出 45，0 和 0 得出 0。
所有输入均有效，因此 -2 和 -30 经过相同的运算会得到 -150。
评测仅比对返回的 `int`，因此向 `std::cout` 发送任何内容都不会改变任何结果，且 `main` 依然由运行器管理。

## 解答

```cpp
struct Solution {
    static int totalSeconds(int minutes, int seconds) {
        // 把分钟换算成秒再加上剩余的秒数
        return minutes * 60 + seconds;
    }
};
```
