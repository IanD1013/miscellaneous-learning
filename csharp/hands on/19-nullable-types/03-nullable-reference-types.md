### 可空引用类型

在现代 C#（8.0+）中，你可以启用可空引用类型来区分可以为 `null` 的引用和不能为 `null` 的引用。
这有助于在编译时防止空引用异常。

### 声明语法

```csharp
string regularText = "hello";   // 不可空：不能为 null
string? nullableText = null;     // 可空：可以为 null
string? alsoNullable = "world"; // 可空，但有值
```

### string? 与 string

| 类型 | 可以为 Null 吗？ | 编译器发出警告的情况... |
| --- | --- | --- |
| `string` | 否 | 你为其赋值 null |
| `string?` | 是 | 你在未进行 null 检查的情况下使用它 |

```csharp
// 编译器帮助捕获潜在的 null 问题
string name = null;        // 警告：不能赋值 null
string? nickname = null;   // OK：显式可空

int length = nickname.Length; // 警告：可能的 null 引用
int safeLength = nickname?.Length ?? 0; // OK：null 安全访问
```

### 结合空合并运算符

```csharp
string? input = null;
string result = input ?? "default";  // result = "default"

string? greeting = "Hello";
string output = greeting ?? "Hi";    // output = "Hello"
```

### 你的任务

编写一个接收两个 string 参数的方法：

- `nullableText`（类型 `string?`）- 可能有值，也可能没有值
- `regularText`（类型 `string`）- 始终有值

返回一个显示这两个值的格式化描述。
如果 `nullableText` 为 null，则在其位置显示单词 "null"。

### 方法签名

```csharp
public static string DescribeStrings(string? nullableText, string regularText)
```

### 预期结果

```
DescribeStrings(null, "world") -> "Nullable: null, Regular: world"
DescribeStrings("hello", "world") -> "Nullable: hello, Regular: world"
DescribeStrings("", "test") -> "Nullable: , Regular: test"
```

### 解答

```csharp
using System;

public class Solution
{
    public static string DescribeStrings(string? nullableText, string regularText)
    {
        // 返回两个字符串的描述
        // 格式："Nullable: [值或 'null'], Regular: [值]"
        return $"Nullable: {nullableText ?? "null"}, Regular: {regularText}";
    }
}
```
