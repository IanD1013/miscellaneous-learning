在 `describe(const Shape& shape)` 内部，调用 `shape.name()` 是根据编译器能看到的类型 `const Shape&` 来解析的，除非 `Shape` 将 `name()` 声明为虚函数（virtual function）。
如果使用初始代码中普通的 `name()`，无论传入什么对象，该调用都是 `Shape::name()`：即使 `Rectangle` 拥有了自己的 `name()`，对 `Rectangle(3, 4)` 调用 `describe` 返回的结果仍然以 `shape` 开头。

一旦声明为 `virtual`，选择就会转移到运行时，并且调用会分派到具体对象上：通过 `const Shape&` 或 `Shape*`，它会运行属于该对象实际类别的版本：

```cpp
class Shape {
public:
    virtual int area() const { return 0; }
    virtual std::string name() const { return "shape"; }
};

class Rectangle : public Shape {
public:
    std::string name() const override { return "rectangle"; }
};
```

`override` 说明符位于参数列表和 `const` 之后，如 `name() const override` 所示。
它本身并不使任何函数变为虚函数；是 `Shape` 中的 `virtual` 起到了这个作用。
它的作用是让编译器确认基类中是否存在一个具有相同名称、相同参数以及相同 `const` 属性的虚函数。

这种检查至关重要，因为“差一点匹配”在 C++ 中是合法的。
如果把 `Rectangle` 的版本写成 `std::string name() { return "rectangle"; }`，忘记了 `const` 且没有 `override`，它依然能编译通过，但会被视为第二个 `name()`，并没有重写任何函数。
对于 `Rectangle rectangle(3, 4);`，这两个调用会返回：

```text
rectangle.name()       "rectangle"
describe(rectangle)    "shape 12"
```

直接在 `Rectangle` 本身调用时，新的 `name()` 会隐藏（hide）`Shape` 的版本：它被优先找到并返回正确的字符串。
而 `describe` 调用的是 `Shape::name() const`，没有任何东西重写了它，因此运行的是 `Shape` 的版本。
当你单独测试该类时它看起来是正确的，只有通过基类访问时才会暴露出 bug。
如果在该行添加 `override`，编译就会在那里中止并报错：

```text
non-virtual member function marked 'override' hides virtual member function
```

### Square 与最近的版本

如果没有编写某个虚函数的派生类，它会使用其上方最近的一个版本。
`Square` 的构造函数已经将其 `Rectangle` 部分构建为 `Rectangle(side, side)`，因此 `Rectangle::area()` 对于正方形来说返回的是正确的数值，`Square` 只需要它自己的 `name()` 即可。
在完成 `Rectangle` 之后，在你编写该 `name()` 之前先运行一下正方形的用例：结果显示的是哪个类的 `name()`？

`Rectangle` 的函数不需要 `virtual` 关键字即可让 `Square` 重写它们。
重写了虚函数的函数本身也是虚函数，因此动态分派会继续沿着继承链向下传递：通过 `const Rectangle&` 访问的 `Square` 仍然会运行 `Square::name()`。

保留初始代码中的 `virtual ~Shape() = default;`；下一节课将解释为什么基类要以这种方式声明其析构函数。

### 在 shapes.hpp 中需要编写的内容

- `Shape`：`area()` 和 `name()` 均声明为虚函数，如上所示。
- `Rectangle`：重写 `area()` 返回宽乘以高，重写 `name()` 返回 `"rectangle"`。
- `Square`：重写 `name()` 返回 `"square"`。
- 将每个重写函数标记为 `override`。
- `describe` 根据 `shape.name()` 和 `shape.area()` 返回名称、一个空格以及面积，例如 `"rectangle 12"`。
  它从不关心传入的具体类是什么；虚函数会做出决定。

`driver.cpp` 中的 `Solution::describeShape(kind, a, b)` 会针对类型 `"rectangle"`、`"square"` 或 `"shape"` 构建一个局部的 `Rectangle(a, b)`、`Square(a)` 或 `Shape`，并将其作为 `const Shape&` 传递给 `describe`。
对于 `"triangle"`，它会构建 `Triangle(a, b)`，这是 `driver.cpp` 从 `Shape` 派生并赋予了自己 `name()` 和 `area()` 的类。
`Triangle` 声明这两者时没有使用 `override`，仅仅是因为 `driver.cpp` 还必须能够针对初始代码进行编译，而在初始代码中 `Shape` 的 `name()` 和 `area()` 尚未变为虚函数，使用 `override` 会导致编译中止。
`shapes.hpp` 从未提及 `Triangle`，但由于 `Shape` 的函数是虚函数，`describe` 对 `Triangle(3, 4)` 返回 `"triangle 6"`：一个稍后在另一个文件中编写的类，无需修改 `describe` 即可正常工作。

### 解答

```cpp
#pragma once
#include <string>

class Shape {
public:
    virtual ~Shape() = default;
    virtual int area() const { return 0; }
    virtual std::string name() const { return "shape"; }
};

class Rectangle : public Shape {
public:
    Rectangle(int width, int height) : width_(width), height_(height) {}
    int area() const override { return width_ * height_; }
    std::string name() const override { return "rectangle"; }

private:
    int width_;
    int height_;
};

class Square : public Rectangle {
public:
    explicit Square(int side) : Rectangle(side, side) {}
    // area() 沿用 Rectangle 的版本
    std::string name() const override { return "square"; }
};

inline std::string describe(const Shape& shape) {
    return shape.name() + " " + std::to_string(shape.area());
}
```
