`std::vector<int>` 可以像任何其他类型一样作为成员，这会将整个集合置于拥有它的对象内部。
当对象构造时，vector 起初为空，并随着对象的销毁而结束；在此期间，它仅通过类自身的成员函数进行扩充。

```cpp
class Log {
public:
    void record(int value) {
        entries_.push_back(value);
    }

    const std::vector<int> &entries() const {
        return entries_;
    }

private:
    std::vector<int> entries_;
};
```

将 vector 成员保持为 private，才能够对其内容作出保证。
当 `entries_` 只能通过 `record` 访问时，该类就能对其内部的所有内容给出确切的保证。
访问器（accessor）仍然可以将集合提供给外部读取：`const std::vector<int> &` 引用了对象自身的 vector 而无需进行拷贝，而 `const` 则会使通过该引用进行的 `push_back`、`erase` 和赋值操作产生编译错误。
如果从返回类型和函数本身中去掉 `const`，变成 `std::vector<int> &entries()`，任何调用者都可以从外部随心所欲地向该成员放入任何内容，这会让类所作出的保证变得毫无意义。

### DistinctList 的保证

每个值仅出现一次，并按照最初添加时的顺序排列。
`std::set` 可以直接提供唯一性，但它是排序后的顺序；而包含 vector 的类则保留了到达顺序，并执行它自己的规则。

因此，`add` 在扩充之前先进行查找，而 `remove` 删除的是位置而不是值：

```cpp
std::vector<int>::iterator position = std::find(items_.begin(), items_.end(), value);
if (position == items_.end()) {
    // items_ 中没有任何匹配项
}
```

`std::find` 遍历该范围并返回一个位置；`items_.end()` 是在没有匹配到任何元素时返回的尾后（one-past-the-end）位置，与它进行比较就是做出判断的测试条件。

### 实现 add 和 remove

- `add(int value)` 仅在 `std::find` 表明该值尚不存在时才调用 `items_.push_back(value)`。
- `remove(int value)` 查找位置，将其与 `items_.end()` 进行比较；当位置有效时，调用 `items_.erase(position)` 并返回 `true`。
  若值不存在，则不删除任何内容并返回 `false`。
  将值本身传递给 `erase` 无法通过编译，因为 `erase` 接收的是位置。
- 保持 `items()` 不变，且不要保留计数成员：`items_.size()` 就是计数，额外的计数成员可能会与它不同步。
- `distinctAfterRemoval` 已经为你编写好了。
  它会添加每个输入值，执行一次删除操作，并返回 `items()` 的副本，评测系统会逐个元素进行比较。
- `removalReport` 也已为你编写好。
  它添加相同的值，执行相同的删除操作，并返回 `remove` 所返回的布尔值，以便单独对该标志进行评测，而不是从集合中推断出来。
- 空输入应返回空 vector，未匹配到任何内容的删除操作应使集合保持原样。
  到达顺序是答案的一部分，因此在输出时不要进行排序。

### 解答

```cpp
#include <algorithm>
#include <vector>

class DistinctList {
public:
    void add(int value) {
        // 只有 std::find 在 items_ 中找不到该值时才 push_back
        std::vector<int>::iterator position = std::find(items_.begin(), items_.end(), value);
        if (position == items_.end()) {
            items_.push_back(value);
        }
    }

    bool remove(int value) {
        // 查找位置并与 items_.end() 比较，值确实存在时按位置删除
        std::vector<int>::iterator position = std::find(items_.begin(), items_.end(), value);
        if (position == items_.end()) {
            return false;
        }
        items_.erase(position);
        return true;
    }

    const std::vector<int> &items() const {
        return items_;
    }

private:
    std::vector<int> items_;
};

struct Solution {
    static std::vector<int> distinctAfterRemoval(const std::vector<int> &values, int toRemove) {
        DistinctList list;
        for (int value : values) {
            list.add(value);
        }
        list.remove(toRemove);
        return list.items();
    }

    static bool removalReport(const std::vector<int> &values, int toRemove) {
        DistinctList list;
        for (int value : values) {
            list.add(value);
        }
        return list.remove(toRemove);
    }
};
```
