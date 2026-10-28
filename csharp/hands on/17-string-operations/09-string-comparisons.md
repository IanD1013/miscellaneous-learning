### 字符串比较

C# 中的字符串比较远不止简单的 `==` 检查。
`String.Equals()` 和 `String.Compare()` 方法让你可以精确控制字符串的比较方式。

### 带有 StringComparison 的 String.Equals

```csharp
// 区分大小写的比较（默认）
string.Equals("Hello", "hello");  // false

// 不区分大小写的比较
string.Equals("Hello", "hello", StringComparison.OrdinalIgnoreCase);  // true

// 区域性敏感的比较
string.Equals("café", "CAFÉ", StringComparison.CurrentCultureIgnoreCase);  // true
```

### StringComparison 选项

| 选项 | 描述 | 用例 |
| --- | --- | --- |
| `Ordinal` | 逐字节比较，区分大小写 | 文件名、标识符 |
| `OrdinalIgnoreCase` | 逐字节比较，忽略大小写 | 用户输入验证 |
| `CurrentCulture` | 使用当前区域性规则 | 面向用户的文本 |
| `InvariantCultureIgnoreCase` | 区域性无关，忽略大小写 | 数据序列化 |

### 理解 String.Compare

`String.Compare()` 比较两个字符串并返回一个整数，指示它们的相对顺序：

```csharp
// 返回值：
//   负数：在排序顺序中，第一个字符串排在第二个之前
//   零：两个字符串相等
//   正数：在排序顺序中，第一个字符串排在第二个之后

string.Compare("apple", "banana", StringComparison.Ordinal);  // 负数 (a < b)
string.Compare("banana", "apple", StringComparison.Ordinal);  // 正数 (b > a)
string.Compare("apple", "apple", StringComparison.Ordinal);   // 零 (相等)
string.Compare("Apple", "apple", StringComparison.Ordinal);   // 负数 (在 ASCII 中 'A' < 'a')
```

**重要提示：** 返回的具体负值或正值取决于具体实现。
切勿依赖它正好是 -1 或 1。
相反，应该检查结果是否为 `< 0`、`== 0` 或 `> 0`：

```csharp
int result = string.Compare("apple", "banana", StringComparison.Ordinal);

if (result < 0)
    Console.WriteLine("First comes before second");
else if (result > 0)
    Console.WriteLine("First comes after second");
else
    Console.WriteLine("Strings are equal");
```

### 使用 String.Compare 进行不区分大小写的比较

```csharp
// 区分大小写：在 ASCII 中 'A' (65) < 'a' (97)
string.Compare("Apple", "apple", StringComparison.Ordinal);  // 负数

// 不区分大小写：视为相等
string.Compare("Apple", "apple", StringComparison.OrdinalIgnoreCase);  // 零
```

### 为什么 == 可能会有问题

```csharp
// == 只能区分大小写
"Hello" == "hello"  // false - 无法忽略大小写！

// 使用 String.Equals 进行不区分大小写的比较
string.Equals("Hello", "hello", StringComparison.OrdinalIgnoreCase);  // true
```

### 你的任务

实现以下三个方法：

1. **AreEqualIgnoreCase**：检查两个字符串是否相等，忽略大小写差异
2. **CompareStrings**：比较两个字符串并返回 -1、0 或 1 来表示顺序
3. **AreExactlyEqual**：检查两个字符串是否完全相等（区分大小写）

### 方法签名

```csharp
public static bool AreEqualIgnoreCase(string text1, string text2)
public static int CompareStrings(string text1, string text2)
public static bool AreExactlyEqual(string text1, string text2)
```

### 预期结果

```
AreEqualIgnoreCase("Hello", "HELLO") -> True
AreEqualIgnoreCase("Test", "Best") -> False
CompareStrings("apple", "banana") -> -1
CompareStrings("cat", "cat") -> 0
AreExactlyEqual("Hello", "Hello") -> True
AreExactlyEqual("Hello", "hello") -> False
```

### 解答

```csharp
using System;

public class Solution
{
    public static bool AreEqualIgnoreCase(string text1, string text2)
    {
        // 检查两个字符串是否相等，忽略大小写
        return string.Equals(text1, text2, StringComparison.OrdinalIgnoreCase);
    }

    public static int CompareStrings(string text1, string text2)
    {
        // 比较两个字符串并返回：
        // -1 表示 text1 排在 text2 之前
        //  0 表示两者相等
        //  1 表示 text1 排在 text2 之后
        int result = string.Compare(text1, text2, StringComparison.Ordinal);

        if (result < 0)
            return -1;
        else if (result > 0)
            return 1;
        else
            return 0;
    }

    public static bool AreExactlyEqual(string text1, string text2)
    {
        // 检查两个字符串是否完全相等（区分大小写）
        return string.Equals(text1, text2, StringComparison.Ordinal);
    }
}
```
