辅助函数可以返回整个结构体（struct），这样只需遍历一次 vector 就能同时回答多个问题：

```cpp
struct Split {
    int evens;
    int odds;
};

static Split countParities(const std::vector<int> &values) {
    Split split{0, 0};
    for (int value : values) {
        if (value % 2 == 0) {
            split.evens = split.evens + 1;
        } else {
            split.odds = split.odds + 1;
        } 
    }
    return split;
}
```

结构体与其他任何类型一样都可以用作返回类型。
`countParities` 在遍历过程中填充其成员并返回整个结构体，调用者通过编写 `Split split = countParities(numbers);` 并使用点号访问 `split.evens`。
返回的是调用者拥有的值，因此第二次调用不会干扰第一次的结果。

评分函数则不能这样做。
评分器只比较数字、布尔值、字符、字符串以及它们的 vector，并会拒绝你自定义的任何类型。
返回 `Summary` 的评分函数仍能编译和运行；但所有测试用例都会失败，其 actual 列为空，并提示该类型无法比较。
因此结构体仅留在程序内部，而入口点函数只从中返回一个 int。

`static Summary summarize(const std::vector<int> &values)` 返回一个包含最小元素、最大元素和计数（count）的 `Summary`，这三者均在一次遍历中填充完毕。
一旦确定存在第一个元素，请使用它来初始化这两个极值，而不是使用 0：包含 3, 9, 4, 7 的 vector 中并不包含 0，返回 0 将会报告一个从未在数据中出现过的答案。
`std::min`、`std::max`、`std::min_element` 和 `std::max_element` 均被禁用，因此需要你自己编写比较逻辑。

`readSummaryField` 调用一次 `summarize`，然后返回由 `field` 指定的单个 int（需进行全小写的精确匹配）：

- `"count"` 返回元素数量，不含任何元素的 vector 计数为 0，而不是报告无答案。
- `"smallest"` 和 `"largest"` 返回对应的成员，但在不含任何元素的 vector 上（两者均不存在）：返回 `absent`，即调用者提供的 int。
- `summarize` 在读取元素之前必须确认 vector 中存在元素。
  在空 vector 上调用 `values[0]` 会导致该用例直接崩溃中止，actual 列没有任何内容且没有错误信息，因此请先判断 `values.empty()`；无论哪种情况，计数均来自 `values.size()`。
- 这三者之外的字段名称也返回 `absent`。
- 元素可能为负数，在其中一个用例中 -1 是真实的最大值。
  没有任何 int 可以自由地用来表示“无答案”，这就是为什么 `absent` 由调用者传入。

## 解答

```cpp
#include <string>
#include <vector>

struct Summary {
    int smallest;
    int largest;
    int count;
};

struct Solution {
    // 一次遍历填充 Summary 的三个成员，并返回给调用者
    static Summary summarize(const std::vector<int> &values) {
        Summary summary{0, 0, static_cast<int>(values.size())};
        if (values.empty()) {
            return summary;
        }
        summary.smallest = values[0];
        summary.largest = values[0];
        for (int value : values) {
            if (value < summary.smallest) {
                summary.smallest = value;
            }
            if (value > summary.largest) {
                summary.largest = value;
            }
        }
        return summary;
    }

    static int readSummaryField(const std::vector<int> &values, const std::string &field, int absent) {
        // 调用辅助函数，再读出 field 指定的成员
        Summary summary = summarize(values);
        if (field == "count") {
            return summary.count;
        }
        if (summary.count == 0) {
            return absent;
        }
        if (field == "smallest") {
            return summary.smallest;
        }
        if (field == "largest") {
            return summary.largest;
        }
        return absent;
    }
};
```
