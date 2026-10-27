`namespace` 打开一个具名作用域，块内编写的每个声明都属于该名称，而不是属于该文件：

```cpp
namespace geo {

int perimeter(int side);

namespace units {

int toMillimeters(int meters);

}

}
```

`geo::perimeter` 和 `geo::units::toMillimeters` 是完整名称。
在标识符前面加上带有 `::` 的作用域会得到一个限定名称（qualified name），每一个 `::` 都会深入一层作用域，这也是访问嵌套块的方式。
完全不带前缀的名称会从它所在的位置向外查找：首先是最内层的外围作用域，然后是围绕它的各层作用域，最后是全局作用域。
在所有块的外部，这意味着全局作用域（即文件起始所在的作用域），因此 `::perimeter` 和 `geo::perimeter` 完全可以是拼写相同但彼此独立的两个函数，由调用处决定需要调用哪一个。
在 `namespace geo` 内部，同样的裸名称 `perimeter` 会找到 `geo::perimeter`，而绝不会找到全局的那一个。
块也可以被重新打开：在稍后或在另一个文件中再次编写 `namespace geo {` 会向同一个作用域添加内容，而不是开启一个与之冲突的新作用域。
要定义在块内声明的内容，请在同名块内编写其定义：

```cpp
namespace geo {

int perimeter(int side) {
    return side * 4;
}

}
```

`std` 的工作机制相同，这也是为什么这里每次使用时都要写上 `std::`。
`using namespace std;` 会在文件的剩余部分省略该前缀，而之后添加到该文件的每个名称都可能与来自 `std` 中此前未曾提及的名称发生冲突。
本运行环境会将项目的 `.cpp` 文件合并为一个单元，因此这里的指令也会延续到其后合并的每个文件中。
在整个练习中 `using` 关键字都会被拒绝，因此每个标准名称都请保留其前缀。

### 需求

- `text_tools.hpp` 是固定的，并且声明了三个函数：`text` 内部的 `wordCount`、`text::letters` 内部的 `count`，以及全局作用域下的第二个 `wordCount`。
  请保留 `main.cpp` 顶部的 include 指令。
- `text::wordCount` 统计由任意空白字符分隔的连续字符段数量，使用 `std::isspace(static_cast<unsigned char>(line[i]))` 检测每个字符。
  `"one two three"` 为 3，`" spaced out "` 为 2，`""` 为 0，`"a\tb c"` 为 3。
- 全局 `wordCount` 定义在所有块之外，以相同的方式统计连续字符段，但仅将空格字符 `' '` 作为分隔符，因此对于它而言 `"a\tb c"` 为 2，`" three words here "` 为 3。
- `text::letters::count` 统计满足 `std::isalpha(static_cast<unsigned char>(line[i]))` 的字符数量，因此 `"a1 b!"` 为 2，`"Mix 42 ok"` 为 5，大写字母和小写字母均包含在内。

### 解答

```cpp
#include "text_tools.hpp"

#include <cctype>
#include <string>

namespace text {

int wordCount(const std::string &line) {
    int words = 0;
    bool inWord = false;
    for (std::string::size_type i = 0; i < line.size(); i++) {
        if (std::isspace(static_cast<unsigned char>(line[i]))) {
            // 分隔符结束它前面的连续段；其他字符要么延续一段，要么开启新的一段
            inWord = false;
        } else if (!inWord) {
            inWord = true;
            words++;
        }
    }
    return words;
}

namespace letters {

int count(const std::string &line) {
    // 统计字母个数，大小写都算
    int letters = 0;
    for (std::string::size_type i = 0; i < line.size(); i++) {
        if (std::isalpha(static_cast<unsigned char>(line[i]))) {
            letters++;
        }
    }
    return letters;
}

}

}

int wordCount(const std::string &line) {
    // 只把空格字符当作分隔符来统计连续段
    int words = 0;
    bool inWord = false;
    for (std::string::size_type i = 0; i < line.size(); i++) {
        if (line[i] == ' ') {
            inWord = false;
        } else if (!inWord) {
            inWord = true;
            words++;
        }
    }
    return words;
}
```
