跨站脚本攻击始于值以标记的形式到达页面。
**输出编码**（output encoding）可以阻止这一点：在值被写入页面的那一刻，可能改变页面结构的字符会被替换成浏览器只会显示的形式。
HTML 编码把 `<` 变成 `&lt;`，把 `>` 变成 `&gt;`，把 `&` 变成 `&amp;`，并为两种引号字符给出同类的编码。
这些编码是 HTML 实体（HTML entities）：浏览器把 `&lt;` 显示为字符 `<`，而不会把它当作标签的开头。
内容安全策略（Content Security Policy）通过告诉浏览器哪些脚本可以运行，为编码被遗漏的地方增加了第二层防护。

### 针对各种上下文的编码

一个评论组件把同一段评论文本在页面中写了三次：

```html
<p>USER_TEXT</p>
<span title="USER_TEXT">...</span>
<script>var greeting = "USER_TEXT";</script>
```

每个位置都是不同的**上下文**（context）：上下文决定了哪些字符可以从中逃逸，因此也决定了值需要哪种编码：

- **元素文本**（element text），如段落中的情形。这里 `<` 会开启一个标签，所以内容为 `<img src=x onerror=alert(1)>` 的评论会变成一个真正的图片元素，其 `onerror` 属性中带有脚本。HTML 编码把它变成读者看到的文本。
- **带引号的属性**（quoted attribute），如 `title`。这里的逃逸途径是结束引号：内容为 `x" onmouseover="alert(1)` 的评论会提前结束 `title`，并在其后添加一个事件处理程序属性。属性编码会同时编码两种引号字符，以及 `&` 和 `<`，这样整条评论就留在属性之内。标准的 HTML 编码器，包括 Razor 的 `@`，都会编码两种引号，所以同一个编码器既覆盖元素文本，也覆盖带引号的属性。`USER_TEXT` 周围的引号本身不起任何作用，因为评论里可以包含同样的引号。
- **JavaScript 字符串**，位于 `<script>` 块内。这里适用 JavaScript 的规则，而 HTML 编码并不是为此设计的。浏览器不会解码 script 块内的实体，所以经过 HTML 编码的评论到达 `greeting` 时是字面的 `&lt;` 文本。标准的 HTML 编码器也不处理反斜杠，而在 JavaScript 字符串中，反斜杠会改变下一个字符的读法。内容为 `hi\` 的评论会产生 `var greeting = "hi\";`，其中的 `\"` 是字符串内的一个引号，而不是字符串的结尾。单独来看，这通常只会破坏脚本，但如果稍后在同一行写入第二个值，它的一部分就可能落在任何字符串之外并作为代码运行。这种上下文需要 JavaScript 字符串编码，它会把有风险的字符（包括反斜杠）写成反斜杠转义，例如 `"` 写成 `"`。在 C# 中就是 `JavaScriptEncoder.Default.Encode(text)`。Razor 的 `@` 在 script 块内仍然做 HTML 编码，这在那里是错误的编码。
- **URL**。放入查询字符串的值需要 URL 编码（JavaScript 中是 `encodeURIComponent`，C# 中是 `Uri.EscapeDataString`），它会把 `&`、`=` 和空格等字符变成 `%` 编码。来自用户的完整链接还需要检查其协议（scheme）：`javascript:` 链接在被点击时会运行脚本，而 HTML 编码不会改变 `javascript:alert(1)`。

由于编码取决于值最终落在哪里，所以它应该在输出时进行，采用适合该位置的形式。
在保存评论时做的一次编码，无法同时适合段落、属性和 script 块。
按输入的原样存储评论，并在每次写出时进行编码。
保存时编码还会弄乱本来适用的位置：Razor 会对已存储的 `&lt;` 再编码一次，于是读者在页面上看到的是 `&lt;`。
为绕开这个问题而解码已存储的值，并不加编码地写出它（例如用 `Html.Raw`），又会把原始标记放回页面。

大多数元素文本不需要手动挑选编码器。
Razor 的 `@`，如 `<p>@comment.Text</p>`，会对它写出的任何内容做 HTML 编码。
在浏览器 JavaScript 中，设置元素的 `textContent` 会把值作为文本插入：

```javascript
paragraph.textContent = comment; // <b> appears as the characters <b>
paragraph.innerHTML = comment;   // <b> becomes a bold element
```

跨站脚本攻击一课中的汇点 `innerHTML` 和 `Html.Raw` 会把值交给 HTML 解析器，由解析器根据它构建元素，所以 `<img onerror>` 评论在段落内与在任何其他地方一样容易运行。
浏览器在解析 HTML 字符串时不会转义任何东西；任何以标记形式到达解析器的内容都会变成标记。

有些评论必须保持为 HTML：该组件允许 `<b>` 和链接，而编码会把这些标签显示为字面字符。
这类内容要经过**净化器**（sanitizer），这是一个库，它解析 HTML，维护一份安全标签和属性的允许列表，并丢弃其余一切，包括 `<script>`、`onerror` 等事件处理程序属性，以及地址以 `javascript:` 开头的链接。
只插入净化后的结果。
DOMPurify 是浏览器中广泛使用的净化器：`DOMPurify.sanitize(html)` 返回清理后的 HTML。
自己移除 `<script>` 标签属于黑名单做法，它会留下 `<img onerror>` 以及其他所有运行脚本的方式。
谁发布了评论并不会改变这一切，因为已登录的用户和任何人一样容易发布载荷。

### 解读基于 nonce 的策略

内容安全策略以 `Content-Security-Policy` 响应头的形式发送，浏览器会对该页面强制执行它。
它的 `script-src` 指令决定哪些脚本可以运行。
评论组件所在的页面带着这样的策略到达：

```http
Content-Security-Policy: script-src 'nonce-r4nd0m'
```

**nonce** 是服务器为一次响应编造的随机值。
服务器把它放进响应头中，写成 `'nonce-` 后跟该值，并把同样的值写入它输出的每个 script 标签的 `nonce` 属性。
只有当内联脚本的 `nonce` 属性匹配时，浏览器才会运行它。
`r4nd0m` 代表一个真正的 nonce，真正的 nonce 在每次响应中都是新生成且不可猜测的。
攻击者在响应存在之前就写好了载荷，所以载荷无法携带该响应的 nonce。
页面包含的内容如下：

```html
<script nonce="r4nd0m">initComments();</script>
<script>alert(1)</script>
<img src="x" onerror="alert(1)">
```

应用的脚本带有匹配的 nonce，因此会运行。
注入的 `<script>` 没有 nonce，所以浏览器会阻止它。
`onerror` 属性同样是内联脚本，而事件处理程序属性无法携带 nonce，所以浏览器也会阻止它。
应用自己的处理程序属性也一样，这就是为什么处于该策略下的应用要用 `addEventListener` 从带 nonce 的脚本中附加它的处理程序。

给每个脚本都加上 nonce 需要花功夫，而团队常走的捷径是 `script-src 'unsafe-inline'`。
`'unsafe-inline'` 允许所有内联脚本，`<script>` 块和事件处理程序属性都包括在内，而浏览器无法把应用的内联脚本与注入的脚本区分开：二者都是同一个响应中的标记。
正是 nonce 把它们区分开来，因为只有服务器知道它。
在 `'unsafe-inline'` 之下，上面注入的 `<script>` 和 `onerror` 处理程序都会运行。
通过 `<script src>` 加载的脚本文件仍然会被阻止，因为该策略没有列出可供加载它们的主机，但能注入标记的攻击者只需要内联脚本，所以该策略不再能阻挡注入的内联脚本。

即使是严格的 nonce 策略也不能取代输出编码。
它在注入之后才起作用，并且只针对脚本。
不运行脚本的注入标记仍然有效：例如一个把密码发送给攻击者的虚假“会话已过期，请重新登录”表单，或是改变页面向读者传达内容的链接和文本。
编码则从根本上阻止评论变成标记。
`innerHTML` 不做任何编码，所以无论有没有该策略，把用户输入传给它都是不安全的。
