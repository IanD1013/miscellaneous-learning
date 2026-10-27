`std::shared_ptr<Document>` 是一种可以复制的持有者（owner）。
复制操作不会复制 Document 本身：它只是同一个对象的又一个持有者，并且所有的持有者共享同一个计数，该计数可通过 `use_count()` 获取。
当计数归零时（即在最后一个持有者释放时），Document 会被销毁。

```cpp
std::shared_ptr<Document> a = std::make_shared<Document>("a");
std::shared_ptr<Document> b = a;   // a.use_count() 和 b.use_count() 都为 2
b.reset();                         // b 为空；a.use_count() 为 1
a.reset();                         // 最后一个持有者释放：~Document 在此处运行
```

`std::make_shared<Document>("a")` 将其参数传递给 `Document` 构造函数，并返回一个 use count 为 1 的 `std::shared_ptr<Document>`。
它在单步操作中构建对象并初始化跟踪其持有者的计数，无需在代码中使用 `new`，本代码中的所有共享对象都是通过这种方式创建的。

每次复制都会增加计数：从另一个持有者进行初始化或赋值、对具名持有者执行 `push_back`，或者函数返回一个仍保留在原处的持有者（例如 vector 的某个元素）。
销毁持有者、从 vector 中将其擦除或对其调用 `reset()` 都会使计数减 1。
`reset()` 会结束该持有者的共享所有权；析构函数则等待最后一个持有者释放。
通过 `std::move` 传递持有者会转交其共享所有权并使源对象变为空，因此计数不会改变。
空的 `std::shared_ptr` 报告的 `use_count()` 为 0。
因此，无论 `std::shared_ptr` 对象存在于何处，`use_count()` 统计的都是当前持有这一个 Document 的 `std::shared_ptr` 对象数量；已经分发出去但随后已被销毁或重置的持有者不再计入其中。

`std::unique_ptr` 无法胜任这项工作。
它无法被复制，因此存储 `std::unique_ptr<Document>` 的类有两种选择：向调用者出借裸指针 `Document*` 或引用 `Document&`（两者都无法保证 Document 继续存活），或者使用 `std::move` 将自己的持有权交出。

### 图书馆（The Library）

`trace.hpp`（只读）定义了 `Document`：它由一个名称构造，`name()` 返回该名称，其析构函数会将 `"-"` 和名称追加到 `record()` 返回的记录中。

在 `library.hpp` 中，完善 `Library`，该类将其持有者保存在 `std::vector<std::shared_ptr<Document>> docs_` 中：

- `open(name)` 返回名为 `name` 的 Document 的持有者。
  首次打开某个名称时，应使用 `std::make_shared<Document>(name)` 创建该 Document，切勿使用 `new`。
  打开已经处于打开状态的名称时，应返回图书馆已持有的该 Document 的另一个持有者，并且不创建任何新对象。
  图书馆将一直是每个 Document 的持有者，直到该名称被关闭。
- `close(name)` 移除图书馆对该 Document 的持有者，并保留其他所有条目不变。
  仍然持有该 Document 的调用者将使其保持存活。
  关闭未打开的名称不会改变任何内容。
- `openCount()` 返回图书馆拥有的 Document 数量，因此先后打开 `"a"`、`"b"`、`"a"` 后，其值保持为 2。

`driver.cpp` 通过两个将观察到的结果以字符串形式返回的函数来使用该类。

`useCounts(holders)` 打开 `"a"` `holders` 次，将每次返回的持有者保存在 vector `held` 中，然后再打开一次 `"a"` 保存到 `first` 中。
随后依次调用 `close("a")`、`held.clear()` 和 `first.reset()`，并在每一步之后读取一个值。
以下是没有持有者和有十个持有者时的输出情况：

```text
                                     [first.use_count(), close("a") 之后, held.clear() 之后的 record, first.reset() 之后的 record]
useCounts(0)                         ["2", "1", "", "-a"]
useCounts(10)                        ["12", "11", "", "-a"]
```

在没有 holders 的情况下计数已经是 2，因为 `docs_` 和 `first` 都持有该 Document。
有十个 holders 时计数为 12：`held` 中的十个、图书馆的以及 `first`，它们都是同一个 Document 的持有者。
在 `first` 仍然持有它的情况下，清空 `held` 不会销毁任何对象。
如果 `close` 错误地将图书馆的持有者留在了 `docs_` 中，会导致 `useCounts(0)` 返回 `["2", "2", "", ""]`：此时 `first.reset()` 并不是最后一个持有者，因此 record 仍为空。

`libraryRun(opens, closes, keep)` 打开 `opens` 中的每个名称，接着除非 `keep` 为 `""`，否则在图书馆外部保留 `kept = library.open(keep)`，然后关闭 `closes` 中的每个名称。
`kept` 声明在 Library 之后，因此它会先被析构。
仅在 `keep` 上有所不同的两次运行：

```text
                                     [opens 之后的 openCount(), closes 之后, closes 之后的 record, kept.use_count(), 最后的 record]
libraryRun({"a", "b"}, {"b"}, "b")   ["2", "1", "", "1", "-b-a"]
libraryRun({"a", "b"}, {"b"}, "")    ["2", "1", "-b", "0", "-b-a"]
```

两者均以 `"-b-a"` 结束，但 `"b"` 销毁的时机不同。
在有 `kept` 持有的情况下，`close("b")` 将其计数降至 1 且不销毁任何对象，`"b"` 会在最后随 `kept` 一起销毁。
在没有 `kept` 的情况下，图书馆的持有者是唯一的持有者，因此在 `close` 期间就会写入 `"-b"`。

### 解答

```cpp
#pragma once
#include <memory>
#include <string>
#include <vector>
#include "trace.hpp"

class Library {
public:
    std::shared_ptr<Document> open(const std::string& name) {
        // 已打开则返回图书馆持有的那个 Document 的又一个持有者
        for (const std::shared_ptr<Document>& doc : docs_) {
            if (doc->name() == name) return doc;
        }
        docs_.push_back(std::make_shared<Document>(name));
        return docs_.back();
    }

    void close(const std::string& name) {
        // 只移除图书馆自己的持有者
        std::erase_if(docs_, [&](const std::shared_ptr<Document>& doc) { return doc->name() == name; });
    }

    int openCount() const { return static_cast<int>(docs_.size()); }

private:
    std::vector<std::shared_ptr<Document>> docs_;
};
```
