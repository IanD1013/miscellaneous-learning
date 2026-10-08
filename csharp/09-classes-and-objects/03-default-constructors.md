### 默认构造函数

**默认构造函数**（default constructor）是一个无参构造函数，用于使用默认值初始化对象。
当您使用 `new ClassName()` 创建新实例时，它会自动运行。

### 为什么使用默认构造函数？

如果没有构造函数，字段将获取其类型的默认值（字符串为 null，数字为 0，布尔值为 false）。
而默认构造函数允许您设置更有意义的初始值。

### 构造函数语法

```csharp
public class Person
{
    public string Name;
    public int Age;
    
    // 默认构造函数 - 与类同名，没有参数
    public Person()
    {
        Name = "Guest";
        Age = 0;
    }
}
```

### 使用默认构造函数

```csharp
// 构造函数会自动运行
Person person = new Person();
Console.WriteLine(person.Name);  // 输出: Guest
Console.WriteLine(person.Age);   // 输出: 0
```

### 有无构造函数的对比

```csharp
// 没有构造函数 - 字段为类型的默认值
public class Car
{
    public string Model;  // 默认为 null
}

// 有构造函数 - 字段具有有意义的默认值
public class Car
{
    public string Model;
    
    public Car()
    {
        Model = "Unknown Model";
    }
}
```

### 您的任务

为 `Book` 类创建一个默认构造函数，使用以下默认值初始化所有字段：

- `Title` = "Untitled"
- `Author` = "Unknown"
- `PageCount` = 0
- `IsAvailable` = true

### 预期结果

```
GetTitle() -> "Untitled"
GetAuthor() -> "Unknown"
GetPageCount() -> 0
GetIsAvailable() -> True
```

### 解答

```csharp
using System;

public class Book
{
    public string Title;
    public string Author;
    public int PageCount;
    public bool IsAvailable;
    
    // 默认构造函数，为所有字段设置默认值
    public Book()
    {
        Title = "Untitled";
        Author = "Unknown";
        PageCount = 0;
        IsAvailable = true;
    }
}

public class Solution
{
    public static string GetBookInfo()
    {
        Book book = new Book();
        return $"{book.Title} by {book.Author}, {book.PageCount} pages, Available: {book.IsAvailable}";
    }
    
    public static string GetTitle()
    {
        Book book = new Book();
        return book.Title;
    }
    
    public static string GetAuthor()
    {
        Book book = new Book();
        return book.Author;
    }
    
    public static int GetPageCount()
    {
        Book book = new Book();
        return book.PageCount;
    }
    
    public static bool GetIsAvailable()
    {
        Book book = new Book();
        return book.IsAvailable;
    }
}
```
