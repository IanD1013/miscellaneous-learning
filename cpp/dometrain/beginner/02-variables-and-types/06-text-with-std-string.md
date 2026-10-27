当 `+` 的至少一侧是 `std::string` 时，它的作用是拼接两段文本。
返回的结果是一个新字符串，其中左侧的字符位于右侧字符之前。

```cpp
#include <string>

std::string first = "ada";
std::string last = "lovelace";
std::string full = first + " " + last;
```

`full` 保存了 `ada lovelace`，并且 `first` 和 `last` 都没有改变。
每个 `+` 都会构建一个新字符串，而不是扩展其操作数之一。
以这种方式拼接文本称为字符串拼接。

决定这些表达式能否编译的一条规则是：每个 `+` 的一侧都需要是 `std::string`，而另一侧必须是以下三者之一：另一个 `std::string`、字符串字面量或单个 `char`。
`first + " "` 符合要求，因为字符串在左侧，字面量在右侧，而它生成的结果随后位于第二个 `+` 的左侧。
如果写成 `"ada" + " "`，两侧都是纯字面量，表达式中根本没有出现字符串，因此编译器会拒绝编译。

### 初始代码中省略的 include

`<iostream>` 是初始代码引入的唯一头文件，而本练习添加了一条自己的规则来检查 `<string>`。
标记规则在编译器介入之前就会进行处理，因此缺少 include 会提示该规则未满足，而不是产生关于 `std::string` 的诊断信息。
显式引入所依赖的每个名称对应的头文件，是一种在底层标准库发生更换时仍能保持文件正常工作的良好习惯。

`joinWithSpace` 接收两段文本，并将它们拼接在一起返回，中间恰好包含一个空格。
无论文本是否为空，该空格每次都会被添加：空的第一个部分与 `beta` 拼接会返回 ` beta`，而两个空部分拼接会返回一个只包含一个空格的字符串。
普通 ASCII 之外的字节会原样传递，因此 `café` 和 `noir` 会返回 `café noir`。
返回的字符串会进行精确比对，两端都不会被修剪，因此多出或缺少空格都会导致用例失败。

- 使用 `+` 进行拼接，它必须出现在你的代码中。
  仅通过 `append` 得到相同的文本会在文件编译前被该规则拦截。
- 自行添加 `#include <string>` 行。
  初始代码仅自带了 `<iostream>`，另一个留给你来添加。

### 解答

```cpp
#include <iostream>
#include <string>

struct Solution {
    static std::string joinWithSpace(const std::string &first, const std::string &second) {
        // 用一个空格连接 first 和 second
        return first + " " + second;
    }
};
```
