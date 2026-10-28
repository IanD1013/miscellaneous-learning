### Private Set 属性

Private set 属性允许从任何地方读取属性，但只能在类本身内部进行修改。
这在保持封装性的同时提供了对数据的受控访问。

### 语法

```csharp
public string Name { get; private set; }
public decimal Balance { get; private set; }
```

### 自动属性与 Private Set

```csharp
// 自动属性：任何人都可以读取和写入
public string Name { get; set; }

// Private set：任何人都可以读取，只有类自身可以写入
public string Name { get; private set; }

// 只读：在构造函数中设置一次，之后不再更改
public string Name { get; }
```

### 何时使用 Private Set

| 场景 | 属性类型 |
| --- | --- |
| 值通过方法更改 | `{ get; private set; }` |
| 创建后值从不更改 | `{ get; }`（只读） |
| 值可以自由更改 | `{ get; set; }` |

### 示例：Counter 类

```csharp
public class Counter
{
    public int Count { get; private set; } = 0;
    
    public void Increment()
    {
        Count++;  // OK - 在类内部
    }
}

// 用法：
var counter = new Counter();
counter.Increment();           // OK
int value = counter.Count;     // OK - 可以读取
// counter.Count = 10;         // 错误 - 不能从外部设置
```

### 你的任务

创建一个带有 private set 属性的 `BankAccount` 类：

1. **AccountHolder** 属性 - 可以被公开读取，但只能被私有设置
2. **Balance** 属性 - 可以被公开读取，但只能被私有设置
3. **Constructor** - 接收账户持有人姓名和初始存款金额
4. **Deposit 方法** - 增加余额并返回新余额
5. **Withdraw 方法** - 如果资金充足则从余额中扣除并返回新余额。如果资金不足则返回 -1。

### 方法签名

```csharp
public string AccountHolder { get; private set; }
public decimal Balance { get; private set; }
public BankAccount(string accountHolder, decimal initialDeposit)
public decimal Deposit(decimal amount)
public decimal Withdraw(decimal amount)
```

### 预期结果

```
GetBankAccountInfo("Alice", 100.00) -> "Alice: 100.00"
DepositAndGetBalance("Bob", 50.00, 25.00) -> 75.00
WithdrawAndGetBalance("Carol", 100.00, 30.00) -> 70.00
WithdrawAndGetBalance("Dan", 50.00, 100.00) -> -1
```

### 解答

```csharp
using System;

public class BankAccount
{
    // 公开读取、私有设置的 AccountHolder 属性
    public string AccountHolder { get; private set; }
    
    // 公开读取、私有设置的 Balance 属性
    public decimal Balance { get; private set; }
    
    // 构造函数同时设置 AccountHolder 和 Balance
    public BankAccount(string accountHolder, decimal initialDeposit)
    {
        AccountHolder = accountHolder;
        Balance = initialDeposit;
    }
    
    // 增加余额并返回新余额
    public decimal Deposit(decimal amount)
    {
        Balance += amount;
        return Balance;
    }
    
    // 资金充足时扣除余额并返回新余额，资金不足时返回 -1
    public decimal Withdraw(decimal amount)
    {
        if (amount > Balance)
        {
            return -1;
        }
        Balance -= amount;
        return Balance;
    }
}

public class Solution
{
    public static string GetBankAccountInfo(string accountHolder, decimal initialDeposit)
    {
        var account = new BankAccount(accountHolder, initialDeposit);
        return $"{account.AccountHolder}: {account.Balance}";
    }
    
    public static decimal DepositAndGetBalance(string accountHolder, decimal initialDeposit, decimal depositAmount)
    {
        var account = new BankAccount(accountHolder, initialDeposit);
        return account.Deposit(depositAmount);
    }
    
    public static decimal WithdrawAndGetBalance(string accountHolder, decimal initialDeposit, decimal withdrawAmount)
    {
        var account = new BankAccount(accountHolder, initialDeposit);
        return account.Withdraw(withdrawAmount);
    }
}
```
