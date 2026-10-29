`/srv/webapp/app` 中 `config.js` 的第一行是一个**硬编码机密（hardcoded secret）**：应用用来签名其 session cookie 的值，作为字符串直接写入了源码中。
应用对每个 cookie 中的 session ID 进行签名，这非常类似于服务器对 JSON Web Token 进行签名的方式，并且仅当签名是使用该值生成时才接受 cookie。
任何拥有该值的人都可以构造出应用接受的 cookie。
在源码中，它会随代码流向任何地方：每次 clone、commit、build 和 backup，甚至包括此处文件旁边的编辑器备份 `config.js~`。
能够读取代码的人远多于能够登录服务器的人。

相反，应用应该从**环境变量（environment variable）**中读取该值，环境变量是进程在启动时接收的具名值。
Node.js 将它们存放在 `process.env` 上，因此 `process.env.SESSION_SECRET` 即为 `SESSION_SECRET` 的值；如果未进行任何设置，则为 `undefined`。
该服务在启动时会加载 `/etc/webapp/app.env`，该文件中的每一行 `NAME=value` 都会成为其环境变量之一。
该文件目前尚不存在。
就像 reports 服务的机密一样，它的所有者应为 root，所属组为 webapp，权限模式为 640，位于 `/etc/webapp` 目录中（该目录权限已经是 root:webapp 750）。
如果在 app 目录下创建 `.env` 文件，在默认 umask 下它会被创建为所有账户均可读，并且会随代码一起被复制。

从 `config.js` 中删除这行代码并不能使旧值重新恢复机密。
它仍然存在于所有那些副本中，因此必须将其视为已**泄露（exposed）**，即已被从未授予过它的人所知晓。
泄露的机密需要被**轮换（rotated）**：生成一个新的随机值，将其放到应用读取它的位置，并淘汰旧值。
对于 session 机密，轮换会在服务下次重启时生效。
使用旧值签名的 cookie 将无法通过签名校验，因此每个已登录的用户都必须重新登录，使用复制或伪造 cookie 的任何人也是如此。
该应用并未运行在此机器上，因此这里无需重启任何服务。

### 移动并轮换 session 机密

在 `config.js` 中，将顶部的硬编码行完全替换为这一行：

```js
const SESSION_SECRET = process.env.SESSION_SECRET;
```

保持整个 `module.exports` 代码块完全不变，包括 `port` 和 `sessionCookieName`。
不要给该变量提供任何形式的回退默认值（fallback），既不要在该行加上 `|| "dev-secret"`，也不要在文件的任何位置为 `process.env.SESSION_SECRET` 分配默认值，因为一旦缺少该变量，应用就会悄无声息地依赖代码中的机密运行。
该行使用了 `const`，因此后面的行无法将 `SESSION_SECRET` 重新赋值为默认值。
在新行之后另起一行添加检查并在未设置时停止应用是值得推荐的做法，例如 `if (!SESSION_SECRET) throw new Error("SESSION_SECRET is not set");`。

使用 nano、vim 或 `sed -i` 进行编辑，且不要保留该文件的副本。
在服务使用新值重启之前，旧值仍然是它用来签名 cookie 的机密，并且代码旁边的任何文件都会随下一次 commit、build 或 backup 一起流出。
使用 `sed -i.bak` 或在编辑前 `cp` 备份 `config.js`，都会在代码旁边的文件中留下旧值。
编辑完成后，使用 `rm`（而不是 `mv`）删除 `config.js~`，以确保在 app 目录或机器上的任何其他地方都不会留下包含旧值的文件。

对于 reports 服务的 SMTP 密码，你曾将密码读取到 shell 变量中，并通过管道将 `printf` 行传给 `install`，类似于这样：

```bash
printf 'SMTP_PASSWORD=%s\n' "$smtp_password" | sudo install -m 640 -o root -g reports /dev/stdin /etc/reports/smtp.env
```

这一次不需要手动输入该值。
`openssl rand -hex 32` 会输出 32 个随机字节，表示为 64 个小写十六进制字符（每个字节对应两个字符）。
要将某个命令的输出嵌入到另一个命令行中，请在命令前加上 `$(`，在命令后加上 `)`。
这就是命令替换（command substitution）：shell 会先执行该命令，并将打印出的内容放在该位置（去除了末尾的换行符）。
在双引号内，结果仍会保持为一个参数，就像 `"$smtp_password"` 那样。
以下是各自独立运行的示例，这里使用 4 字节以使输出较短：

```text
$ openssl rand -hex 4
9c41e07b
$ printf 'TOKEN=%s\n' "$(openssl rand -hex 4)"
TOKEN=3fa8d2c6
```

以相同的方式将新值直接写入 `/etc/webapp/app.env`，即通过管道将 `printf` 行传给 `sudo install`，这样该值直接从 `openssl` 写入文件，绝不会显示在屏幕上、shell 历史记录中或另一个文件中。
不要先将其写入 app 目录或 `/tmp` 下的文件中。
看似容易记住的短语实际上比想象中脆弱得多，因为持有该应用任一 cookie 的人都可以利用自己的硬件在不受尝试次数限制的情况下对签名进行暴力破解或猜测。
而面对 32 个随机字节，这种方法完全行不通。

完成后的 `app.env` 只有一行，即 `SESSION_SECRET=` 后跟 64 个字符，不包含引号、空格或 `export`。
保持 `/etc/webapp` 原样。
先计算出这一行应该有多大（算上末尾的换行符），然后在不打印机密的情况下检查文件：`sudo stat -c '%U:%G %a %s' /etc/webapp/app.env` 会打印其所有者、所属组、权限模式和以字节为单位的大小。
