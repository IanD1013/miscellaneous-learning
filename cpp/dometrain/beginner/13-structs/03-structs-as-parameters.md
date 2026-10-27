将整个结构体传递给一个只读取它的函数，是 const 引用的用武之地：

```cpp
struct Box {
    std::string tag;
    int side;
};

static int areaOf(const Box &box) {
    return box.side * box.side;
}
```

参数 `const Box &box` 将名称 `box` 绑定到调用者的 Box 上，因此不会产生任何拷贝，成员也是直接从原对象中读取的。
相反，如果将参数声明为普通的 `Box`，则意味着每次调用时都会拷贝每个成员（包括 `std::string`），而字符串拷贝会复制其拥有的字符。
这种开销正是将结构体传递给只读函数时默认使用 const 引用的原因。

`const` 涵盖整个对象而不仅仅是某一条语句。
`areaOf` 内部的 `box.side = 0;` 会被编译器拒绝，任何会修改成员的调用也是如此，而所有读取操作则保持可用，这就是 `box.side * box.side` 可以编译的原因。

有两个辅助函数属于 `Solution`，且每个函数前面都需要加上 `static`：没有该关键字的成员只能通过对象来调用，而静态入口点内部并不存在对象。

- `static int fahrenheitOf(const Reading &reading)` 转换 celsius 成员：乘以 9，然后除以 5，再加上 32，全部使用 int 进行运算。
  除法会截断小数，因此读数 3 会返回 37 而不是 37.4，-5 则返回 23。
- `static int labelLengthOf(const Reading &reading)` 报告 label 成员包含的字符数。
  `size()` 返回 `std::size_t`，因此请通过 `static_cast<int>` 将其返回，空标签的长度为 0。

两种书写形式被禁止以防止引入拷贝。
`Reading reading)` 排除了按值传递的参数（无论类型前面是否有 `const`），而 `(Reading &` 排除了没有 const 保证的引用。
剩下的形式就是 `const Reading &reading`。

`fahrenheitOfReading` 和 `labelLengthOfReading` 是两个评分入口点，它们各自已经从参数构建了一个 `const Reading`。
让它们分别调用对应的辅助函数并返回结果，写法为 `fahrenheitOf(reading)` 和 `labelLengthOf(reading)`，这样传递的是整个结构体而不是其中的某一个成员。
系统会检查这两种写法，因此请保留名为 `reading` 的局部变量。
任何输入都不会被拒绝：空标签与其他标签一样正常转换，因此没有任何标签的 20 度仍然返回 68。

## 解答

```cpp
#include <string>

struct Reading {
    std::string label;
    int celsius;
};

struct Solution {
    // 两个辅助函数都以 const 引用读取 Reading：一个转换 celsius，一个报告 label 的长度
    static int fahrenheitOf(const Reading &reading) {
        return reading.celsius * 9 / 5 + 32;
    }

    static int labelLengthOf(const Reading &reading) {
        return static_cast<int>(reading.label.size());
    }

    static int fahrenheitOfReading(const std::string &label, int celsius) {
        const Reading reading{label, celsius};
        return fahrenheitOf(reading);
    }

    static int labelLengthOfReading(const std::string &label, int celsius) {
        const Reading reading{label, celsius};
        return labelLengthOf(reading);
    }
};
```
