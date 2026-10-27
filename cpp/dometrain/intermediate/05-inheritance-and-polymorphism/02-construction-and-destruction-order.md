trace.hpp 中的每个 `Part` 在构造时都会将 `+` 及其名称追加到一个共享记录中，并在析构时追加 `-` 及其名称。
运行初始代码，单台机器的情况会返回 `+Frame+Motor+Sensor-Sensor-Motor-Frame`。
构造函数的成员初始化器列表中，`sensor_` 写在 `motor_` 之前，但 Motor 部件却先被构建：成员是按照声明顺序初始化的，也就是它们在类中出现的顺序。
该列表仅提供每个成员的构造函数参数（`Part` 不能在没有名称的情况下构建），编译器在接受顺序不同的列表时不会报错。
一旦某个成员的构造函数使用了另一个成员，顺序就变得至关重要，此时被使用的成员必须声明在前面。

### 派生类对象的构造顺序

构建 `Machine` 始终遵循相同的构造顺序：

1. 基类部分，通过初始化列表指定的基类构造函数 `Part("Frame")`；
2. 成员变量，按照声明顺序；
3. `Machine()` 的函数体。

当函数体运行时，基类部分和两个成员都已存在，因此在函数体中记录的条目会排在所有这些条目之后。
析构顺序则完全相反。
`~Machine()` 的函数体最先运行，此时每个部分都仍然有效，然后成员按照与声明相反的顺序（从最后声明的到最先声明的）依次析构，基类部分最后析构。
这就是为什么初始代码的记录以 `-Sensor-Motor-Frame` 结尾：因为 `sensor_` 是最后声明的。

### `Machine` 类

修改 `machine.hpp` 中的 `Machine`，使其满足以下要求：

- 它仍然是一个基类部分名为 `"Frame"` 的 `Part`。
  `driver.cpp` 会在期望 `const Part&` 的地方传入一个 `Machine`，并通过它读取名称。
- 它包含两个分别名为 `"Sensor"` 和 `"Motor"` 的 `Part` 成员，并且 Sensor 部件在 Motor 部件之前构造。
  它们的记录条目来自它们自己的构造函数和析构函数，而不是来自 `mark`。
- 它的构造函数体记录 `"+Machine"`，其析构函数体记录 `"-Machine"`。
  `mark(entry)` 是 `Part` 的公共静态成员，用于将任意文本追加到记录中，因此 `Machine` 可以直接调用它。

这样一台机器就会生成记录 `+Frame+Sensor+Motor+Machine-Machine-Motor-Sensor-Frame`。

`driver.cpp` 中的 `Solution::buildRecord(machines)` 返回对应数量相互嵌套的机器所产生的记录：一个辅助函数创建一个 `Machine`，并在该机器存活期间调用自身来创建下一个机器。
`buildRecord(2)` 返回一个字符串，在此处按照每台机器条目的起始和结束进行了拆分展示：

```text
+Frame+Sensor+Motor+Machine   外层机器构造完成
+Frame+Sensor+Motor+Machine   内层机器构造完成
-Machine-Motor-Sensor-Frame   内层机器析构完成
-Machine-Motor-Sensor-Frame   外层机器析构完成
```

对于 0 台机器，记录为空字符串。
`Solution::baseNameAndLiveParts()` 构建一台 `Machine`，并在其存在期间返回其基类部分的名称和当前存活的 `Part` 对象数量，以空格分隔：`"Frame 3"`。

### 解答

```cpp
#pragma once
#include "trace.hpp"

class Machine : public Part {
public:
    Machine() : Part("Frame"), sensor_("Sensor"), motor_("Motor") { mark("+Machine"); }
    ~Machine() { mark("-Machine"); }

private:
    // 成员按声明顺序构造：sensor_ 先于 motor_
    Part sensor_;
    Part motor_;
};
```
