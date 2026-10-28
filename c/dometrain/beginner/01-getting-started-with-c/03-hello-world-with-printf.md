在自助终端启动之前，必须按以下顺序向标准输出发送两行内容：

```
Hello, World!
Toolchain ready.
```

起始代码中已经包含了声明 `printf` 的 `stdio.h`，因此所有操作都在 `say_hello` 内部进行。

函数调用先指明函数名称，后跟圆括号。
在 `printf("Ready");` 中，`printf(` 开始调用，括号内包含一个参数，分号 `;` 结束该语句。
该参数是一个字符串字面量（string literal）。
它的引号用于界定源代码文本的边界，不会被打印出来。

字面量中的换行转义符 `\n` 会将其后面的文本移到下一行。
包含 `First\nSecond` 的字面量会先输出 `First`，接着换行，然后输出 `Second`。

`say_hello` 的返回类型为 void。
这里的 `void` 表示该函数不会向调用者返回任何值。
它唯一可见的操作是控制台输出，因此不需要任何 return 表达式。

请编写单次 `printf` 调用，并在单个字符串字面量中同时包含这两行内容，中间用 `\n` 分隔。
请完全按照所示内容保留逗号、感叹号、大写字母、句号和行顺序，且前后不要打印任何多余内容。
有两种捷径已被禁用：`puts`（它无需通过本节课所讲的调用方式即可打印一行）以及显式指定 `stdout` 流（`printf` 绝不需要它）。
评分系统会逐字符比对捕获到的输出。

### 解答

```c
#include <stdio.h>

// 用一次 printf 调用打印两行诊断信息
void say_hello(void) {
    printf("Hello, World!\nToolchain ready.\n");
}
```
