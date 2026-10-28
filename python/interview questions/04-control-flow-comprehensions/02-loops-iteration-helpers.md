Python 的循环是围绕遍历一个值序列构建的，而不是围绕一个你手动递增的计数器。
去用 `range(len(...))` 或手动索引，通常说明你还没学会能干净利落完成这件事的辅助函数。
本课涵盖 `for` 和 `while`、`range`、遍历列表、字典和字符串、`enumerate` 和 `zip` 辅助函数、`for/else` 和 `while/else` 子句、`break` 和 `continue`，以及在遍历列表时修改它这个经典陷阱。

### for、while 和 range

`for` 循环直接遍历任何可迭代对象（iterable）的元素。
你几乎从不需要索引。

```python
for name in ["ann", "bo", "cy"]:
    print(name)
```

`range(stop)`、`range(start, stop)` 和 `range(start, stop, step)` 会产生整数。
stop 值是不包含的，所以 `range(3)` 产生 `0, 1, 2`。
`range` 是惰性的（lazy）：它不会构建一个列表，而是按需计算值。

```python
list(range(2, 10, 3))   # [2, 5, 8]
list(range(5, 0, -1))   # [5, 4, 3, 2, 1]
```

`while` 循环只要其条件保持为真值就会一直运行。
当你事先不知道迭代次数时使用它。
忘记推进循环变量会让你得到一个无限循环。

### 遍历字典和字符串

遍历一个字典产生的是它的键，而不是它的值或键值对。
用 `.values()` 获取值，用 `.items()` 获取键/值对。

```python
prices = {"pen": 2, "ink": 5}
for k in prices:            # pen, ink   （键）
    ...
for k, v in prices.items(): # pen 2, ink 5
    ...
```

遍历一个字符串每次产生一个字符，每个都是长度为 1 的字符串。
Python 中没有单独的字符类型。

### enumerate

当你同时需要索引和值时，使用 `enumerate` 而不是手动计数器。
它产生 `(index, value)` 对，并接受一个可选的 `start`。

```python
for i, ch in enumerate("ab"):       # (0, 'a'), (1, 'b')
    ...
for i, ch in enumerate("ab", start=1):  # (1, 'a'), (2, 'b')
    ...
```

`start` 只会偏移报告出来的编号；它不会跳过任何元素。

### zip 和长度不等的情况

`zip` 同步地遍历多个可迭代对象，产生元组。
它在最短的输入处停止，静默地丢弃较长输入多出来的尾部。

```python
list(zip([1, 2, 3], ["a", "b"]))   # [(1, 'a'), (2, 'b')]
```

如果你希望在长度不匹配时报错，传入 `strict=True`（3.10 中新增），它会抛出 `ValueError`。
`zip` 也是惰性的，所以要把它包在 `list` 或 `dict` 中来实际生成结果。

### for/else 和 while/else

循环的 `else` 子句只有在循环没有遇到 `break` 而结束时才会执行。
它在"搜索并报告"的模式中很方便。
如果循环为空或运行完毕，`else` 会执行；`break` 会跳过它。

```python
for n in [1, 3, 5]:
    if n % 2 == 0:
        print("found even")
        break
else:
    print("no even number")   # 这一行会打印
```

`continue` 会跳到下一次迭代，并且不算作 `break`，所以在只使用了 `continue` 的循环之后，`else` 仍然会执行。

### 在遍历列表时修改它

在遍历列表时删除或插入元素，会让迭代器底下的索引发生偏移，于是有些元素会被跳过。

```python
nums = [1, 2, 2, 3]
for n in nums:
    if n == 2:
        nums.remove(n)
print(nums)   # [1, 2, 3]  -- 有一个 2 留了下来
```

第一次删除把所有元素都向左移动之后，迭代器越过了第二个 `2`。
解决办法是构建一个新列表（通常用推导式或 filter），或者用 `nums[:]` 遍历一个副本。
在迭代期间改变字典的大小更糟糕：它会抛出 `RuntimeError: dictionary changed size during iteration`。
