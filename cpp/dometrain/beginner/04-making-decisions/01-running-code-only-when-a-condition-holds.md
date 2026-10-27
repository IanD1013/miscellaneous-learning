`if` 语句是程序跳过不应执行的操作的方式：关键字、括号内的条件以及大括号内的主体。

```cpp
bool verbose = true;
std::string line = "done";
if (verbose) {
    line = line + " in 12 steps";
}
```

条件会被求值一次，其产生的结果是一个 `bool`。
当该值为 `true` 时，`{` 和 `}` 之间的每条语句都会运行。
当它为 `false` 时，控制流会跳过右大括号并继续执行后面的内容，`line` 则保持原有的文本。
`verbose` 本身就是一个 `bool`，因此在括号中它旁边不需要任何其他内容。
像 `value < 0` 这样的比较也会产生一个 `bool`：当 `value` 小于零时为 `true`，在零或以上时为 `false`，所以比较可以直接放入 `if (` 和 `)` 之间。

大括号将任意数量的语句组合成一个主体。
如果不写大括号，`if` 仅控制紧随其后的那一条语句。
缩进不起任何作用，因此对齐的第二行在每次调用时都会运行。
`)` 和 `{` 之间也不应该有任何内容：`if (value < 0);` 可以通过编译，那个多余的分号会变成一个空主体，而警告在此处不会阻止运行，因此其下方的赋值语句每次都会执行。

完成 `clampNegativeToZero`，它接收一个名为 `value` 的 `int` 并返回一个 `int`。
负数输入（包括 -1）返回 0。
0、1 以及任何更大的数字则原样返回。
起始代码将 `value` 复制到 `result` 并返回它，因此你需要添加的是将 `result` 设置为 0 的代码行，且写在 `if` 主体内部。
在条件不满足的所有路径上，`result` 已经保存了 `value`，这就是为什么在此处编译文件之前就禁止使用 `else` 的原因。
最终比较的是你返回的数字；打印输出不起任何作用。

## 解答

```cpp
struct Solution {
    static int clampNegativeToZero(int value) {
        int result = value;
        // 仅当 value 小于零时，才在 if 主体内将 result 设为 0
        if (value < 0) {
            result = 0;
        }
        return result;
    }
};
```
