### C# 13 中的分部属性（Partial Properties）

C# 13 引入了分部属性（partial properties），允许你在分部类（partial class）中将属性的声明与实现拆分到多个文件中。
这对于代码生成器以及实现关注点分离非常有用。

### 声明与实现

```csharp
// File1.cs - 声明
public partial class Product
{
    public partial string Name { get; }  // 仅声明
}

// File2.cs - 实现
public partial class Product
{
    private string _name = "";
    
    public partial string Name  // 实现
    {
        get => _name;
    }
}
```

### 分部属性的规则

| 方面 | 要求 |
| --- | --- |
| 修饰符 | 两部分都必须使用 `partial` 关键字 |
| 签名 | 必须完全匹配（类型、名称、访问器） |
| 访问器 | 声明部分使用 `;`，实现部分使用主体代码块 |
| 单一实现 | 只能有一个部分包含主体 |

### 只读（Get-Only）与读写（Get/Set）

```csharp
// 只读的分部属性
public partial string ReadOnly { get; }        // 声明
public partial string ReadOnly { get => "value"; }  // 实现

// 可读写的分部属性
public partial int Count { get; set; }         // 声明
public partial int Count                        // 实现
{
    get => _count;
    set => _count = value;
}
```

### 你的任务

在 `Main.cs` 中完成分部属性的实现。
属性声明位于 `PersonProperties.cs`（只读文件）中。

1. **FullName**：返回 `FirstName + " " + LastName`
2. **Age**：计算年龄为 `2024 - BirthYear`

### 方法签名

```csharp
public static string GetPersonInfo(string firstName, string lastName, int birthYear)
```

### 预期结果

```
GetPersonInfo("John", "Doe", 1990) -> "John Doe is 34 years old"
GetPersonInfo("Jane", "Smith", 2000) -> "Jane Smith is 24 years old"
```

### 解答

```csharp
using System;

public class Solution
{
    public static string GetPersonInfo(string firstName, string lastName, int birthYear)
    {
        var person = new Person
        {
            FirstName = firstName,
            LastName = lastName,
            BirthYear = birthYear
        };
        
        return person.Summary;
    }
}

// 完成分部属性的实现
public partial class Person
{
    // 属性声明位于 PersonProperties.cs
    public partial string FullName
    {
        get
        {
            // 返回 FirstName + " " + LastName
            return FirstName + " " + LastName;
        }
    }
    
    public partial int Age
    {
        get
        {
            // 以 2024 作为当前年份，根据 BirthYear 计算年龄
            return 2024 - BirthYear;
        }
    }
}
```
