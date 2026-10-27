一个函数只有一个返回类型，因此在过去，返回最小值、最大值和计数通常意味着要为它们声明一个 struct。
`std::tuple` 则无需声明 struct 即可保存固定数量的值，元素类型按顺序写在尖括号内：

```cpp
std::tuple<std::string, int, bool> entry{"retries", 3, true};
auto reading = std::make_tuple(4, 21.5, false);
std::string label = std::get<0>(entry);
```

花括号会构建一个由你明确写出类型的 tuple。
`std::make_tuple` 会从其实参推导元素类型，因此 `reading` 的类型是 `std::tuple<int, double, bool>`。
`std::get<0>(entry)` 读取位置 0 处的元素 `"retries"`。
该位置是一个模板实参，而不是像 `operator[]` 所接受的运行时索引，因此它必须是一个常量，并且编译器会根据 tuple 的类型检查它：`std::get<3>(entry)` 无法通过编译，报错信息为 `tuple_element index out of range`。

在 `std::optional` 内部，tuple 意味着包含其所有值，或者一个都没有。
返回 `std::optional<std::tuple<int, int, int>>` 的函数要么返回 `std::nullopt`，要么返回填充了 optional 的 `std::make_tuple(...)`。
optional 本身并不是 tuple。
对于名为 `summary` 的 optional，请先检查 `summary.has_value()`；随后 `*summary` 即为内部的 tuple，而结构化绑定（structured binding）解包的正是该 tuple。

### 结构化绑定

`std::get` 调用永远无法说明元素的具体含义。
而结构化绑定可以在一条语句中为每个元素声明一个名称：

```cpp
auto [name, attempts, enabled] = entry;
```

这些名称按位置匹配：无论名称是什么，`name` 获取元素 0，`attempts` 获取元素 1，`enabled` 获取元素 2。
对于包含最小值、最大值和计数（均为 `int`）的 tuple，`auto [high, low, count] = ...` 可以通过编译并将最小值赋给 `high`。
名称的数量必须与元素的数量相等。
如果给一个三元素 tuple 赋予两个名称，编译器会报错 `decomposes into 3 elements, but only 2 names were provided`。

使用普通的 `auto` 时，这些名称引用的是隐藏副本中的元素，因此给 `attempts` 赋值不会改变 `entry`。
`auto&` 将它们绑定到 `entry` 本身的元素上，而 `const auto&` 则以只读方式执行相同的绑定。
按值返回的函数结果是临时对象，而非 const 引用不能绑定到临时对象，因此 `auto&` 无法对其进行解包。
普通的 `auto` 可以解包，`const auto&` 也可以，并且 `const auto&` 会在这些名称的作用域内延长临时对象的生命周期。

同样的声明也可以按成员声明的顺序解包 `std::pair` 以及成员均为 public 的 struct。
map 循环 `for (const auto& [key, value] : totals)` 也是基于该特性：`std::map` 中的每个条目都是键和值构成的 pair，该循环会按键的升序访问各条目。

结构化绑定总是声明新变量。
而 `std::tie(name, attempts, enabled) = entry;` 则是为已存在的变量赋值，因为 `std::tie` 构建了一个包含这些变量引用的 tuple。

tuple 适合用于调用方会立即解包的短期生命周期结果，例如 private 辅助函数的返回值，即使每个元素都是 `int` 也没问题。
一旦调用方需要保留该结果并在各处传递，struct 的成员名称就会比基于位置的 tuple 传达更多信息。

### 编写要求

在 `tuples.cpp` 中，为 `struct Solution` 添加两个 private static 辅助函数：

- `summarize(const std::vector<int>& values)` 返回 `std::optional<std::tuple<int, int, int>>`：当 vector 为空时返回 `std::nullopt`，否则依次返回最小值、最大值和元素数量。
- `quotientAndRemainder(int value, int divisor)` 返回一个包含 `value` 除以 `divisor` 的商和余数的 `std::pair<int, int>`。

然后实现三个 public 函数，并使用结构化绑定解包它们所使用的每个 tuple 和 pair。

`minMaxCount(values)` 返回由 `summarize` 得出的 `{minimum, maximum, count}`，例如针对 `{6, -3, 6, 1}` 返回 `{-3, 6, 4}`，针对 `{-8}` 返回 `{-8, -8, 1}`；当 `summarize` 返回 `std::nullopt` 时返回一个空 vector。

`keysAtLeast(keys, values, threshold)` 将每个 `keys[i]` 与 `values[i]` 存入一个 `std::map<std::string, int>` 中，并按键的升序返回其值不小于 `threshold` 的所有键。
重复出现的键保留后面的值：对于 `keysAtLeast({"b", "a", "b"}, {9, 4, 2}, 4)`，map 最终保存 `a` 对应 4，`b` 对应 2，因此返回 `{"a"}`。
当两个 vector 的长度不同时，返回包含一个空字符串的 vector `{""}`。
空 vector 不能用于标记该错误，因为当没有任何值达到 `threshold` 时其返回值也是空 vector。
键永远不会为空字符串，因此 `{""}` 绝不会是正常的结果。

`divideAll(values, divisor)` 依次返回每个值除以 `divisor` 的商，紧接着是余数。
`/` 向零截断，而 `%` 得到的余数与被除数符号相同，这就是为什么 -9 会得到 -2 和 -1。
负除数会翻转每个商的符号，但保持余数不变：

```text
位置                     {9 的商, 9 的余数, -9 的商, -9 的余数}
divideAll({9, -9}, 4)    {2, 1, -2, -1}
divideAll({9, -9}, -4)   {-2, 1, 2, -1}
```

当 `divisor` 为 0 时返回一个空 vector，因为 `int` 除以零是未定义行为。
-2147483648 除以 -1 是另一种未定义的 `int` 除法：其商 2147483648 比最大的 `int` 大 1。
当 `divisor` 为 -1 时，`values` 绝不会包含 -2147483648，因此 `divideAll` 无需针对这种情况进行检查。

### 解答

```cpp
#include <map>
#include <optional>
#include <string>
#include <tuple>
#include <utility>
#include <vector>

struct Solution {
    static std::vector<int> minMaxCount(const std::vector<int>& values) {
        auto summary = summarize(values);
        if (!summary.has_value()) {
            return {};
        }
        auto [minimum, maximum, count] = *summary;
        return {minimum, maximum, count};
    }

    static std::vector<std::string> keysAtLeast(const std::vector<std::string>& keys, const std::vector<int>& values, int threshold) {
        if (keys.size() != values.size()) {
            return {""};
        }
        std::map<std::string, int> totals;
        for (std::size_t i = 0; i < keys.size(); ++i) {
            totals[keys[i]] = values[i];  // 重复的键保留后面的值
        }
        std::vector<std::string> result;
        for (const auto& [key, value] : totals) {
            if (value >= threshold) {
                result.push_back(key);
            }
        }
        return result;
    }

    static std::vector<int> divideAll(const std::vector<int>& values, int divisor) {
        if (divisor == 0) {
            return {};
        }
        std::vector<int> result;
        for (int value : values) {
            auto [quotient, remainder] = quotientAndRemainder(value, divisor);
            result.push_back(quotient);
            result.push_back(remainder);
        }
        return result;
    }

private:
    static std::optional<std::tuple<int, int, int>> summarize(const std::vector<int>& values) {
        if (values.empty()) {
            return std::nullopt;
        }
        int minimum = values[0];
        int maximum = values[0];
        for (int value : values) {
            if (value < minimum) {
                minimum = value;
            }
            if (value > maximum) {
                maximum = value;
            }
        }
        return std::make_tuple(minimum, maximum, static_cast<int>(values.size()));
    }

    static std::pair<int, int> quotientAndRemainder(int value, int divisor) {
        return {value / divisor, value % divisor};
    }
};
```
