在声明前加上 `const` 会在该名称被初始化时固定其值：

```cpp
const int daysPerWeek = 7;
const double litersPerGallon = 3.785;
```

它们中的每一个都是具名常量：在其下方随处可读，但无法再被赋值。
如果在更下方写上 `daysPerWeek = 8;`，该行将被编译器拒绝。
类似 `const int limit;` 这样的声明也是如此，因为一个永远无法被赋值且从未获得初始值的名称，在程序的其余部分中将没有任何可用内容。
初始化是指定该数值的唯一机会。

被声明为 `const` 并不代表其值必须在何时计算得出。
在函数内部写 `const double half = seconds / 2.0;` 是完全可行的，它是根据只有在程序运行时才存在的参数计算出来的。
`const` 所排斥的只是后续对该名称的赋值。

### 此转换所需的两个六十

- 一个名为 `seconds` 的 `int` 传入 `hoursFromSeconds`，返回一个 `double`，而返回的这个数字是测试唯一读取的内容。
- 初始代码中已经包含 `const int secondsPerMinute = 60;`。
  在其旁边添加 `const int minutesPerHour = 60;`，然后用 `secondsPerMinute * minutesPerHour` 初始化 `secondsPerHour`。
  直接输入字面量 `3600` 是被禁用的，因此除数必须通过计算构建而不是直接写出，并且会逐字比对乘积：如果命名了第二个六十，却使用折叠后的 `60 * 60` 进行除法，将不符合规则要求。
- `secondsPerHour` 保持为 `const double`。
  两个 `const int` 值相乘得到一个 `int`，而将该乘积保存在 `double` 中，使得 `seconds / secondsPerHour` 成为 `double` 与 `int` 之间的除法运算，因此 5400 秒会返回 `1.5` 而不是 `1`。
- `seconds` 可以为零或负数，两者都不会被拒之门外：0 返回 `0`，-3600 返回 `-1`。
- 此处禁用了 `static_cast`。
  第 3.4 课使用了 `static_cast<double>` 来强制在两个 `int` 值之间进行除法，这种方法依然有效；但本练习需要另一种方式，即除数本身已经被你命名并声明为 `double`，因此在除法运算时无需进行任何转换。

### 解答

```cpp
struct Solution {
    static double hoursFromSeconds(int seconds) {
        // 再为一小时的分钟数命名，并用两个常量的乘积得到每小时的秒数
        const int secondsPerMinute = 60;
        const int minutesPerHour = 60;
        const double secondsPerHour = secondsPerMinute * minutesPerHour;
        return seconds / secondsPerHour;
    }
};
```
