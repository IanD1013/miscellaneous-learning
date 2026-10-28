一个 4 GiB（gibibyte）的录制内容占用 4,294,967,296 字节，这超出了该平台上 `int` 的表示范围。
gibibyte 缩写为 GiB，是二进制单位，等于 1,073,741,824 字节。
它不同于十进制的 gigabyte（即 GB，1,000,000,000 字节）。

C 语言的有符号整数宽度家族包括 `short`、`int`、`long` 和 `long long`。
每种类型都有保证的最小范围。
所选类型必须能够表示最大的中间值和最终值。
如果带符号 `int` 乘法超出其范围，带符号溢出将导致未定义行为（undefined behavior）。

乘法运算的类型取决于其操作数。
如果两个操作数都是 `int`，运算将作为 `int` 执行，而 `long long` 返回类型仅在运算完成后才接收结果。
这无法修复溢出。
请将 1073741824 存储在一个表示每 gibibyte 字节数的 `long long` 变量中。
当 `gibibytes` 与该更宽的操作数相乘时，乘法将以较宽的类型执行。

按照该顺序实现 `video_file_bytes`。
1 GiB 返回 `1073741824`，4 GiB 返回 `4294967296`，25 GiB 返回 `26843545600`。
约定的数量范围为 0 到 2147483647，评测程序也会测试该最大数值：先拓宽类型后，它会产生 2305843008139952128，该值仍在 `long long` 范围内。
公开函数名称保持不变；参数和说明请使用正确的二进制单位。

### 解答

```c
long long video_file_bytes(int gibibytes)
{
    // 1 GiB 等于 1073741824 字节；用 long long 操作数让乘法以较宽类型执行
    long long bytes_per_gibibyte = 1073741824;
    return gibibytes * bytes_per_gibibyte;
}
```
