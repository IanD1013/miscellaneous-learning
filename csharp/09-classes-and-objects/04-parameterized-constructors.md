### 有参构造函数

有参构造函数在创建对象时接收参数，使你能够立即使用特定值初始化字段。

### 默认构造函数与有参构造函数

```csharp
// 默认构造函数 - 没有参数
public class Car
{
    public string Model;
    
    public Car()
    {
        Model = "Unknown";
    }
}

// 有参构造函数 - 接收值
public class Car
{
    public string Model;
    
    public Car(string model)
    {
        Model = model;
    }
}
```

### 使用有参构造函数

```csharp
// 使用初始值创建对象
Car myCar = new Car("Tesla Model 3");
Console.WriteLine(myCar.Model); // 输出: Tesla Model 3

// 多个参数
public class Rectangle
{
    public int Width;
    public int Height;
    
    public Rectangle(int width, int height)
    {
        Width = width;
        Height = height;
    }
}

Rectangle rect = new Rectangle(10, 5);
```

### 构造函数语法

| 元素 | 说明 |
| --- | --- |
| `public` | 访问修饰符 - 允许从任何地方创建 |
| 类名 | 构造函数必须与类具有相同的名称 |
| 参数 | 括号中传递的值 |
| 主体 | 创建对象时运行的代码 |

### 你的任务

创建一个带有有参构造函数的 `Person` 类，该构造函数：

1. 接收 `string name` 和 `int age` 作为参数
2. 将这些值赋给 `Name` 和 `Age` 字段

然后实现 `CreatePersonInfo` 来创建一个 Person 并返回其信息。

### 方法签名

```csharp
public Person(string name, int age)
public static string CreatePersonInfo(string name, int age)
```

### 预期结果

```
CreatePersonInfo("Alice", 25) -> "Name: Alice, Age: 25"
CreatePersonInfo("Bob", 30) -> "Name: Bob, Age: 30"
```

### 解答

```csharp
using System;

public class Person
{
    public string Name;
    public int Age;
    
    // 接收 name 和 age 的有参构造函数
    public Person(string name, int age)
    {
        Name = name;
        Age = age;
    }
}

public class Solution
{
    public static string CreatePersonInfo(string name, int age)
    {
        // 使用有参构造函数创建 Person
        Person person = new Person(name, age);
        // 返回格式为 "Name: [name], Age: [age]" 的字符串
        return $"Name: {person.Name}, Age: {person.Age}";
    }
}
```
