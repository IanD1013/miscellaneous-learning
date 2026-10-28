### 什么是数组（Array）？

**数组**（array）是一种将相同类型的多个值保存在单个变量中的集合。
与其为每个项目创建单独的变量（例如 `fruit1`、`fruit2`、`fruit3`），不如将它们全部存放在同一个容器中。

### 创建数组

```csharp
// 声明并用值初始化数组
string[] fruits = { "Apple", "Banana", "Cherry" };

// 声明指定大小的数组（所有元素初始为默认值）
int[] numbers = new int[5]; // 创建有 5 个位置的数组，全部为 0

// 使用 new 关键字声明并初始化
string[] colors = new string[] { "Red", "Green", "Blue" };
```

### 访问数组元素

数组使用**从零开始的索引**（zero-based indexing），第一个元素位于索引 0：

```csharp
string[] fruits = { "Apple", "Banana", "Cherry" };
Console.WriteLine(fruits[0]); // 输出：Apple
Console.WriteLine(fruits[1]); // 输出：Banana
Console.WriteLine(fruits[2]); // 输出：Cherry
```

### 数组长度

使用 `Length` 属性获取元素的数量：

```csharp
string[] fruits = { "Apple", "Banana", "Cherry" };
Console.WriteLine(fruits.Length); // 输出：3
```

### Foreach 循环

`foreach` 循环专门用于遍历数组等集合。
它会自动处理迭代，因此你无需管理索引变量。

```csharp
foreach (type variableName in collection)
{
    // 使用 variableName 访问每个元素
}
```

### Foreach 与 For 循环的对比

```csharp
string[] names = { "Alice", "Bob", "Charlie" };

// For 循环 - 由你管理索引
for (int i = 0; i < names.Length; i++)
{
    Console.WriteLine(names[i]);
}

// Foreach 循环 - 更简洁、更安全
foreach (string name in names)
{
    Console.WriteLine(name);
}
```

### 何时使用 Foreach

- 当你需要按顺序处理每个元素时
- 当你不需要索引位置时
- 当你希望代码更简洁、更具可读性时

### 你的任务

编写一个方法，接收一个水果名称数组，并使用 `foreach` 循环在单独的行上打印出每种水果。

### 方法签名

```csharp
public static void PrintFruits(string[] fruits)
```

### 预期结果

```
PrintFruits(new string[] { "Apple", "Banana", "Cherry" }) 打印：
Apple
Banana
Cherry

PrintFruits(new string[] { "Mango" }) 打印：
Mango
```

### 解答

```csharp
using System;

public class Solution
{
    public static void PrintFruits(string[] fruits)
    {
        // 使用 foreach 循环把每种水果打印在单独的一行
        foreach (string fruit in fruits)
        {
            Console.WriteLine(fruit);
        }
    }
}
```
