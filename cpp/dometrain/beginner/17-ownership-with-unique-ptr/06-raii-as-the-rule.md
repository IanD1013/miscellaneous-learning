RAII 是本章一直在构建的概念名称：构造函数获取对象所需的一切资源，而析构函数将其释放。
程序中没有任何语句显式调用 release。
关于对象何时销毁，语言本身的规则构成了清理计划，并且这些规则是固定的：

- 局部变量按其声明顺序的逆序进行销毁。
- 对象的成员在其析构函数体执行完毕后销毁，同样按其声明顺序的逆序进行。
- `std::unique_ptr` 成员在自身被销毁时释放其所拥有的对象。

综合来看，任何作用域的后半部分看起来就像是前半部分的倒序执行。

### 读取记录

`Tracked` 在其构造函数中追加 `+` 及其名称，并在 `~Tracked()` 中追加 `-` 及其名称。
这两个标记都会写入同一个 `std::string`（通过借用的 `std::string *` 访问），因此所有三个对象都会写入同一条记录中。
`Holder` 包含两个成员：一个普通的 `Tracked` 和一个 `std::unique_ptr<Tracked>`；`Group` 包含一个 `Holder` 和一个独立的 `Tracked`。
`releaseOrder` 位于 `driver.cpp` 中，是固定的并在读取你的文件后执行：它声明记录，打开一个内部作用域，在其中构建一个 `Group`，将 `|` 作为该作用域的最后一条语句追加，并在大括号结束离开作用域后返回该记录。
`|` 之后的所有标记都是由无人调用的析构函数写入的。

### 选择两种顺序

三次构造必须按照名称到达的顺序进行，这由两个决定来确定：`Holder` 的两个成员的声明顺序，以及 `Group` 的两个成员的声明顺序。
重新调整每个 private 部分中的声明顺序，然后将该类的初始化列表调整为相同的顺序。
无论初始化列表如何给出，成员都会按照声明顺序构建，因此不一致的列表描述的是一种从未发生的顺序。
由 `make_unique` 构建的被拥有的 `Tracked` 与 `Holder` 的生命周期一样长；构造函数执行完毕并不会结束它。

`names[0]` 和 `names[1]` 传递给 `Holder`，`names[2]` 传递给独立的 `Tracked`，因此 `{"ann", "bob", "cat"}` 会返回 `+ann+bob+cat|-cat-bob-ann`，作为单个字符串进行比对。

- 三个相同的名称会产生 `+dot+dot+dot|-dot-dot-dot`，因为每个标记来自于位置而不是名称。
- 空名称仅写入其符号而无其他内容：`{"a", "", "z"}` 会产生 `+a++z|-z--a`。
- 如果名称数量不恰好是三个，则返回 `invalid` 且不构建任何内容；该守卫逻辑位于固定文件中。
- `new` 和 `delete` 被禁用，`Tracked` 是固定的夹具类无需修改，`releaseOrder` 也是固定的。
  `std::unique_ptr<Tracked>` 和 `std::make_unique<Tracked>(` 都必须出现在你的解答中，以便被拥有的成员保持其所有者。
  `Holder` 和 `Group` 是你需要编辑的全部内容，并且每个标记都来自构造函数或析构函数，而不是显式调用。

### 解答

```cpp
#include <memory>
#include <string>

// 提供的夹具类：保持 Tracked 原样不动。它在构建时写入一个标记，释放时再写入一个，
// 写入的记录是借用的而不是拥有的。
class Tracked {
public:
    Tracked(const std::string &name, std::string *record)
        : name_(name), record_(record) {
        if (record_ != nullptr) {
            *record_ += "+";
            *record_ += name_;
        }
    }

    ~Tracked() {
        if (record_ != nullptr) {
            *record_ += "-";
            *record_ += name_;
        }
    }

private:
    std::string name_;
    std::string *record_;
};

class Holder {
public:
    Holder(const std::string &first, const std::string &second, std::string *record)
        : plain_(first, record), held_(std::make_unique<Tracked>(second, record)) {
    }

private:
    // 这两个成员的声明顺序决定了哪一个先被释放：先声明的先构建、后释放。
    Tracked plain_;
    std::unique_ptr<Tracked> held_;
};

class Group {
public:
    Group(const std::string &first, const std::string &second, const std::string &third, std::string *record)
        : holder_(first, second, record), loose_(third, record) {
    }

private:
    // 在上一层，这两个成员的声明顺序同样决定了构建和释放的顺序。
    Holder holder_;
    Tracked loose_;
};
```
