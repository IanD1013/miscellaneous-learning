根据变量自身当前的值来更新变量的操作非常常见，因此有简写形式。
`value += amount` 会读取 `value`，给它加上 `amount`，然后将结果存回同一个变量中，这相当于简写了 `value = value + amount`：

```cpp
int value = 10;
value += 5;   // 15
value *= 3;   // 45
value /= 4;   // 11，因为 /= 与 / 一样进行截断
value -= 1;   // 10
```

这些都是复合赋值（compound assignment）：算术运算符直接位于 `=` 前面，左侧的变量既是要读取的变量，也是要写入的变量。
它的当前值始终作为左操作数，因此 `value /= divisor` 是将 `value` 除以 `divisor`，绝不会颠倒过来。
右侧的整个表达式在应用运算符之前就会计算完毕，这使得 `value *= factor + 1` 相当于乘以该总和。
颠倒这两个符号会导致不易察觉的隐蔽错误：`value =+ addend` 会被编译为将正的 `addend` 赋给变量的普通赋值，从而直接替换当前运行的值而不是累加。

步进 1 也有自己的简写。
递增运算符 `++` 将变量加 1，而递减运算符 `--` 将变量减 1：

```cpp
int steps = 7;
steps++;   // 8
steps--;   // 7
```

作为单独的一条语句，`steps++;` 等同于 `++steps;`，且两者都等同于 `steps += 1`。
这些写法的区别仅在于表达式本身产生的值，而此处并没有读取该值。

`runningTotal(int start, int addend, int factor, int divisor)` 开头会将 `start` 复制到一个名为 `value` 的 `int` 变量中。
按以下顺序对 `value` 执行四个步骤，然后返回它：使用 `+=` 加上 `addend`，使用 `*=` 乘以 `factor`，使用 `/=` 除以 `divisor`，以及使用 `++` 加一。
因为 `/=` 向零截断，所以当当前值为 -18、除数为 4 时，结果为 -4 而不是 -5。
`factor` 和 `divisor` 都是 1 到 10 之间的 int，因此 `/=` 步骤绝不会遇到除数为 0 的情况，而 `start` 和 `addend` 则介于 -1000 到 1000 之间。

## 解答

```cpp
struct Solution {
    static int runningTotal(int start, int addend, int factor, int divisor) {
        int value = start;
        // 依次对 value 本身应用这四个步骤
        value += addend;
        value *= factor;
        value /= divisor;
        value++;
        return value;
    }
};
```
