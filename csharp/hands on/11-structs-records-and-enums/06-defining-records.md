### C# 中的 Record

Record 是专为不可变数据设计的引用类型。
它们提供了内置的基于值的相等性比较，非常适合用于数据传输对象和模型。

### 定义 Record

```csharp
// 位置记录语法（最简洁）
public record Person(string Name, int Age);

// 这会自动创建：
// - 属性：Name 和 Age
// - 构造函数：new Person("Alice", 30)
// - 基于值的相等性
// - ToString() 方法
```

### Record 与 Class 的对比

```csharp
// 使用 class，你需要这样写：
public class PersonClass
{
    public string Name { get; init; }
    public int Age { get; init; }
    // 还要重写 Equals、GetHashCode、ToString...
}

// 使用 record，只需一行：
public record Person(string Name, int Age);
```

### 基于值的相等性比较

Record 通过其属性值进行比较，而不是通过引用：

```csharp
var person1 = new Person("Alice", 30);
var person2 = new Person("Alice", 30);

person1 == person2  // True！值相同
```

### 访问属性

```csharp
var person = new Person("Bob", 25);
Console.WriteLine(person.Name);
Console.WriteLine(person.Age);
```

### 你的任务

1. 定义一个包含 `Name` (string) 和 `Age` (int) 属性的 `Person` record
2. 实现 `CreatePerson` 以创建并返回一个 Person record
3. 实现 `GetPersonInfo` 以返回格式化信息
4. 实现 `ArePeopleEqual` 以比较两个 Person record

### 方法签名

```csharp
public record Person(string Name, int Age);
public static Person CreatePerson(string name, int age)
public static string GetPersonInfo(Person person)
public static bool ArePeopleEqual(Person person1, Person person2)
```

### 预期结果

```
CreatePerson("Alice", 30) -> Person { Name = Alice, Age = 30 }
GetPersonInfo(person) -> "Name: Alice, Age: 30"
ArePeopleEqual(person1, person2) -> True（如果值相同）
```

### 解答

```csharp
using System;

// 定义 Person record
public record Person(string Name, int Age);

public class Solution
{
    public static Person CreatePerson(string name, int age)
    {
        // 创建并返回一个 Person record
        return new Person(name, age);
    }
    
    public static string GetPersonInfo(Person person)
    {
        // 按 "Name: [name], Age: [age]" 格式返回信息
        return $"Name: {person.Name}, Age: {person.Age}";
    }
    
    public static bool ArePeopleEqual(Person person1, Person person2)
    {
        // record 基于值比较相等性
        return person1 == person2;
    }
}
```
