### ref 关键字

`ref` 关键字允许你**按引用**传递参数，这意味着方法可以修改原始变量，而不仅仅是其值的副本。

### 按值传递 vs 按引用传递

```csharp
// 不使用 ref - 值被复制，原始变量不变
void Double(int x) { x = x * 2; }  // 原始变量不会被修改

// 使用 ref - 引用原始变量
void Double(ref int x) { x = x * 2; }  // 原始变量会被修改
```

### 使用 ref 参数

```csharp
// 声明：在参数中使用 ref
public static void Increment(ref int value)
{
    value++;  // 修改原始变量
}

// 调用：也必须使用 ref 关键字
int number = 5;
Increment(ref number);  // number 现在为 6
```

### 经典的 Swap 模式

```csharp
public static void Swap(ref int a, ref int b)
{
    int temp = a;  // 保存第一个值
    a = b;         // 用第二个值覆盖第一个
    b = temp;      // 将第二个设为保存的值
}

int x = 10, y = 20;
Swap(ref x, ref y);  // x=20, y=10
```

### 可用的辅助文件

- `ResultFormatter.Format(a, b)` - 返回格式化字符串，例如 `"a=5, b=10"`
- `SwapHelper.DemoSwap(ref x, ref y)` - swap 的参考实现

### 你的任务

1. 实现 `Swap` 方法，使用 `ref` 交换两个整数
2. 在 `SwapAndReturn` 中，使用正确的 `ref` 语法调用你的 `Swap` 方法
3. 使用 `ResultFormatter.Format(a, b)` 返回结果

### 方法签名

- `public static void Swap(ref int x, ref int y)` - 交换变量的值
- `public static string SwapAndReturn(int a, int b)` - 调用 Swap 并返回格式化的结果

### 预期结果

```
SwapAndReturn(5, 10) -> "a=10, b=5"
SwapAndReturn(1, 2) -> "a=2, b=1"
```

### 解答

```csharp
using System;

public class Solution
{
    public static string SwapAndReturn(int a, int b)
    {
        // 调用下面自己实现的 Swap 方法交换两个值
        Swap(ref a, ref b);
        // 然后使用 ResultFormatter.Format 返回结果
        return ResultFormatter.Format(a, b);
    }
    
    // 使用 ref 交换两个整数的 Swap 方法
    public static void Swap(ref int x, ref int y)
    {
        int temp = x;  // 保存 x 的值
        x = y;         // 用 y 覆盖 x
        y = temp;      // 将 y 设为保存的值
    }
}
```
