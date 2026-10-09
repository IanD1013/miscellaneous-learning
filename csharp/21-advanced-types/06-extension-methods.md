### C# 中的扩展方法

扩展方法允许你向现有类型添加新方法，而无需修改原始类型或创建派生类。

### `this` 参数语法

扩展方法定义在**静态类（static class）**中，并在第一个参数上使用特殊的 `this` 修饰符：

```csharp
public static class StringExtensions
{
    public static bool IsNullOrEmpty(this string str)
    {
        return string.IsNullOrEmpty(str);
    }
}
```

### 调用扩展方法

定义完成后，你可以像调用实例方法一样调用扩展方法：

```csharp
// 调用扩展方法（看起来像实例方法）
string name = "Alice";
bool empty = name.IsNullOrEmpty();

// 等价的静态调用
bool empty2 = StringExtensions.IsNullOrEmpty(name);
```

### 关键规则

| 规则 | 描述 |
| --- | --- |
| 静态类 | 扩展方法必须位于静态类中 |
| 静态方法 | 方法本身必须是静态的 |
| `this` 关键字 | 第一个参数使用 `this` 修饰符 |
| 第一个参数类型 | 决定了哪个类型获得扩展 |

### 更多示例

```csharp
public static class IntExtensions
{
    public static bool IsEven(this int number)
    {
        return number % 2 == 0;
    }
    
    public static int Square(this int number)
    {
        return number * number;
    }
}

// 用法
int x = 4;
bool even = x.IsEven();   // true
int squared = x.Square(); // 16
```

### 你的任务

为 `string` 类型创建一个扩展方法 `WordCount`，返回字符串中的单词数量。
单词由空白字符（空格、制表符、换行符）分隔。

### 方法签名

```csharp
public static int WordCount(this string text)
```

### 预期结果

```
"Hello World".WordCount() -> 2
"The quick brown fox".WordCount() -> 4
"".WordCount() -> 0
```

### 解答

```csharp
using System;

public static class StringExtensions
{
    public static int WordCount(this string text)
    {
        // 按空白字符拆分，并去掉空项
        return text.Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries).Length;
    }
}

public class Solution
{
    public static int CountWords(string text)
    {
        // 在这里使用你的扩展方法
        return text.WordCount();
    }
}
```
