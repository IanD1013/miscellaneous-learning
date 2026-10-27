`enum class` 声明了一个新类型，其值是一组固定的名称列表，称为枚举项（enumerator）：

```cpp
enum class Direction { North, East, South, West };

Direction facing = Direction::North;
```

枚举项的作用域限定在该类型内部：代码中需写为 `Direction::North`，而单独的 `North` 是未声明的标识符。
`Direction` 也绝不会自动转换为 `int`，因此 `facing + 1`、`facing == 0` 以及将 `facing` 传递给 `int` 参数都会导致编译错误。
而没有加 `class` 声明的普通 `enum` 则允许上述所有操作：其名称会溢出到外围作用域中，且其值会静默转换为 `int`。
在针对 `Direction` 的 `switch` 中，case 标签为带作用域的名称，如 `case Direction::North:` 等。

### 枚举项的值与底层类型

每个枚举项仍然具有一个整数值。
像这里这样没有显式列出值时，它们按顺序从 0 开始计数：`North` 为 0、`East` 为 1、`South` 为 2、`West` 为 3。
你只能通过显式编写的类型转换来获取该数字。
`static_cast<int>(facing)` 用于读取它，而 `static_cast<Direction>(n)` 可以从数字构造一个 `Direction`。
后一种转换不进行任何检查：`static_cast<Direction>(7)` 可以通过编译并生成一个与这四个名称均不匹配的 `Direction`，因此确保 `n` 保持在 0 到 3 之间需要由你的代码来保证。

`enum class` 将数字存储在其底层类型中，除非在名称后的冒号后面跟有其他整数类型，否则默认是 `int`。
在这里，每个 `Level` 占用一个字节：

```cpp
enum class Level : unsigned char { Low, High };
```

`Direction` 可以保留 `int` 或声明更小的类型；任何能容纳 0 到 3 的整数类型均可。

转向是对这些数字进行算术运算，并用 `% 4` 进行取模。
从 `West` 顺时针旋转一次是 (3 + 1) % 4，结果为 0，即 `North`。
最直观的转向是将旋转次数相加并直接转换余数：

```cpp
static_cast<Direction>((static_cast<int>(start) + quarterTurns) % 4)
```

跟踪三次转向，展示 `nameOf` 为每个结果返回的内容：

```text
起始    quarterTurns   和    和 % 4    名称     正确值
South   -1               1         1   "East"   "East"
North   -1              -1        -1   ""       "West"
North   -5              -5        -1   ""       "West"
```

`South` 能够得到正确结果是因为它的和非负。
当结果小于 0 时，这种直观的转向就会失效：C++ 取模后的余数符号与左操作数相同，因此 `-5 % 4` 为 -1 而不是 3，而 -1 与 7 一样，是没有对应名称的 `Direction`。
逆时针旋转 5 次（即 -5）与顺时针旋转 3 次到达的方向相同，因此在传递给 `static_cast<Direction>` 之前，负余数必须调整到 0 到 3 的范围内。

### 任务

完成 `direction.hpp`：

- 将 `Direction` 定义为一个 `enum class`，其枚举项按顺时针顺序依次为 `North`、`East`、`South` 和 `West`。
  省略 `class` 不会导致编译失败，因为普通 `enum` 也接受 `Direction::North`。
- `turnedClockwise(Direction start, int quarterTurns)` 返回从 `start` 开始顺时针旋转 `quarterTurns` 个 90 度（四分之一周）后到达的方向，同样支持负数计数。
- `nameOf(Direction d)` 通过 `switch` 返回 `"North"`、`"East"`、`"South"` 或 `"West"`，对于这四个值之外的数值则返回 `""`。
- `directionNamed(const std::string& name)` 返回一个包含完全匹配且区分大小写名称的 `std::optional<Direction>`，对于其他任何内容（包括 `"north"`）则返回 `std::nullopt`。

只读的 `driver.cpp` 会使用这些函数，测试将对比其报告的结果：

- 当 `directionNamed` 未找到任何内容时，`afterTurns(start, quarterTurns)` 返回 `"unknown"`，否则返回转向后的方向名称。
- `ordinalOf(name)` 返回指定名称方向的对应数值，如果名称未知则返回 -1。
- `convertsToInt()` 询问编译器 `Direction` 本身是否会自动转换为 `int`，对于 `enum class` 来说结果为 `false`。

### 解答

```cpp
#pragma once
#include <optional>
#include <string>

// 按顺时针顺序排列
enum class Direction { North, East, South, West };

inline Direction turnedClockwise(Direction start, int quarterTurns) {
    int index = (static_cast<int>(start) + quarterTurns) % 4;
    // 负余数调整到 0 到 3
    if (index < 0) {
        index += 4;
    }
    return static_cast<Direction>(index);
}

inline std::string nameOf(Direction d) {
    switch (d) {
        case Direction::North:
            return "North";
        case Direction::East:
            return "East";
        case Direction::South:
            return "South";
        case Direction::West:
            return "West";
    }
    // 不对应任何名称的值
    return "";
}

inline std::optional<Direction> directionNamed(const std::string& name) {
    if (name == "North") {
        return Direction::North;
    }
    if (name == "East") {
        return Direction::East;
    }
    if (name == "South") {
        return Direction::South;
    }
    if (name == "West") {
        return Direction::West;
    }
    return std::nullopt;
}
```
