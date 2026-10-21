# Git 使用笔记

## Git 网络问题解决方法

使用镜像源加速 Clone：

- 临时使用镜像：

  ```bash
  git clone https://gitclone.com/<要克隆的Github地址>
  ```

- 使用 `git config` 设置永久镜像源：

  ```bash
  git config --global url."https://gitclone.com/".insteadOf https://
  nano ~/.gitconfig # 查看配置是否生效
  ```

设置代理：

```bash
git config --global http.proxy http://proxyserver:port
git config --global https.proxy http://proxyserver:port
```

打开 v2rayN，左下角看到`本地:[mixed:<port>]`，故代理地址为 `http://127.0.0.1:<port>`

## Git 基本操作

![git基本操作](git_workflow.png)

- `git pull`：从远程仓库拉取最新代码到本地
- `git add .`：将修改的代码添加到暂存区
- `git commit -m "提交说明"`：将暂存区的代码提交到本地仓库，并添加提交说明
- `git push`：将本地仓库的代码推送到远程仓库

### Git Clone

```bash
git clone <repository_url> # 克隆远程仓库到本地
git clone -b <branch_name> <repository_url> # 指定克隆分支
# 克隆后会在当前目录下创建一个新的文件夹，文件夹名称与仓库名称相同，如果想指定文件夹名称，可以在命令末尾添加一个参数
git clone <repository_url> <folder_name>
```

Git Clone 可以选择 https 或者 ssh 方式

#### HTTPS

```bash
git clone https://github.com/username/repository.git
```

如果克隆私有仓库，会提示输入 GitHub 用户名和密码，注意密码一栏要填入**个人访问令牌（Personal Access Token）**，而不是 GitHub 密码

生成个人访问令牌：

1. 登录 GitHub，进入 `Settings → Developer settings → Personal access tokens → Tokens (classic) → Generate new token`
2. 选择repo权限，生成令牌
3. 复制令牌，保存好
4. 使用时在密码栏填入该令牌

#### SSH

1. 生成SSH密钥：`ssh-keygen`
   一路回车即可，默认会生成在 `~/.ssh/id_ed25519`
2. 添加公钥到 GitHub：
   打开公钥文件`id_ed25519.pub`
   登录 `GitHub → Settings → SSH and GPG keys → New SSH key` 粘贴进去
3. 测试连接：`ssh -T git@github.com`
   如果成功，会出现 `Hi username! You've successfully authenticated, but GitHub does not provide shell access.`
4. 克隆仓库：`git clone git@github.com:username/repository.git`

### add & commit

配置用户名和邮箱：

```bash
git config --global user.name "your name"
git config --global user.email "your email"
# 如果去掉 --global 参数只对当前仓库有效
```

初始化仓库：

```bash
git init
touch .gitignore && nano .gitignore
```

修改文件后，add 至暂存区：

```bash
git add <file> # 添加单个文件
git add . # 添加当前目录下的所有文件
# 撤销 add
git restore <file> # 撤销工作区中未提交的修改
   --staged <file> # 取消暂存，但保留工作区修改
```

查看当前状态：

```bash
git status
git diff --cached # 查看已 add 的文件的修改内容
```

提交到本地仓库：

```bash
git commit -m "commit message"
# 撤销某次提交
git revert <commit_hash> # 创建一个新的提交来撤销指定的提交，保留历史记录
git reset --soft <commit_hash> # 将 HEAD 移动到指定提交，但保留工作区和暂存区的修改
git reset --hard <commit_hash> # 将 HEAD 移动到指定提交，并重置工作区和暂存区到该提交的状态，**会丢失修改**，慎用
```

#### 文件回退与恢复

如果对当前的某个文件不满意，可以使用以下命令回退到上一次提交的状态：

```bash
git checkout <commit_hash> -- <path/to/file> # 将指定文件回退到指定提交的状态
```

### .gitignore

.gitignore 文件用于让git在add时忽略某些文件或文件夹，写法为：

```bash
# 忽略单个文件
config.ini
# 忽略整个文件夹
build/
# 忽略特定类型的文件
*.log
# 忽略特定目录下的文件
logs/*.log
temp/**
# 不忽略某个文件（即使父目录被忽略）
!important.txt
```

### .gitmodule

.gitmodule 文件用于管理 Git 子模块，子模块是一个 Git 仓库嵌套在另一个 Git 仓库中的情况，使用子模块可以让你在一个仓库中包含另一个仓库的代码，并且保持它们之间的独立性

.gitmodule 文件遵循 INI 格式，包含子模块的路径和 URL，例如：

```ini
[submodule "submodule_name"]
    path = path/to/submodule # 相对于父仓库的路径
    url = https://github.com/username/submodule.git # 子模块的 Git 仓库 URL
```

在克隆带有子模块的仓库时，需要使用 `--recursive` 参数来同时克隆子模块：

```bash
git clone --recursive <repository_url>
```

如果已经克隆了仓库但没有使用 `--recursive`，可以使用以下命令来初始化和更新子模块：

```bash
git submodule init # 初始化子模块的本地配置，不会拉取代码
git submodule update # 按父仓库记录的提交检出子模块
git submodule update --init --recursive # 初始化并递归更新所有子模块，通常更常用
```

其中 `git submodule update --init --recursive` 一般就够用了；如果子模块里还有嵌套子模块，这个命令也会一起处理。需要注意的是，`update` 默认只是切到父仓库记录的提交，不会自动跟踪子模块远端的最新分支

### branch

Git 分支管理是 Git 强大功能之一，使用分支可以让你从开发主线上分离开来，然后在不影响主线的同时继续工作

查看所有分支：

```bash
git branch # 查看所有分支
   -r # 查看远程分支
   -a # 查看所有分支（本地和远程）
```

创建与切换分支：

```bash
git branch <branchname> # 创建新分支，但不切换
	-m <branchname> # 将当前分支重命名
git switch <branchname> # 切换到已有分支（已有分支包含远程分支）
   -c <branchname> # 创建新分支并切换，等价于 git checkout -b <branchname>
   -c <branchname> <startpoint> # 从startpoint创建新分支并切换
# startpoint 可以是另一个分支名
git switch -c <new_branch> <branchname> # 从 branchname 创建新分支并切换
git switch -c <new_branch> <shortname>/<branchname> # 从远程分支创建新分支并切换
# 也可以是一个提交的哈希值
git switch -c <new_branch> <commit_hash> # 从指定提交创建新分支并切换
# 也可以是一个标签
git switch -c <new_branch> <tagname> # 从指定版本标签创建新分支并切换
# 还可以是相对提交位置
git switch -c <new_branch> HEAD~3 # 从当前提交的上三个提交创建新分支并切换
```

> checkout 也可以切换分支，但由于 checkout 功能太杂，现已有更专门的 switch 命令

当你切换分支的时候，Git 会用该分支的最后提交的快照替换你的工作目录的内容，所以多个分支不需要多个目录

合并分支：

```bash
git merge <branchname> # 将指定分支合并到当前分支
```

当合并过程中出现冲突时，Git 会标记冲突文件，你需要手动打开冲突文件，按照标记解决冲突，解决后 add 该文件并 commit 即可

删除分支：

```bash
git branch -d <branchname> # 删除本地分支
   -D <branchname> # 强制删除未合并的分支
git push <shortname> --delete <branchname> # 删除远程分支
```

### 远程仓库

链接远程仓库：

```bash
git remote add <shortname> https://github.com/username/repo.git # 添加远程仓库
git remote # 查看远程仓库列表，列出远程仓库的 shortname
git remote -v # 列出远程仓库的 shortname 和 URL
```

shortname 是远程仓库的别名，默认是 origin，可以自定义为其他名称。shortname 可以在后续的 pull 和 push 命令中使用，代替完整的远程仓库 URL

与远程仓库的交互主要使用三个命令：

- `git fetch`：从远程仓库拉取最新代码到本地的远程缓存，但不会自动合并到本地分支
- `git pull`：从远程仓库拉取最新代码到本地，pull = fetch + merge，会自动合并到当前分支
- `git push`：将本地代码推送到远程仓库

要指定推送的远程仓库和分支，可以使用以下命令：

```bash
git push <shortname> <branchname>
```

此外，git 支持一个本地库链接多个远程仓库，只需要按上面的命令添加即可。其主要应用场景是 Fork 后需要同时链接原仓库和 Fork 仓库，方便从原仓库拉取最新代码和向 Fork 仓库推送修改，例如：

```bash
git fetch upstream # 从上游仓库拉取最新代码
git push origin # 将修改推送到 Fork 仓库
```

远程提交先于本地提交时的解决方法：选取合并策略，合并策略决定合并后提交树的结构，一般选择 merge 即可

```bash
git config pull.rebase false  # merge，表示使用合并的方式将远程提交和本地提交合并，保留两者的提交历史
git config pull.rebase true   # rebase，表示使用变基的方式将远程提交和本地提交合并，重写提交历史，使其看起来像是本地提交在远程提交之后进行的
git config pull.ff only       # fast-forward only，表示只允许快进合并，如果远程提交先于本地提交，则拒绝合并，要求先将本地提交推送到远程仓库
git config --global pull.rebase false  # 设置全局默认合并策略为 merge
```

再次推送后，编辑器提示有冲突，使用冲突编辑器解决冲突，将冲突解决后，add 解决后的文件，commit 后再次 push 即可

### Git Release

管理 Release Tag：

```bash
# 创建一个新的 Tag
git tag -a v1.0.0 -m "Release version 1.0.0"
# 查看所有 Tag
git tag
# 删除本地 Tag
git tag -d v1.0.0
# 删除远程 Tag
git push origin --delete v1.0.0
```

### Git 凭证管理

使用 VSCode 的 Git 功能时，弹出 git-credential-manager

如何管理 Git 凭证：

```bash
git credential-manager github list
git credential-manager github logout 要移除的账号名称
```

使用Git时总是需要反复填入用户名和密码（HTTPS协议），如何配置凭据缓存？

- 方案1：永久存储密码

     ```bash
     git config --global credential.helper store
     ```

   下次 `git push/pull` 输入一次用户名密码后，会永久存储到 `~/.git-credentials` 文件（明文），之后不再需要输入密码，但不安全，不推荐
- 方案2：使用 SSH 密钥
  - 生成 SSH 密钥：`ssh-keygen -t ed25519 -C "你的邮箱"`
  - 复制公钥：`cat ~/.ssh/id_ed25519.pub`
  - 添加到 Gitee：登录 Gitee → 右上角头像 → 设置 → SSH 公钥 → 粘贴刚才复制的内容
  - 切换远程地址为 SSH：`git remote set-url origin git@gitee.com:openrover/OpenRover.git`
  - 测试：`ssh -T git@gitee.com`
  - 之后 push/pull 不再需要密码

## 清理提交历史

## 删库跑路

取消本地的Git管理：

```bash
rm -rf .git
```

## Git 原理

- [原来我一点都不懂Git](https://www.bilibili.com/video/BV18ZiFB3EUy)
