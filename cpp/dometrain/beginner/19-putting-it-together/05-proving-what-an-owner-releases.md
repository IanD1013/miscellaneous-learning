内存泄漏在这个引擎上不会留下任何痕迹。
没有任何机制会报告从未归还的资源，而且从未运行过的析构函数看起来与运行过的析构函数毫无二致，因此释放资源的唯一证据就是资源在销毁退出时写下的记录。

`driver.cpp` 是固定的，包含两个用于评分的函数。
`releaseOrder` 声明了一个局部 `std::vector<int> record`，开启一个嵌套作用域，构建一个借用该 record 地址的 `ResourceStore`，添加每个 id，请求移除一个元素，让作用域结束，并返回 record。
`looseRelease(id)` 规模更小：在一个独立的作用域中创建一个 `Resource`，不涉及任何 store，并在该作用域结束后返回 record。
两个答案中的每个数字都是由你编写的析构函数追加的。

`Resource` 只是借用 record 而不是拥有它：record 的生命周期长于每一个 resource，这使得普通的 `std::vector<int> *` 成为合适的成员变量。
`~Resource()` 在将其与 `nullptr` 进行比较后，通过该指针追加自身的 id。

`ResourceStore` 是拥有所有权的容器。
它的 `items_` 是一个 `std::vector<std::unique_ptr<Resource>>`，因此从 `add` 调用 `std::make_unique<Resource>(id, record_)` 的那一刻起，resource 就有了唯一的所有者，并且这里没有任何手动归还内存的操作：resource 销毁是因为其所有者销毁了。
`remove` 遍历这些项并擦除第一个 `id()` 匹配的项：

```cpp
if (items_[i]->id() == id) {
    items_.erase(items_.begin() + i);
    return;
}
```

该 erase 接受的是位置而非索引，这正是 `items_.begin() + i` 所构建的，而 `items_[i]->id()` 则通过该槽位中的所有者访问到 resource。
此时执行擦除会立即销毁该 resource，而不是等到最后才销毁，这就是为什么被移除的 id 会先于所有存留项进入 record。

其余部分的释放顺序由 store 决定。
vector 销毁其元素的顺序是未指定的，因此如果契约中规定了顺序，所有者就需要自行释放其元素，从最前面开始：

```cpp
for (std::size_t i = 0; i < items_.size(); i += 1) {
    items_[i].reset();
}
```

`reset()` 会释放所有者持有的任何内容，并使其不再持有任何内容，因此从索引 0 开始递增会将存留的元素按照添加顺序写入 record。

### 要求

- 你需要填写的内容，全部在 `store.hpp` 中：`~Resource()`、`add`、`remove` 和 `~ResourceStore()`。
- 当 `record_` 不为 `nullptr` 时，`~Resource()` 将 `id_` 压入 record，否则什么都不做。
  仅凭这一行，`looseRelease(5)` 的结果就是 `{5}`。
- `remove(int id)` 会擦除带有该 id 的第一个元素并停止，因此具有相同 id 的两个元素只会失去一个。
  `removeId` 为 -1 或任何没有任何元素持有的 id 不会移除任何内容。
- 你的答案中应包含 `std::make_unique<Resource>(` 和 `nullptr`；`delete`、`std::move` 和 `main` 均被禁用。
- `releaseOrder` 的结果读取为被移除的 id，后跟按添加顺序排列的存留项，空的 id 列表则产生一个没有任何内容的 record。

### 解答

```cpp
#pragma once

#include <cstddef>
#include <memory>
#include <vector>

class Resource {
public:
    Resource(int id, std::vector<int> *record) : id_(id), record_(record) {}

    int id() const {
        return id_;
    }

    ~Resource() {
        // 释放时把自己的 id 写入借用的记录
        if (record_ != nullptr) {
            record_->push_back(id_);
        }
    }

private:
    int id_;
    std::vector<int> *record_;
};

class ResourceStore {
public:
    ResourceStore(std::vector<int> *record) : record_(record) {}

    void add(int id) {
        // 在这里为 store 增加一个所有者；remove 取出第一个匹配的所有者；两个析构函数按契约规定的顺序写入记录
        items_.push_back(std::make_unique<Resource>(id, record_));
    }

    void remove(int id) {
        // 擦除第一个 id 匹配的元素后立即停止
        for (std::size_t i = 0; i < items_.size(); i += 1) {
            if (items_[i]->id() == id) {
                items_.erase(items_.begin() + i);
                return;
            }
        }
    }

    ~ResourceStore() {
        // 从最前面开始逐个释放，让存留项按添加顺序写入记录
        for (std::size_t i = 0; i < items_.size(); i += 1) {
            items_[i].reset();
        }
    }

private:
    std::vector<std::unique_ptr<Resource>> items_;
    std::vector<int> *record_;
};
```
