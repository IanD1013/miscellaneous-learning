这四种缺陷在运行时都不会显现出来。
该文件中的每个函数都能在该引擎上正常编译、执行完毕并返回一个看似合理的结果，因此源代码是唯一存在的证据。

### 源代码中的四种形态

- **内存泄漏**（**leak**）是指任何 `delete` 都无法触及的内存分配，通常是因为 `return` 或 `break` 跳过了释放操作，或者是因为第二次 `new` 覆盖了持有该地址的唯一指针。
  该内存块永远不会被释放，而且输出中没有任何迹象能将其与正常运行区分开来。
- **重复释放**（**double free**）是指对已经释放的地址执行了第二次 `delete`。
  当释放操作同时出现在分支内部和分支下方，或者两个指针持有同一个地址时，就会出现这种情况。
  在该运行环境下的探测表明，析构函数会运行两次，并且程序会确定性地正常结束。
- **悬空**（**dangling**）指针持有一个已被释放的内存块地址，或者持有一个作用域已结束的局部变量地址。
  在这里，读取已释放的内存块是不可重复的：探测表明，一个包含三个元素的链表能完整保留下来以至于错误的代码也能通过，而一个包含十个元素的链表则会丢失其中的六个节点。
  一个看起来正确的值并不能说明产生它的读取操作没有问题。
- **释放形式与分配不匹配**（**release form that does not match**）是指对来自 `new[]` 的内存块使用了 `delete`，而此处原本应使用 `delete[]`。
  在该运行环境下的探测表明，这种不匹配只会运行一个析构函数，其余部分保持存活，且程序不会中止。

在释放后将指针设置为 `nullptr` 并不能修复上述任何问题。
它只会将随后的意外读取转换为对空指针的读取，而该引擎对此会返回 0。

### 每个函数的代码

`defectIn` 接收一个 `int functionNumber`，并返回注释中带有该编号的函数的代码。
请阅读这五个函数。
这里没有任何代码会调用它们，你的答案也不应该调用它们。

- 0 表示没有缺陷的函数
- 1 表示内存泄漏（leak）
- 2 表示重复释放（double free）
- 3 表示通过已释放的指针进行读取
- 4 表示释放形式与分配不匹配
- -1 表示未指定任何函数的编号，包括 0、负数和 6

每个函数最多包含一个缺陷，在其他方面均正确无误，且五个函数中有一个是完全正常的。
针对编号的 switch 语句或 if 链即可构成完整的函数体。

### 解答

```cpp
// 函数 1
int sumDoubledBlock(int count) {
    if (count <= 0) {
        return 0;
    }
    int *block = new int[count];
    int total = 0;
    for (int i = 0; i < count; i++) {
        block[i] = i * 2;
        total = total + block[i];
    }
    delete block;
    return total;
}

// 函数 2
int sumUpTo(int count) {
    int *block = new int[8];
    int total = 0;
    for (int i = 0; i < count; i++) {
        if (i >= 8) {
            return total;
        }
        block[i] = i;
        total = total + block[i];
    }
    delete[] block;
    return total;
}

// 函数 3
int highestOf(int count) {
    if (count <= 0) {
        return 0;
    }
    int *block = new int[count];
    int best = 0;
    for (int i = 0; i < count; i++) {
        block[i] = (i * 7) % 13;
        if (block[i] > best) {
            best = block[i];
        }
    }
    delete[] block;
    return best;
}

// 函数 4
int firstValueOf(int count) {
    if (count <= 0) {
        return 0;
    }
    int *block = new int[count];
    for (int i = 0; i < count; i++) {
        block[i] = i + 1;
    }
    delete[] block;
    return block[0];
}

// 函数 5
int spanOf(int count) {
    if (count <= 0) {
        return 0;
    }
    int *block = new int[count];
    for (int i = 0; i < count; i++) {
        block[i] = i * 3;
    }
    int span = block[count - 1] - block[0];
    if (span > 100) {
        delete[] block;
    }
    delete[] block;
    return span;
}

struct Solution {
    static int defectIn(int functionNumber) {
        // 根据上面每个函数携带的缺陷返回对应代码
        switch (functionNumber) {
            case 1:
                return 4;
            case 2:
                return 1;
            case 3:
                return 0;
            case 4:
                return 3;
            case 5:
                return 2;
            default:
                return -1;
        }
    }
};
```
