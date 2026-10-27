使用初始代码时，`sharedByThumbnails(10)` 返回 `["1", "0", "-img", "-img"]`。
驱动程序从其 `img` 构建了十个缩略图，但 `img.use_count()` 仍然为 1，并且一旦驱动程序重置 `img`，记录就会显示 `-img`：Image 已经消失，而所有十个缩略图却仍然指向它。
`Thumbnail` 保存了 `image.get()`，这是一个借用的 `const Image*`，因此它从未成为所有者。
`Importer` 则走向了另一个极端。
它将其暂存的 Image 保存在 `std::shared_ptr` 中，因此 `publish()` 返回了第二个所有者，而不是将 Image 移交出去，并且编译器允许你复制 `Importer`。
面积总和为 0 仅仅是因为初始代码的 `measure` 返回了 0。

修复方法是仅赋予每个持有者其任务所需的最低所有权：仅读取的代码无需所有权，单个对象拥有 Image 时采用独占所有者，仅在多个持有者必须保持其存活时才使用共享所有者。
只读的 `trace.hpp` 中的 `Image` 接受宽度、高度和名称，具有 `width()` 和 `height()`，不可复制，且其析构函数会将 `-` 及其名称追加到记录中。

### 仅读取的代码采用引用

`measure` 读取两个数字且不保留任何内容，因此其参数保持为 `const Image&`。
无论 Image 的所有权归属如何，引用都可以绑定到它：驱动程序对 `*result`（由 `std::shared_ptr` 拥有的 Image）以及 `local`（完全没有所有者的栈上 Image）调用 `measure`。
如果改为要求所有者，即使用 `const std::shared_ptr<const Image>&`，则两个调用都无法编译：`no matching function for call to 'measure'`。
若按值传递 `Image`，`images.hpp` 会报告 `call to deleted constructor of 'Image'`。

### 独占所有者持有 std::unique\_ptr

在发布之前，`Importer` 暂存的 Image 仅属于该 `Importer`，因此 `Importer` 是其独占所有者，并持有 `std::unique_ptr<Image>`。
单凭这一点就能阻止复制。
根据零法则（rule of zero），`Importer` 不声明五个特殊成员函数中的任何一个，并且由于其成员无法复制，编译器将 `Importer` 的拷贝构造函数定义为已删除（deleted），同时仍然生成其移动操作。
驱动程序使用类型特征 `std::is_copy_constructible<Importer>` 向编译器查询这一点。
如果使用 `std::shared_ptr` 成员，`Importer b = a;` 可以编译通过，并留下两个各自都可以发布同一暂存 Image 的 Importer。

### 将独占所有者移交给共享所有者

`std::unique_ptr` 右值可以转换为 `std::shared_ptr`。
新的 `std::shared_ptr` 接管该对象，引用计数（use count）为 1，并使 `std::unique_ptr` 变为空：

```cpp
std::unique_ptr<Image> draft = std::make_unique<Image>(4, 5, "d");
auto shared = std::shared_ptr<Image>(std::move(draft));
```

`draft` 是一个具名变量，因此如果没有 `std::move`，该转换将需要复制 `std::unique_ptr`，而它是不可复制的。
被移动后的 `std::string` 或 `std::vector` 处于有效但未指定（valid but unspecified）的状态。
而被移动后的 `std::unique_ptr` 保证为空，因此在第二行之后 `draft == nullptr` 为 true。
这就是为什么在 `publish()` 之后 `hasStaging()` 具有明确定义的结果，也是为什么第二次调用 `publish()` 会返回一个空的 `std::shared_ptr`。

这种转换是单向的。
`std::shared_ptr` 所指向的对象可能拥有其他所有者，因此无法从 `std::shared_ptr` 创建 `std::unique_ptr`。

### 共享生命周期的共享所有者

缩略图真正共享同一个 Image：驱动程序在它们仍在使用 Image 时放弃了 `img`，因此 Image 必须存活到最后一个缩略图销毁为止。
这是 `std::shared_ptr<const Image>` 的用武之地，它是一个可以读取 Image 但不能修改它的共享所有者。
复制 `std::shared_ptr` 会增加一个所有者，因此 `Thumbnail` 通过复制或移动传入的 `std::shared_ptr` 来加入 `img` 的所有者行列。
`image.get()` 返回的是一个不拥有任何所有权的裸指针。

### images.hpp 需要完成的工作

保持 `images.hpp` 中的所有签名不变：

- `measure(image)` 返回宽度乘以高度。
  驱动程序将每条边保持在 0 到 10000 之间，因此最大面积 100000000 可以容纳在 `int` 中。
- `Thumbnail` 及其副本保持其 Image 存活，直到它们中的最后一个被销毁，且 `area()` 返回该 Image 的 `measure` 结果。
- `Importer` 将其暂存的 Image 保存在使用 `std::make_unique`（而非 `new`）创建的 `std::unique_ptr<Image>` 中，且不可复制。
  `publish()` 将该 Image 作为其唯一所有者返回在 `std::shared_ptr` 中，并使 `Importer` 变为空，`hasStaging()` 会报告这一点。

`sharedByThumbnails(count)` 使用 `std::make_shared<const Image>(2, 3, "img")` 创建 `img`，并由此创建 `count` 个缩略图（第一个缩略图，然后是其副本），对它们的面积求和，重置 `img`，然后销毁缩略图。
第三个值为空表示 Image 在重置后存活了下来。

```text
各位置                  [img.use_count(), 面积总和, reset 之后的 record, 缩略图销毁后的 record]

                        初始代码                      修复后
sharedByThumbnails(10)  ["1", "0", "-img", "-img"]    ["11", "60", "", "-img"]
sharedByThumbnails(0)   ["1", "0", "-img", "-img"]    ["1", "0", "-img", "-img"]
```

`publishFlow()` 构建 `Importer importer(3, 4, "p")` 并调用两次 `publish()`；1 表示是。
中间行是持有 `std::shared_ptr` 并在 `publish()` 中将其移动出去的 `Importer`（且已修复 `measure`）：与修复后的行相比，仅最后一个值不同。

```text
各位置                       [之前的 staging, 之后的 staging, result.use_count(), measure(*result), 第二次 publish 为空, Importer 可复制]

初始代码                     [1, 1, 2, 0, 0, 1]
std::shared_ptr 被移出       [1, 0, 1, 12, 1, 1]
修复后                       [1, 0, 1, 12, 1, 0]
```

`measureLocal(width, height)` 测量指定尺寸的栈上 Image。

### 解答

```cpp
#pragma once
#include <memory>
#include <string>
#include <utility>
#include "trace.hpp"

inline int measure(const Image& image) { return image.width() * image.height(); }

class Thumbnail {
public:
    // 加入 Image 的共享所有者
    explicit Thumbnail(std::shared_ptr<const Image> image) : image_(std::move(image)) {}
    int area() const { return measure(*image_); }

private:
    std::shared_ptr<const Image> image_;
};

class Importer {
public:
    Importer(int width, int height, std::string name)
        : staging_(std::make_unique<Image>(width, height, std::move(name))) {}
    bool hasStaging() const { return staging_ != nullptr; }
    // 把独占所有者移交给共享所有者，staging_ 变为空
    std::shared_ptr<Image> publish() { return std::shared_ptr<Image>(std::move(staging_)); }

private:
    std::unique_ptr<Image> staging_;  // 独占所有者，使 Importer 不可复制
};
```
