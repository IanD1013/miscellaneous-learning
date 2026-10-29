当 dpkg 解包软件包时，会记录其安装的每个文件的 MD5 校验和；对于普通文件，该列表位于 `/var/lib/dpkg/info/<package>.md5sums`。

`dpkg --verify` 会重新计算它们，并为每个内容不再匹配的文件输出一行。
该机器的每个全新副本都已显示两条此类输出，这是由镜像自身的品牌定制留下的：

```text
$ sudo dpkg --verify base-files
??5?????? c /etc/issue
??5??????   /usr/lib/os-release
```

这 9 个字符的字段遵循 rpm 的验证格式。
第三位的 `5` 表示校验和不匹配；每个 `?` 表示 dpkg 未执行的检查，其中包括权限模式（mode）和所有者（owner），因此在打包文件上执行 `chmod` 绝不会显示出来。
路径前面的 `c` 标记了一个 conffile（软件包留给管理员管理的配置文件）。
修改后的 conffile 通常是有意的；而变动的程序或手册页则通常不是。

保留 `sudo`：
作为 `learner` 用户，dpkg 对于无法读取的文件会输出 `?????????`。

`sudo dpkg --verify sl nginx-light nginx-common` 仅检查这三个软件包并立即返回。
如果不指定软件包名称，它会检查已安装的所有内容（此处大约需要 51 秒）并报告任何软件包中变动的文件。
`dpkg -S` 可以指出路径的所有者：
`dpkg -S /usr/games/sl` 会输出 `sl: /usr/games/sl`。


### 在不丢失配置的情况下重新安装

`sudo apt-get install --reinstall sl` 会从软件源重新解包已安装版本的 `sl`，覆盖每个普通文件及其权限模式。
Conffile 的处理方式有所不同。
它们的校验和不在 `.md5sums` 列表中：
dpkg 在其状态数据库中保留了每个 conffile 出厂自带的校验和，而 `dpkg-query -W -f='${Conffiles}\n' nginx-common` 会输出这些条目，每行一个路径和校验和（`-W` 选择软件包，`-f` 指定要输出的字段）。
在重新安装期间，dpkg 会将磁盘上的每个 conffile 与其自带的校验和进行比较。
存在差异意味着管理员编辑了该文件，并且由于正在解包的软件包包含相同的 conffile，dpkg 会保留这些编辑。
重新安装相同版本会替换普通文件，同时保留每个被编辑过的 conffile。

### 恢复被修改的文件

在终端提示符出现之前，系统已安装了 `sl` 和 `nginx-light`（`nginx-light` 引入了 `nginx`、`nginx-common` 和 `libnginx-mod-http-echo`，而 `sl` 引入了 `libncurses6`），并且它们的一些文件随后被修改了。
其中有一处修改是经过批准的：
`/etc/nginx/nginx.conf` 末尾的 `# ops: worker tuning` 行必须保留。

1. 将这些软件包中所有被修改但不是 conffile 的文件的完整路径写入 `/home/learner/ops/tampered`，每行一个，按顺序排序，不要包含其他内容。
   任何其他软件包（包括 `base-files`）的文件均不在本任务范围内。
   请先记录该列表：
   重新安装会修复这些文件，它们随后将不再出现在输出中。
2. 通过使用 `sudo` 重新安装拥有这些文件的软件包来恢复列表中的每个文件，该软件包并不总是你直接按名称安装的软件包。
   之后，`sudo dpkg --verify sl nginx-light nginx-common` 应仅输出经过批准的 `nginx.conf` 行。

### 解答

```bash
# 查看这六个软件包（含依赖）中所有被修改的文件
sudo dpkg --verify sl libncurses6 nginx-light nginx nginx-common libnginx-mod-http-echo

# 第二列为 c 的是 conffile，排除后只保留路径，排序写入列表
sudo dpkg --verify sl libncurses6 nginx-light nginx nginx-common libnginx-mod-http-echo | awk '$2 != "c" {print $2}' | sort > /home/learner/ops/tampered
cat /home/learner/ops/tampered

# 用 dpkg -S 找出每个文件真正的所属软件包（去掉 :amd64 等架构后缀）
dpkg -S $(cat /home/learner/ops/tampered)

# 重新安装这些所属软件包，修复普通文件，保留被编辑的 conffile
sudo apt-get install -y --reinstall $(dpkg -S $(cat /home/learner/ops/tampered) | cut -d: -f1 | sort -u)

# 应只剩经过批准的 /etc/nginx/nginx.conf 一行
sudo dpkg --verify sl nginx-light nginx-common
tail -n 1 /etc/nginx/nginx.conf
```
