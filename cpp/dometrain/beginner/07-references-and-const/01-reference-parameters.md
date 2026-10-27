在参数的类型与名称之间添加 `&`，会使该参数成为调用方所传递变量的别名，而不是其副本：

```cpp
void doubleIt(int &n) {
    n = n * 2;
}

int score = 21;
doubleIt(score);
```

在调用之后，`score` 的值为 42。
`n` 从未作为一个内部存有自身 21 的独立变量存在。
在调用期间，它指代的就是调用方的对象，因此 `n = n * 2` 直接写入了 `score`。
以这种方式声明的参数称为引用参数（reference parameter），并且 `&` 与类型紧密相关，因此一个代表调用方 `int` 的名为 `value` 的参数写作 `int &value`。

写入操作是在赋值执行时生效的，而不是在结束的右花括号处，因此函数体中间的 `return` 会保留所有已写入的内容。
在调用点（call site）需要注意两点：实参保持常规形式 `doubleIt(score)`，因为在实参前面加 `&` 代表其他含义，编译器无法将其绑定到引用，从而导致编译失败；实参还必须是已声明的变量，`doubleIt(21)` 会被拒绝，因为字面量无法让被调用方为其附加别名。

初始代码中的 `increaseBy` 声明了 `int value`（一个副本），因此 `applyIncrease` 内部的局部变量未被修改，所有非零增量的测试用例都会返回起始数值。
请将该参数重写为能够修改调用方变量的形式，使声明为 `void increaseBy(int &value, int amount)`。
其背后的检测规则会查找 `increaseBy(int &`（包含此处所示的空格），因此文件中其他位置的 `&` 或写成 `int& value` 都无法满足要求。
其余部分保持不变：`increaseBy` 保留其名称和 `void` 返回类型，调用继续按此顺序传入 `value` 和 `amount`，并且 `applyIncrease` 返回传入的局部变量，而不是自行计算总和。
`applyIncrease` 接收 `int start` 和 `int amount`（每个都在 -1000 到 1000 之间），并在辅助函数处理完毕后返回其局部变量。
当 amount 为 `0` 时原样返回起始值，负数增量则减小数值，评分系统仅读取返回的数字。

## 解答

```cpp
void increaseBy(int &value, int amount) {
    // 通过引用直接修改调用方自己的变量，而不是副本
    value += amount;
}

struct Solution {
    static int applyIncrease(int start, int amount) {
        int value = start;
        increaseBy(value, amount);
        return value;
    }
};
```
