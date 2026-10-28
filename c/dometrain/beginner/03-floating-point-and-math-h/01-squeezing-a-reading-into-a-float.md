测量记录仪接收到一个高精度的距离，并将其存储在一种较旧的、较低精度的格式中。
`survey_roundtrip` 通过返回存储的读数使这种精度损失变得可见。

参数声明为 double 类型参数，因此 `meters` 传入时具有 `double` 精度。
`double` 保留的有效数字比 `float` 更多；float 通常大约保留 7 位有效数字。
在 `float stored = meters;` 中，声明创建了 `stored`，而初始化器提供了它的初始值。
这就是初始化。
后续的赋值则是一个单独的语句，用于修改已经声明的变量，而本练习不需要这样做。

从 double 参数进行初始化会执行窄化转换（narrowing）：float 会保留最接近的可表示值并丢弃多余的细节。
从返回值类型仍为 `double` 的函数中返回该局部变量。
将存储的 float 转换回 double 会赋予它一个更宽的容器，但无法重构丢失的数字。

测距仪报告的范围为 0 到 10000 米，这完全在 `float` 可以容纳的范围内，因此这里不会发生溢出。
评分系统会检查高精度数值、干净的二进制半值、刚好低于 10 千米的读数以及零。
强制标记规则要求学员代码中包含 `float`。
请勿添加四舍五入、类型转换（cast）或文本格式化；所观察到的变化直接来自于初始化 float 存储。

### 解答

```c
#include <stdio.h>

double survey_roundtrip(double meters) {
    // 让读数经过一个 float 变量，并返回取回的值
    float stored = meters;
    return stored;
}
```
