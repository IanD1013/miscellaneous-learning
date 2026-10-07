### C# 中的范围和索引

C# 提供了强大的语法来从末尾访问数组元素并提取切片，使数组操作更具表达力和可读性。

### 索引类型 (^)

`^` 运算符创建一个从数组末尾开始计数的 Index。
`^1` 表示最后一个元素，`^2` 表示倒数第二个元素，依此类推。

```csharp
int[] numbers = { 10, 20, 30, 40, 50 };

int last = numbers[^1];      // 50（最后一个元素）
int secondLast = numbers[^2]; // 40（倒数第二个）
int third = numbers[^3];      // 30（倒数第三个）
```

### 范围类型 (..)

`..` 运算符创建一个指定数组切片的 Range。
起始索引是包含的（inclusive），结束索引是不包含的（exclusive）。

```csharp
int[] numbers = { 10, 20, 30, 40, 50 };

int[] slice1 = numbers[1..3];   // { 20, 30 } - 索引 1 到 2
int[] slice2 = numbers[..3];    // { 10, 20, 30 } - 起始到索引 2
int[] slice3 = numbers[2..];    // { 30, 40, 50 } - 索引 2 到末尾
int[] all = numbers[..];        // { 10, 20, 30, 40, 50 } - 完整副本
```

### 将 ^ 与范围结合使用

你可以在范围中使用 `^` 从末尾开始计数：

```csharp
int[] numbers = { 10, 20, 30, 40, 50 };

int[] lastTwo = numbers[^2..];     // { 40, 50 } - 最后两个元素
int[] exceptLast = numbers[..^1];  // { 10, 20, 30, 40 } - 除最后一个以外的所有元素
int[] middle = numbers[1..^1];     // { 20, 30, 40 } - 跳过第一个和最后一个
```

### 范围参考表

| 语法 | 说明 | 示例（针对 {1,2,3,4,5}） |
| --- | --- | --- |
| `arr[^1]` | 最后一个元素 | 5 |
| `arr[^2]` | 倒数第二个元素 | 4 |
| `arr[1..3]` | 索引 1 到 2 | {2, 3} |
| `arr[..2]` | 起始到索引 1 | {1, 2} |
| `arr[2..]` | 索引 2 到末尾 | {3, 4, 5} |
| `arr[^2..]` | 最后两个元素 | {4, 5} |
| `arr[..^1]` | 除最后一个以外的所有元素 | {1, 2, 3, 4} |

### 你的任务

编写一个方法，使用带有 `^` 运算符的范围语法返回数组的最后两个元素。

### 方法签名

```csharp
public static int[] GetLastTwoElements(int[] numbers)
```

### 预期结果

```
GetLastTwoElements([1, 2, 3, 4, 5]) -> [4, 5]
GetLastTwoElements([10, 20]) -> [10, 20]
GetLastTwoElements([7, 8, 9]) -> [8, 9]
```

### 解答

```csharp
using System;

public class Solution
{
    public static int[] GetLastTwoElements(int[] numbers)
    {
        // 使用范围语法，从倒数第二个元素取到末尾
        return numbers[^2..];
    }
}
```
