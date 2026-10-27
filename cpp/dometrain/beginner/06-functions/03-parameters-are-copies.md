给形参赋值看起来似乎会修改调用方传入的变量。
但事实并非如此。
当函数调用发生时，实参的值会被复制到形参中，从那一刻起，形参就只是一个属于被调用函数的普通变量。

```cpp
static int shrink(int amount) {
    amount = amount - 1;
    return amount;
}
```

在调用方中写入 `int size = 10;` 并在其下方写入 `int smaller = shrink(size);`：`smaller` 最终为 9，而 `size` 依然保持为 10。
`amount` 是用 `size` 中保存的值的副本初始化的，因此 `shrink` 内部的赋值只会修改该副本并止步于此。
这就是按值传递（pass by value），类型对这一机制没有任何影响，因为 `int`、`double` 和 `std::string` 形参同样都是副本。
函数调用传回给外部的只有返回值，因此调用方必须保存接收到的返回值。

`tripleValue` 接收一个名为 `value` 的 `int`。
将 `value` 的三倍重新赋值给 `value`，然后返回 `value`。
`gapAfterTripling(int start)` 将 `start` 传递给 `tripleValue`，用它自己的一个变量保存返回的数字，并返回 `start` 减去该数字的结果。
函数调用不会影响 `start` 本身，因此结果就是 `start` 减去 `start` 的三倍：5 得到 -10，0 得到 0，-7 得到 14（因为 -7 的三倍是 -21）。
`start` 的范围始终在 -1000 到 1000 之间，并且 `tripleValue` 本身也会被单独评分，因此如果该辅助函数只是原样返回传入的值，在计算差值之前就会判定失败。
请将 `tripleValue` 保留在 `struct Solution` 的上方（即起始代码所在的位置）。
评测程序会直接调用该独立函数名，若将定义移动到 struct 内部将无法访问，由此产生的编译错误会报告在你从未写过的代码行上。
此外也不要编写 `main` 函数：运行器已经提供了一个，重复定义会在执行任何测试用例之前导致构建失败。

## 解答

```cpp
static int tripleValue(int value) {
    // 把 value 的三倍赋回给 value，然后返回 value
    value = value * 3;
    return value;
}

struct Solution {
    static int gapAfterTripling(int start) {
        // 调用 tripleValue 并保存返回值，再返回 start 减去该值的结果
        int tripled = tripleValue(start);
        return start - tripled;
    }
};
```
