一个针对 `int` 的 `larger` 重载和另一个针对 `std::string` 的重载会用不同的类型重复相同的函数体。
函数模板只需编写一次该函数体。
函数前面的 `template <typename T>` 声明了 `T`，这是一个代表类型的模板参数：

```cpp
template <typename T>
T larger(const T& a, const T& b) {
    return a < b ? b : a;
}
```

`larger(3, 8)` 返回 8，而 `larger(std::string("apple"), std::string("pear"))` 返回 `"pear"`。
这些调用运行的是两个不同的函数。
对于调用所使用的每种类型，编译器都会实例化该模板：它会根据 `larger` 生成一个将 `T` 替换为 `int` 的函数，以及另一个将 `T` 替换为 `std::string` 的函数，并分别编译这些实例化版本。
在程序运行期间，不会对 `T` 进行任何检查。

类型必须支持的操作恰恰是函数体对其执行的操作。
`larger` 使用 `<` 比较其实参并通过值返回其中一个（这会进行拷贝），因此 `T` 必须支持 `<` 和拷贝操作。
`int`、`double` 和 `std::string` 两者都支持。
如果传入没有定义 `operator<` 的 `Point` 结构体的两个值调用它，则 `Point` 实例化将无法编译，并在 `larger` 内部的 `<` 处报错 `invalid operands to binary expression ('const Point' and 'const Point')`。

编译器在每次实例化调用时都需要函数体，因此函数模板应在头文件中完整定义。
与在头文件中定义的普通函数不同，它不需要 `inline`：同一个模板定义可以出现在每个包含该头文件的 `.cpp` 文件中。

### 推导 T

`larger(3, 8)` 从未显式指定 `int`；编译器会从实参中推导 `T`。
这就是实参推导。
每个实参都会给出自己推导出的 `T`，这些结果必须一致，并且编译器不会尝试进行诸如从 `int` 到 `double` 的类型转换来使其一致。
如果使用一个 `int` 值和两个 `double` 边界来调用你在下方编写的第一个模板 `clampTo`：

```cpp
clampTo(5, 1.5, 4.5)   // 无法编译：no matching function for call to 'clampTo'
```

`5` 将 `T` 推导为 `int`，而 `1.5` 和 `4.5` 则将其推导为 `double`。
由于得到了两个不同的推导结果，因此没有可调用的 `clampTo`，即便接受三个 `double` 形参的普通函数可以接受 `5`。
自己显式写出模板实参（即函数名后尖括号中的类型）可以跳过推导：

```cpp
clampTo<double>(5, 1.5, 4.5)   // 返回 4.5
```

仅对本次调用而言 `T` 为 `double`，形参变为 `const double&`，且 `5` 会像在普通函数中一样转换为 `5.0`。
模板本身保持不变。

### 编写内容

在 `generic.hpp` 中，编写两个函数模板：

- `template <typename T> T clampTo(const T& value, const T& low, const T& high)`：当 `value` 小于 `low` 时返回 `low`，当 `value` 大于 `high` 时返回 `high`，否则返回 `value`。
  可以假设 `low` 不大于 `high`。
  仅使用 `<` 进行比较，以便类型除了 `<` 和拷贝之外无需支持其他操作，并且请自行编写比较逻辑而不是调用 `std::clamp`。
- `template <typename T> int countEqual(const std::vector<T>& values, const T& target)`：返回 `values` 中使用 `==` 比较与 `target` 相等的元素数量，若 vector 为空则返回 0。
  `T` 会从两个参数中推导：vector 的元素类型以及 `target` 的类型。

`driver.cpp` 使用三个 `int` 值、三个 `std::string` 值调用 `clampTo`，并使用一个 `int` 值和两个 `double` 边界以 `clampTo<double>` 形式调用它，然后将每个结果作为一个单元素 vector 返回。
它还使用一个 `std::vector<int>` 和一个 `int` 目标值调用 `countEqual`，并使用一个 `std::vector<std::string>` 和一个 `std::string` 目标值以 `countEqual<std::string>` 形式调用它。

`std::string` 的 `<` 比较字符编码，且每个大写字母的编码都小于任何小写字母。
其中一个用例将 `"Apple"` 限制在 `"apple"` 和 `"melon"` 之间：在运行之前，先确定它会返回三者中的哪一个。

### 解答

```cpp
#pragma once
#include <vector>

// 只用 < 比较，把 value 限制在 [low, high] 内
template <typename T>
T clampTo(const T& value, const T& low, const T& high) {
    if (value < low) {
        return low;
    }
    if (high < value) {
        return high;
    }
    return value;
}

// 统计与 target 相等的元素个数
template <typename T>
int countEqual(const std::vector<T>& values, const T& target) {
    int count = 0;
    for (const T& value : values) {
        if (value == target) {
            ++count;
        }
    }
    return count;
}
```
