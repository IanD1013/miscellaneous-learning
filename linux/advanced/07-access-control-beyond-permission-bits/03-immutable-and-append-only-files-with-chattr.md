权限位是针对调用者进行检查的，而 root 拥有 `CAP_DAC_OVERRIDE`，这会跳过该检查：
在 `sudo` 下，权限模式为 0444 的文件仍然可以打开进行写入。
Inode 属性则是针对文件本身进行检查的，无论操作者是谁。
`chattr` 通过独立于权限模式的 ioctl 来设置它们，其中有两个属性甚至对 root 也有效：

- `+i` 使文件不可变（immutable）。
  它不能被写入、重命名、删除或创建硬链接，并且其权限模式、所有者和时间戳都无法更改。
- `+a` 使文件仅可追加（append-only）。
  它只能以追加模式打开，因此新行只能添加到末尾，而截断、重写、重命名和删除都会被拒绝。

设置或清除这两个标志都需要 `CAP_LINUX_IMMUTABLE` 权能。
Root 拥有此权能，而 learner 账户没有，因此 `chattr` 需要在 `sudo` 下运行。
合法的修改需要三步：`chattr -i`、修改文件、`chattr +i`。

`/srv/ops/vault` 是 `/dev/sda`，这是为本节课挂载的一个 ext4 磁盘，因为文件系统必须支持这些标志，而此虚拟机的主根文件系统会拒绝 `chattr` 并报错 `Operation not supported`。

`lsattr` 将标志打印为一排字母，其中 `i` 和 `a` 就是这两个标志，而 ext4 添加到每个文件上的 `e` 代表 extents。
读取这些标志只需要文件的读取权限，因此在此处的一个 0644 文件上运行 `lsattr` 无需 `sudo`。

列出整个 vault 时才需要 `sudo`：
`lost+found` 的权限是 0700，因此普通的 `lsattr /srv/ops/vault` 会对该行打印 `Permission denied`，而 `sudo lsattr /srv/ops/vault` 则会列出每一行。

`chattr +FLAG FILE` 用于设置标志，`chattr -FLAG FILE` 用于清除标志。
以下是在 vault 中的临时文件上应用 `+i` 的示例：

```console
$ printf 'v1\n' | sudo tee /srv/ops/vault/draft.txt >/dev/null
$ sudo chattr +i /srv/ops/vault/draft.txt
$ lsattr /srv/ops/vault/draft.txt
----i---------e------- /srv/ops/vault/draft.txt
$ sudo mv /srv/ops/vault/draft.txt /srv/ops/vault/draft.old
mv: cannot move '/srv/ops/vault/draft.txt' to '/srv/ops/vault/draft.old': Operation not permitted
$ sudo chmod 0600 /srv/ops/vault/draft.txt
chmod: changing permissions of '/srv/ops/vault/draft.txt': Operation not permitted
$ sudo chattr -i /srv/ops/vault/draft.txt
$ sudo rm -- /srv/ops/vault/draft.txt
```

### 需求

`/srv/ops/vault` 包含 `policy.conf`（必须完全不允许任何更改）以及 `audit.log`（必须保持能够接收新行）。
两者初始权限均为 0644 且所有者为 root。
请在 `/dev/sda` 上就地为这两个文件设置这些标志；不得在 vault 或这两个文件中的任何一个之上挂载任何内容。

在您运行每条命令后，会有一个以 root 身份运行的检查来对每个文件测试三种更改（但不实际应用更改）：通过重命名另一个文件覆盖其名称来进行替换、以追加模式打开以及以读写模式打开。
它会在 `/run/dometrain-state/vault-check` 中为每个测试记录一行（`sudo cat` 可查看最新内容）。
当更改可以通过时，该行显示为 `ok`；当被文件自身的标志拒绝时，显示为 `denied`。

任何其他原因导致的拒绝（例如挂载覆盖了文件）会显示为 `blocked`，不再是常规文件的路径则会显示为 `missing`。

该文件内容必须如下：

```text
policy-rename=denied
policy-append=denied
policy-rewrite=denied
audit-append=ok
audit-rewrite=denied
audit-rename=denied
```

`policy.conf` 必须准确保持其当前的四行内容：

```text
policy_version = 7
retention_days = 400
export = disabled
admin_override = never
```

在设置任何标志之前，所有六行都显示为 `ok`。

任何一个标志都会阻止重命名覆盖该文件，因为内核会将正在被替换的文件视为正在被删除的文件：
它的名称将会消失，而这两个标志都不允许这种情况发生。


### 解答

```bash
# policy.conf 设为不可变：重命名覆盖、追加、读写全部拒绝
sudo chattr +i /srv/ops/vault/policy.conf
# audit.log 设为仅可追加：只允许追加，重写和重命名覆盖被拒绝
sudo chattr +a /srv/ops/vault/audit.log
# 确认标志（policy.conf 显示 i，audit.log 显示 a）
lsattr /srv/ops/vault/policy.conf /srv/ops/vault/audit.log
# 确认 policy.conf 内容未变
cat /srv/ops/vault/policy.conf
# 查看检查结果
sudo cat /run/dometrain-state/vault-check
```
