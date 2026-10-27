关键字 `struct` 通过一系列成员声明来构建一个新类型：

```cpp
struct Point {
    int x;
    int y;
};

Point origin;
origin.x = 3;
origin.y = 4;
int sum = origin.x + origin.y;
```

`struct Point {` 命名了该类型并开启其定义，而 `};` 则结束该定义。
与函数体的闭合大括号不同，这里的大括号后面跟着一个分号，因为整个定义本身是一条声明语句。
在大括号之间，每一行都像声明局部变量一样声明一个成员，拥有自己的类型、名称和分号，并且成员会保持其声明时的顺序。

结构体定义本身并不占用任何存储空间。
它描述了该类型的每个变量包含什么内容，而 `Point origin;` 这一行才真正创建了两个 int。
变量与成员名称之间的点号用于访问该变量的对应成员，因此 `origin.x` 的行为就像普通的 int 一样：可以对其赋值、进行比较或进行乘法运算。
点号的左侧必须是一个变量，因为成员存在于变量中，而不是存在于定义中。

`Point origin;` 还会使两个成员处于未定义值的状态。
在向其写入任何内容之前读取成员，会返回该内存中原本残留的数据，因此每个成员都应先写入再读取。

`totalPrice` 接收一个 `int unitPrice` 和一个 `int quantity`，并返回一个 int。

- 为 `Part` 提供两个 int 成员：`unitPrice` 和 `quantity`，每行一个声明。
- 在 `totalPrice` 内部声明 `Part`，并将变量命名为 `part`，然后将两个参数分别写入其成员中。
  本练习要求的两次读取形式分别为 `part.unitPrice` 和 `part.quantity`。
- 根据这些成员保存的值计算总价。
  直接使用参数相乘的四种写法已被禁用：`unitPrice * quantity`、`quantity * unitPrice`，以及去除空格后的对应写法，因此乘法运算必须通过结构体成员来进行。
- 负的单价或负的数量应返回 -1，该判断应在进行任何乘法运算之前完成。
- 任意一边为零都是一个有效的结果而非拒绝处理：单价为 25 且数量为 0 时总价为 0。
- 两个参数的范围均在 -1000 到 1000 之间，因此总价始终不会超出 int 的范围。

## 解答

```cpp
struct Part {
    // 两个 int 成员：单价和数量
    int unitPrice;
    int quantity;
};

struct Solution {
    static int totalPrice(int unitPrice, int quantity) {
        // 声明 Part 并用参数填充，再根据成员计算总价
        Part part;
        part.unitPrice = unitPrice;
        part.quantity = quantity;
        if (part.unitPrice < 0 || part.quantity < 0) {
            return -1;
        }
        return part.unitPrice * part.quantity;
    }
};
```
