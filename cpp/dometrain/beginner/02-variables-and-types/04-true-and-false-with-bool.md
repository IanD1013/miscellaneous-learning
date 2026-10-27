比较运算会产生一个 `bool`，而 `bool` 的值只能是 `true` 或 `false`。
之后无需进行任何转换，因为比较运算的结果已经落在这两者之一了。

```cpp
bool ready = 3 > 1;
return ready;
```

在存储任何内容之前，`3 > 1` 计算出的结果为 `true`，而 `ready` 保存了该值。
返回的 `bool` 传给评分程序时会打印为 `true` 或 `false`，绝不会是 `1` 或 `0`，并且声明返回 `bool` 的函数可以直接返回比较表达式的结果，而无需中间变量。

`isPositive(int value)` 返回一个 `bool`，当 `value` 大于零时返回 `true`。
使用大于号将 `value` 与 `0` 进行比较，并返回该比较结果。
这里禁用了 `if` 和 `?`，因为在两条独立路径上选择 `true` 和 `false` 是在重复进行比较运算已经完成的工作。

边界条件是本练习的重点。
零不是正数，因此针对 `0` 的用例期望得到 `false`，如果测试写成大于或等于零，则会使这单个用例失败，而其他三个用例仍然通过。
`5` 返回 `true`，`-7` 返回 `false`，而 `2147483647`（该目标平台上 `int` 能容纳的最大值）返回 `true` 的原因与 `5` 相同。
直接返回 `value` 本身又是另一种不同的结果：每个非零数值都会报告为 `true`，其中包括负数。

## 解答

```cpp
struct Solution {
    static bool isPositive(int value) {
        // 将 value 与 0 比较，并返回比较结果
        return value > 0;
    }
};
```
