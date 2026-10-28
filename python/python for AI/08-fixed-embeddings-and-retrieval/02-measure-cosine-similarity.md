余弦相似度在消除向量大小的影响后比较它们的几何方向。
即使方向保持不变，将每个分量翻倍也会使与另一个向量的点积翻倍。
除以两个向量的模长可以消除这种尺度效应。

向量的**模长**（**magnitude**）是它到全零起点的距离。
将每个分量平方、相加，然后取平方根。
对于 `[3, 4]`，即 `math.sqrt(3 * 3 + 4 * 4)`，结果为 `5`。
余弦分数为：

```text
score = dot product / (left magnitude * right magnitude)
```

指向相同方向的非零向量分数为 `1`；相反方向分数为 `-1`。
垂直方向的分数为 `0`，因为它们的点积为零。
介于其间的方向会产生介于其间的分数。
这衡量的是数值对齐程度；它既不是概率，也不能保证两段文本含义相同。

这里的浮点运算需要特别小心。
对诸如 `1e-300` 这样的极小值求平方会产生零，因为结果小到无法表示。
即使对原始分量使用 `math.hypot` 也可能丢失方向信息：对于最小的正浮点数 `5e-324`，`[5e-324, 5e-324]` 的模长会舍入回 `5e-324`。

首先将每个非零向量除以其绝对值最大的分量。
这会在保持其方向的同时改变其大小。
对于经过验证的向量，构建一个单独缩放后的列表：

```python
import math

vector = [3, 4]
scale = 0.0
for value in vector:
    scale = max(scale, abs(value))

scaled = []
magnitude = 0.0
for value in vector:
    component = value / scale
    scaled.append(component)
    magnitude = math.hypot(magnitude, component)
```

`abs(value)` 消除符号；`max` 保留迄今为止找到的最大值。
这里 `scale` 为 `4`，`scaled` 变为 `[0.75, 1.0]`。
`math.hypot(a, b)` 可以在不直接对极小输入进行平方的情况下组合两个长度。
每次更新都将累积的长度与下一个缩放后的分量结合，在此得到模长 `1.25`。
对于 `[5e-324, 5e-324]`，缩放后产生 `[1.0, 1.0]`，因此模长不再以原始的微小尺度进行舍入。

在除法之前检查 `scale == 0`：全零向量没有方向。
此时应返回 `None`，这与垂直向量的有效分数 `0.0` 有所不同。

通过将每个缩放向量的各缩放分量除以其缩放后的模长来对其进行归一化。
得到的向量长度为 1。
计算这两个归一化向量的点积即可获得余弦相似度。
使用单独的列表可以避免覆盖调用者可能重复使用的坐标。
独立地对每个向量应用缩放，并保留每个非零向量的有效性，无论其分量有多微小。

`round(0.707106781, 6)` 返回 `0.707107`：第二个参数指定六位小数。
在累加分数之后四舍五入一次。

### 实现比较功能

编写 `cosine_similarity(left, right)`：

- 接收两个等长列表，每个列表包含 1 到 64 个分量。
- 每个分量必须是介于 `-1000` 到 `1000`（含两端）之间的有限 `int` 或 `float`。
  排除布尔值。
  这些边界限制属于本练习的要求。
  在检查类型后，`not -1000 <= value <= 1000` 可排除超出范围和非有限的值。
- 对于无效输入、空列表或长度不匹配的列表，或者任意一个全零向量，返回 `None`。
- 否则返回四舍五入保留六位小数的分数。
  如果四舍五入后的结果等于零，则返回 `0.0` 以避免带符号零的结果。

### 解答

```python
import math


def cosine_similarity(left, right):
    if not isinstance(left, list) or not isinstance(right, list):
        return None
    if len(left) != len(right) or not 1 <= len(left) <= 64:
        return None
    unit_vectors = []
    for vector in [left, right]:
        scale = 0.0
        for value in vector:
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                return None
            if not -1000 <= value <= 1000:
                return None
            scale = max(scale, abs(value))
        if scale == 0:
            return None
        scaled = []
        magnitude = 0.0
        for value in vector:
            component = value / scale
            scaled.append(component)
            magnitude = math.hypot(magnitude, component)
        unit = []
        for component in scaled:
            unit.append(component / magnitude)
        unit_vectors.append(unit)
    score = 0.0
    for left_value, right_value in zip(unit_vectors[0], unit_vectors[1]):
        score += left_value * right_value
    result = round(score, 6)
    if result == 0:
        return 0.0
    return result
```
