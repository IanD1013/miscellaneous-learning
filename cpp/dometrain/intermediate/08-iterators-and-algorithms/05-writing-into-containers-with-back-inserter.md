`std::copy_if` 和 `std::transform` 会通过它们的第三个参数（一个输出迭代器）写入每个结果：算法通过它赋值一个结果，然后将其向前步进。
vector 自身的迭代器可以充当输出迭代器，但通过它进行写入绝不会添加新元素。
传入空 vector 的 `begin()` 依然可以通过编译：

```cpp
std::vector<int> negatives;
std::copy_if(values.begin(), values.end(), negatives.begin(),
             [](int v) { return v < 0; });
```

`negatives` 中没有任何元素，因此每次写入都会落在该 vector 并不拥有的内存中。
这是未定义行为。
vector 仅能通过自身的成员函数（例如 `push_back`）来扩容，而通过其迭代器进行写入不会调用其中的任何函数。

`std::back_inserter(v)` 可以创建一个确实能够扩容 `v` 的输出迭代器：通过它进行的每次赋值都会调用 `v.push_back(value)`，因此结果会被追加到 `v` 原本已持有的内容之后：

```cpp
#include <iterator>

std::vector<int> negatives{0};
std::copy_if(values.begin(), values.end(), std::back_inserter(negatives),
             [](int v) { return v < 0; });
// values {4, -1, 7, -9} 会使 negatives 变为 {0, -1, -9}
```

`std::copy_if(first, last, out, pred)` 按输入顺序仅写入令 `pred` 返回 `true` 的元素。
`std::transform(first, last, out, op)` 为每个元素写入 `op(element)`，并且 `op` 可以返回与它所接收的类型不同的类型，因此 `int` 范围可以用来填充 `std::vector<std::string>`。

在调用 `std::transform` 之前，你可以先调整目标容器的大小，因为每个输入正好对应写入一个结果。
而 `std::copy_if` 则无法提供这样的计数：只有当谓词检查完所有元素之后，才能知道会写入多少个元素。
使用 `std::back_inserter`，这两种调用都不需要预先知道数量。

### 需要编写的内容

实现 `inserters.cpp` 中的三个函数，每个函数都使用 `std::back_inserter` 来构建其结果。

- `keepMultiples(values, factor)` 使用 `std::copy_if` 按输入顺序返回属于 `factor` 倍数的值：传入 `{3, -6, 4, 9}` 和 3 会返回 `[3, -6, 9]`。
  在执行任何 `%` 运算之前，单独处理 factor 为 0 和 -1 的情况。
  0 是 0 的唯一倍数，且 `v % 0` 是未定义行为，因此 factor 为 0 时仅保留零。
  每个 `int` 都是 -1 的倍数，因此 factor 为 -1 时无需计算 `%` 即可保留每个值：`-2147483648 % -1` 是未定义行为，因为商 2147483648 超出了 `int` 的表示范围。
- `labelled(values, prefix)` 使用 `std::transform` 将每个值转换为文本并加上 `prefix` 前缀返回：传入 `{7, 12}` 和 `"id-"` 会返回 `["id-7", "id-12"]`。
- `appendSquares(base, values)` 使用 `std::transform` 将每个值的平方追加到 `base` 原有元素之后，并返回 `base`。

以 base 为 `{1}`、values 为 `{2, -3}` 为例，传递给 `std::transform` 的目标容器决定了 `appendSquares` 的返回值：

```text
base，使用 std::back_inserter 扩容             [1, 4, 9]
一个新 vector，使用 std::back_inserter 扩容    [4, 9]
base 调整大小为 3，从 base.begin() 开始写入    [4, 9, 0]
```

只有第一种是正确的。
新 vector 从未包含过 1。
`resize(3)` 会保留 1 并添加两个零，然后从 `begin()` 开始的两次写入会覆盖掉 1 和第一个零。

平方值必须能够放入 `int` 中：46340 \* 46340 = 2147395600 小于 `std::numeric_limits<int>::max()` (2147483647)，而 46341 \* 46341 = 2147488281 大于它。
当任何值小于 -46340 或大于 46340 时，返回一个空 vector 而不是 `base`。
在对任何值求平方之前，使用 `std::all_of` 检查每个值，因为在 `int` 下计算 46341 的平方会导致有符号整数溢出：这是未定义行为，而不是事后可以检查的结果。
`std::all_of` 对空范围返回 true，因此当没有值时，`base` 会保持原样返回。

将 46340 存入一个 `constexpr int` 中，并附带一个 `static_assert`，用以将其作为 `long long` 计算出的平方与 `std::numeric_limits<int>::max()` 进行比较；如果边界错误，就会阻止构建。

### 解答

```cpp
#include <algorithm>
#include <iterator>
#include <limits>
#include <string>
#include <vector>

struct Solution {
    static std::vector<int> keepMultiples(const std::vector<int>& values, int factor) {
        std::vector<int> result;
        std::copy_if(values.begin(), values.end(), std::back_inserter(result), [factor](int v) {
            // 0 只是 0 的倍数，避免 v % 0
            if (factor == 0) {
                return v == 0;
            }
            // 每个值都是 -1 的倍数，避免 INT_MIN % -1
            if (factor == -1) {
                return true;
            }
            return v % factor == 0;
        });
        return result;
    }

    static std::vector<std::string> labelled(const std::vector<int>& values, const std::string& prefix) {
        std::vector<std::string> result;
        std::transform(values.begin(), values.end(), std::back_inserter(result),
                       [&prefix](int v) { return prefix + std::to_string(v); });
        return result;
    }

    static std::vector<int> appendSquares(std::vector<int> base, const std::vector<int>& values) {
        constexpr int maxRoot = 46340;
        // 边界错误时阻止构建
        static_assert(static_cast<long long>(maxRoot) * maxRoot <= std::numeric_limits<int>::max());
        static_assert(static_cast<long long>(maxRoot + 1) * (maxRoot + 1) > std::numeric_limits<int>::max());
        // 求平方前先检查，避免有符号溢出
        bool fits = std::all_of(values.begin(), values.end(),
                                [](int v) { return v >= -maxRoot && v <= maxRoot; });
        if (!fits) {
            return {};
        }
        std::transform(values.begin(), values.end(), std::back_inserter(base), [](int v) { return v * v; });
        return base;
    }
};
```
