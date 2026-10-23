### 告诉 git 你是谁

每次提交都会标记作者姓名和电子邮箱。
该环境以默认身份启动，因此在记录任何内容之前，请声明你自己的身份。

1. `git config user.name "Ada Lovelace"`：必须完全是这个名字，检查点会读取它。
2. `git config user.email ada@example.com`。
3. `git config --list`：显示所有已存储的内容，包括身份信息。
4. 地址可能会更改。使用 `git config --unset user.email` 删除旧地址，然后设置新地址：`git config user.email ada@lovelace.dev`。

这个浏览器内置的 git 仅存储 `user.name` 和 `user.email`。
真实的 git 还接受 `--global` 和 `--local` 来选择设置的存储位置；在这里两者都被接受且含义相同。
