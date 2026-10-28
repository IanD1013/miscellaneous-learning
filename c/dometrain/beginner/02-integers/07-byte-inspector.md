字节检查器（byte inspector）结合了本章关于宽度、字面量以及度量决策的知识，来计算一个未压缩 32 位位图的大小。
宽度（width）和高度（height）均在 0 到 1000000 之间。

### 文件布局

每个文件都以一个 `0x36` 字节的文件头开头。
每个像素包含四个通道，每个通道占用 `sizeof(unsigned char)` 字节。
最大像素区域为 4 万亿字节，最大的完整结果为 4000000000054，完全在 `long long` 的安全表示范围内。

在第一次乘法之前进行类型拓宽（widen）。
将 `width` 复制到一个 `long long` 局部变量中，然后用一个普通的表达式将该拓宽后的值与 `height`、4 以及测得的通道宽度相乘，来初始化另一个 `long long` 变量。
请勿使用复合赋值运算符：该运算符尚未介绍。
如果仅在 `width * height` 之后才进行拓宽就太晚了，因为有符号溢出属于未定义行为（undefined behavior）。

### 要求

- 返回 `long long`。
- 保持精确的文件头标记 `0x36`；在学员代码中禁止使用十进制的 54。
- 使用精确表达式 `sizeof(unsigned char)` 来初始化通道宽度值。
- 从一开始就在 `long long` 中进行尺寸乘法计算，使用普通的初始化和乘法。
- 在尺寸为零时保留文件头大小，并正确处理一百万平方的边界情况。

无需使用失败哨兵值（failure sentinel）。
有限的尺寸上限和提前拓宽确保了每个规定范围内的结果都可以正确表示。

### 解答

```c
long long bitmap_file_bytes(int width, int height)
{
    // 文件头：0x36 字节。每个像素包含四个单字节通道。
    long long channel_bytes = sizeof(unsigned char);
    // 在第一次乘法之前先拓宽为 long long
    long long wide_width = width;
    long long pixel_bytes = wide_width * height * 4 * channel_bytes;
    return 0x36 + pixel_bytes;
}
```
