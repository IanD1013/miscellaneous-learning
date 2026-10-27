对文本的每次更改都是一个可以自行应用（apply）和自行撤销（reverse）的 `Command`。
`Editor` 将其已运行的命令保存在一个由 `std::unique_ptr<Command>` 作为所有者的栈上，在调用 `undo()` 时将最新的命令移动到第二个栈上，并在调用 `redo()` 时将其移回。

### 自行撤销的命令

`apply` 和 `undo` 是 `Command` 的纯虚函数，它们通过引用接收文本。
三个 `final` 类 `Append`、`EraseLast` 和 `Upper` 都重写了这两个函数，`Editor` 在调用它们时无需询问它持有的是哪种命令。
保留虚析构函数：各个栈通过 `std::unique_ptr<Command>` 销毁每个命令，只有虚析构函数 `~Command` 才能同时执行 `~Append`。

`Upper` 和 `EraseLast` 无法仅从当前文本推导出旧文本。
`Upper` 将 `"Ab"` 转换为 `"AB"`，而将其转为小写则会得到 `"ab"`。
因此，它们中的每一个在应用时都会保存被更改的内容，其 `undo` 会将完全相同的内容恢复回去。
`Append` 则不需要保存任何内容：它的后缀指明了要从末尾移除多少个字符。

- `Append` 将其后缀追加到文本末尾。
- `EraseLast` 移除末尾的 `count` 个字符；当文本较短时，移除整个文本。
  计数无法表明要恢复什么内容：从 `"abc"` 中擦除 5 个字符会移除 3 个字符，而 `undo` 必须恢复 `"abc"`。
- `Upper` 将 `a` 到 `z` 转换为大写，并保留所有其他字符不变。

### 在栈之间移动所有者

`run` 应用该命令并将其推入 `done_`。
执行新命令还会使所有已撤销的命令变得不可访问：在执行 `append "a"`、`undo`、`append "b"` 之后，重做 `"a"` 会将其添加到它从未应用过的文本中，因此 `redo()` 将没有任何可重做的内容。

`undo()` 将最新的命令从 `done_` 移动到 `undone_` 并将其撤销。
`redo()` 将最新的命令从 `undone_` 移回 `done_` 并重新应用它。
每个函数在成功时返回 `true`，或者在其栈为空时返回 `false` 且不更改任何内容。
请先测试 `empty()`，因为在空的 `std::stack` 上调用 `top()` 和 `pop()` 是未定义行为。

每个命令在同一时间仅由一个栈拥有：使用 `std::move` 将其 `std::unique_ptr` 从一个栈移动到另一个栈，切勿使用 `release()` 将命令从其 `std::unique_ptr` 中取出。

### `driver.cpp` 返回的内容

`Solution::edit` 接收两个长度相同的列表，即操作名称及其参数，并在一个初始文本为空的 `Editor` 上重放它们：`append` 向 `run` 传递 `std::make_unique<Append>(argument)`，`erase` 传递带计数的 `EraseLast`，`upper` 传递 `Upper`，而 `undo` 和 `redo` 则调用 `Editor` 自身的方法。
它返回两个字符串：

- `[0]`：最终的文本
- `[1]`：返回 `false` 的 `undo()` 或 `redo()` 调用的次数

传入 `["append","erase","undo","undo","undo"]` 与 `["xyz","2","","",""]` 会返回 `["","1"]`。
擦除操作留下 `"x"`，第一个撤销操作恢复 `"xyz"`，第二个撤销操作移除追加的内容，第三个撤销操作发现没有可撤销的内容。

`Solution::applyThenUndo(op, argument, text)` 以相同的方式构建单个 `append`、`erase` 或 `upper` 命令，但不使用 `Editor`。
它在 `text` 上调用命令的 `apply`，然后调用其 `undo`，并返回每次操作后的文本：`applyThenUndo("erase", "2", "xyz")` 返回 `["x","xyz"]`。

### 解答

```cpp
#pragma once
#include <algorithm>
#include <memory>
#include <stack>
#include <string>

class Command {
public:
    virtual ~Command() = default;
    virtual void apply(std::string& text) = 0;
    virtual void undo(std::string& text) = 0;
};

class Append final : public Command {
public:
    explicit Append(std::string suffix) : suffix_(std::move(suffix)) {}
    void apply(std::string& text) override { text += suffix_; }
    // 后缀长度就是要从末尾移除的字符数
    void undo(std::string& text) override { text.erase(text.size() - suffix_.size()); }
private:
    std::string suffix_;
};

class EraseLast final : public Command {
public:
    explicit EraseLast(int count) : count_(count) {}
    void apply(std::string& text) override {
        // 文本较短时移除整个文本，并保存被移除的内容
        std::size_t n = std::min(text.size(), static_cast<std::size_t>(count_));
        erased_ = text.substr(text.size() - n);
        text.erase(text.size() - n);
    }
    void undo(std::string& text) override { text += erased_; }
private:
    int count_;
    std::string erased_;
};

class Upper final : public Command {
public:
    void apply(std::string& text) override {
        // 保存旧文本，undo 时原样恢复
        before_ = text;
        for (char& c : text) {
            if (c >= 'a' && c <= 'z') c = static_cast<char>(c - 'a' + 'A');
        }
    }
    void undo(std::string& text) override { text = before_; }
private:
    std::string before_;
};

class Editor {
public:
    void run(std::unique_ptr<Command> command) {
        command->apply(text_);
        done_.push(std::move(command));
        // 新命令使已撤销的命令不可再重做
        undone_ = {};
    }
    bool undo() {
        if (done_.empty()) return false;
        std::unique_ptr<Command> command = std::move(done_.top());
        done_.pop();
        command->undo(text_);
        undone_.push(std::move(command));
        return true;
    }
    bool redo() {
        if (undone_.empty()) return false;
        std::unique_ptr<Command> command = std::move(undone_.top());
        undone_.pop();
        command->apply(text_);
        done_.push(std::move(command));
        return true;
    }
    const std::string& text() const { return text_; }
private:
    std::string text_;
    std::stack<std::unique_ptr<Command>> done_;
    std::stack<std::unique_ptr<Command>> undone_;
};
```
