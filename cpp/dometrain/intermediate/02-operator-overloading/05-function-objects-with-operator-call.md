如果一个类的定义中包含 `operator()`，那么其实例对象就可以像函数一样被调用，这样的对象被称为函数对象（function object）。
下面展示的每个类还包含一项配置：其构造函数将其存储在成员变量中，每次调用时都会读取它。

```cpp
class MultipleOf {
public:
    explicit MultipleOf(int divisor) : divisor_(divisor) {}

    bool operator()(int value) const {
        return value % divisor_ == 0;
    } 

private:
    int divisor_;
};

std::vector<int> values{3, 4, 9, 12};
MultipleOf divisibleBy3(3);
bool hit = divisibleBy3(12);
auto count = std::count_if(values.begin(), values.end(), MultipleOf(3));
```

该操作符的名称是 `operator()`，其后紧跟着参数列表，因此会有两对括号。
`divisibleBy3(12)` 会执行 `divisibleBy3.operator()(12)`，因此 `hit` 为 true。
`std::count_if` 接收函数对象的方式与接收 lambda 表达式相同，因此 `count` 为 3。

配置项必须通过构造函数传入。
`std::count_if` 在调用该对象时传入一个参数（即元素本身），而 `std::sort` 在调用其比较函数时传入两个参数，因此除数或目标值无法作为额外的参数传入。
虽然全局变量也可以保存它，但两次使用不同除数的计数操作就会共享同一个变量；而使用成员变量则能让每个对象拥有自己独立的配置。

构造函数被声明为 `explicit`，因为 3 是 `MultipleOf` 的除数，而不是 `MultipleOf` 本身。
`operator()` 被声明为 `const`，因为每次调用只读取 `divisor_`，绝不会修改它。

### 使用 `std::sort` 进行排序

`std::sort` 在调用其比较函数时会传入两个元素：`bool operator()(int a, int b) const` 在 `a` 应该排在 `b` 之前时返回 true。
这种比较必须是严格弱序（strict weak ordering），即当 `a` 和 `b` 在该度量标准下相等时必须返回 false，因此应使用 `<`，绝不能使用 `<=`。
如果给 `std::sort` 传入一个对两个相等值返回 true 的比较函数，其行为将是未定义的（undefined behavior）。

`CloserTo` 按照值与目标之间的距离 `|value - target|` 进行排序。
如果没有绝对值，在目标值下方 `value - target` 会是负数，这会导致小于目标值的数据排在目标值本身之前。
你可以对负差值取反，或者调用 `<cstdlib>` 中的 `std::abs`。

仅靠距离可能会产生平局（tie）。
以 5 为中心，数值 5、1、9、4 和 6 的距离分别为 0、4、4、1 和 1，因此 4 和 6 平局，1 和 9 也平局。
平局中的两个值谁也不该排在对方前面，因此 `std::sort` 将两者视为等价，可能会把其中任意一个放在前面。
仅按距离排序时，`{6, 4}` 在某些环境下排序后仍是 `{6, 4}`，而另一个标准库实现可能会返回 `{4, 6}`。
引入决胜规则（tie-break）可以解决这一问题：当距离相等时，使用 `a < b` 比较数值大小，使较小的数值排在前面。
有了这一规则，`{5, 1, 9, 4, 6}` 将排序为 `{5, 4, 6, 1, 9}`。
由于两个不同的数值不可能在两个条件上都平局，因此排序依然保持严格。

### 编写内容

完成 `closeness.hpp` 中的两个类：

- `CloserTo(target)` 将 `target` 存储在 `target_` 中，其 `operator()(a, b)` 是上述包含平局决胜规则的比较操作。
  在 `driver.cpp` 中，`sortByCloseness(values, target)` 执行 `std::sort(values.begin(), values.end(), CloserTo(target))` 并返回 `values`。
  `closestToEach(values, firstTarget, secondTarget)` 在针对任意目标进行排序之前，先为每个目标构建一个 `CloserTo`，然后依次返回最接近 `firstTarget` 的值和最接近 `secondTarget` 的值，因此每个对象都必须维护自己的目标值。
- `WithinDistance(center, radius)` 同时保存这两个值，其 `operator()(value)` 在 `value` 与 `center` 的距离至多为 `radius` 时返回 true。
  `countWithin(values, center, radius)` 返回 `std::count_if` 搭配 `WithinDistance(center, radius)` 统计出的元素数量。
  距离恰好为 `radius` 的数值也算作符合条件：在 `countWithin({1, 5, 9, 12}, 8, 3)` 中，各数值的距离分别为 7、3、1 和 4，因此返回 2；如果使用严格的 `<` 则会漏掉 5 并返回 1。
  半径为 0 仅匹配中心点本身，而负半径不匹配任何值，因为距离不可能小于零。

所有距离均在 `int` 范围内，因此两个类都不需要进行溢出检查。

### 解答

```cpp
#pragma once
#include <cstdlib>

class CloserTo {
public:
    explicit CloserTo(int target) : target_(target) {}

    bool operator()(int a, int b) const {
        const int distanceA = std::abs(a - target_);
        const int distanceB = std::abs(b - target_);
        // 距离相同时较小的值在前
        if (distanceA != distanceB) {
            return distanceA < distanceB;
        }
        return a < b;
    }

private:
    int target_ = 0;
};

class WithinDistance {
public:
    WithinDistance(int center, int radius) : center_(center), radius_(radius) {}

    bool operator()(int value) const {
        // 距离恰好等于半径也算
        return std::abs(value - center_) <= radius_;
    }

private:
    int center_ = 0;
    int radius_ = 0;
};
```
