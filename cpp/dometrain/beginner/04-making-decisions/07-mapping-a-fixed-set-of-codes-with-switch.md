当需要将一个值与一组固定的精确代码列表进行比较时，`switch` 可以通过单条语句来实现，直接跳转到匹配标签下的语句执行。

```cpp
static int sideCount(char shape) {
    int sides = 0;
    switch (shape) {
        case 't':
        case 'T':
            sides = 3;
            break;
        case 's':
            sides = 4;
            break;
        default:
            sides = -1;
            break;
    }
    return sides;
}
```

括号中的值是控制表达式，在进行任何比较之前计算一次。
每个 `case` 标签都带有一个编译器已知的单个常量，因此字符字面量或整数适合放在那里，而变量则不能；并且一个标签代表一个精确的值，而不是一个范围。
只有整数和字符值才能以这种方式进行匹配，这也是为什么文本仍然需要使用比较运算符的原因。
`default:` 负责处理没有标签认领的所有其他值。

`break;` 会结束 switch 并将控制权转移到其闭合大括号之后的语句。
如果省略它，就会发生贯穿（fallthrough）：控制权会继续进入下一个标签的语句中，并悄悄覆盖刚才赋予的值。
堆叠标签是有意利用这一特性的做法，例如 `case 't':` 直接位于 `case 'T':` 上方且它们之间没有任何内容，这样两个代码就可以共享同一个主体。
而主体中间遗漏的 `break;` 则是意外错误，并且不会有编译错误来阻止你。

填写 `romanDigitValue(char symbol)`，使其针对 `'I'` 和 `'i'` 返回 1，针对 `'V'` 和 `'v'` 返回 5，针对 `'X'` 和 `'x'` 返回 10。
任何其他符号（包括 `'Z'` 和数字字符 `'0'`）都应返回 `-1`（第 4.5 课中记录的失败值），并且必须通过 `default:` 返回。
初始代码已在 switch 上方声明了 `int value = 0;` 并在下方将其返回，因此每个分组都应为 `value` 赋值然后 break，而 `default:` 是写入 `-1` 的唯一地方。
你的答案必须保留 `switch`、`break` 和 `default`，初始代码已经在页面上为你提供了这三者。

## 解答

```cpp
struct Solution {
    static int romanDigitValue(char symbol) {
        int value = 0;
        switch (symbol) {
            case 'I':
            case 'i':
                value = 1;
                break;
            case 'V':
            case 'v':
                value = 5;
                break;
            case 'X':
            case 'x':
                value = 10;
                break;
            default:
                value = -1;
                break;
        }
        return value;
    }
};
```
