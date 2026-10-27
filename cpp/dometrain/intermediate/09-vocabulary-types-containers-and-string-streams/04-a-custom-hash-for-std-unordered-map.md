`std::unordered_map` 分两步查找键。
首先，它对键调用哈希函数，并使用返回的 `std::size_t` 选择一个桶（bucket），即 map 分散存储键的众多槽位之一。
然后，它仅使用 `operator==` 将该键与该桶中已有的键进行比较。
该 map 的默认哈希支持诸如 `std::string` 和 `int` 等标准类型。
对于 `NameKey`，你需要将其作为第三个模板参数提供：

```cpp
struct NameKeyHash {
    std::size_t operator()(const NameKey& key) const {
        return std::hash<std::string>{}(key.text);
    }
};

std::unordered_map<NameKey, int, NameKeyHash> counts;
```

`NameKeyHash` 是一个哈希函数对象：一个结构体，其 `operator()` 接受键并返回 `std::size_t`，map 调用它的方式就像 `std::sort` 调用比较对象一样。
`std::hash<std::string>{}` 创建了标准库针对字符串的哈希对象，而 `(key.text)` 则对其进行调用。
map 还通过接受两个 `const NameKey&` 参数的 `operator==` 来比较键；如果没有这个运算符，`driver.cpp` 将无法编译。
初始代码仅声明了 `NameKey`，因此目前 `driver.cpp` 会报错并停在 `use of undeclared identifier 'NameKeyHash'`，并且在 `name_key.hpp` 定义 `NameKeyHash` 和 `operator==` 之前，所有测试用例都会失败。

### 相等的键需要相等的哈希值

上述 `NameKeyHash` 适用于使用普通的 `a.text == b.text` 进行比较的键。
但在本题中，`Ada`、`ada` 和 `ADA` 是同一个名字，仅让 `operator==` 忽略大小写是不够的：这三种拼写会哈希成不同的数字，因此它们通常会落入不同的桶中，而 `operator==` 永远没有机会比较它们。
将大小写不敏感的 `operator==` 与上述哈希配对，运行后会显示错误的计数：

- `distinctNames({"Ada", "ada", "ADA", "Bob"})` 返回 3，而不是 2。
  这三种拼写中恰好有两个落入同一个桶，`operator==` 将它们合并了；而第三个则单独留在其他桶中。
- 对于出现过两次的名字，`countOf({"Ada", "bob", "aDa"}, "ADA")` 却返回 0。

如果换用其他库实现或桶数量，可能会产生其他的错误数字，因为语言标准无法保证当哈希与 `operator==` 产生分歧时 map 的行为。
哈希必须与相等性保持一致。
比较结果相等的键必须产生相等的哈希值，因此哈希必须针对与 `operator==` 比较时相同形式的文本（即小写）进行计算。
该规则是单向的：不相等的键可以共享相同的哈希值，因为 `operator==` 仍然可以在桶内部将它们区分开来。

将单个字符转为小写的方法：

```cpp
c = static_cast<char>(std::tolower(static_cast<unsigned char>(c)));
```

`std::tolower` 期望接收一个 `unsigned char` 能容纳的值，而从字符串中获取的 `char` 可能是负数，因此内部的类型转换是保证调用合法的关键。
对于 `A` 到 `Z`，它返回对应的小写字母，其他字符则保持不变。

有两种方法可以让哈希与 `operator==` 保持一致。
第一种是在两处都转为小写：`operator==` 比较转为小写后的名字，而 `NameKeyHash` 对 `key.text` 的小写副本进行哈希。
第二种是只转一次小写：为 `NameKey` 提供一个接受 `const std::string&` 的构造函数，并在内部存储小写文本，这样针对 `text` 的普通 `==` 与上述哈希就已经保持一致了。
driver 会以 `NameKey{name}` 的形式构建每个键，这两种设计都可以正常工作。

### 需要编写的内容

在 `name_key.hpp` 中，编写 `operator==`，使得当两个名字仅在字母大小写上存在差异时视为相等；将 `operator!=` 实现为 `!(a == b)`；并编写一个与你的 `operator==` 保持一致的 `NameKeyHash`。
`driver.cpp` 会在 `std::unordered_map<NameKey, int, NameKeyHash>` 中对名字进行计数：

- `distinctNames(names)` 返回列表中包含多少个不同的名字：`{"Ada", "ada", "ADA", "Bob"}` 返回 2，空列表返回 0。
- `countOf(names, probe)` 返回 `probe`（无论哪种拼写形式）在 `names` 中出现的次数，未出现时返回 0。
  `Adam` 和 `ADAM` 是同一个名字，但与 `Ada` 不同。
- `firstSpellings(names)` 按照名字首次出现的顺序，返回每个名字的第一种拼写形式：`{"bob", "Ada", "BOB", "ada"}` 返回 `["bob", "Ada"]`。

### 解答

```cpp
#pragma once
#include <cctype>
#include <cstddef>
#include <functional>
#include <string>

struct NameKey {
    std::string text;
};

// 返回小写副本
inline std::string lowered(std::string text) {
    for (char& c : text) {
        c = static_cast<char>(std::tolower(static_cast<unsigned char>(c)));
    }
    return text;
}

inline bool operator==(const NameKey& a, const NameKey& b) {
    return lowered(a.text) == lowered(b.text);
}

inline bool operator!=(const NameKey& a, const NameKey& b) {
    return !(a == b);
}

struct NameKeyHash {
    // 对与 operator== 相同的小写形式求哈希
    std::size_t operator()(const NameKey& key) const {
        return std::hash<std::string>{}(lowered(key.text));
    }
};
```
