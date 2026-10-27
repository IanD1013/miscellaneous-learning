`while` 会在条件测试为 true 的期间重复执行一段代码块：

```cpp
int n = 3;
while (n > 0) {
    n -= 1;
}
```

圆括号内包含条件，即第 4.3 课所介绍的那种 bool 表达式。
花括号内包含循环体，即重复执行的代码块。
条件会在循环体运行之前进行测试，并且每一次循环（包括第一次）都会进行测试。
当测试结果为 false 时，循环体将被跳过，程序会继续执行闭合花括号后面的代码，因此起始 `n` 为 0 时会执行零次而不是一次。

正常运行的循环的另一半关键是朝着退出条件推进。
条件所读取的内容必须在循环体内发生改变，并且必须朝着使测试为 false 的方向变化。
在上面，每次循环 `n` 都会减一，而 0 保持不变，因此差距每次缩小一，测试在三次循环后变为 false。
如果删掉该减法操作，条件的结果就永远不会改变；编译器不会报错，运行将因 runner 的 20 秒看门狗超时而终止且没有任何结果。

编写 `countDownPasses(int start, int stopAt)`。
它返回将 `start` 递减到 `stopAt` 所需的单步步数，每步计为一次循环，因此 `countDownPasses(10, 0)` 返回 10。
`stopAt` 可以是 0 或负数：`countDownPasses(3, -3)` 返回 6。
`countDownPasses(4, 4)` 返回 0，因为第一次测试就已经失败，而小于其停止值的起始值也出于同样的原因返回 0，无需单独进行检查。
两个 int 都保持在 -100000 和 100000 之间，因此最大跨度的运行会统计 200000 次循环。
你的代码中必须出现 `while` 循环，因为本练习考核的是步数的计数过程，而不是直接计算差值。

## 解答

```cpp
struct Solution {
    static int countDownPasses(int start, int stopAt) {
        // 每把 start 减一就计一次循环，直到它降到 stopAt
        int passes = 0;
        while (start > stopAt) {
            start -= 1;
            passes += 1;
        }
        return passes;
    }
};
```
