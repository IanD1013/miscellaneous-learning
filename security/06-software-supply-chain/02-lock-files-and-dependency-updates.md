`package.json` 中的大多数条目指定的是**版本范围（version range）**，即允许一组版本的规则，因此最终进入构建的版本取决于构建运行的那一天。
**锁文件（lock file）**记录一次安装所选定的确切版本，从它安装的构建只会得到这些版本，不会有别的。
以一个依赖 Express 和一个日期库的 Node.js API 为例。
它的 `package.json` 这样声明 Express：

```json
"dependencies": {
  "express": "^4.18.0"
}
```

npm 包以 major.minor.patch 的形式给发布版本编号，按照语义化版本（semantic versioning）的约定，可能破坏现有代码的发布会提高主版本号。
`^4.18.0` 中的脱字符允许从 4.18.0 起、直到但不包括 5.0.0 的任何发布版本：4.18.2 和 4.21.2 符合，而 5.0.0 和 5.1.0 不符合。
波浪号范围 `~4.18.0` 更窄，只停留在 4.18.x 之内。

没有锁文件时，`npm install` 会在运行的那一刻询问注册表，并安装该范围所允许的最新版本。
今天的构建可能得到 4.21.2，而下个月的构建会得到此后出现的任何更新的 4.x 发布版本，中间没有任何提交。
构建服务器只能看到已提交的文件和注册表，因此开发者碰巧在自己机器上的版本不起任何作用。
该范围同样会接纳被劫持的维护者账户明天发布的版本，连同它的安装脚本一起。

### `package-lock.json` 记录了什么

`npm install` 会把它实际安装的依赖树写入 **`package-lock.json`**，也就是 npm 的锁文件。
下面是该 Node.js API 的两个条目，每个都裁剪为三个字段：

```json
"node_modules/express": {
  "version": "4.21.2",
  "resolved": "https://registry.npmjs.org/express/-/express-4.21.2.tgz",
  "integrity": "sha512-28HqgMZAmih1Czt9ny7qr6ek2qddF4FclbMzwhCREB6OFfH+rXAnuNCwo1/wFvrtbgsQDb4kSbX9de9lFbrXnA=="
},
"node_modules/body-parser": {
  "version": "1.20.3",
  "resolved": "https://registry.npmjs.org/body-parser/-/body-parser-1.20.3.tgz",
  "integrity": "sha512-7rAxByjUMqQ3/bHJy7D6OGXvx/MMc4IqBn/X0fcM1QUcAItpZrBEYhWGem+tzXH90c+G01ypMcYJBO9Y30203g=="
}
```

`version` 是安装的确切版本。
`resolved` 是 npm 下载该包文件（一个 `.tgz` 压缩包）的位置，`integrity` 是该文件的哈希值，这里使用 SHA-512 生成。
文件字节的任何变化都会改变哈希值，因此每当 npm 再次下载该文件时，它会对收到的内容计算哈希，与 `integrity` 比较，并在不匹配时报错停止，而不会安装不匹配的文件。

该 API 从未提到 body-parser，它是 Express 所依赖的。
锁文件中为依赖树里的每个包都保存着这样的条目，传递依赖也包括在内。
它不包含任何与安全有关的内容：没有字段说明某个版本是否存在已知漏洞，恶意版本得到的条目与干净版本完全一样。

### 从锁文件安装

**`npm ci`** 安装 `package-lock.json` 中列出的确切版本，并对照每个 `integrity` 值检查每次下载。
它需要锁文件，当锁文件不再满足 `package.json` 时它会报错停止，并且它从不写入这两个文件中的任何一个。

`npm install` 同样从锁文件开始，并保留每个仍然满足 `package.json` 的锁定版本。
有两种编辑会使锁文件不再满足 `package.json`：添加依赖，以及修改范围使锁定的版本落到范围之外。
无论哪种编辑之后，`npm install` 都会自行从注册表为该依赖解析一个版本，并写入锁文件。
因此，当开发者做了其中任一种编辑并推送，却没有对应的锁文件变更时，构建服务器上的 `npm ci` 会报错停止。
`npm install` 则会从范围中挑选一个版本，安装它，并在构建服务器上重写锁文件，于是构建会发布一个无人审查过的版本。
在构建服务器上，请使用 `npm ci`。

使用 `npm ci` 时，在锁文件写入之后发布的版本，无论在范围之内还是之外，都不会进入构建，直到有人有意更新锁文件。
来自被劫持的维护者账户的日期库新版本永远不会到达构建服务器，它的安装脚本也不会。
在锁定之后被人改动的包文件会无法通过 `integrity` 检查，npm 不会安装它。
不过锁文件不做任何判断。
如果某个版本在被锁定时已经包含恶意代码，或者某个仿冒包名的相似包连同它的锁条目一起被提交到了 `package.json` 中，`npm ci` 会像安装其他任何包一样安装它。

只要 `.csproj` 设置一个属性，C# 服务就能从 NuGet 获得同样的保证：

```xml
<PropertyGroup>
  <RestorePackagesWithLockFile>true</RestorePackagesWithLockFile>
</PropertyGroup>
```

随后 `dotnet restore` 会在项目旁边写入 **`packages.lock.json`**，列出每个包（传递依赖也包括在内）及其确切版本和内容哈希。
每当项目的 `PackageReference` 项发生变化时，普通的 `dotnet restore` 都会重写该文件。
`dotnet restore --locked-mode` 会恢复 `packages.lock.json` 所列出的确切内容，并在引用不再与之匹配时失败，这使它成为构建场景中与 `npm ci` 对应的 NuGet 命令。

### 已知漏洞和经过审查的更新

**已知漏洞（known vulnerability）**是指特定版本的包中存在、并已在安全公告（advisory）中公布的缺陷，公告会指明受影响的版本、严重程度，通常还有第一个修复版本。
许多公告带有 **CVE** 标识符，即 `CVE-` 后跟年份和编号，这样每个工具和厂商都可以指代同一个缺陷。

公告在版本发布之后才会出现，因此一个在锁定时没有已知问题的版本，可能在仓库没有任何变化的情况下变成已知存在漏洞的版本。
构建同样不会改变。
`npm ci` 仍然安装确切的锁定版本，从不阻止或替换它。
注册表从不更改已发布版本的内容（修复总是以新版本号的形式出现），而且 `integrity` 仍然匹配，因为它描述的是文件的字节，并不说明这些字节是否安全。
一个在应用能工作后就停止更新的团队，会从公告发布的那一天起，在每一次构建中都发布这个漏洞。

**`npm audit`** 可以发现这些漏洞。
它把已安装版本的列表发送给注册表，由注册表与已发布的公告数据比较，并报告每一项发现的严重程度（low、moderate、high 或 critical）、受影响的包，以及是否有可用的修复。
对于 C# 服务，`dotnet package list --vulnerable` 会列出项目中存在已知漏洞的直接 NuGet 引用，添加 `--include-transitive` 还会检查传递包。
在 .NET 9 SDK 及更早版本中，该命令是 `dotnet list package`。

`npm audit fix` 会应用已声明范围所允许的更新，包括其父包所声明范围内某个传递包的较新版本，并把它们写入锁文件。
`npm audit fix --force` 还会安装新的主版本，这可能破坏应用。

请把修复当作一次代码变更来对待。
在分支上运行 `npm audit fix` 或安装已修复的版本，运行测试，审查锁文件的变更，然后合并。
此后 `npm ci` 会在每次构建中安装已修复的版本。
把构建改为使用 `npm install`，或者在构建脚本中运行修复，会把无人审查过的版本放进构建。
删除 `package-lock.json` 同样什么也不会更新：`npm ci` 没有可供安装的依据，会失败。
保留旧版本就是保留漏洞。
