### 类中的字段 (Fields)

字段是属于类的变量，用于存储对象的数据（状态）。
它们定义了对象可以容纳的信息。

### 声明公共字段 (Public Fields)

```csharp
public class Car
{
    public string Brand;      // 存储汽车品牌的字段
    public int Year;          // 存储生产年份的字段
    public double Price;      // 存储价格的字段
}
```

### 访问字段

创建对象后，可以使用点表示法读取和写入其字段：

```csharp
Car myCar = new Car();    // 创建一个对象
myCar.Brand = "Toyota";   // 设置 Brand 字段
myCar.Year = 2023;        // 设置 Year 字段

string carBrand = myCar.Brand;  // 读取 Brand 字段
```

### 默认值

如果未显式设置，字段会自动初始化为默认值：

| 类型 | 默认值 |
| --- | --- |
| `int`, `double` | 0 |
| `string` | null |
| `bool` | false |

### 你的任务

通过按以下顺序添加两个公共字段来完成 `Person` 类：

1. `Name` (string) - 存储人的姓名
2. `Age` (int) - 存储人的年龄

然后完成 `CreatePerson` 方法以：

1. 使用提供的参数设置 person 对象的 `Name` 和 `Age` 字段
2. 返回 person 对象本身

测试将检查你返回的对象上的 `Name` 和 `Age` 字段，因此请确保两者都已设置。

### 方法签名

```csharp
public static Person CreatePerson(string name, int age)
```

### 预期结果

```
CreatePerson("Alice", 25) -> Person { Name = Alice, Age = 25 }
CreatePerson("Bob", 30) -> Person { Name = Bob, Age = 30 }
```

### 解答

```csharp
using System;

public class Person
{
    // 公共 string 字段 Name
    public string Name;

    // 公共 int 字段 Age
    public int Age;
}

public class Solution
{
    public static Person CreatePerson(string name, int age)
    {
        // 创建一个新的 Person 对象
        Person person = new Person();

        // 使用提供的参数设置 person 对象的 Name 和 Age 字段
        person.Name = name;
        person.Age = age;

        // 返回 person
        return person;
    }
}
```
