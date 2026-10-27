取余运算符 `%` 用于返回除法未能整除的部分。
它与其它算术运算符一样作用于两个整数操作数，并将剩余部分作为 `int` 返回：

```cpp
int total = 17;
int groupSize = 5;

int wholeGroups = total / groupSize;  // 3
int leftover = total % groupSize;     // 2
```

这两行代码构成了同一个答案的两个部分。
17 可以分出 3 个完整的 5，而 2 则是无法再组成一个完整组的剩余部分。
将 3 乘以 5，再加上 2，结果正好回到 17，这正是 `%` 所定义并保持的关系。

这个符号是百分号的一种不同用途。
`total % 5` 与“百分之五”毫无关系。
它将 `total` 按每组 5 进行拆分，并返回无法成组的剩余部分。
两边的操作数都必须是整数，该运算符无法对 `double` 类型进行编译。

### 负数 total 保留其符号

`-17 / 5` 的结果是 -3，因为除法是向零截断，而不是向下取整到 -4。
因此，余数必须能够配合该商重构出 total：-3 组 5 是 -15，而 -15 加上 -2 得到 -17，所以 `-17 % 5` 是 -2。
计算结果始终带有左操作数的符号，而绝不会带有右操作数的符号。

编写函数 `leftoverOf`，它依次接收 `total` 和 `groupSize` 并返回一个 `int`：即 `total` 被分成大小为 `groupSize` 的组后剩余的部分。
它接收的 `total` 范围从 -1000 到 1000（包括 0 以及小于组大小的总数），`groupSize` 的范围从 1 到 12。
`groupSize` 绝不会为 0，因此算术运算可直接执行，无需自行编写保护逻辑。
测试仅比对返回值，且该值必须来自 `%`：使用 `total - (total / groupSize) * groupSize` 虽然能用前两课的运算符得出相同的数字，但因跳过了本课所讲的运算符而会被判定为无效。

### 解答

```cpp
struct Solution {
    static int leftoverOf(int total, int groupSize) {
        // 返回取出完整的组之后 total 剩下的部分
        return total % groupSize;
    }
};
```
