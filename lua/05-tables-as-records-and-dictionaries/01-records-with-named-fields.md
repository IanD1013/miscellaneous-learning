table 中的每个值都存储在一个键（key）下。
在你之前构建的数组中，键是位置 1、2、3。
键也可以是一个名称：

```lua
local person = {first = "Grace", last = "Hopper"}
print(person.first)
print(person["last"])
print(person.middle)
```

这会依次打印出 `Grace`、`Hopper`，然后是 `nil`。

在花括号内部，`first = "Grace"` 将字符串 `"Grace"` 存储在键 `first` 下。
键与其对应的值组合在一起称为字段（field），逗号用于分隔各个字段。
这里的键名不需要加引号。
字段组合在一起用于描述同一个事物的 table（例如这里的 person），通常被称为记录（record）。

`person.first` 用于读取字段：table、一个点号，然后是字段名。
它是 `person["first"]` 的简写，后者将键作为字符串写在方括号中，就像 `items[1]` 将数字放在方括号中一样。
请保留引号。
如果没有引号，`first` 会被当作变量名，而由于不存在名为 `first` 的变量，`person[first]` 会返回 `nil`。

`print(person.middle)` 不会报错，即使 `person` 没有 `middle` 字段：从未设置过的字段读取结果为 `nil`。
只有当你把该 `nil` 当作文本使用时才会出错。
`"Grace " .. person.middle` 会因 `attempt to concatenate a nil value (field 'middle')` 而终止运行。
由于 `nil` 在条件判断中算作 false，因此 `if person.middle then` 仅在记录包含 middle name 时才会执行其代码块。

编写 `full_name(person)`。
调用它时传入的记录结构与上文类似：`first` 和 `last` 始终存在，部分记录还包含 `middle`。
返回一个字符串：名字（first name），如果有中间名（middle name）则加上中间名，然后是姓氏（last name），中间以单个空格分隔。

### 解答

```lua
function full_name(person)
  if person.middle then
    return person.first .. " " .. person.middle .. " " .. person.last
  end
  return person.first .. " " .. person.last
end
```
