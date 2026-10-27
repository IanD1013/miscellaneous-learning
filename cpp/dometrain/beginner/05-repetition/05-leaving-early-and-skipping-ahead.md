有两个语句可以在循环体内部控制循环的执行。
`continue;` 会放弃当前轮次剩余的代码，而 `break;` 则会直接彻底结束循环：

```cpp
for (int n = 1; n <= 5; ++n) {
    if (n == 2) {
        continue;
    }
    if (n == 4) {
        break;
    }
    std::cout << n << "\n";
}
```

控制台会输出两行，分别是 1 和 3。
在 `n` 为 2 的那一轮中，`continue;` 表示跳到下一轮：其下方的打印语句永远不会执行，但循环头部仍然会运行 `++n`（与 `n++` 一样的自增一步），并再次检测 `n <= 5`，因此计数器会继续递增，循环依然会结束。
在 `n` 为 4 的那一轮中，`break;` 表示立即离开循环，并且彻底跳出循环：循环体内位于它下方的任何代码都不会执行，也不会再开启后续的任何轮次，程序将从右大括号后面的第一条语句继续执行。
这就是为什么 `n` 为 5 的轮次从未发生。

`multiplesUntilShared(int firstFactor, int secondFactor, int limit)` 会让 `value` 从 1 遍历到 `limit`（包含 `limit`），并统计它遇到的 `firstFactor` 的倍数个数。
一旦这些倍数中某一个也能被 `secondFactor` 整除，当时的累计计数就是答案。
如果达到了 `limit` 仍未找到共享的公倍数，则返回 -1；任何因子或限制小于等于 0 的调用也会返回 -1。
已经为你准备好了四部分内容：防护检测、递增 `value` 的 `for` 循环头部、计数器 `checked` 以及第 3.3 节中的余数测试 `value % firstFactor != 0` 和 `value % secondFactor == 0`。

循环体内的两个关键字位置放反了。
不能被第一个因子整除的数值根本不是倍数，因此在增加 `checked` 之前必须放弃当前轮次，同时扫描继续进行。
能被两个因子同时整除的数值就是答案，因此其后无需再检查任何内容。
`multiplesUntilShared(3, 4, 30)` 的结果是 4：统计的倍数是 3、6、9 和 12，而 12 是其中第一个也能被 4 整除的数。
`multiplesUntilShared(2, 5, 100)` 的结果是 5，因为 10 是第 5 个偶数，而不是第 10 个数值。
`multiplesUntilShared(4, 6, 10)` 的结果是 -1，因为 `value` 超出了限制仍未找到共享倍数。
如果第一个倍数就符合条件，则计数为 1，因此 `multiplesUntilShared(7, 7, 7)` 为 1。
当这两个词放在正确的位置后，`continue` 和 `break` 都会保留在最终的代码体中。

## 解答

```cpp
struct Solution {
    static int multiplesUntilShared(int firstFactor, int secondFactor, int limit) {
        if (firstFactor <= 0 || secondFactor <= 0 || limit <= 0) {
            return -1;
        }
        int checked = 0;
        int answer = -1;
        for (int value = 1; value <= limit; ++value) {
            // 不是第一个因子的倍数就跳过本轮，找到共享倍数就结束循环
            if (value % firstFactor != 0) {
                continue;
            }
            checked += 1;
            if (value % secondFactor == 0) {
                answer = checked;
                break;
            }
        }
        return answer;
    }
};
```
