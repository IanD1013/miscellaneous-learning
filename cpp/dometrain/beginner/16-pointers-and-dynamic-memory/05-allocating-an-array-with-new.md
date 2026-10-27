一次请求多个对象是另一种形式：`new int[count]` 会连续预留 `count` 个 int 的空间，并返回第一个元素的地址，因此返回的是一个 `int *`。

```cpp
int size = 3;
int *buffer = new int[size];

for (int i = 0; i < size; i++) {
    buffer[i] = i * 10;
}

delete[] buffer;
```

`buffer[i]` 可以读取和写入该位置的元素，使用的方括号与 vector 相同。
内存块没有 `size()` 来告诉你请求了多少个元素，因此该计数必须保存在你自己的变量中，并且在通过方括号访问之前，必须根据该计数验证每个索引。
越界写入在此处不会报错（静默发生）：程序不会终止，也不会打印任何内容，而错误的结果可能会在其他地方显现，或者根本不显现。

释放形式必须与分配内存块的形式相匹配：通过 `new[]` 分配的块使用 `delete[]`，普通的 `new` 使用普通的 `delete`。
不匹配的形式也能编译通过，这里的测试表明它既不会终止用例也不会报告任何内容，因此这种配对规则需要你通过仔细阅读代码来遵守。
允许请求零个元素：`new int[0]` 会返回一个不能应用任何索引的指针，并且它仍然需要被释放。

### 要求

- `doubledPrefix` 接收 `const std::vector<int> &values` 以及一个 `int keep`，并返回一个 `std::vector<int>`。
- 如果 `keep` 小于 0，或大于元素数量，则在分配任何内存之前拒绝：返回一个包含 -1 的单元素 vector。
- 否则，分配恰好 `keep` 个 int，将 `values[i] * 2` 放入位置 `i`，然后将该内存块复制到你返回的 vector 中并释放它。
  `{3, 1, 4, 1}` 且 `keep` 为 3 时返回 `[6, 2, 8]`，第四个元素完全不会被访问。
- 如果前 `keep` 个位置中存在负数元素，也同样予以拒绝：释放该内存块，然后返回相同的单元素 -1。
  超出保留范围的负数不会触发拒绝，也不会改变任何结果，因此 `{3, -7, 4}` 且 `keep` 为 3 时返回 `[-1]`，而 `{3, 4, -7}` 且 `keep` 为 2 时返回 `[6, 8]`。
- `keep` 为 0 时返回一个空 vector，这也是为什么拒绝时返回 -1 而不是空 vector。
- 内存块通过 `new` 分配并由 `delete[]` 归还；这两种拼写都会被检查。
  任何后面带空格的 `delete` 都会被拒绝，这就排除了 `delete [] buffer` 以及普通的 `delete`，因此请让方括号紧跟在关键字后面。

### 解答

```cpp
#include <vector>

struct Solution {
    static std::vector<int> doubledPrefix(const std::vector<int> &values, int keep) {
        // 先拒绝列表无法满足的 keep，再分配恰好 keep 个 int 的内存块，填充后用 delete[] 释放
        std::vector<int> result;
        int count = values.size();
        if (keep < 0 || keep > count) {
            result.push_back(-1);
            return result;
        }
        int *block = new int[keep];
        for (int i = 0; i < keep; i++) {
            if (values[i] < 0) {
                delete[] block;
                result.push_back(-1);
                return result;
            }
            block[i] = values[i] * 2;
        }
        for (int i = 0; i < keep; i++) {
            result.push_back(block[i]);
        }
        delete[] block;
        return result;
    }
};
```
