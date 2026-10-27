当函数进行除法运算时，会有两个事实发生冲突。
每个 `int` 都可能是正确的商，其中包括 0，因为 `0 / 4` 和 `3 / 5` 的结果都是 0。
分母为 0 则根本没有商，而且 C++ 将除以 0 视为未定义行为：换一个编译器可能就会直接终止程序。
此执行引擎恰好会返回 0 并继续运行，这也是为什么要在除法之前检查分母，而不是在除法之后检查。
第 4.5 课中的哨兵值仅在某些值不可能出现时才有效，而在这里任何值都是可能的。

因此，答案本身与“是否存在有效答案”的信息是分开传递的：

```cpp
static bool tryHalf(int total, int &result) {
    if (total < 0) {
        return false;
    }
    result = total / 2;
    return true;
}

int half = 0;
bool ok = tryHalf(9, half);
```

`int &result` 是一个引用参数，函数向其写入而不是从中读取；以这种方式使用时，它被称为输出参数（out-parameter）。
调用方声明它，将其传入，并在调用后读取它。
在执行这两行代码之后，`ok` 为 `true`，`half` 为 4。

返回的 `bool` 表示状态。
`tryHalf` 在成功时返回 true，在无法计算时返回 false，而且其文档约定的规范还补充了一条：返回 false 时不对 `result` 做任何修改。
该约定也是调用方必须先检查状态的原因：如果在 false 之后读取 `half`，得到的只会是调用方预先写入的初始值，却披着答案的外衣。

`tryDivide` 接受 `int numerator`、`int denominator` 和 `int &quotient`。
当 `denominator` 为 0 时不存在商，因此 `return false;` 且不对 `quotient` 写入任何内容。
否则，赋给商并报告成功。
商向零截断，因此 -7 除以 2 得到的是 -3 而不是 -4。

`divideOrFallback` 根据其返回的 `int` 进行评分。
它声明 `int answer = 0`，调用 `tryDivide(numerator, denominator, answer)`，然后根据返回值进行分支：为 false 时 `return fallback;`，为 true 时 `return answer;`。
`fallback` 是调用方传入的自定义数值，可能在一个用例中传入 -1，在另一个用例中传入 99，因此它不是一个固定写入的值。
`bool` 保持为 `tryDivide` 所报告的结果，`return false;` 保持在其无商分支上。
写入操作本身为辅助函数内部的 `quotient = numerator / denominator;`，因为如果测试驱动自行进行除法运算，就根本不会测试引用；相关规则要求使用 `quotient =`（`=` 前带空格）。
两个返回出口保持独立，即 `return fallback;` 和 `return answer;`：如果用 `fallback` 初始化 `answer` 并跳过状态检查，即便碰巧得到相同的数值，原理也是完全错误的。

## 解答

```cpp
struct Solution {
    static bool tryDivide(int numerator, int denominator, int &quotient) {
        // 分母为 0 时没有商，直接报告失败；否则通过 quotient 写回商并报告成功
        if (denominator == 0) {
            return false;
        }
        quotient = numerator / denominator;
        return true;
    }

    static int divideOrFallback(int numerator, int denominator, int fallback) {
        int answer = 0;
        bool ok = tryDivide(numerator, denominator, answer);
        if (!ok) {
            return fallback;
        }
        return answer;
    }
};
```
