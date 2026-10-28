### 虚方法

`virtual` 关键字用于标记可以被派生类重写（override）的方法。
这实现了**多态**（polymorphism），即不同类型对同一个方法调用做出不同响应的能力。

### 声明虚方法

```csharp
public class Animal
{
    // virtual 允许派生类重写此方法
    public virtual string Speak()
    {
        return "Some sound";
    }
}
```

### 重写虚方法

```csharp
public class Dog : Animal
{
    // override 提供新的实现
    public override string Speak()
    {
        return "Woof!";
    }
}

public class Cat : Animal
{
    public override string Speak()
    {
        return "Meow!";
    }
}
```

### 运行时的多态性

```csharp
Animal myPet = new Dog();  // 变量是 Animal 类型
string sound = myPet.Speak();  // 调用 Dog.Speak() -> "Woof!"

myPet = new Cat();  // 同一个变量，不同的对象
sound = myPet.Speak();  // 调用 Cat.Speak() -> "Meow!"
```

### virtual 与非虚方法对比

| 关键字 | 是否可重写？ | 运行时行为 |
| --- | --- | --- |
| `virtual` | 是，使用 `override` | 调用实际对象的方法 |
| (无) | 否 | 调用声明类型的方法 |

### 你的任务

创建一个包含虚方法的类层次结构：

1. **Animal** 基类，包含一个返回 `"Some sound"` 的 `virtual` 方法 `Speak()`
2. **Dog** 类，继承自 Animal 并重写 `Speak()`，返回 `"Woof!"`
3. **Cat** 类，继承自 Animal 并重写 `Speak()`，返回 `"Meow!"`
4. 完善 `TestAnimalSpeak()`，根据传入参数创建对应的动物对象并返回其 `Speak()` 的结果

### 方法签名

```csharp
public static string TestAnimalSpeak(string animalType)
```

### 预期结果

```
TestAnimalSpeak("animal") -> "Some sound"
TestAnimalSpeak("dog") -> "Woof!"
TestAnimalSpeak("cat") -> "Meow!"
```

### 解答

```csharp
using System;

public class Solution
{
    public static string TestAnimalSpeak(string animalType)
    {
        // 根据 animalType 创建对应的动物（不区分大小写）
        // 未知类型默认使用 Animal 基类
        Animal animal = animalType.ToLower() switch
        {
            "dog" => new Dog(),
            "cat" => new Cat(),
            _ => new Animal()
        };
        
        // 返回调用 Speak() 的结果
        return animal.Speak();
    }
}

// Animal 基类，包含虚方法 Speak()
public class Animal
{
    public virtual string Speak()
    {
        return "Some sound";
    }
}

// Dog 类重写 Speak()
public class Dog : Animal
{
    public override string Speak()
    {
        return "Woof!";
    }
}

// Cat 类重写 Speak()
public class Cat : Animal
{
    public override string Speak()
    {
        return "Meow!";
    }
}
```
