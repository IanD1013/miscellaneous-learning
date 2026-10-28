### float 类型

`float` 是一种 32 位浮点数，用于在需要节省内存且不需要高精度时存储小数值。

### float 与 double

| 类型 | 大小 | 精度 | 后缀 | 使用场景 |
| --- | --- | --- | --- | --- |
| float | 32 位 | ~7 位数字 | f 或 F | 图形、游戏、内存敏感场景 |
| double | 64 位 | ~15 位数字 | d 或 D | 常规计算、科学计算 |

### 声明 float

```csharp
// float 字面量必须使用 'f' 后缀
float temperature = 98.6f;
float price = 19.99f;
float pi = 3.14159f;

// 没有 'f' 时，编译器会将其视为 double（错误！）
// float wrong = 3.14;  // 编译错误！
```

### 必须使用 'f' 后缀

在 C# 中，像 `3.14` 这样的小数字面量默认会被视为 `double`。
要创建一个 `float`，必须添加 `f` 后缀：

```csharp
float correct = 3.14f;    // 可行！
float alsoCorrect = 0.5f; // 可行！
// float wrong = 3.14;    // 错误：无法将 double 转换为 float
```

### 何时使用 float

- 游戏开发（位置、速度）
- 图形编程（颜色、坐标）
- 对内存敏感的大型数组
- 不需要超过 7 位有效数字的精度时

### 你的任务

返回一个表示人体正常体温的 float 值：**98.6**

记得使用 `f` 后缀来创建 float 字面量！

### 方法签名

```csharp
public static float GetTemperature()
```

### 预期结果

```
GetTemperature() -> 98.6
```

### 解答

```csharp
using System;

public class Solution
{
    public static float GetTemperature()
    {
        // 返回表示体温的 float 值 98.6，记得使用 'f' 后缀
        return 98.6f;
    }
}
```
