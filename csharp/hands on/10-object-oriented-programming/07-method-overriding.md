### 方法重写（Method Overriding）

方法重写允许派生类为已在其基类中定义的方法提供特定实现，从而完全替换继承的行为。

### override 关键字

```csharp
public class Animal
{
    public virtual string Speak()  // 必须是 virtual
    {
        return "Some sound";
    }
}

public class Cat : Animal
{
    public override string Speak()  // 使用 override 关键字
    {
        return "Meow";
    }
}
```

### 重写的工作原理

当你重写一个方法时：

1. 基类方法必须被标记为 `virtual`
2. 派生类方法必须使用 `override` 关键字
3. 方法签名必须完全匹配（相同的名称、参数和返回类型）

```csharp
Cat cat = new Cat();
cat.Speak();  // 返回 "Meow" - 派生类版本

Animal animal = new Cat();  // 多态！
animal.Speak();  // 仍然返回 "Meow" - 重写生效
```

### 重写（Override）与隐藏（new 关键字）的对比

| 方式 | 关键字 | 行为 |
| --- | --- | --- |
| 重写（Overriding） | `override` | 多态地替换基类行为 |
| 隐藏（Hiding） | `new` | 隐藏基类方法，不支持多态 |

### 你的任务

Animal.cs 中的 `Animal` 类有一个返回 `"Some sound"` 的虚方法 `Speak()`。
创建一个 `Dog` 类，满足以下要求：

1. 继承自 `Animal`
2. 重写 `Speak()` 方法并返回 `"Woof"`

### 方法签名

```csharp
public override string Speak()
```

### 预期结果

```
new Dog().Speak() -> "Woof"
new Animal().Speak() -> "Some sound"
((Animal)new Dog()).Speak() -> "Woof" (多态！)
```

### 解答

```csharp
using System;

public class Dog : Animal
{
    // 重写 Speak 方法，返回 "Woof"
    public override string Speak()
    {
        return "Woof";
    }
}

public class Solution
{
    public static string TestDogSpeak()
    {
        Dog dog = new Dog();
        return dog.Speak();
    }
    
    public static string TestAnimalSpeak()
    {
        Animal animal = new Animal();
        return animal.Speak();
    }
    
    public static string TestPolymorphicSpeak()
    {
        Animal animal = new Dog();
        return animal.Speak();
    }
    
    public static string TestDogName(string name)
    {
        Dog dog = new Dog();
        dog.Name = name;
        return dog.Name;
    }
}
```
