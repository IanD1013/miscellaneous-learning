### `this` 关键字

`this` 关键字引用类的当前实例。
它通常用于区分同名的类字段与构造函数/方法参数。

### 为什么使用 `this`？

当参数与字段同名时，参数会在该作用域内“遮蔽”（shadow）该字段。
使用 `this` 可以显式引用该实例字段。

```csharp
public class Example
{
    private int value;  // 这是一个字段
    
    public Example(int value)  // 这是一个同名的参数
    {
        // 不使用 'this' 时，'value' 指的是参数
        this.value = value;  // this.value = 字段，value = 参数
    }
}
```

### `this` 的常见用法

```csharp
// 1. 区分字段与参数
this.name = name;

// 2. 将当前实例传递给另一个方法
SomeMethod(this);

// 3. 调用另一个构造函数（构造函数链）
public Person() : this("Unknown", 0) { }
```

### 不使用 `this` 的问题

```csharp
public Person(string name, int age)
{
    name = name;  // 这是把参数赋值给它自己！字段没有改变。
    age = age;    // 这里也是同样的问题。
}
```

### 你的任务

完成 `Person` 构造函数，使用 `this` 关键字将 `name` 和 `age` 参数正确赋值给对应的私有字段。

### 方法签名

```csharp
public Person(string name, int age)
```

### 预期结果

```
CreateAndDescribePerson("Alice", 30) -> "Alice is 30 years old"
CreateAndDescribePerson("Bob", 25) -> "Bob is 25 years old"
```

### 解答

```csharp
using System;

public class Person
{
    private string name;
    private int age;
    
    // 使用 this 关键字区分字段和参数
    public Person(string name, int age)
    {
        this.name = name;  // this.name 是字段，name 是参数
        this.age = age;    // this.age 是字段，age 是参数
    }
    
    public string Describe()
    {
        return $"{name} is {age} years old";
    }
}

public class Solution
{
    public static string CreateAndDescribePerson(string name, int age)
    {
        Person person = new Person(name, age);
        return person.Describe();
    }
}
```
