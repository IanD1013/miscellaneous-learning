大括号初始化（Brace initialization）会在结构体变量创建时为其赋值。
列表位于变量名之后，每个成员对应一个值，并按照成员声明的顺序进行匹配。

```cpp
struct Span {
    int start;
    int length;
};

int firstIndex = 4;
Span span{firstIndex, 9};
firstIndex = 100;
```

`span.start` 获取第一个值，因为 `start` 是声明的第一个成员，而 `span.length` 获取第二个值。
每个成员对应一个值，按位置匹配，绝不会按提供该值的变量名称匹配，因此 `Span span{9, firstIndex}` 同样可以顺利编译，但含义完全不同。

这些值是在那一刻被复制进去的。
之后将 `firstIndex` 设置为 100，`span.start` 依然为 4，因为该成员保存的是副本，而不是对提供该值的变量的引用。

初始代码为你提供了一个原样返回 `value` 的 `clampToRange`。
传入的三个参数为 `int value`、`int low` 和 `int high`，返回结果为一个 int。
编译器不接受 `Range.low`，因为点运算符（dot）左侧需要一个变量。

### 需求

- 自行在一行内声明 `Range`，将变量命名为 `range`，并使用大括号列表将 `low` 填入第一个成员，将 `high` 填入第二个成员。
- 位于范围内或等于任意一端的值原样返回。
- 小于 `range.low` 的值返回 `range.low`，大于 `range.high` 的值返回 `range.high`。
  你的解答中必须同时出现对这两个成员的读取。
- 两端相等会将所有内容固定为一个数字：当 low 为 3 且 high 为 3 时，任何值都会返回 3。
- `std::clamp(` 已被禁用。
- low 大于 high 时不表示任何数字。
  针对这种情况，请原样返回 `value` 而不是返回失败值，因为区间限定的结果可以是任意 int，没有空闲的值可以用来表示无解。
  先将两端调换回正确顺序是另一种不同的功能：若 low 为 9 且 high 为 2，它会将值 1 提升至 2，而此时正确答案应为 1。

### 解答

```cpp
struct Range {
    int low;
    int high;
};

struct Solution {
    static int clampToRange(int value, int low, int high) {
        // 用大括号列表构建 Range，读取成员后决定返回哪个值
        Range range{low, high};
        if (range.low > range.high) {
            return value;
        }
        if (value < range.low) {
            return range.low;
        }
        if (value > range.high) {
            return range.high;
        }
        return value;
    }
};
```
