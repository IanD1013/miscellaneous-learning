### 元组解构

解构（Deconstruction）允许你在单条语句中将元组的值拆分到单独的具名变量中。
这能让你的代码更具可读性，也更便于使用。

### 基本解构语法

```csharp
// 给定一个元组
var person = ("Alice", 30, "London");

// 解构为单独的变量
var (name, age, city) = person;

// 现在可以独立使用每个变量
Console.WriteLine(name);  // Alice
Console.WriteLine(age);   // 30
```

### 显式类型的解构

```csharp
// 可以显式指定类型
(string name, int age, string city) = person;

// 或者将 var 与显式类型混合使用
var (name, age, _) = person;  // 使用 _ 丢弃不需要的值
```

### 解构与直接访问对比

```csharp
// 不使用解构 - 直接访问元组成员
var greeting = $"{person.Item1} is {person.Item2}";

// 使用解构 - 变量名更清晰
var (name, age, _) = person;
var greeting = $"{name} is {age}";
```

### 忽略不需要的值（弃元）

```csharp
// 使用下划线忽略不需要的值
var (name, _, city) = person;  // 忽略 age
```

### 你的任务

将输入的元组解构成单独的变量，然后使用这些变量构建一个格式化字符串。

### 方法签名

```csharp
public static string DeconstructPerson((string Name, int Age, string City) person)
```

### 预期结果

```
DeconstructPerson(("Alice", 25, "Paris")) -> "Alice is 25 years old and lives in Paris"
DeconstructPerson(("Bob", 40, "Tokyo")) -> "Bob is 40 years old and lives in Tokyo"
```

### 解答

```csharp
using System;

public class Solution
{
    public static string DeconstructPerson((string Name, int Age, string City) person)
    {
        // 将元组解构为单独的变量
        var (name, age, city) = person;
        
        // 然后返回格式化字符串："Name is Age years old and lives in City"
        return $"{name} is {age} years old and lives in {city}";
    }
}
```
