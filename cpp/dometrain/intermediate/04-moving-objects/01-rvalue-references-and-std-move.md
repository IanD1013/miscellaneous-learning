运行初始代码，`driver.cpp` 中的所有七次调用都会返回 `"lvalue"`。
`categories.hpp` 中有一个 `category` 重载，其 `const std::string&` 参数可以绑定到任何字符串表达式：变量、专门为调用构建的字符串、拼接的结果。
仅凭这一个重载，`category` 无法区分调用者仍可继续使用的字符串与即将消失的字符串。

### 左值与右值

实参属于哪一种取决于表达式，而非其类型。
给定 `std::string named = "x";`，`named` 和 `named + "!"` 都是 `std::string`。
`named` 是左值（lvalue）：它指代一个生命周期超出该表达式的对象，因此下一条语句可以再次读取它。
`named + "!"` 是右值（rvalue）：在 `answer = category(named + "!");` 中，它创建了一个临时对象，即一个没有名称的字符串，在该语句结束时被销毁。
`std::string("x")` 也以同样的方式创建临时对象。
变量名或参数名无论其声明类型是什么，始终都是左值，因此 `const std::string& ref = named;` 中的 `ref` 也是左值。

### 右值引用重载

类型为 `std::string&&` 的参数是右值引用，它只能绑定到右值。
在 `const std::string&` 重载旁边添加一个接受右值引用的重载，编译器就会在每次调用时在它们之间做出选择。
非常量右值（如 `named + "!"`）可以绑定到任一参数，而重载决议更倾向于选择右值引用。
左值根本无法绑定到 `std::string&&`，因此它会保持匹配 `const std::string&`。
在 vector 上的同类配对示例如下：

```cpp
std::string kind(const std::vector<int>& values) { return "kept"; }
std::string kind(std::vector<int>&& values) { return "temporary"; }

std::vector<int> scores = {1, 2};
kind(scores);                  // "kept"
kind(std::vector<int>{3, 4});  // "temporary"
```

这种偏好仅在两个引用参数之间进行抉择。
如果第二个重载改为按值传递字符串，例如 `category(std::string text)`，则无法通过编译：对于每个实参（无论是临时对象还是 `named`），绑定 `const std::string&` 与初始化一个新字符串是同等良好的匹配，因此编译器会在每次调用 `category` 时报错 `call to 'category' is ambiguous`。

### std::move

`std::move(x)` 来自 `<utility>`，而 `categories.hpp` 已经通过 `#include <utility>` 包含了它。
它是一种类型转换：将 `x` 转换为同类型的右值，除此之外不做任何事情。
`category(std::move(named))` 会调用右值重载，但既没有构建新字符串，也没有清空字符串。
由于 `category` 接受引用，因此它接收的是 `named` 本身，随后 `named` 仍然保存着 `"x"`。

该转换保留了 `const` 属性。
对于 `const std::string fixed = "x";`，`std::move(fixed)` 是一个常量右值（const rvalue），而 `std::string&&` 会拒绝它，因为如果允许绑定，就会让函数能够修改被声明为 `const` 的字符串。
因此它会匹配到 `const std::string&`，后者可以接受任何字符串。
`category` 返回的字符串告诉你执行的是哪个重载，而不是其实参是什么，因此在这里一个右值会导致 `category` 返回 `"lvalue"`。

具名参数也不例外。
`forwardCategory` 通过 `std::string&& text` 接收一个临时对象，但在函数内部 `text` 是一个名称，因此它是一个左值，初始代码中的 `category(text)` 会匹配到 const 重载。

### 七种形式

`driver.cpp` 中的 `Solution::categoryOf(form)` 如上所述设置了 `named`、`fixed` 和 `ref`，对该形式进行调用并返回调用结果。

1. `category(named)`
2. `category(std::string("x"))`
3. `category(std::move(named))`
4. `category(named + "!")`
5. `category(std::move(fixed))`
6. `forwardCategory(std::string("x"))`
7. `category(ref)`

完成代码后，其中四个将返回 `"rvalue"`。
在运行之前，试着把它们找出来。

在 `categories.hpp` 中，在初始代码标记的位置添加返回 `"rvalue"` 的 `category(std::string&& text)`，并保持 `const std::string&` 重载返回 `"lvalue"`。
然后在 `forwardCategory` 中使用 `std::move`，以便形式 6 能够调用新的重载，同时保持其函数体仅包含一条返回 `category` 调用的 `return` 语句。
`forwardCategory` 不是类成员，因此其函数体内的 `category` 调用只能看到在该文件中之前声明的重载。
这就是为什么新的重载要放在 `forwardCategory` 上方的原因。

### 解答

```cpp
#pragma once
#include <string>
#include <utility>

inline std::string category(const std::string& text) { return "lvalue"; }

// 右值引用重载：只绑定右值
inline std::string category(std::string&& text) { return "rvalue"; }

// text 是具名形参（左值），用 std::move 转回右值
inline std::string forwardCategory(std::string&& text) { return category(std::move(text)); }
```
