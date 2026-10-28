类型提示（Type hints）描述了函数期望接收以及返回的值。
在形参名称后添加冒号即可对其进行注解，并在返回值注解前加上 `->`：

```python
def keep_labels(labels: list[str]) -> list[str]:
    return labels
```

`list[str]` 表示元素为字符串的列表。
方括号用于描述元素类型；它们不会创建列表。
在此处，两个注解都描述了原样传入并返回的列表。
Python 不会在运行时根据这些提示来验证实参或返回值。
当需要验证时，诸如 `isinstance` 检查和显式异常抛出仍需编写独立代码。
对于字典，`dict[str, int]` 按顺序依次描述字符串键和整数值。
这些内置类型无需导入。

注解还可以提供文档信息。
已编写完成的 `describe_count_labels()` 辅助函数使用 `typing.get_type_hints` 来读取函数的注解并解析写为字符串的注解。
其内部调用的 `get_origin` 和 `get_args` 会将容器类型与其元素类型分离，因此等价的 `typing.List` 和 `typing.Dict` 注解会获得相同的描述。
使用预期的注解时，它会返回 `{'labels': 'list[str]', 'return': 'dict[str, int]'}`，其中 `labels` 排在 `return` 之前。
缺失或不同的注解将产生不同的描述。

已编写完成的 `count_labels_by_keyword()` 辅助函数调用了 `count_labels(labels=["blue", "amber", "blue"])`。
关键字实参指定了形参名称，因此保留名称 `labels` 可以让调用者使用此接口。

完成 `count_labels(labels: list[str]) -> dict[str, int]`，使其计数与文档一致。
保留 `labels` 形参以及相应的形参和返回值注解。
保持两个已完成的辅助函数不变。
输入是一个字符串列表；返回一个将每个标签映射到其出现次数的字典。
在一个单独的字典中构建计数，以避免修改调用者的列表。
按照标签首次出现的顺序插入：字典会保留插入顺序，而更新计数会使键保持在原位。
空列表返回 `{}`。
空字符串 `""` 是有效标签，必须进行计数。

### 解答

```python
def count_labels(labels: list[str]) -> dict[str, int]:
    counts = {}
    for label in labels:
        counts[label] = counts.get(label, 0) + 1
    return counts


def describe_count_labels():
    from typing import get_type_hints, get_origin, get_args

    def describe(annotation):
        if annotation is None:
            return "missing"
        origin = get_origin(annotation)
        arguments = get_args(annotation)
        if origin is list and len(arguments) == 1:
            return "list[" + describe(arguments[0]) + "]"
        if origin is dict and len(arguments) == 2:
            return "dict[" + describe(arguments[0]) + ", " + describe(arguments[1]) + "]"
        return getattr(annotation, "__name__", str(annotation))

    try:
        annotations = get_type_hints(count_labels)
    except (NameError, TypeError, SyntaxError):
        annotations = count_labels.__annotations__
    return {
        "labels": describe(annotations.get("labels")),
        "return": describe(annotations.get("return")),
    }


def count_labels_by_keyword():
    return count_labels(labels=["blue", "amber", "blue"])
```
