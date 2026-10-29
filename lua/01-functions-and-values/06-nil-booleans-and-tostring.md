`..` 可以连接字符串和数字，因此 `"total: " .. 42` 会得到 `"total: 42"`。
如果传入 `true` 或 `nil`，程序就会报错停止。
来看这个函数：

```lua
function label(value)
  return "value: " .. value
end
```

调用 `label(true)` 并点击 Run，会报错 `main.lua:2: attempt to concatenate a boolean value (local 'value')`。
调用 `label(nil)` 也会以相同的方式失败，提示遇到了 `nil` 值。
`..` 只接受字符串和数字，所以任何其他类型的值在进行连接之前，都必须先通过 `tostring` 转换。

`nil` 表示缺失的值。
当调用未传入对应实参时，形参的值就是 `nil`；另外，如果一个函数只是打印了文本而没有返回任何内容，其结果也会显示为 `nil`。
它既不是 `0`，也不是空字符串 `""`（它们分别是普通的数字和普通的字符串）。

`true` 和 `false` 是两个布尔值（boolean），代表 Lua 中的“是”与“否”。
编写它们时不要加引号：`true` 是布尔值，而 `"true"` 则是由四个字母组成的字符串。

`type(value)` 会以字符串形式返回某个值所属类型的名称。
整数和浮点数的结果都是 `"number"`：

```text
call            returns
type("apple")   "string"
type(42)        "number"
type(2.5)       "number"
type(false)     "boolean"
type(nil)       "nil"
```

`tostring(value)` 可以将一个值转换为文本：`tostring(true)` 返回 `"true"`，`tostring(nil)` 返回 `"nil"`，`tostring(2.5)` 返回 `"2.5"`。
它的结果始终是一个字符串，因此可以使用 `..` 进行连接。

### 你的任务

编写 `describe(value)` 的函数体。
它需要返回 `value` 的类型名称，后跟一个冒号和一个空格，然后是转换为文本形式的 `value`。
`value` 可能是单词、整数、带一位小数的数字、`true`、`false` 或 `nil`，因此 `describe(42)` 返回 `number: 42`，`describe(true)` 返回 `boolean: true`，`describe(nil)` 返回 `nil: nil`。

### 解答

```lua
function describe(value)
  return type(value) .. ": " .. tostring(value)
end
```
