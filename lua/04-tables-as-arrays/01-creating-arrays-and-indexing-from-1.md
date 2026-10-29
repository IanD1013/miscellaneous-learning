将值放在花括号之间并用逗号分隔，Lua 就会构建一个 table（表），它是一个容纳所有这些值的单一值。
以这种方式使用、其值位于位置 1、2、3 及之后的 table 被称为数组（array）。
每个值都是一个元素（element），而它的位置就是它的索引（index）。

```lua
local primes = {2, 3, 5, 7}
print(primes[1])
print(primes[#primes])
print(primes[0])
```

这将依次打印 `2`、`7`，然后是 `nil`。
table 后面的方括号会读取写在其中的索引处的元素，因此 `primes[1]` 是第一个元素。
计数从 1 开始，就像字符串中的字符位置一样，因此索引 0 处不存储任何内容。
读取没有元素的索引不会报错：它会返回 `nil`，在索引 0 处如此，在超出末尾一位的 `primes[5]` 处也是如此。

`#` 返回数组中元素的数量，就像 `#text` 返回字符串的长度一样，因此 `#primes` 是 4。
由于第一个元素位于索引 1，最后一个元素则位于等于该数量的索引处，因此无论数组的长度是多少，`primes[#primes]` 都会读取最后一个元素。

花括号还可以利用已有的值构建一个 table，并且函数可以直接返回它：

```lua
function both(a, b)
  return {a, b}
end
```

`both("x", "y")` 返回一个新数组，索引 1 处为 `"x"`，索引 2 处为 `"y"`。
结果面板会用方括号展示数组，因此它将其显示为 `["x", "y"]`。

编写 `first_and_last(items)`。
`items` 是一个包含字符串或数字的数组，它以类似于 `primes` 的 table 形式传入。
返回一个包含其第一个元素和最后一个元素的新数组。
`items` 可能为空，此时结果应为一个空 table。

### 解答

```lua
function first_and_last(items)
  return {items[1], items[#items]}
end
```
