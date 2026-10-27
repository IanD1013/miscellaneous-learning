一个 `std::weak_ptr<Document>` 会记录一个 `Document`，但并不是其所有者之一。
从 `std::shared_ptr` 赋值时，它引用同一个对象，但 `use_count` 仍保持所有者所决定的计数；即使 `weak_ptr` 仍然存在，当其最后一个 `std::shared_ptr` 销毁时，该 `Document` 就会被销毁：

```cpp
std::shared_ptr<Document> owner = std::make_shared<Document>("notes");
std::weak_ptr<Document> entry = owner;          // owner.use_count() 仍为 1

if (std::shared_ptr<Document> alive = entry.lock()) {
    // alive 是第二个所有者：此处 owner.use_count() 为 2
}

owner.reset();                                  // Document 被销毁
bool gone = entry.expired();                    // true
std::shared_ptr<Document> none = entry.lock();  // 空
```

即使在 `expired()` 为 false 时，`weak_ptr` 也没有 `*` 或 `->` 运算符。
访问该对象的方式是 `lock()`，它返回一个 `std::shared_ptr<Document>`。
当对象仍然存活时，这就是一个新的所有者，只要你持有它，它就会保持 `Document` 处于存活状态，这就是为什么在 `if` 内部计数为 2 的原因。
一旦对象被销毁，`lock()` 就会返回一个空的 `std::shared_ptr`。

`if` 语句在其条件中声明了 `alive` 并像指针一样对其进行判断，因此仅当 `alive` 拥有该对象时才会执行代码块。
直接从 `weak_ptr` 构造 `std::shared_ptr<Document>` 无法替代 `lock()`：当对象已被销毁时，该构造函数会终止程序。

### weak\_ptr 条目的 map

`cache.hpp` 中的 `Cache` 存储了一个 `std::map<std::string, std::weak_ptr<Document>>`，因此它能记录它创建过的每个 `Document`，而不会保持其中任何一个处于存活状态。
当一个 `Document` 被销毁时，其条目仍会保留在 map 中（处于过期状态），直到有操作将其擦除。
这就是为什么 `entries()`（已实现）和 `liveEntries()` 可能会有所不同的原因。

从未赋值的 `weak_ptr`（例如 `entries_[name]` 为新名称插入的那个）不引用任何内容：`expired()` 为 true 且 `lock()` 返回空的 `std::shared_ptr`，这与针对已销毁的 `Document` 的行为相同。
要替换已过期的 `weak_ptr`，请将新的指针赋值给该条目。
`emplace` 和 `insert` 会保留 map 中已存在的键而不做修改，因此使用它们会导致过期的条目保留下来，并且随后对该名称的每次 `get` 调用都会创建另一个 `Document`。

在 `cache.hpp` 中实现以下成员：

- `get(name)` 返回名为 `name` 的 `Document` 的一个所有者。
  在该 `Document` 存活期间，`get` 通过 `lock()` 获取它；否则使用 `std::make_shared<Document>(name)`（切勿使用 `new`）创建一个，并在 `name` 下存储指向它的 `weak_ptr`。
  map 仅持有 `std::weak_ptr`，因此缓存永远不是所有者。
- `created()` 已经返回了 `created_`；保持该值等于 `get` 所创建的 `Document` 的数量。
- `liveEntries()` 返回其 `Document` 仍然存活的条目数量。
- `purge()` 擦除所有已过期的条目并保留其余条目。
  在 `std::map` 上，`erase(it)` 会返回被擦除条目之后的迭代器；由于 `it` 不再引用条目，请从该迭代器继续循环。

### driver.cpp 报告的内容

`Solution::cacheRun(dropped, kept)` 对 `dropped` 中的每个名称调用 `get` 并立即丢弃每个结果，然后对 `kept` 中的每个名称调用 `get` 并将每个结果保存在 vector 中。
根据结果是否被持有，相同的三个名称会给出不同的计数。

每个结果列出：created、live entries、entries、purge 后的 entries。

- `cacheRun({"a", "a", "b"}, {})` 返回 `[3, 0, 2, 0]`
- `cacheRun({}, {"a", "a", "b"})` 返回 `[2, 2, 2, 2]`

被丢弃的结果是唯一的所有者，因此每个 `Document` 在 `get` 返回后会立即被销毁，而第二个 `"a"` 会找到一个已过期的条目。
在被持有时，当第二个 `get` 执行 lock 时，第一个 `"a"` 仍然存活。
当一个 `"a"` 被丢弃然后两个被持有时，`cacheRun({"a"}, {"a", "a"})` 会返回哪四个计数？
Run 会显示答案，因为它是测试用例之一。

`Solution::observerFacts()` 获取 `"a"`，在持有第一个所有者的同时再次获取它，释放两个所有者，然后再次获取 `"a"`。

其结果列出：仅第一个所有者的 `use_count()`、持有第二个所有者时的相同计数、两者都销毁后的 `liveEntries()` 和 `entries()`，以及最后一次 `get` 之后的 `created()`。

- `observerFacts()` 返回 `[1, 2, 0, 1, 2]`

### 解答

```cpp
#pragma once
#include <map>
#include <memory>
#include <string>
#include "trace.hpp"

class Cache {
public:
    std::shared_ptr<Document> get(const std::string& name) {
        std::weak_ptr<Document>& entry = entries_[name];
        // 仍存活则通过 lock() 取得新的所有者
        if (std::shared_ptr<Document> alive = entry.lock()) return alive;
        std::shared_ptr<Document> doc = std::make_shared<Document>(name);
        entry = doc;  // 赋值替换过期或空的条目
        ++created_;
        return doc;
    }

    int created() const { return created_; }

    int liveEntries() const {
        int live = 0;
        for (const auto& [name, entry] : entries_) {
            if (!entry.expired()) ++live;
        }
        return live;
    }

    void purge() {
        for (auto it = entries_.begin(); it != entries_.end();) {
            // erase 返回下一个条目的迭代器
            if (it->second.expired()) it = entries_.erase(it);
            else ++it;
        }
    }

    int entries() const { return static_cast<int>(entries_.size()); }

private:
    std::map<std::string, std::weak_ptr<Document>> entries_;
    int created_ = 0;
};
```
