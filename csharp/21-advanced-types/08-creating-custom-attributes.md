### 创建自定义特性

自定义特性（Custom attributes）允许你定义自己的元数据，这些元数据可以附加到代码元素上，并在运行时使用反射（reflection）进行读取。

### 定义自定义特性

创建一个继承自 `System.Attribute` 的类：

```csharp
public class DescriptionAttribute : Attribute
{
    public string Text { get; }
    
    public DescriptionAttribute(string text)
    {
        Text = text;
    }
}
```

### 使用 AttributeUsage

`[AttributeUsage]` 特性用于控制自定义特性可以应用在哪些位置：

```csharp
[AttributeUsage(AttributeTargets.Class | AttributeTargets.Method)]
public class LoggableAttribute : Attribute { }

// AttributeTargets 选项：
// Class, Method, Property, Field, Parameter, All 等。
```

你还可以控制该特性是否可以多次应用：

```csharp
[AttributeUsage(AttributeTargets.Class, AllowMultiple = false)]
public class SingletonAttribute : Attribute { }
```

### 添加属性

特性可以包含构造函数参数和命名属性：

```csharp
[AttributeUsage(AttributeTargets.Class)]
public class TableAttribute : Attribute
{
    public string TableName { get; }  // 必填（构造函数）
    public string Schema { get; set; } = "dbo";  // 可选（属性）
    
    public TableAttribute(string tableName)
    {
        TableName = tableName;
    }
}

// 用法：
[Table("Users", Schema = "app")]
public class User { }
```

### 读取自定义特性

在运行时使用反射读取特性：

```csharp
var attr = typeof(User).GetCustomAttribute<TableAttribute>();
Console.WriteLine(attr.TableName);  // "Users"
```

### 你的任务

1. 在 AuthorAttribute.cs 中完成 `AuthorAttribute` 类：

   - 继承自 `System.Attribute`
   - 添加 `[AttributeUsage]`，使其仅允许应用于类（classes），且不可多次应用（no multiple）
   - 添加 `Name` 属性（通过构造函数设置）
   - 添加 `Version` 属性（可选，默认值为 "1.0"）
2. 将 `[Author]` 应用于 `Calculator` 类，其中 name 为 "John Smith"，version 为 "2.0"
3. 将 `[Author]` 应用于 `StringHelper` 类，其中 name 为 "Jane Doe"（使用默认 version）
4. 实现 `GetAuthorInfo` 以读取该特性并返回格式化后的字符串

### 方法签名

```csharp
public static string GetAuthorInfo(Type type)
```

### 预期结果

```csharp
GetAuthorInfo(typeof(Calculator)) -> "Author: John Smith, Version: 2.0"
GetAuthorInfo(typeof(StringHelper)) -> "Author: Jane Doe, Version: 1.0"
GetAuthorInfo(typeof(string)) -> "No author information"
```

### 解答

`Main.cs`

```csharp
using System;
using System.Linq;
using System.Reflection;

public class Solution
{
    public static string GetAuthorInfo(Type type)
    {
        // 从类型上获取 AuthorAttribute，并返回
        // 格式为 "Author: {Name}, Version: {Version}" 的字符串
        // 如果没有找到该特性，则返回 "No author information"
        var author = type.GetCustomAttribute<AuthorAttribute>();
        if (author == null)
        {
            return "No author information";
        }
        return $"Author: {author.Name}, Version: {author.Version}";
    }
}

// 在这里应用你的 AuthorAttribute
[Author("John Smith", Version = "2.0")]
public class Calculator
{
    public int Add(int a, int b) => a + b;
}

// 在这里使用不同的值应用你的 AuthorAttribute
[Author("Jane Doe")]
public class StringHelper
{
    public string Reverse(string s) => new string(s.ToCharArray().Reverse().ToArray());
}
```

`AuthorAttribute.cs`

```csharp
using System;

// 在这里创建你的自定义 AuthorAttribute
// 它应该：
// 1. 继承自 System.Attribute
// 2. 拥有 Name 属性（string）
// 3. 拥有 Version 属性（string，默认值为 "1.0"）
// 4. 只能应用于类
// 5. 不允许在同一个类上多次应用

[AttributeUsage(AttributeTargets.Class, AllowMultiple = false)]
public class AuthorAttribute : Attribute
{
    public string Name { get; }  // 必填（构造函数）
    public string Version { get; set; } = "1.0";  // 可选（属性）
    
    public AuthorAttribute(string name)
    {
        Name = name;
    }
}
```
