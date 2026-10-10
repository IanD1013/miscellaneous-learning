### 集合中的展开运算符（Spread Operator）

展开运算符 `..`（C# 12+）允许你将一个集合中的元素“展开”或扩展到另一个集合中。
这在合并数组、列表或任何可枚举集合时非常有用。

### 基本语法

```csharp
int[] numbers1 = [1, 2, 3];
int[] numbers2 = [4, 5, 6];

// 使用展开运算符合并数组
int[] combined = [..numbers1, ..numbers2];  // [1, 2, 3, 4, 5, 6]
```

### 展开的同时添加元素

```csharp
int[] original = [2, 3, 4];

// 在前面、中间或后面添加元素
int[] withPrefix = [1, ..original];           // [1, 2, 3, 4]
int[] withSuffix = [..original, 5];           // [2, 3, 4, 5]
int[] withBoth = [0, ..original, 5, 6];       // [0, 2, 3, 4, 5, 6]
```

### 合并多个集合

```csharp
int[] a = [1, 2];
int[] b = [3, 4];
int[] c = [5, 6];

int[] all = [..a, ..b, ..c];  // [1, 2, 3, 4, 5, 6]
```

### 展开运算符 vs 传统 Concat

| 方式 | 语法 | 说明 |
| --- | --- | --- |
| Spread | `[..arr1, ..arr2]` | 简洁、现代、易读 |
| Concat | `arr1.Concat(arr2).ToArray()` | 需要 LINQ，较为繁琐 |

### 你的任务

实现一个方法，使用展开运算符将两个整数数组合并为一个数组。
第一个数组的元素应当位于第二个数组的元素之前。

### 方法签名

```csharp
public static int[] MergeArrays(int[] first, int[] second)
```

### 预期结果

```
MergeArrays([1, 2, 3], [4, 5, 6]) -> [1, 2, 3, 4, 5, 6]
MergeArrays([10], [20, 30]) -> [10, 20, 30]
MergeArrays([], [1, 2]) -> [1, 2]
```

### 解答

```csharp
using System;

public class Solution
{
    public static int[] MergeArrays(int[] first, int[] second)
    {
        // 先展开第一个数组，再展开第二个数组
        return [..first, ..second];
    }
}
```
