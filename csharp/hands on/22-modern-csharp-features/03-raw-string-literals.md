### 原始字符串字面量（Raw String Literals）

原始字符串字面量（C# 11+）允许你编写无需转义特殊字符的字符串。
它们以至少三个双引号（`"""`）开头和结尾。

### 基本语法

```csharp
// 传统字符串 - 需要转义
string json1 = "{\"name\": \"John\"}";

// 原始字符串字面量 - 无需转义！
string json2 = """
               {"name": "John"}
               """;
```

### 多行字符串

原始字符串会保留格式。
闭合的 `"""` 位置决定了缩进方式：

```csharp
string html = """
              <div>
                  <p>Hello World</p>
              </div>
              """;
// 结果没有前导空格 - 它们会根据闭合引号的位置被裁剪掉
```

### 原始字符串中的字符串插值

使用带有双大括号 `{{}}` 的 `$$` 前缀进行插值：

```csharp
string name = "Alice";
int score = 95;

// $$ 表示使用 {{ }} 进行插值
string result = $$"""
                Name: {{name}}
                Score: {{score}}
                """;
```

`$` 符号的数量决定了插值所需的大括号数量。

### 为什么使用双大括号？

JSON 使用 `{}` 表示对象。
使用 `$$` 时，单个大括号 `{}` 表示字面量字符，而 `{{}}` 会触发插值：

```csharp
// 这会在 JSON 中输出字面量 { }，但 {{name}} 会被替换
string json = $$"""
              { "person": "{{name}}" }
              """;
```

### 你的任务

创建一个方法，使用带有插值的原始字符串字面量返回表示某个人的 JSON 字符串。

### 方法签名

```csharp
public static string CreatePersonJson(string name, int age, string city)
```

### 预期 JSON 格式

```json
{
    "name": "John",
    "age": 30,
    "city": "New York"
}
```

### 预期结果

```
CreatePersonJson("John", 30, "New York") -> JSON with name "John", age 30, city "New York"
CreatePersonJson("Alice", 25, "London") -> JSON with name "Alice", age 25, city "London"
```

### 解答

```csharp
using System;

public class Solution
{
    public static string CreatePersonJson(string name, int age, string city)
    {
        // 使用 $$ 原始字符串：单个 { } 是字面量，{{ }} 用于插值
        // 闭合 """ 的缩进会从每一行中裁剪掉
        return $$"""
            {
                "name": "{{name}}",
                "age": {{age}},
                "city": "{{city}}"
            }
            """;
    }
}
```
