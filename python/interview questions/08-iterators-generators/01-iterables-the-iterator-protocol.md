Python 中的每一个 `for` 循环都建立在两个小概念之上：可迭代对象（iterable）和迭代器（iterator）。
它们听起来像是同一个词，初学者也会把它们当作同义词使用，但它们是不同的对象，承担不同的职责。
可迭代对象是你可以从中获取迭代器的东西；迭代器则是一次性的游标，真正负责逐个产出值。
面试官会考察这一点，因为它解释了一整类令人意外的现象：为什么一个列表可以被反复循环，为什么 `zip` 或文件句柄在遍历一次后似乎就"变空"了，以及 `for` 循环在底层到底在做什么。
本节课涵盖 `iter()` 和 `next()`、`StopIteration` 信号、使用层面上的 `__iter__`/`__next__` 协议，以及为什么迭代器在遍历一次后就会被耗尽。

### 可迭代对象 vs 迭代器

可迭代对象是任何在你对它调用 `iter()` 时能交给你一个迭代器的对象。
列表、元组、字符串、字典、集合和 range 都是可迭代对象。
迭代器是知道如何获取下一个值、并记住自己停在哪里的对象。

```python
nums = [10, 20, 30]      # 一个列表：可迭代对象
it = iter(nums)          # 该列表上的一个迭代器
print(type(it))          # <class 'list_iterator'>
```

关键的区分在于：可迭代对象会按需产生新的迭代器，但它本身并不跟踪位置。
迭代器携带位置。
列表不是它自己的迭代器，这正是为什么你可以对同一个列表循环两次，并且两次都能得到所有的值。

### iter() 和 next()

`iter(obj)` 向一个可迭代对象请求一个新的迭代器。
`next(it)` 从迭代器中取出下一个值，并让它前进一步。

```python
it = iter(["a", "b"])
print(next(it))   # a
print(next(it))   # b
```

`next` 还接受一个可选的默认值，当迭代器为空时返回该默认值而不是抛出异常：

```python
it = iter([1])
print(next(it))        # 1
print(next(it, "done")) # done  （没有错误，使用了默认值）
```

### StopIteration 以及 for 循环如何使用它

当迭代器没有更多值时，对它调用 `next()` 会抛出 `StopIteration`。
这个异常并不是一个本该让你看到的错误；它是供应已经结束的信号。

```python
it = iter([1])
next(it)   # 1
next(it)   # 抛出 StopIteration
```

`for` 循环只是对此的一个整洁的封装。
从概念上讲，`for x in data:` 做的是以下事情：调用一次 `iter(data)`，然后反复对该迭代器调用 `next()`，把每个结果绑定到 `x`，并在 `StopIteration` 被抛出的那一刻安静地停止。
在普通循环中，你永远不需要自己捕获 `StopIteration`；`for` 语句会替你吸收它。

```python
# for 循环所做的事情，手动实现：
it = iter(data)
while True:
    try:
        x = next(it)
    except StopIteration:
        break
    # 循环体使用 x 运行
```

### 迭代器在遍历一次后就被耗尽

迭代器是一次性的。
一旦它产出了所有值并抛出了 `StopIteration`，它就会一直保持为空。
它不会重置。

```python
it = iter([1, 2, 3])
print(list(it))   # [1, 2, 3]
print(list(it))   # []   第二次遍历为空，迭代器已经用完
```

这就是 `zip`、`enumerate`、`map`、`filter` 和文件对象背后的陷阱：它们是迭代器（或会产生迭代器），所以消费一次后，第二次循环就什么都没有了。
如果你需要使用这些值两次，先把它们物化（materialize）成一个列表。

```python
pairs = zip([1, 2], ["a", "b"])
list(pairs)   # [(1, 'a'), (2, 'b')]
list(pairs)   # []   已经被耗尽
```

相比之下，列表是可迭代对象，而不是迭代器。
每次循环列表时都会重新调用 `iter()`，产生一个全新的游标，所以你可以想迭代多少次就迭代多少次。

### `__iter__` / `__next__` 协议

在底层，`iter(obj)` 调用 `obj.__iter__()`，`next(it)` 调用 `it.__next__()`。
如果一个对象定义了 `__iter__`，它就是可迭代对象。
如果一个对象定义了 `__next__`（并且按照惯例，还有一个返回自身的 `__iter__`），它就是迭代器。

```python
nums = [1, 2]
it = nums.__iter__()      # 等同于 iter(nums)
it.__next__()             # 等同于 next(it) -> 1
```

一个很能说明问题的测试：迭代器从 `iter()` 返回的是它自己，而普通的可迭代对象每次返回的都是一个不同的对象。

```python
lst = [1, 2, 3]
print(iter(lst) is lst)        # False  （列表不是它自己的迭代器）
it = iter(lst)
print(iter(it) is it)          # True   （迭代器就是它自己的迭代器）
```

你很少会手写 `__next__`；生成器（下一节课）才是构建迭代器的常规方式。
但了解这个协议可以解释为什么 `iter()` 和 `next()` 能作用于从字符串到文件句柄的一切对象。
