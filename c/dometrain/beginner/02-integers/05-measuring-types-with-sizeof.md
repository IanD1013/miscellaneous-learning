### 测量而非猜测

媒体目录为每个索引条目写入四个原始整数值：一个 `short`、一个 `int`、一个 `long` 和一个 `long long`。
它们组合在一起的总宽度必须由编译器提供，因为原始类型的宽度可能会因平台而异。

`sizeof` 运算符以字节为单位返回大小。
应用于原始类型名称时，其语法为 `sizeof(type)`：`sizeof` 后面跟着包含被测量类型的圆括号。
例如，`sizeof(short)` 用于获取当前平台上 `short` 所占用的字节数。
此处无需提供变量或值。

将这四个独立的字节计数相加。
在课程目标平台上，每个条目总计 18 字节，但学员代码中不得包含硬编码的标记 `18`。
`entries` 声明的数值范围是 0 到 100000000，因此可表示的乘积最多可达 1800000000。

### 要求

- 分别使用 `sizeof` 测量 `short`、`int`、`long` 和 `long long`。
- 将这些原始类型宽度相加，然后乘以 `entries`。
- 返回所得的 `int`。
- 让编译器提供每个宽度，而不是替换为记住的总数。

强制标记检查要求使用 `sizeof`，并且上限验证将确保按比例缩放的原始宽度算术运算保持在有效范围内。

### 解答

```c
int index_record_bytes(int entries)
{
    // 每条记录包含一个 short、一个 int、一个 long 和一个 long long
    return (sizeof(short) + sizeof(int) + sizeof(long) + sizeof(long long)) * entries;
}
```
