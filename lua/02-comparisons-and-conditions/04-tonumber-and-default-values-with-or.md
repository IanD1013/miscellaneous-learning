`tonumber` 可以将写成数字的文本转换为对应的数字。
比较这两行代码：

```lua
print("42" == 42)
print(tonumber("42") == 42)
```

第一行输出 `false`。
引号使 `"42"` 成为一个字符串，而无论它们看起来多么相似，字符串永远不等于数字。
第二行输出 `true`，因为 `tonumber("42")` 返回数字 `42`。
同样，`tonumber("2.5")` 返回 `2.5`，而 `tonumber("-8")` 返回 `-8`。
当文本不是数字时，比如 `tonumber("abc")` 或 `tonumber("")`，`tonumber` 会返回 `nil`。
它不会抛出错误来中止程序，因此你的代码可以继续运行，并选择使用其他值作为替代。

### 使用 `or` 设置默认值

到目前为止，`or` 一直用于连接两个比较表达式，例如 `x < 0 or x > 10`。
`a or b` 的完整规则是：当 `a` 为真（truthy）时，结果就是 `a` 本身；否则结果是 `b`。
两个比较表达式会得到两个布尔值，因此在那里的结果也是布尔值。
其他类型的值表明 `or` 从不将其结果转换为 `true` 或 `false`：`nil or 5` 的结果是 `5`，而 `"x" or 5` 的结果是 `"x"`。

这使得 `or` 成为提供默认值的常用方式，在期望的值为 `nil` 时作为备用值：

```lua
local count = tonumber("15") or 0
```

当 `tonumber` 返回数字时，`count` 就是该数字。
当它返回 `nil`（属于假值/falsy）时，`count` 会得到默认值 `0`。
那么 `print((tonumber("ten") or 0) + 1)` 会输出什么呢？
这行代码不需要你的函数，所以你现在就可以把它粘贴到编辑器中并点击 Run 来看看结果。

数字 0 不需要额外检查：`tonumber("0")` 是数字 `0`，每个数字都是真值（truthy），因此 `tonumber("0") or 7` 的结果是 `0`。

### 任务

编写 `number_or_default(text, default)`。
`text` 是一个简短的字符串：一个整数（例如 `"15"`）、一个小数（例如 `"2.5"`），或者不是数字的内容（例如 `"abc"`、`""` 或 `"12ab"`）。
`default` 是一个整数。
返回 `text` 中表示的数字；当 `text` 不是数字时，返回 `default`。

### 解答

```lua
function number_or_default(text, default)
  return tonumber(text) or default
end
```
