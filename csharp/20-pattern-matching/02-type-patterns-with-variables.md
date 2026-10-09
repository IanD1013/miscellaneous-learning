### 带变量的类型模式

类型模式使用 `is Type variableName` 语法，将类型检查和变量声明合并在单个表达式中。

### 基本语法

```csharp
// 旧方式：检查和转换分开进行
if (obj is string)
{
    string s = (string)obj;  // 需要手动转换
    Console.WriteLine(s.Length);
}

// 新方式：带变量的类型模式
if (obj is string s)
{
    Console.WriteLine(s.Length);  // s 已经是对应类型！
}
```

### 变量具有作用域

```csharp
if (value is int number)
{
    // 'number' 在这里可以作为 int 使用
    return number * 2;
}
// 'number' 在这里无法访问
```

### 与 else if 结合使用

```csharp
if (value is int i)
    return $"Got int: {i}";
else if (value is double d)
    return $"Got double: {d}";
else
    return "Unknown";
```

### 你的任务

编写一个方法，使用带变量的类型模式根据值的类型来描述该值：

- 如果 `value` 是 `int`，返回 `"Integer: {doubled value}"`（乘以 2）
- 如果 `value` 是 `string`，返回 `"String: {uppercase text}"`
- 如果 `value` 是 `double`，返回 `"Double: {value with 2 decimal places}"`
- 如果 `value` 是 `bool`，若为 true 则返回 `"Boolean: yes"`，若为 false 则返回 `"Boolean: no"`
- 对于任何其他类型，返回 `"Unknown type"`

### 方法签名

```csharp
public static string DescribeValue(object value)
```

### 预期结果

```
DescribeValue(5) -> "Integer: 10"
DescribeValue("hello") -> "String: HELLO"
DescribeValue(3.14159) -> "Double: 3.14"
DescribeValue(true) -> "Boolean: yes"
```

### 解答

```csharp
using System;

public class Solution
{
    public static string DescribeValue(object value)
    {
        // 使用带变量的类型模式逐一检查类型
        if (value is int i)
            return $"Integer: {i * 2}";
        else if (value is string s)
            return $"String: {s.ToUpper()}";
        else if (value is double d)
            return $"Double: {d:F2}";
        else if (value is bool b)
            return b ? "Boolean: yes" : "Boolean: no";
        else
            return "Unknown type";
    }
}
```
