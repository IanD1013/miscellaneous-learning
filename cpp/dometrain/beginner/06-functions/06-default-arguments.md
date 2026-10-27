参数可以带有一个默认值，当调用者省略该实参时，编译器会提供该值。
该值在形参列表中用 `=` 表示：

```cpp
static int shifted(int value, int offset = 1) {
    return value + offset;
}
```

`shifted(4, 3)` 按照普通方式返回 7。
`shifted(4)` 返回 5：该调用只提供了一个实参，`value` 接收 4，而 `offset` 采用写在其旁边的 1。
所写入的值是默认实参（default argument），它属于函数的声明，而不是任何调用。
因此，`shifted(4, 1)` 和 `shifted(4)` 构建出相同的调用。

哪个参数可以带有默认实参取决于实参是按位置进行匹配的。
调用唯一能省略的实参是位于末尾的那些，因此默认值必须位于末尾的形参上，并且在带有默认值的形参之后的每一个形参也都必须有自己的默认值。
`static int shifted(int offset = 1, int value)` 无法通过编译。
写入的值本身也是独立的：它不能引用另一个形参的名称，因此默认值无法通过 `value` 计算得出。
它在定义本身中声明一次。

### 提前结束的调用

`countDigits(int value, int base = 10)` 返回当 `value` 用 `base` 进制表示时所拥有的位数。
保持起始代码中的形参列表不变，并在 `base` 上保留 `= 10`：一些用于评分的调用会传递两个实参，而一些只会传递一个。

- `countDigits(1000)` 为 4，`countDigits(255, 16)` 为 2，而 `countDigits(255, 2)` 为 8。
- `countDigits(0)` 为 1。
  零在任何进制下都只占一位数，因此按要求其答案为 1。
- 小于 0 的 `value` 或小于 2 的 `base` 返回 -1。
  在进行任何除法之前先检查这两个条件，这也可以防止基数为 1 时陷入死循环除法。
- 计数的具体做法是：计数从 1 开始，将 `value` 除以 `base` 一次，然后在剩余值大于 0 时继续相除，并在每一轮中将计数加 1。
  整数除法会舍去小数部分，正是这一机制让剩余值逐步递减至 0。
- 可计数的 `value` 范围为 0 到 2000000000，可用的 `base` 范围为 2 到 36；评分调用还会传入负的 `value` 以及为 1 的 `base`。

总共有六个评分调用会访问此函数，其中三个调用仅写入 `value`。
测试运行器会从其自带的 `main` 发起所有六个调用，如果在这里添加第二个 `main` 会导致编译失败。

### 解答

```cpp
struct Solution {
    static int countDigits(int value, int base = 10) {
        // 先拒绝没有位数可言的输入，再不断除以进制直到剩余值为 0
        if (value < 0 || base < 2) {
            return -1;
        }
        int digits = 1;
        value /= base;
        while (value > 0) {
            value /= base;
            digits += 1;
        }
        return digits;
    }
};
```
