`static` 成员属于类本身，而不是属于任何具体的对象。
第 15.1 课曾提到，到目前为止所编写的每个成员都属于单个对象，而这个关键字则代表了特例：一个变量支撑着整个类，在构建第一个对象之前就已经存在，并且每个对象都会读写这同一个变量。

```cpp
class Machine {
public:
    static int limit() {
        return limit_;
    }

private:
    static int limit_;
};

int Machine::limit_ = 10;
```

这两处对 `limit_` 的提及承担着不同的职责。
在类内部，`static int limit_;` 声明了该成员并仅止于此：它提供了类型和名称，并没有创建任何内容。
该变量是由类下方的定义所创建的，写在文件作用域中，依次读取类型、类名、成员名以及它的初始值。
如果跳过这行代码，文件仍然可以通过编译，因为编译器只需要声明就足够了，但随后构建会在链接时因 `Machine::limit_` 存在未定义符号（undefined symbol）而失败，因为没有任何文件定义过它。

`limit()` 同样是 `static` 的，因此可以在没有具体对象的情况下作为 `Machine::limit()` 调用。
这与修饰 `createdCount` 的关键字相同，运行器正是通过这种方式在无需构建 `Solution` 的情况下访问待评分函数的。

### 属于类的计数

已经构造了多少个对象描述的是类的历史，而不是任何单一对象，因此普通成员并不适合存放它：每个对象只会对自己进行计数。
无论对象在哪里构建，构造函数都会为每个对象运行一次，因此写在构造函数中的 `created_ += 1;` 会对该构造函数构建的每个对象进行计数。

初始代码中的 `Tracked` 包含一个空构造函数和一个返回 0 的 `static int created()`。
为它添加一个私有的 `static int created_;`，在构造函数中递增计数，从 `created()` 中返回该成员，并在类外部将其定义一次：`int Tracked::created_ = 0;`。
`createdCount` 已在您无法编辑的第二个文件中为您编写好：它会构建 `howMany` 个对象，然后向 `Tracked::created()` 查询该数量，因此该计数除了来自类内部之外别无出处。

每个测试用例都会从头重新运行程序，因此在每个用例中计数都从 0 开始，答案就是该次调用所构建的对象数量，而不包含更早的内容。
`howMany` 最大为 50，而 0 或任何负数都不会构建任何对象并返回 0。

### 解答

```cpp
class Tracked {
public:
    Tracked() {
        // 每构造一个对象，类级别的计数加 1
        created_ += 1;
    }

    static int created() {
        // 返回属于整个类而不是某个对象的计数
        return created_;
    }

private:
    // 静态成员在类内声明，在类下方定义一次
    static int created_;
};

int Tracked::created_ = 0;
```
