### Public 访问修饰符

`public` 访问修饰符使类成员（字段、属性、方法）可以从代码中的任何位置访问，包括从类的外部。

### 为什么访问修饰符很重要

访问修饰符控制类成员的可见性和可访问性。
`public` 关键字是最宽松的，它允许任何代码读取、写入或调用该成员。

```csharp
public class Car
{
    public string Brand;        // 任何人都可以读写此字段
    public int Year;            // 任何人都可以读写此字段
    
    public void StartEngine()   // 任何人都可以调用此方法
    {
        Console.WriteLine("Engine started!");
    }
}
```

### 访问 Public 成员

可以在代码的任何部分使用点表示法（dot notation）来访问 Public 成员：

```csharp
Car myCar = new Car();
myCar.Brand = "Toyota";      // 设置一个 public 字段
myCar.Year = 2023;           // 设置另一个 public 字段
string carBrand = myCar.Brand; // 读取一个 public 字段
myCar.StartEngine();         // 调用一个 public 方法
```

### Public 对比 Private

| 修饰符 | 可访问范围 | 使用场景 |
| --- | --- | --- |
| `public` | 任何地方 | API 接口层、预期的公开接口 |
| `private` | 仅限同一个类中 | 内部实现细节 |

### 你的任务

创建一个包含以下内容的 `Person` 类：

1. 一个 `string` 类型的 public 字段 `Name`
2. 一个 `int` 类型的 public 字段 `Age`
3. 一个返回格式化问候字符串的 public 方法 `Greet()`

然后实现 `GetPersonInfo` 来创建一个 Person 实例、设置其字段并返回问候语。

### 方法签名

```csharp
public static string GetPersonInfo(string name, int age)
```

### 预期结果

```
GetPersonInfo("Alice", 25) -> "Hello, I'm Alice and I'm 25 years old."
GetPersonInfo("Bob", 30) -> "Hello, I'm Bob and I'm 30 years old."
```

### 解答

```csharp
using System;

public class Person
{
    // string 类型的 public 字段 Name
    public string Name;
    
    // int 类型的 public 字段 Age
    public int Age;
    
    // 返回问候字符串的 public 方法 Greet()
    public string Greet()
    {
        return $"Hello, I'm {Name} and I'm {Age} years old.";
    }
}

public class Solution
{
    public static string GetPersonInfo(string name, int age)
    {
        // 创建 Person，设置 public 字段，并返回 Greet() 的结果
        Person person = new Person();
        person.Name = name;
        person.Age = age;
        return person.Greet();
    }
}
```
