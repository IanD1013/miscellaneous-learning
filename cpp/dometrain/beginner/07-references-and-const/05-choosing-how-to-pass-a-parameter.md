三个参数，三种不同的答案，而决定每一个参数的都是相同的两个问题：函数是否必须修改调用者的对象？实参的拷贝代价是否昂贵？

对第一个问题的回答若是“是”，则使用普通引用。
被调用方通过它进行赋值，调用方的变量在调用结束后携带新值。
对第一个问题的回答若是“否”，则由第二个问题来决定。
`std::string` 包含传入给它的文本量，因此仅为了读取而进行拷贝是徒劳无功的，而 `const std::string &` 可以直接绑定到调用者的字符串，同时 `const` 保证不会对其进行修改。
`int`、`double`、`char` 或 `bool` 只有几个字节大小，因此按值拷贝传入即可。

```cpp
static void addOne(int &counter) {
    counter = counter + 1;
}

static std::string repeated(const std::string &text) {
    return text + text;
}

static int tripled(int value) {
    return value * 3;
}
```

`addOne` 修改了调用者的对象，因此其形参是一个引用。
`repeated` 读取其字符串且不进行任何拷贝，因此是一个常量引用。
`tripled` 读取一个较小的数字，因此是按值拷贝。
在阅读任何函数体之前，每一行代码就已经展示了其选择：按值传递、按引用传递还是按常量引用传递。

有两种不良习惯会导致错误。
引用并不是一种性能加速设置：在函数仅用于读取的形参上使用 `int &`，表明了可能会发生修改但实际上从未发生。
而 `const int value` 并不能对调用方提供任何保护，因为实参在函数开始执行前就已经被拷贝了；这里的 `const` 仅仅是阻止函数重新给自己的副本赋值。

### 三个函数签名

- `totalDoubledOnMatch` 会根据其返回的 `int` 进行评分，且已经为你编写完毕：`int total = start;` 初始化局部变量，`addTo(total, amount)` 改变它，`sameText(first, second)` 进行判断，`doubled(total)` 替换它，最后将 `total` 返回给评分系统。
  该初始化行以及所有三个函数调用均保持原样：若驱动代码直接以 `start + amount` 开头、自行比较字符串或直接乘以 2，都将被禁止。
- `addTo` 返回 `void`，因此它的形参是将其处理结果传出函数的唯一途径。
  将 `int running` 修改为 `int &running`，并在该辅助函数的函数体中执行相加操作，写作 `running += amount;` 或 `running = running + amount;`。
  负的 `amount` 会执行减法；`amount` 为 0 则保持总数不变。
- `sameText` 保持 `const std::string &left` 和 `const std::string &right`，并返回 `left == right` 的结果。
  禁止以传值方式拷贝任意一个参数。
  两个空字符串包含相同的文本，因此这一对会触发翻倍。
- `doubled` 接受一个 `int` 并返回 `value * 2`。
  其形参保持为普通的 `int`：在其前面添加 `&` 或 `const` 将被禁止。

按上述说明键入这三个函数体：判定规则依赖于字符 `running +`、`left ==` 和 `value *`。

手动推导最后一个测试用例：`start` 为 -3，`amount` 为 -2，且两个字符串相等时，返回值应为 -10，只有当 amount 在翻倍读取之前已作用于驱动函数的局部变量时，才会得到此结果。

### 解答

```cpp
#include <string>

struct Solution {
    static void addTo(int &running, int amount) {
        // 把 amount 加到调用方自己的累计总数上
        running += amount;
    }

    static bool sameText(const std::string &left, const std::string &right) {
        return left == right;
    }

    static int doubled(int value) {
        return value * 2;
    }

    static int totalDoubledOnMatch(int start, int amount, const std::string &first, const std::string &second) {
        int total = start;
        addTo(total, amount);
        if (sameText(first, second)) {
            total = doubled(total);
        }
        return total;
    }
};
```
