### foreach 循环

当不需要索引时，`foreach` 循环提供了一种更简单的方式来遍历集合。
它会自动处理迭代，并让你直接访问每个元素。

### 基本语法

```csharp
foreach (Type variableName in collection)
{
    // 直接使用 variableName
}
```

### foreach 与 for 对比

```csharp
// 使用 for - 由你管理索引
for (int i = 0; i < names.Length; i++)
{
    Console.WriteLine(names[i]);
}

// 使用 foreach - 只需要值时更简洁
foreach (string name in names)
{
    Console.WriteLine(name);
}
```

### 何时使用 foreach

- 当你需要按顺序读取每个元素时
- 当你不需要知道索引时
- 当你在遍历过程中不需要修改数组时

### 何时改用 for

- 当你需要索引进行计算时
- 当你需要修改数组元素时
- 当你需要反向遍历或跳过元素时

### 你的任务

编写一个方法，使用 `foreach` 循环将数组中的每个名字单独打印在一行上。

### 方法签名

```csharp
public static void PrintNames(string[] names)
```

### 预期输出

```
PrintNames(["Alice", "Bob", "Charlie"]) 打印：
Alice
Bob
Charlie
```

### 解答

```csharp
using System;

public class Solution
{
    public static void PrintNames(string[] names)
    {
        // 使用 foreach 将每个名字单独打印在一行上
        foreach (string name in names)
        {
            Console.WriteLine(name);
        }
    }
}
```
