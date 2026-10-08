### Private 访问修饰符

`private` 关键字限制了对成员的访问权限，使其只能在同一个类内部被使用。
这是**封装**（encapsulation）的基础，隐藏内部数据，并通过 public 方法暴露受控的访问方式。

### 为什么使用私有字段？

```csharp
public class Counter
{
    private int count;  // 只能在 Counter 类内部访问
    
    public void Increment()
    {
        count++;  // OK - 同一个类
    }
    
    public int GetCount()
    {
        return count;  // OK - 同一个类
    }
}

// 在类的外部：
Counter c = new Counter();
// c.count = 100;  // 错误：'count' 是 private 的
c.Increment();     // OK - 使用 public 方法
int value = c.GetCount();  // OK - 使用 public 方法
```

### Public 与 Private 对比

| 修饰符 | 可访问范围 | 适用场景 |
| --- | --- | --- |
| `public` | 任何地方 | 外部代码需要调用的方法/属性 |
| `private` | 仅限同一个类 | 内部数据、辅助方法 |

### 封装模式

```csharp
public class Temperature
{
    private double celsius;  // 隐藏的内部状态
    
    public void SetCelsius(double value)
    {
        // 存储之前先进行验证
        if (value >= -273.15)
            celsius = value;
    }
    
    public double GetCelsius()
    {
        return celsius;
    }
}
```

### 格式化为两位小数

本练习需要将余额显示为 `50.00` 而不是 `50`。
在插值字符串中的值后面加上 `:F2`：

```csharp
double balance = 50;
Console.WriteLine($"Balance: {balance:F2}");  // Balance: 50.00
```

有关此类格式化的内容将在本课程稍后的章节中专门讲解。
在这里你只需要使用 `:F2` 即可。

### 你的任务

创建一个 `BankAccount` 类，使用**私有字段**来保护余额不被直接篡改：

1. 一个 **private** 的 `balance` 字段
2. 一个用于设置初始余额的构造函数
3. 一个用于读取余额的 public `GetBalance()` 方法
4. 一个用于存钱的 public `Deposit(double amount)` 方法
5. 一个 public `Withdraw(double amount)` 方法：
   - 如果资金充足，扣除对应金额并返回 `true`
   - 如果资金不足，保持余额不变并返回 `false`

### 方法签名

```csharp
public static string TestBankAccount(double initialDeposit, double withdrawAmount)
```

### 预期结果

```
TestBankAccount(100.0, 50.0) -> "Balance: 50.00, Withdrawal: Success"
TestBankAccount(100.0, 150.0) -> "Balance: 100.00, Withdrawal: Failed"
```

### 解答

```csharp
using System;

public class Solution
{
    public static string TestBankAccount(double initialDeposit, double withdrawAmount)
    {
        // 使用 initialDeposit 创建 BankAccount
        BankAccount account = new BankAccount(initialDeposit);
        // 尝试取出 withdrawAmount
        bool success = account.Withdraw(withdrawAmount);
        // 按 "Balance: X.XX, Withdrawal: Success/Failed" 格式返回结果，余额保留两位小数
        string result = success ? "Success" : "Failed";
        return $"Balance: {account.GetBalance():F2}, Withdrawal: {result}";
    }
}

public class BankAccount
{
    // 私有的 balance 字段
    private double balance;
    
    // 接收初始存款的构造函数
    public BankAccount(double initialDeposit)
    {
        balance = initialDeposit;
    }
    
    // 返回余额的 public 方法
    public double GetBalance()
    {
        return balance;
    }
    
    // 增加余额的 public 方法
    public void Deposit(double amount)
    {
        balance += amount;
    }
    
    // 资金充足时扣除金额并返回 true，资金不足时保持余额不变并返回 false
    public bool Withdraw(double amount)
    {
        if (amount > balance)
        {
            return false;
        }
        balance -= amount;
        return true;
    }
}
```
