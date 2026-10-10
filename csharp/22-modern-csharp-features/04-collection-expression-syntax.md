### 集合表达式语法

集合表达式（C# 12+）提供了一种使用 `[...]` 语法创建数组、列表和其他集合的简明方式。

### 基本用法

```csharp
// 使用集合表达式创建数组
int[] numbers = [1, 2, 3, 4, 5];

// 使用集合表达式创建 List
List<string> names = ["Alice", "Bob", "Charlie"];

// 空集合
int[] empty = [];
```

### 与传统语法对比

集合表达式比传统方式更简短且更具可读性：

```csharp
// 传统的数组初始化
int[] oldWay = new int[] { 1, 2, 3 };

// 集合表达式（C# 12+）
int[] newWay = [1, 2, 3];

// 传统的 List 初始化
List<int> oldList = new List<int> { 1, 2, 3 };

// 用于 List 的集合表达式
List<int> newList = [1, 2, 3];
```

### 在集合表达式中使用变量

你可以在集合表达式内部使用变量和表达式：

```csharp
int x = 10;
int y = 20;
int[] values = [x, y, x + y, 100];
// 结果：[10, 20, 30, 100]
```

### 你的任务

创建一个接收五个整数参数的方法，并使用集合表达式语法返回一个包含这五个数字的数组。

### 方法签名

```csharp
public static int[] CreateNumberArray(int first, int second, int third, int fourth, int fifth)
```

### 预期结果

```
CreateNumberArray(1, 2, 3, 4, 5) -> [1, 2, 3, 4, 5]
CreateNumberArray(10, 20, 30, 40, 50) -> [10, 20, 30, 40, 50]
```

### 解答

```csharp
using System;
using System.Collections.Generic;

public class Solution
{
    public static int[] CreateNumberArray(int first, int second, int third, int fourth, int fifth)
    {
        // 使用集合表达式语法，按顺序创建并返回包含五个数字的数组
        return [first, second, third, fourth, fifth];
    }
}
```
