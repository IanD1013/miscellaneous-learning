不变量（invariant）是关于对象的一个断言，其所属的类会始终保持该断言为真：对于 `Percentage`，存储的值永远不小于 0 且永远不大于 100。
在构造函数执行完毕后，以及每次写入成员变量的函数返回时，该断言都必须成立。

私有成员使得这样的断言变得完全可检查：唯一能够写入 `storedValue_` 的代码位于类的内部，因此需要进行检查的地方数量极少且清晰可数。
单靠私有性本身起不到保护作用：如果一个公有函数在写入成员变量前不先对值进行校验，同样会彻底破坏数值范围。

校验必须在构造函数中执行，并且在每个写入成员变量的函数中也要执行；将这两处都路由到同一个私有函数中，可以防止规则的两份副本产生偏差：

```cpp
class Volume {
public:
    Volume(int level) {
        set(level);
    }

    void turnTo(int level) {
        set(level);
    }

private:
    void set(int level) {
        // 范围规则只在这里写一次
    }

    int level_ = 0;
};
```

接下来要处理的是超出范围的值会发生什么。
构造函数没有声明返回类型，因此它无法像普通函数那样返回表示失败的值，无论如何对象都会被创建。
因此，该类公开了一份契约。
`Percentage` 本可以将值限制在最接近的端点，但它选择直接拒绝：超出范围的值绝不会被存储，对象保持原有的值，并用一个私有计数器记录拒绝次数，这也使得该行为能够从外部被验证。

初始代码已经将其构造函数和 `update` 路由到了 `store`。
请完成该函数体：

- 小于 0 或大于 100 的值不会被存储：对其进行计数，并保持已存储的值不变。
  0 和 100 都在有效范围内。
- 构造函数将 `start` 交给相同的校验逻辑处理，因此初始值为 150 会使对象保持文档中所述的默认值 0，并记录一次拒绝。
- `applyUpdates` 已在另一个您无法编辑的文件中编写完成。
  它使用 `start` 构建一个 `Percentage`，并通过 `tracker.update(value)` 按顺序将 `updates` 中的每个元素传入，最后同时报告 `tracker.current()` 与 `tracker.refusals()`。
  `store` 的函数体是您唯一需要编写的代码。
- 更新数据每次最多传入 20 个，范围低至 -1000、高至 1100，计数器除了统计这些更新之外，也会涵盖构造函数中的初始值。

## 解答

```cpp
class Percentage {
public:
    Percentage(int start) : storedValue_(0), refusedCount_(0) {
        store(start);
    }

    void update(int candidate) {
        store(candidate);
    }

    int current() const {
        return storedValue_;
    }

    int refusals() const {
        return refusedCount_;
    }

private:
    void store(int value) {
        // 小于 0 或大于 100 的值不存储，只记一次拒绝
        if (value < 0 || value > 100) {
            refusedCount_ += 1;
            return;
        }
        storedValue_ = value;
    }

    int storedValue_;
    int refusedCount_;
};
```
