批次大小（batch size）设置了每组记录的最大数量。
将你已经了解的切片与带有步长的 range 结合起来，可以直接移动到下一组的起始索引：

```python
values = [10, 20, 30, 40, 50]
for start in range(0, len(values), 3):
    part = values[start:start + 3]
```

`range(start, stop, step)` 的第三个参数是步长（step）：连续索引之间增加的量。
在此示例中，`start` 取值 `0` 和 `3`，并在达到 `len(values)`（即 `5`）之前停止。
切片生成 `[10, 20, 30]` 和 `[40, 50]`。
切片的结束位置是不包含的（excluded），因此下一个切片恰好从前一个切片结束的位置开始。
超出列表长度的结束位置只会保留剩余的元素。
丢弃这个较短的分组会丢失记录；对其进行填充则会添加从未提供的记录。

### 构建批次

完成 `make_batches(records, batch_size)` 并返回一个由连续批次列表组成的列表。
练习使用带有步长的 `range`、切片以及 `.append()` 来收集它们。

- 要求 `records` 必须是一个列表。
  其元素可以是任何值；保留它们及其顺序，且不要修改输入的列表。
- 要求 `batch_size` 必须是 `1` 到 `100`（含两端）之间的整数。
  如果任一参数无效，则返回 `None`。
  明确排除布尔值：`isinstance(True, int)` 为 `True`。
- 在将批次大小用作步长之前进行验证。
  这些边界仅适用于本练习。
- 对于有效的空输入，返回 `[]`。
  保留最后的任何不完整批次，不需要填充，也不要产生多余的空批次。

### 解答

```python
def make_batches(records, batch_size):
    if not isinstance(batch_size, int) or isinstance(batch_size, bool):
        return None
    if batch_size < 1 or batch_size > 100:
        return None
    if not isinstance(records, list):
        return None
    batches = []
    for start in range(0, len(records), batch_size):
        batches.append(records[start:start + batch_size])
    return batches
```
