**最小特权原则**（Least privilege）意味着仅赋予每个组件其工作所需的访问权限，从而使该组件中的漏洞或失窃凭据造成的损害被限制在最小范围内。
程序通过其连接所使用的账号来获取对数据库的访问权限，因此该规则既适用于人员，也同样适用于服务和任务（job）。

在您即将绘制的在线商店中，客户在浏览器中下单，API gateway 将每个请求传递给 order service，随后 order service 将订单保存到 orders database 中。
每天晚上，一个 report job 会读取当天的订单，并将其作为 CSV 文件上传到 object storage 中。

order service **拥有数据所有权**：它是唯一写入订单的组件。
report job 仅执行读取操作，因此它获得的是**只读账号**，仅被授予对 orders 表的 SELECT 权限，无其他权限。
假设报表查询存在 SQL 注入漏洞，或者该任务的密码从其配置文件中泄露。
攻击者可以读取订单但无法修改订单：在数据库前端的信任边界处，数据库会检查打开连接的账号，并拒绝 report job 账号发送的所有 INSERT、UPDATE 和 DELETE 操作。
如果两个组件共享同一个账号，那么同样的漏洞或泄露的密码就可能导致所有订单被删除。
此类任务有时会被授予写权限以便在中途失败后进行清理，但此任务无需清理任何内容：它没有对数据库进行任何更改，因此只需重新运行即可。
它唯一的写入操作是 object storage 中的 CSV 文件。

网关仅负责路由请求，因此它不会获得数据库账号，浏览器也同样不会。

### 画板上的数据库访问

连接的 **Data flow** 设置记录了其访问权限；数据库访问的取值为 `read`、`write` 和 `read_write`。
连接始于打开它的组件，而 Data flow 则指明该组件通过该连接执行的操作，因此 report job 的只读账号就表现为从该任务到数据库的 **read 连接**。
选中一个连接以在检查器中设置其 Data flow；新建连接的初始值为 None。

按照描述绘制商店。
report job 对应 Worker / Background Job 模块。
它通过自己的连接读取数据库，既不连接到 order service，也不连接到 API gateway：因为 order service 可以写入订单，而网关会将请求转发给它，所以连接到其中任何一个都会为该任务提供绕过其只读账号的途径。
将 report job 的数据库连接设置为 `read`。
您还可以将 order service 的连接设置为 `write`，或者在其还需要向客户显示订单时设置为 `read_write`。
不要绘制任何从浏览器或网关指向数据库的连线。
然后将 order service、report job 和数据库放置在同一个 Private Network 区域内。
