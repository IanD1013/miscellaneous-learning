写在成员函数参数列表之后、函数体之前的 `const` 是一种承诺，保证运行该函数不会改变对象：

```cpp
class Meter {
public:
    Meter(int reading) : reading_(reading) {}

    int reading() const {
        return reading_;
    }

    int halves() const {
        return reading() / 2;
    }

private:
    int reading_;
};

int readHalves(const Meter &meter) {
    return meter.halves();
}
```

在带有该承诺的函数内部，每个成员都是只读的，因此在那里编写 `reading_ = 0;` 会在您自己的代码行处被拒绝。
它仍然可以声明局部变量并进行任何所需的算术运算，也可以调用自身对象的其他函数，但只能调用做出了相同承诺的函数：如果去掉 `reading()` 上的 `const`，`halves()` 内部的调用将无法通过编译，并且错误会出现在类内部而不是调用方处。

这种承诺还使得对象可以通过 const 引用被访问，这也正是只读函数接收对象的方式。
`readHalves` 以这种方式持有 meter，因此它唯一能够调用的函数就是那些做出了承诺的函数。
如果改为标记返回类型，例如 `const int reading()`，则不会对对象做出任何承诺，并会导致该调用失败。

### 需求

- `quarterTurnsOf` 接收 `const std::vector<int> &degrees`，并按相同顺序为每个角度返回一个 `int`，因此不包含任何角度的 vector 会生成空结果。
- `degrees()` 返回创建角度时的值，而 `quarterTurns()` 返回 `degrees() / 90`。
- 两者的参数列表后都带有 `const`，书写为 `degrees() const` 和 `quarterTurns() const`，这是为每个元素构建的 `const Angle` 所要求的。
  这两种书写形式都会被检查，因为如果改为从驱动代码中移除 `const` 虽然也能消除相同的错误，但这会让类无法做出任何承诺。
- `readQuarterTurns` 保留其 `const Angle &` 参数并返回 `angle.quarterTurns()`。
- 除法向零截断，因此 89 返回 0，90 返回 1，359 返回 3，-90 返回 -1，-45 返回 0。
  所有角度均在 -1000 到 1000 之间。

### 解答

```cpp
#include <vector>

class Angle {
public:
    Angle(int startingDegrees) : degreeValue_(startingDegrees) {}

    int degrees() const {
        return degreeValue_;
    }

    int quarterTurns() const {
        // 把角度除以 90，返回整数部分
        return degrees() / 90;
    }

private:
    int degreeValue_;
};

// 角度以 const 引用传入，因此只能调用承诺不修改对象的成员函数。
int readQuarterTurns(const Angle &angle) {
    // 向这个角度查询四分之一圈数并返回
    return angle.quarterTurns();
}

struct Solution {
    static std::vector<int> quarterTurnsOf(const std::vector<int> &degrees) {
        std::vector<int> result;
        for (int value : degrees) {
            const Angle angle(value);
            result.push_back(readQuarterTurns(angle));
        }
        return result;
    }
};
```
