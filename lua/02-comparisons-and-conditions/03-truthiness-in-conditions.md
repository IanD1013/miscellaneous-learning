在这个 `if` 语句中，条件是数字 `0`，完全没有任何比较操作，而主体部分仍然会执行。
这会打印出 `runs`：

```lua
if 0 then
  print("runs")
end
```

Lua 接受任何值作为条件，并且遵循一条规则：`nil` 和 `false` 会使条件判断为假，而其他所有值都会使条件判断为真。
这包括 `0`、空字符串 `""` 以及字符串 `"false"`。
引号使得 `"false"` 成为一个字符串，而无论字符串的内容是什么，它都会通过条件判断。
只有不带引号的布尔值 `false` 才会判断为假。

能够通过条件判断的值被称为 **truthy**，而判断为假的两个值 `nil` 和 `false` 则被称为 **falsy**。
因此，对于任何 truthy 的 `value`，`if value then` 都会执行其主体。

这比 `if value == true then` 的测试范围更广。
只有当 `value` 本身就是布尔值 `true` 时，比较操作 `value == true` 才为 true，因此 `0 == true` 和 `"yes" == true` 的结果都是 `false`。
当你想要匹配任何 truthy 值时，请省略比较操作。

`not` 也遵循同样的规则。
对于 falsy 值它返回 `true`，对于 truthy 值它返回 `false`，所以 `not nil` 为 `true`，而 `not 0` 为 `false`。

### 统计 truthy 参数

编写 `count_truthy(a, b, c)`。
每个参数为 `nil`、`false`、`true`、`0`、`1`、`""`、`"false"` 或一个简短的单词。
返回这三个参数中有多少个是 truthy，结果为一个 0 到 3 的数字。

维护一个从 0 开始的局部计数器，每遇到一个 truthy 参数就加 1，最后返回该计数器。
为每个参数分别编写独立的 `if` 语句，而不是编写带有 `elseif` 分支的单个 `if`：`elseif` 链只会执行第一个满足条件的分支，因此计数永远无法超过 1。

### 解答

```lua
function count_truthy(a, b, c)
  local count = 0
  if a then
    count = count + 1
  end
  if b then
    count = count + 1
  end
  if c then
    count = count + 1
  end
  return count
end
```
