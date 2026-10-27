起始代码中的 `buildChain({"a", "b", "c"})` 构建了一个以 `a` 为根节点、以 `c` 为底部的链。
驱动程序将每个节点保存在一个 vector 中，并保留了根节点的第二个所有者。
它首先清空 vector，最后释放根节点，并在每一步之后记录状态：

```text
[从 c 出发的路径, vector 清空后的 record, 根节点释放后的 record]
["c<b<a", "", ""]
```

到第三个值时，驱动程序已经释放了每个节点（包括根节点），然而记录（其中每个 `~TreeNode` 都会通过 `trace.hpp` 中的 `note()` 记录 `"-"` 及其名称）仍然为空。
没有任何对象被销毁。

`attach(parent, child)` 双向连接两个节点：父节点在 `children_` 中持有子节点的所有者，而子节点在 `parent_` 中持有其父节点的所有者。
双向都使用 `std::shared_ptr` 时，每个节点都由与其相邻的节点所拥有。
一旦驱动程序释放所有节点，`a` 的引用计数仍为 1（因为 `b` 的 `parent_` 持有着它），`c` 的引用计数也仍为 1（因为 `b` 的 `children_` 持有着它），而 `b` 的引用计数为 2。
这是一个循环引用（reference cycle）：链中每个节点的引用计数都被另一个节点保持在大于零的状态，因此没有任何计数归零，析构函数不会运行，也不会有任何机制报告内存泄漏。

### 哪个链接不再拥有所有权

为了打破循环引用，必须让一个方向仅进行观察而不是拥有所有权，而保留所有权的方向将决定谁使谁存活。
`std::shared_ptr` 可以隐式转换为 `std::weak_ptr`，因此无论哪个成员变量变成弱引用，`attach` 都能保持不变并正常编译。
使用相同的三个名称，依次将每个链接设置为弱引用：

```text
                                    [从 c 出发的路径, vector 清空后的 record, 根节点释放后的 record]
children_ 为弱引用，parent_ 拥有    ["c<b<a", "-c-b", "-c-b-a"]
parent_ 为弱引用，children_ 拥有    ["c<b<a", "", "-a-b-c"]
```

当 `children_` 为弱引用时，每个子节点都会使其父节点存活，而除了驱动程序的 vector 外没有任何东西拥有 `c`。
一旦 vector 被清空，尽管根节点仍然被持有，`b` 和 `c` 就会立即被销毁，并且 `-c` 最先出现，因为 `c` 的 `parent_` 会一直拥有 `b` 直到 `c` 被销毁。

当 `parent_` 为弱引用时，根节点的第二个所有者通过 `children_` 让整条链保持存活。
当驱动程序释放它时，`a` 的引用计数降为零，`~TreeNode` 的函数体记录 `-a`，接着销毁 `children_` 会释放 `b`，使 `b` 的计数随之归零，而 `b` 也会对 `c` 执行相同的操作。

如果两个链接都是弱引用，那么在 vector 被清空后，又有什么能拥有 `b` 和 `c` 呢？
在你的通过版本中把 `children_` 也设为弱引用试试，第二个值就会说明一切。

### 使用 lock() 向上回溯

一旦 `parent_` 变成弱引用，起始代码中的 `pathToRoot` 就会编译失败，因为 `std::weak_ptr<TreeNode>` 不能隐式转换回 `std::shared_ptr<TreeNode>`。
在向上回溯的途中，`parent_.lock()` 会在两种情况下返回一个空的 `std::shared_ptr`。
根节点的 `parent_` 从未被赋值，因此回溯在此处终止。
而在 `childOutlivesRoot` 中，在依然持有 `b` 的同时释放了 `a`：`a` 被销毁，`b` 的 `parent_` 已过期，从 `b` 开始的路径仅为 `"b"`。

`std::shared_ptr<TreeNode>(parent_)` 也能编译，但它并不是 `lock()` 的另一种写法：从一个空或已过期的 `std::weak_ptr` 构造 `std::shared_ptr` 是一种会导致程序终止的错误，而每次向上回溯最终都会到达根节点的空链接。

使用原始指针 `TreeNode*` 作为反向链接也能打破循环，但它无法感知其父节点是否已被销毁：在 `childOutlivesRoot` 中，它仍会指向已被销毁的 `a`，导致 `pathToRoot` 读取一个已不存在的节点。
请使用 `std::weak_ptr`。

### 需要编写的内容

在 `tree.hpp` 中，打破循环引用，使得每个父节点保持其子节点的存活：第二个值保持为空，并且释放根节点时会自顶向下销毁整条链。
通过修改成员变量的类型来打破循环引用，因此不要添加清空 `children_` 或 `parent_` 的代码。
然后重写 `pathToRoot(node)`，使其返回 `node` 的名称，后跟 `"<"` 以及通过 `lock()` 获取到的每个祖先节点的名称：例如对于 `c` 返回 `"c<b<a"`，对于没有父节点的节点返回 `"solo"`。

`driver.cpp` 中的 `Solution::buildChain(names)` 会使用 `std::make_shared` 为每个名称创建一个节点，并将每个节点附加到其前一个节点上，因此 `names[0]` 是根节点，并返回该链上述的三个值。
`Solution::childOutlivesRoot()` 将 `b` 附加到 `a`，在持有 `b` 的同时释放 `a`，并返回 `pathToRoot(b)`、记录以及 `b` 释放后的记录。

### 解答

```cpp
#pragma once
#include <memory>
#include <string>
#include <utility>
#include <vector>
#include "trace.hpp"

class TreeNode {
public:
    explicit TreeNode(std::string name) : name_(std::move(name)) {}
    ~TreeNode() { note("-" + name_); }
    const std::string& name() const { return name_; }

private:
    std::string name_;
    std::weak_ptr<TreeNode> parent_;  // 只观察父节点，打破循环引用
    std::vector<std::shared_ptr<TreeNode>> children_;  // 父节点拥有子节点

    friend void attach(const std::shared_ptr<TreeNode>& parent, const std::shared_ptr<TreeNode>& child);
    friend std::string pathToRoot(const std::shared_ptr<TreeNode>& node);
};

inline void attach(const std::shared_ptr<TreeNode>& parent, const std::shared_ptr<TreeNode>& child) {
    child->parent_ = parent;
    parent->children_.push_back(child);
}

inline std::string pathToRoot(const std::shared_ptr<TreeNode>& node) {
    std::string path = node->name();
    // 根节点或已销毁的父节点会让 lock() 返回空
    std::shared_ptr<TreeNode> current = node->parent_.lock();
    while (current) {
        path += "<" + current->name();
        current = current->parent_.lock();
    }
    return path;
}
```
