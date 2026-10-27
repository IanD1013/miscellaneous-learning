在循环体内部声明总和变量会在每次循环迭代时重新创建它，因此上一次迭代计算出的内容在下一次迭代开始前就会被丢弃。
该变量名在右大括号处也会停止存在，因此写在循环下方的 `return total;` 引用的将是一个已不存在的变量，导致文件无法编译。
相反，累计总和应声明在循环之前：

```cpp
int total = 0;
int value = 1;
while (value <= 3) {
    total += value;
    value += 1;
}
```

在该循环的整个运行过程中只存在一个 `total`，并且 `total +=` 会将值累加到它已有的内容上，而不是替换它。
这种用法的变量称为累加器（accumulator），其初始值为循环执行零次时的结果，对于加法操作来说就是 0。
每次迭代 `value` 增加 1，而上限保持不变，因此在三次迭代后条件不再成立。

### 包含两端边界

编写 `sumRange(int low, int high)`，返回从 `low` 到 `high`（包含 `high`）之间每个 int 的总和。
`sumRange(1, 5)` 返回 15，其中 5 本身也是总和的一部分。
任意一个边界都可以是负数，因此 `sumRange(-3, 2)` 返回 -3。
当 `low` 大于 `high` 时表示一个空范围：条件立即为 false，累加器完全不会被修改，文档规定的返回值为 0，因此无需为此添加额外的保护检查。
边界值在 -1000 到 1000 之间。
在 `while` 循环中计算总和，将每个值累加到累加器中；返回的值就是当条件变为 false 时累加器中保存的值。

### 解答

```cpp
struct Solution {
    static int sumRange(int low, int high) {
        // 把从 low 到 high（包含 high）的每个值累加到 total 中
        int total = 0;
        int value = low;
        while (value <= high) {
            total += value;
            value += 1;
        }
        return total;
    }
};
```
