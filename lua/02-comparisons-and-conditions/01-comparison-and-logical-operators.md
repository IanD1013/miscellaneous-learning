`3 < 5` 是一个比较运算，其值为布尔值 `true`。
`5 ~= 5` 为 `false`，因为 `~=` 表示不等于，而这两个值是相等的。
Lua 拥有六个比较运算符：

- `==` 等于
- `~=` 不等于（一个波浪号后跟一个等号）
- `<` 小于，`>` 大于
- `<=` 小于或等于，`>=` 大于或等于

等于使用两个等号：单个 `=` 不是比较运算，`return a = b` 会引发错误。
在其他某些语言中用于表示不等于的 `!=` 也是错误的。

比较运算的结果是一个值，因此函数可以直接返回它：

```lua
function is_positive(n)
  return n > 0
end
```

`is_positive(4)` 返回 `true`。
`is_positive(0)` 返回 `false`，因为 0 并不大于其自身。
`0 >= 0` 为 `true`，因为 `>=` 也接受两个相等的数字。

### 组合比较

`and`、`or` 和 `not` 是逻辑运算符。
这里的 `and` 连接了两个比较运算：

```lua
function all_same(a, b, c)
  return a == b and b == c
end
```

Lua 会先计算 `a == b`。
如果结果为 `false`，`and` 将直接得出 `false`，而不会再去检查 `b == c`。
如果结果为 `true`，最终结果将取决于 `b == c` 的计算结果，因此 `all_same(2, 2, 3)` 计算为 `true and false`，即 `false`。
`and` 的两侧都需要是完整的比较运算：`a == b and == c` 会报错，因为第二个 `==` 的左侧没有任何内容。

`or` 同样从左侧开始计算，但只要左侧为 `true` 就会立即得出结果为 `true`。
在左侧为 `false` 的情况下，才由右侧决定结果：`3 == 4 or 4 == 4` 为 `true`，而 `3 == 4 or 5 == 6` 为 `false`。

`not` 返回相反的布尔值：`not (3 < 5)` 为 `false`，而 `not (5 ~= 5)` 为 `true`。
圆括号可以让 Lua 先计算比较运算。

编写 `is_between(value, low, high)`。
这三个参数均为整数。
当 `value` 至少为 `low` 且至多为 `high`（包含两端端点，因此等于 `low` 或 `high` 的 `value` 也在范围内）时返回 `true`。
其他任何情况均返回 `false`，包括 `low` 大于 `high` 的调用情况：因为此时该区间为空。

### 解答

```lua
function is_between(value, low, high)
  return value >= low and value <= high
end
```
