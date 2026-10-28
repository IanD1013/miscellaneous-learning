座位账本从场地容量开始，扣除已售出的座位，然后恢复释放的保留座位块。
维护一个运行中的单一值可以使事件顺序清晰可见。

复合赋值会读取变量的当前值，使用右操作数应用其运算符，并将结果存回同一个变量中。
例如，`available -= sold` 会从 `available` 的当前值中减去右操作数 `sold`，然后将结果存储在 `available` 中。
同样，`available += released` 会加上释放的数量并保存新值。
目标在每个语句中仅写入一次。

声明的数值范围使 `capacity`、`sold` 和 `released` 均在 0 到 1000000（含）之间。
减法操作后，`available` 介于 -1000000 和 1000000 之间。
加上释放数量最多可产生 2000000。
每个可表示的中间值和最终值均在有符号 `int` 范围内。

通过用 `capacity` 初始化一个局部总数，使用 `-=` 扣除 `sold`，然后使用 `+=` 恢复 `released` 来实现 `seats_open`。
强制性的 token 检查需要同时使用这两种形式。
负数结果仍然有效，记录了超售的情况。
不要对其进行截断（clamp），也不要用预先计算的单个公式替换这种有序的更新。
返回该整数，不要输出到控制台。

### 解答

```c
// 从容量开始，按顺序应用当天的变化
int seats_open(int capacity, int sold, int released) {
    int available = capacity;
    available -= sold;
    available += released;
    return available;
}
```
