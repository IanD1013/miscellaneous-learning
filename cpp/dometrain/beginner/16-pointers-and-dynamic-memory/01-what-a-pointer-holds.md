每个变量都位于内存中的某个位置，该位置就是它的地址。
指针是一种保存地址而非普通值的变量：

```cpp
int count = 4;
int *p = &count;

*p = *p + 10;
```

`int *p` 声明了一个只能保存 `int` 地址的指针，因此它的类型固定为其允许指向的目标类型。
`&count` 是写在变量名前面的取地址运算符（address-of operator），它会生成该变量的地址，这也是 `p` 唯一能被赋予的值类型。
执行完第二行后，`p` 指向了 `count`。

星号有两个互不相关的用途，很容易被混为一谈。
在 `int *p` 中，它属于被声明类型的一部分。
而在 `*p` 中，它是解引用运算符（dereference operator），用于访问存储地址处的对象：`*p` 在表达式内部读取该对象，而 `*p = 14` 则向该对象写入数据。
这三行代码最终让 `count` 保存了 14，尽管 `count` 从未出现在赋值语句的左侧。
这里没有进行任何复制，也没有在任何地方产生第二个 int；只要 `count` 还存在，`count` 和 `*p` 访问的就是同一个对象。

给 `p` 本身赋值则是另一回事。
`p = &other;` 会让指针指向另一个 int，并保持两个 int 原封不动。
只有通过 `*p` 进行的赋值才会改变对应的值。

`differenceAfterStep` 接收 `int first`、`int second`、`int step` 和 `bool addToSecond`，并返回一个 `int`。
声明一个名为 `target` 的 `int *`，当 `addToSecond` 为 `true` 时使其指向 `second`，为 `false` 时指向 `first`；通过 `*target` 而非变量本身的名称将 `step` 加到该局部变量上，并返回 `first - second`。
在构建代码之前会检查三种拼写：`&first` 和 `&second`（标志的每个分支各一个），以及 `*target +`（只有通过星号写入才会生成）。
请将其写为 `*target += step;`。
声明中已经包含了 `*target`，因此仅靠指向指针本身并不能证明任何事情。
`auto` 也被禁用了，因此必须完整写出指针的类型。
`first` 和 `second` 的范围在 -1000 到 1000 之间，`step` 在 -100 到 100 之间，`step` 为 0 是一个普通的输入，不会改变差值。
评测仅检查返回的 int，由于这两个局部变量是贯穿整个调用生命周期的参数，因此你获取的地址在函数返回前始终有效。

## 解答

```cpp
struct Solution {
    static int differenceAfterStep(int first, int second, int step, bool addToSecond) {
        // 让指针指向标志选中的局部变量，再通过指针修改它
        int *target = &first;
        if (addToSecond) {
            target = &second;
        }
        *target += step;
        return first - second;
    }
};
```
