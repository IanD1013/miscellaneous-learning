你的第一个 Lua 函数共有三行，它会返回一小段文本：

```lua
function greeting()
  return "Hello, Lua!"
end
```

`function` 开始函数定义，`greeting` 是函数名。
你通过调用函数来运行它，也就是在函数名后面加上圆括号：`greeting()`。
定义中的空括号表示 `greeting` 不需要任何输入。
`return` 将一个值返回给调用该函数的代码，而 `end` 则结束该定义。
定义 `greeting` 并不会运行它的函数体（即 `function` 行和 `end` 之间的代码行）；只有当代码调用 `greeting()` 时，`return` 行才会运行。
当你点击 Run 时，你的文件会运行，在这个练习中，Run 还会为你调用 `greeting()` 并检查它返回的值。

双引号内的文本是字符串。
引号标记了文本的起始和结束位置，它们本身并不是值的一部分。
在这个问候语中，大写字母、空格和标点符号都算在内，因此 `"hello, lua!"` 和 `"Hello, Lua"` 都与 `"Hello, Lua!"` 是不同的字符串。
如果不加引号，Lua 会尝试将 `Hello, Lua!` 作为代码读取，因此 Run 会报错。

你的文件中没有任何打印输出，因此控制台将保持为空。
若想在控制台中看到返回的字符串，可以在 `end` 之后添加 `print(greeting())`：`greeting()` 先运行并返回其字符串，然后 `print` 在控制台中显示该字符串。
`print` 会显示文本但不会返回它。
如果在到达 `end` 时没有执行 `return` 行，函数将不返回任何值，结果中会显示为 `nil`。

### 你的任务

编辑器中已经包含了 `greeting` 的首行和末行。
在它们之间编写 `return` 行，使 `greeting()` 精确返回字符串 `Hello, Lua!`。

### 解答

```lua
function greeting()
  return "Hello, Lua!"
end
```
