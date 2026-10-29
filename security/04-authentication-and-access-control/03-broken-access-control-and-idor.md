登录告诉 API 谁在调用。
它没有说明该调用者可以读取或修改哪些记录，所以一个从请求中获取记录 ID 的端点必须对每个请求单独检查这一点。
这里的示例使用一个发票 API。
它的控制器带有 `[Authorize]`，这是一个 ASP.NET Core 特性，应用于控制器中的每个路由，在这个应用中它只要求有已登录的用户。
客户 A 拥有发票 1001，客户 B 拥有发票 1002，两行都在同一张 `invoices` 表中，该表保存所有客户的发票。
这是读取端点：

```csharp
[HttpGet("/invoices/{id}")]
public async Task<IActionResult> Get(int id)
{
    var invoice = await db.QuerySingleOrDefaultAsync<Invoice>(
        "SELECT * FROM invoices WHERE id = @id", new { id });
    return invoice is null ? NotFound() : Ok(invoice);
}
```

路由中的 `{id}` 填充 `id` 参数，`new { id }` 把它绑定到 `@id` 占位符。
这使它成为参数化查询，能防止 SQL 注入，但它仍然允许任何客户读取任何发票。
已登录的 A 打开 `/invoices/1001`，把地址栏中的数字改成 1002，就得到了 B 的发票。
查询返回任何具有该 ID 的行，其中没有任何地方提到调用者。
`[Authorize]` 放行了请求，因为 A 已登录；它从不查看记录。

这就是**不安全的直接对象引用**（insecure direct object reference，**IDOR**）：端点从请求中获取记录 ID，并在没有检查该记录是否属于调用者的情况下返回或修改它。
IDOR 是 OWASP Top 10 中 A01:2025 失效的访问控制（Broken Access Control）的一种常见形式。

A 的页面只链接到 A 的发票，这并不构成任何限制。
A 可以在地址栏中输入任何 ID，或从任何 HTTP 客户端发送请求，服务器只看到请求，从不知道它的 ID 从何而来：应用中的链接、截图和猜测看起来都一样。
数据库执行给它的 WHERE 子句，对谁发送了 HTTP 请求一无所知，所以除非代码添加该条件，否则没有任何东西把查询限制在调用者的行上。

角色检查留下的是同样的缺口。
`PUT /invoices/{id}` 带有 `[Authorize(Roles = "Customer")]`，并运行 `UPDATE invoices SET billing_address = @billingAddress WHERE id = @id`。
角色说明的是调用者是哪一类用户，而不是哪些记录属于他们。
A 和 B 都具有 Customer 角色，所以两者都能通过，而 UPDATE 会修改 URL 中 ID 对应的任何发票：A 发送 `PUT /invoices/1002` 就改写了 B 的账单地址。
这同样是一个 IDOR，只不过发生在写操作上。
服务器不会把 1002 替换成 A 自己的某个发票 ID，所以 A 的发票 1001 保留原来的地址。

### 在服务器上检查所有者

**对象级授权**（object-level authorization）在服务器上对每个请求检查已登录用户是否可以对这条记录执行该操作。
对于发票，这意味着把它的所有者与调用者比较。
一种方法是同时用记录 ID 和所有者 ID 进行查询：

```csharp
await db.ExecuteAsync(
    "UPDATE invoices SET billing_address = @billingAddress " +
    "WHERE id = @id AND owner_id = @userId",
    new { id, billingAddress, userId });
```

另一个客户的行不再匹配，所以 A 对 1002 的请求不会修改任何东西，读取查询中的同样条件也会让 B 的发票什么都查不到。
另一种方法是先按 ID 加载发票，除非它的 `owner_id`（C# `Invoice` 上的 `OwnerId`）等于已登录用户的 ID，否则拒绝请求。
无论哪种方式，A 仍然可以读取和更新发票 1001，这正是这些路由的用途。

这个检查的可靠程度取决于 `userId`。
它必须是已登录用户的 ID，取自服务器已经验证过的会话或令牌。
会话 cookie 或令牌同样随请求而来，但服务器会先检查它：在会话存储中查找会话 ID，或检查令牌的签名和 `exp`，然后才知道是谁在调用。
作为普通值发送的用户 ID 得不到这样的检查。
查询字符串参数、表单字段、应用自己的 JavaScript 添加的请求头、以及 JavaScript 写入的 cookie，都是由调用者选择的，调用者可以在那里填上 B 的 ID。
从发票中读取所有者，再与同一张发票的 `owner_id` 比较，什么也没检查，因为一行总是与自身匹配。

`[Authorize]` 保留它自己的职责：没有已登录用户的请求会在路由运行之前被拒绝。
无论加在控制器上、操作上还是两者都有，它检查的就只有这些。

对用户隐藏东西并不能代替所有者检查。
把发票 ID 从连续数字换成随机 GUID，只会让它们难以猜测，仅此而已。
ID 会通过共享链接、截图、浏览器历史、服务器日志和其他 API 响应泄露。
GUID 并不与账户绑定，也没有加密，而查询仍然是 `WHERE id = @id`，所以只按 ID 加载的服务器会把发票返回给任何发送该 GUID 的已登录账户。
随机 ID 可以叠加在所有者检查之上，但不能取代它。

页面也不是一种控制手段。
只在 A 自己的发票上显示编辑地址按钮，改变的是 A 看到的内容，而不是服务器接受的内容：A 仍然可以为 1002 发送 PUT。
整个路由也是同样的道理。
发票 API 还有 `GET /admin/invoices/export`，它返回所有客户的发票。
菜单只向管理员显示它的链接，而该路由除了控制器的 `[Authorize]` 之外什么也不检查，所以任何在应用的 JavaScript 中找到该路径的客户都可以直接请求它并得到导出数据。
面向部分用户的路由需要在服务器上有它自己的检查。

### 默认拒绝

逐个列出操作的检查，还必须决定没人列出的操作会怎样。
**默认拒绝**（deny by default）意味着代码拒绝一切它没有明确允许的东西。
这个检查指明谁可以做什么，并拒绝其他一切：

```csharp
bool CanAccess(int userId, Invoice invoice, string action)
{
    bool ownerAction = action == "view" || action == "update";
    if (ownerAction && invoice.OwnerId == userId) return true;
    return false;
}
```

之后添加一个 PDF 下载功能，使用操作名 `download`，对它来说 `ownerAction` 为 false，所以方法会到达 `return false`：在有人把 `download` 加入列表之前，连所有者也会被拒绝。
这个 bug 在第一次有人尝试时就会暴露出来。
反过来写这个检查，为每个要拒绝的操作写一个 `if`，并在末尾 `return true`，新操作就会对所有人开放，无论是不是所有者。
没有人会注意到，因为每个请求都成功了。
把 `action` 与一个不相等的字符串比较，结果就是 false，所以在两种写法中，未列出的操作都会落到最后一行，由最后一行来决定。

路由遵循同样的规则：新路由应该拒绝每一个请求，直到有人声明谁可以调用它。
导出路由展示了另一种结果，即一个路由在有人想起来保护它之前一直保持开放。
