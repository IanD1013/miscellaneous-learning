`.deb` 是一个文件归档，其中包含按安装路径排列的文件，以及一个描述软件包的 control 文件。
`dpkg-deb` 可以将一个目录打包为 `.deb` 文件。
单个脚本的构建目录树包含两个条目：

```text
ops-tool_1.0/DEBIAN/control
ops-tool_1.0/usr/bin/ops-tool
```

`DEBIAN/` 之外的所有内容都会安装到 `/` 下的相应路径中，因此 `usr/bin/ops-tool` 会安装为 `/usr/bin/ops-tool`。

`DEBIAN/control` 包含 dpkg 和 apt 读取的字段：

```text
Package: ops-tool
Version: 1.0
Architecture: all
Maintainer: Ops Team <ops@example.com>
Depends: procps
Description: ops helper that reports the running process count
```

`Architecture: all` 声明该软件包不包含编译代码（Shell 脚本正是如此），因此一次构建即可安装在任何架构上。
`Depends` 指定了使该软件包正常运行所必须存在的依赖包；`/home/learner/ops/src/ops-tool` 会运行 `ps`，而 `ps` 来自 procps。

归档还会记录构建树中每个文件的权限模式（mode）和所有者（owner），并在 dpkg 安装时还原这两者。
如果在目录树中将脚本保持为 0644 权限，安装后也会是 0644，从而导致无法运行。
如果以 `learner` 用户身份构建目录树，则每个条目都会存储为 `learner/learner`，这样安装后的 `/usr/bin/ops-tool` 将属于 uid 1000，进而可能导致每个用户运行的程序都能被该 uid 改写。
无论构建者是谁，`--root-owner-group` 都会将每个条目存储为 `root/root`，因此构建本身不需要 `sudo`：

```bash
dpkg-deb --build --root-owner-group ops-tool_1.0
dpkg-deb -c ops-tool_1.0.deb
```

第一条命令会在构建树旁边生成 `ops-tool_1.0.deb`。

`-c` 会列出归档中的文件及其权限模式和所有者，而 `-I` 会输出其 control 字段。

### 为 apt 发布软件包

`sudo dpkg -i ops-tool_1.0.deb` 会解压该文件，但 dpkg 只会检查 `Depends`：
如果缺少依赖，它会让软件包处于未配置状态，且不会下载任何内容。
apt 则会解析依赖关系并安装缺失的包，但它绝不会直接扫描文件夹查找 `.deb` 文件。
它读取的是一个 Packages 索引，其中每个软件包对应一个段落（stanza），包含其 control 字段、文件名以及校验和。
包含 `.deb` 文件和该索引的目录被称为扁平仓库（flat repository），在目录内运行 `apt-ftparchive packages . > Packages` 即可写入该索引。
`/srv/ops/repo` 尚不存在。
你需要使用 `sudo mkdir -p /srv/ops/repo` 创建它，因此它属于 root。
`>` 重定向是由你自己的无特权 shell 打开的，无法在其中直接创建 `Packages`，因此请改用管道将其传递给 `sudo tee Packages >/dev/null`。


apt 通过 `/etc/apt/sources.list.d/` 中的一行配置找到该仓库：

```text
deb [trusted=yes] file:/srv/ops/repo ./
```

末尾的 `./` 表示选择扁平布局：
apt 会直接从该目录读取 `Packages`。

普通仓库还会发布一个签名的 Release 文件。
当前仓库没有该文件，`trusted=yes` 告诉 apt 接受未签名的仓库。
随后运行 `sudo apt-get update` 会加载该索引，`apt-cache policy ops-tool` 则会显示候选版本及其来源仓库。

### 需求

脚本位于 `/home/learner/ops/src/ops-tool`，权限模式为 0644；`/home/learner/ops/build` 是构建树的合适位置。
在 `/srv` 和 `/etc/apt` 下的所有操作以及执行 `apt-get update` 和 `apt-get install` 时都需要 `sudo`。


- 一个名为 `ops-tool` 的软件包，版本为 `1.0`，`Architecture: all`，`Depends: procps`，安装 `/usr/bin/ops-tool`，权限模式为 0755，所有者为 root:root。
- 该 `.deb` 及其 `Packages` 索引位于 `/srv/ops/repo`。
  对该 `.deb` 运行 `dpkg-deb -c` 应将 `./usr/bin/ops-tool` 列为 `-rwxr-xr-x root/root`，且 `Packages` 必须准确描述该文件，因此每次重新构建后都要重新生成它。
- `/etc/apt/sources.list.d/ops.list` 包含上述软件源配置行。
- 在 `apt-cache policy ops-tool` 将其显示为候选版本后，通过 `sudo apt-get install ops-tool` 按名称从该仓库安装 ops-tool。
  安装的副本必须来自仓库中当前的 `.deb` 文件：
  重新构建后，运行 `sudo apt-get update`，然后运行 `sudo apt-get install --reinstall ops-tool`。

### 解答

```bash
# 确保新建的目录为 0755（dpkg-deb 拒绝组可写的 DEBIAN 目录）
umask 022

# 搭建构建树
mkdir -p /home/learner/ops/build/ops-tool_1.0/DEBIAN /home/learner/ops/build/ops-tool_1.0/usr/bin
cp /home/learner/ops/src/ops-tool /home/learner/ops/build/ops-tool_1.0/usr/bin/ops-tool
# 归档会记录权限模式，脚本必须是 0755
chmod 0755 /home/learner/ops/build/ops-tool_1.0/usr/bin/ops-tool

# 写入 control 文件
cat > /home/learner/ops/build/ops-tool_1.0/DEBIAN/control <<'EOF'
Package: ops-tool
Version: 1.0
Architecture: all
Maintainer: Ops Team <ops@example.com>
Depends: procps
Description: ops helper that reports the running process count
EOF

# 以 root/root 构建并检查归档内容
cd /home/learner/ops/build
dpkg-deb --build --root-owner-group ops-tool_1.0
dpkg-deb -c ops-tool_1.0.deb
dpkg-deb -I ops-tool_1.0.deb

# 建立扁平仓库并生成 Packages 索引
sudo mkdir -p /srv/ops/repo
sudo cp /home/learner/ops/build/ops-tool_1.0.deb /srv/ops/repo/
cd /srv/ops/repo
apt-ftparchive packages . | sudo tee Packages >/dev/null

# 添加软件源
echo 'deb [trusted=yes] file:/srv/ops/repo ./' | sudo tee /etc/apt/sources.list.d/ops.list >/dev/null

# 加载索引，确认 ops-tool 的候选版本为 1.0 且来自 file:/srv/ops/repo
sudo apt-get update
apt-cache policy ops-tool

# 按名称安装
sudo apt-get install -y ops-tool
ls -l /usr/bin/ops-tool
```
