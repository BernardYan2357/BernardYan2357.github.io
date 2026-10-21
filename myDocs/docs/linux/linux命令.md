# linux 命令

[54 Essential Linux Commands You Need To Know](https://www.youtube.com/watch?v=F7rMWdB1s08)

## 命令的命令

```bash
alias ls='ls --color=auto' # alias命令可以用来创建命令别名，简化常用命令的输入
# alias 默认只对当前 shell 会话有效
# 注意别名不能有空格
which ls # 输出ls命令的可执行文件路径，例如/usr/bin/ls，如果参数是一个别名，则输出别名的定义
whereis ls # 输出ls命令的可执行文件路径，源代码路径和手册页路径
whatis ls # 输出ls命令的简要描述，例如ls (1) - list directory contents
man ls # 显示ls命令的手册页，按q退出
```

## 终端操作

```bash
Ctrl + Alt + T # 快捷键打开终端
clear # 清屏
exit # 退出终端
```

### 高效地键入命令

历史记录：
```bash
Page Up/Down # 回滚终端命令历史
history # 显示命令历史，默认显示最近1000条命令，可以使用history n显示最近n条命令
```

光标导航：
- `Home`：光标移动到命令头
- `End`：光标移动到命令尾
- `Ctrl + ←`：光标向左移动一个单词，是否可用取决于终端是否支持
- `Ctrl + →`：光标向右移动一个单词，是否可用取决于终端是否支持

## 文件操作

> “一切皆文件” 是 Linux 的基本哲学之一，它是指 Linux 中的一切都可以通过文件的方式访问、管理，即使不是文件，也以文件的形式来管理。例如硬件设备、进程、套接字等都抽象成文件，使用统一的用户接口，虽然文件类型各不相同，但是对其提供的却是同一套操作

```bash
pwd # 显示当前目录
ls # 列出当前目录下的文件和文件夹
    -l # 显示详细信息
    -lh # 显示详细信息，文件大小以人类可读的方式显示
    -a # 显示所有文件，包括隐藏文件（以.开头的文件）
    -r # 逆序显示
    -R # 递归显示
find 目录 -name 文件名 # 在目录及其子目录中查找文件，可以使用正则表达式，例如：find . -name "*.txt"
    -type f # 仅查找文件
    -type d # 仅查找目录
cd 目录名 # 切换目录
    ~(or)null # 用户主目录，对于一般用户，回到/home/username
    ..(or)- # 上一级目录
mkdir 目录名 # 创建目录
touch 文件名 # 创建文件
cp 源文件 目标文件 # copy
mv 源文件 目标文件 # 移动文件或重命名文件
rm 文件名 # 删除文件
    -r # 递归删除目录及其内容
    -f # 强制删除文件或目录，不提示确认
    -rf # 递归强制删除目录及其内容
    -i # 删除文件时提示确认
rmdir 目录名 # 删除空目录
cmp 文件1 文件2 # 比较两个文件是否相同
diff 文件1 文件2 # 显示两个文件的差异
```

### 压缩&解压

```bash
zip 文件名.zip 文件1 文件2 文件夹/ # 压缩文件，注意文件夹要使用相对路径，避免压缩后解压时出现路径问题
    -r # 递归压缩目录及其内容
    -q # 压缩时不显示压缩过程
    -m # 压缩后删除源文件
    -x 文件名 # 压缩时排除指定文件或目录，例如 .git/
    -9 # 压缩时使用最大压缩比
unzip 文件名.zip # 解压文件
    -d 目录名 # 解压到指定目录
```

Link: [[linux命令#文件权限管理]]

## 文本处理

Link: [[linux文本编辑器]]

```bash
cat 文件名 # 显示文件内容
less 文件名 # 分页显示文件内容，按j向下翻页，按k向上翻页，按q退出
nano 文件名 # 使用nano文本编辑器编辑文件
vim 文件名 # 使用vim文本编辑器编辑文件
sed -i 's/旧字符串/新字符串/g' 文件名 # 替换文件中的字符串，-i表示直接修改文件，g表示替换所有匹配的字符串
awk '{print $1}' 文件名 # 打印文件中的某一列，例如打印第一列
```

grep 命令用来从输入文本中查找，grep 的关键词支持正则表达式，例如：

```bash
bernard@LAPTOP:~$ ls -a | grep test.py
test.py
test_py
```

想要只搜索 "test.py"，使用 `-F` 参数（全称是 `--fixed-strings`），把匹配模式设为普通固定字符串

```bash
grep 关键词 文件名 # 在文件中搜索关键词
```

echo 命令可以用来输出文本：

```bash
echo "Hello, World!" # 输出文本
echo $PATH # $PATH是环境变量，因此可以使用echo命令输出环境变量的值
echo "Hello, World!" > file.txt # 将Hello, World!写入file.txt文件，覆盖原有内容
echo "Hello, World!" >> file.txt # 将Hello, World!追加到file.txt文件末尾
```

## 系统管理

### 环境变量

在 Linux 中，环境变量是一组动态的键值对，用于影响进程的行为或存储配置信息（如系统路径、用户设置等）

查看环境变量：

```bash
printenv # 列出所有环境变量
echo $变量名 # 查看单个变量的值
```

设置临时环境变量（仅在当前终端会话中有效）

  ```bash
  export 变量名="value" # 设置变量，并使其对子进程可见
  变量名=值 # 仅为当前进程设置变量，不会传递给子进程
  ```

永久设置环境变量：

- 编辑配置文件，如 `~/.bashrc`（用户级）、`~/.bash_profile`、`/etc/environment`（系统级）或 `/etc/profile`（系统级）
- 添加 `export` 语句到对应配置文件，然后执行 `source ~/.bashrc` 使其生效

环境变量的引用：

- `$NAME`：基本形式，但后面紧跟字母或数字时容易歧义
- `${NAME}`：推荐形式，可以明确界定变量名边界，并能加后缀，如 `ros-${ROS_DISTRO}-xxx`

常用环境变量：

| 变量名       | 说明                         |
| --------- | -------------------------- |
| `PATH`    | 可执行程序的搜索路径，路径间用 `:` 分隔     |
| `HOME`    | 当前用户的主目录                   |
| `USER`    | 当前登录的用户名                   |
| `SHELL`   | 当前使用的 Shell（如 `/bin/bash`） |
| `LANG`    | 系统语言和编码（如 `zh_CN.UTF-8`）   |
| `PWD`     | 当前工作目录的路径                  |
| `OLD_PWD` | 上一个工作目录的路径                 |

修改与删除环境变量：

  ```bash
  unset 变量名 # 删除环境变量
  export PATH=$PATH:/新路径 # 追加新路径到 PATH 变量中
  ```

### 用户和权限

#### 用户管理

```bash
sudo 命令         # 以管理员权限执行命令
whoami            # 显示当前用户
adduser 用户名    # 添加用户
userdel -r 用户名 # 删除用户及其主目录
su 用户名         # 切换用户
passwd 用户名     # 设置用户密码
```

#### 文件权限管理

`ls -l`查看文件权限：`-rw-r--r--`

- 第一个字符表示文件类型，-表示普通文件，d表示目录，l表示符号链接等
- 后面9个字符分为三组，每组三个字符分别表示所有者、所属组和其他用户的权限，r表示读权限，w表示写权限，x表示执行权限，-表示没有该权限

符号模式调整`x`权限：

```bash
chmod +x update_system.sh # 所有用户（拥有者、组、其他）都添加执行权限
chmod u+x update_system.sh # 仅文件拥有者（user）添加执行权限
chmod -x update_system.sh # 所有用户移除执行权限
chmod u-x update_system.sh # 仅文件拥有者移除执行权限
```

数字模式调整`x`权限：

- 4表示读权限，2表示写权限，1表示执行权限，0表示没有权限
- 例如，权限`-rwxr-xr--`可以表示为754（4+2+1=7，4+1=5，4=4）

```bash
chmod 755 update_system.sh   # 设置权限为 rwxr-xr-x（常用）
chmod 700 update_system.sh   # 仅拥有者可执行
chmod 644 update_system.sh   # 移除所有执行权限（仅读写）
```

#### 用户组

Linux 的文件权限对 `user / group / others` 三类对象分别设置。若没有组，多用户共享文件只能二选一：

- 给 others 权限 → 全系统用户都能访问，失去控制
- 逐个用户授权 → 维护成本高，难以统一回收

组作为用户与权限之间的中间层，把若干用户归为集合统一授权：

- 权限绑定在组上，而不是单个用户上，管理一组人而非逐个管理
- 一个用户可加入多个组，权限取并集
- 主组（primary group）决定新建文件的默认所属组；附加组（supplementary group）用于额外授权
- 典型应用：`sudo` 组、`docker` 组、项目协作的 `dev` 组

```bash
groupadd 组名               # 添加用户组
groupdel 组名               # 删除用户组
groupmod -n 新组名 旧组名    # 重命名用户组

usermod -aG 组名 用户名       # 将用户加入附加组（-a 追加，-G 指定附加组）
gpasswd -d 用户名 组名        # 将用户移出组
groups 用户名                # 查看用户所属的所有组
id 用户名                    # 显示 UID、GID 及所属组信息

chgrp 组名 文件路径           # 修改文件/目录的所属组
newgrp 组名                  # 临时切换当前会话的有效组（退出后恢复）

# 创建用户时直接指定主组和附加组
useradd -m -g 主组名 -G 附加组名 用户名
```

### 系统监控

```bash
uname -a # 查看系统信息
htop # 实时显示系统资源占用情况
free -h # 显示内存使用情况，-h表示以人类可读的方式显示
```

### 进程管理

进程是正在运行的程序实例，每个进程有一个进程 ID（PID）

#### 进程信号

信号（signal）用于向进程通知事件或发送控制请求

下表编号适用于 Linux x86/ARM；部分架构编号不同，但信号名称统一，可用 `kill -l` 查看本机列表

| 信号                    | 编号      | 默认行为        | 常见来源或用途                                       |
| --------------------- | ------- | ----------- | --------------------------------------------- |
| `SIGHUP`              | 1       | 终止          | 控制终端挂断；部分服务会自行处理它来重新加载配置，具体看程序约定              |
| `SIGINT`              | 2       | 终止          | 终端通常用 `Ctrl+C` 向前台进程组发送，请求中断                  |
| `SIGQUIT`             | 3       | 终止并尝试生成核心转储 | 终端通常用 `Ctrl+\` 触发，可用于保留调试信息                   |
| `SIGABRT`             | 6       | 终止并尝试生成核心转储 | 程序调用 `abort()` 主动异常终止，如部分断言失败                 |
| `SIGKILL`             | 9       | 强制终止        | `kill -KILL PID`（即 `kill -9 PID`）；程序无法捕获它执行清理 |
| `SIGUSR1` / `SIGUSR2` | 10 / 12 | 终止          | 留给程序自定义用途，如输出状态或触发操作，需先确认程序约定                 |
| `SIGSEGV`             | 11      | 终止并尝试生成核心转储 | 无效内存访问，常见报错为“段错误”（Segmentation fault）         |
| `SIGPIPE`             | 13      | 终止          | 向已无读取端的管道或连接已关闭的流式套接字写入数据                     |
| `SIGALRM`             | 14      | 终止          | `alarm()` 等定时器到期通知                            |
| `SIGTERM`             | 15      | 终止          | `kill PID` 默认发送；程序可以捕获后保存数据、释放资源再退出           |
| `SIGCHLD`             | 17      | 忽略          | 通知父进程：子进程已终止、暂停或恢复；父进程可用 `wait` 系列调用回收退出状态    |
| `SIGCONT`             | 18      | 恢复运行        | `kill -CONT PID`；使已暂停的进程继续运行                  |
| `SIGSTOP`             | 19      | 暂停          | `kill -STOP PID`；强制暂停进程，保留其运行状态               |
| `SIGTSTP`             | 20      | 暂停          | 终端通常用 `Ctrl+Z` 向前台进程组发送，程序可以自行处理              |
| `SIGTTIN` / `SIGTTOU` | 21 / 22 | 暂停          | 后台进程组读取控制终端，或在特定条件下写入、操作控制终端时触发               |

- 表中是**默认行为**；程序可以为多数信号注册处理函数或选择忽略，但 `SIGKILL` 和 `SIGSTOP` **不能被捕获、忽略或阻塞**
- 终止进程通常先发送 `SIGTERM`，给程序清理和退出的机会；确认无法正常退出后再考虑 `SIGKILL`
- 暂停不会结束进程，可用 `SIGCONT` 恢复；核心转储（core dump）用于调试，实际是否生成文件取决于系统配置和资源限制

#### 查看与终止进程

```bash
ps aux # 查看所有用户的进程，显示用户、PID、CPU/内存占用、命令等
ps -p 进程ID -o pid,ppid,stat,etime,args # 查看指定进程的 PID、父进程、状态、运行时长和命令
pgrep -af 'train.py' # 按完整命令行查找进程，显示 PID 和命令

kill 进程ID # 默认发送 SIGTERM（15），请求进程退出
kill -INT 进程ID # 发送 SIGINT（2），程序可能按 Ctrl+C 的方式处理中断
kill -9 进程ID # 发送 SIGKILL（9），强制终止，进程无法捕获该信号进行清理
pkill -x 进程名 # 按进程名精确匹配，向所有匹配进程发送 SIGTERM
```

`ps aux` 中，`a` 和 `x` 组合表示查看所有用户的进程（包括无控制终端的进程），`u` 表示使用面向用户的详细输出格式

#### 前台与后台任务

- **前台任务**：占用当前终端的前台，通常需要等待任务结束后才能继续输入 Shell 命令
- **后台任务**：Shell 不等待其结束，可以继续输入命令；未重定向时，输出仍可能显示在终端
- **作业（job）**：当前 Shell 管理的一条命令或一组管道进程，用 `%1` 等作业编号引用；作业编号与 PID 不同

```bash
python train.py                    # 在前台运行
python train.py > train.log 2>&1 & # 在后台运行，并将输出写入日志

jobs -l                         # 查看当前 Shell 的作业、状态和 PID
fg %1                           # 将编号为 1 的作业移到前台；若已暂停则恢复
bg %1                           # 让编号为 1 的已暂停作业在后台继续运行
```

前台运行时：

- `Ctrl+C`：通常向前台进程组发送 SIGINT，请求中断程序
- `Ctrl+Z`：通常向前台进程组发送 SIGTSTP，暂停任务，不会使其继续在后台运行

例如，已经在前台运行的进程，可以先按 `Ctrl+Z`，再用 `jobs -l` 确认编号，最后执行 `bg %1` 恢复到后台。需要终端输入的后台任务可能再次暂停

`jobs` 只显示当前 Shell 的作业；重新连接后的新 Shell 不能靠它查看旧 Shell 的作业。单独使用 `&` 或 `bg` 不保证关闭终端后任务继续运行

#### 断开终端后继续运行

References: 
- [GNU nohup](https://www.gnu.org/software/coreutils/manual/html_node/nohup-invocation.html)
- [Bash disown](https://www.gnu.org/software/bash/manual/html_node/Job-Control-Builtins.html)

**启动新任务：使用 nohup**

在后台运行的进程仍会因为终端的终止而结束。`nohup` 使启动的命令忽略 SIGHUP（终端挂断信号），`&` 负责后台运行。对于不需要交互输入的长任务，可以显式重定向输入和输出：

```bash
nohup python -u train.py > train.log 2>&1 < /dev/null &
echo $!                         # 查看最近一个后台任务的 PID，建议启动后立即记录
```

| 写法 | 含义 |
| --- | --- |
| `nohup` | 使启动的命令忽略 SIGHUP，本身不会将命令放到后台 |
| `python -u` | Python 使用无缓冲的标准输出和标准错误，便于及时查看日志 |
| `> train.log` | 将标准输出写入日志，覆盖原有内容；用 `>>` 则追加 |
| `2>&1` | 将标准错误重定向到标准输出当前的位置，此处也写入日志 |
| `< /dev/null` | 从空设备读取标准输入，不再依赖终端输入 |
| `&` | 在后台运行 |

重定向从左到右处理，`> train.log 2>&1` 与 `2>&1 > train.log` 的效果不同。日志路径包含目录时，需要提前创建该目录

```bash
tail -n 50 train.log            # 查看最近 50 行日志
tail -f train.log               # 持续跟踪日志，Ctrl+C 只退出日志查看
ps -p 进程ID -o pid,stat,etime,args # 确认记录的进程是否仍在运行
kill 进程ID                     # 停止对应的后台进程
```

**已启动的任务：使用 disown**

在原来的 Bash 中，可将任务放到后台后使用 `disown`：

```bash
# 若任务仍在前台，先按 Ctrl+Z 暂停
jobs -l                         # 确认作业编号，下面假设为 1
bg %1                           # 若已暂停，让其在后台继续运行
disown -h %1                    # 保留作业记录，但标记为 Bash 挂断时不向它转发 SIGHUP
```

另一种写法是 `disown %1`，直接将作业从当前 Shell 的作业表移除，之后不能再用 `jobs`、`fg`、`bg` 管理它，但仍能通过 PID 查看和终止

`disown` **不会改变任务已有的标准输入、输出和错误输出**。若它们仍连接原终端，终端关闭后仍可能出现输入输出问题；准备长任务时，应在启动时使用完整重定向或放进 tmux / screen

`nohup` 和 `disown` 处理的是挂断信号相关问题，不能防止程序崩溃、内存不足被杀或系统关机，也不保证绕过管理员配置的会话清理策略。需要退出后自动重启时，使用适当配置的 systemd 服务

#### 保留和恢复终端会话

References: 
- [tmux 手册](https://man7.org/linux/man-pages/man1/tmux.1.html)
- [GNU Screen 分离会话](https://www.gnu.org/software/screen/manual/html_node/Detach.html)

tmux 和 screen 可以将终端会话与当前连接分离，之后重新连接到原会话，继续查看输出和交互操作。应先创建会话，再在其中启动任务

**tmux**

```bash
tmux new -s train               # 创建名为 train 的会话，并进入
python -u train.py              # 在会话内启动任务
```

离开会话时，先按 `Ctrl+B`，松开后再按 `D`，即可分离会话，任务继续运行。重新连接服务器后：

```bash
tmux ls                         # 列出当前用户的会话
tmux attach -t train            # 回到 train 会话
```

分离会话不会停止任务；在会话内按 `Ctrl+C` 则通常会中断前台任务。任务结束后，可在会话的 Shell 中执行 `exit` 关闭该窗格；最后一个窗格关闭后，会话结束

**screen**

```bash
screen -S train                 # 创建名为 train 的会话，并进入
python -u train.py              # 在会话内启动任务
```

先按 `Ctrl+A`，松开后再按 `D`，即可分离会话。重新连接服务器后：

```bash
screen -ls                      # 列出当前用户的会话
screen -r train                 # 恢复对应会话；重名时使用列表中的完整会话标识
```

### 服务管理

服务通常由服务管理器统一启动、停止和监控。下面适用于使用 systemd 的 Linux 系统，`服务名.service` 需要替换为已存在的服务单元名称

#### start, stop & state

```bash
sudo systemctl start 服务名.service   # 立即启动
sudo systemctl stop 服务名.service    # 立即停止
sudo systemctl restart 服务名.service # 重新启动；未运行时也会启动
sudo systemctl reload 服务名.service  # 让服务重读自身配置，需要服务支持
systemctl status 服务名.service       # 查看状态和近期日志，按 q 退出分页
systemctl list-units --type=service --state=running # 列出当前运行的服务
```

#### 开机自启

```bash
sudo systemctl enable 服务名.service        # 配置开机自启，不会立即启动
sudo systemctl disable 服务名.service       # 取消开机自启，不会立即停止
systemctl is-enabled 服务名.service         # 查看是否已启用自启
```

#### 日志与配置重载

```bash
sudo journalctl -u 服务名.service -n 50 # 查看服务最近 50 条日志
sudo journalctl -u 服务名.service -f    # 持续查看日志，Ctrl+C 退出查看
sudo journalctl -u 服务名.service -b    # 查看本次系统启动以来的服务日志

sudo systemctl daemon-reload           # 新增或修改单元文件后，让 systemd 重新读取
sudo systemctl restart 服务名.service   # 随后按需重启服务，使修改应用到运行进程
```

`reload` 是让服务重读自身配置；`daemon-reload` 是让 systemd 重读单元文件，本身不会重启服务

以上默认管理系统级服务；管理当前用户的服务时，使用 `systemctl --user ...` 和 `journalctl --user -u 服务名.service ...`，通常不加 `sudo`

若要让自己的脚本作为服务运行，需要先编写对应的 `.service` 单元；异常退出后是否自动重启由 `Restart=` 等配置决定，`enable` 本身不负责自动重启

### 磁盘空间管理

```bash
df -h # 显示磁盘使用情况，-h表示以人类可读的方式显示
```

挂载硬盘的步骤可以参考：[[RDK S100 使用笔记#挂载硬盘]]

## 网络工具

```bash
wget URL # 下载文件
curl URL # 发送HTTP请求，获取URL内容
curl -x <代理服务器地址> <访问地址>
ping IP地址或域名 # 测试网络连接
ifconfig # 查看网络接口信息
hostname -I # 查看本机IP地址
ip addr show# 查看网络接口信息
```

## 时间同步

有时在安装软件时会遇到网络问题，当你检查认为网络一切正常时，可能是因为系统时间不正确导致的SSL证书验证失败：

```bash
sunrise@ubuntu:~$ sudo pip install rosdepc
WARNING: Retrying (Retry(total=4, connect=None, read=None, redirect=None, status=None)) after connection broken by 'ProtocolError('Connection aborted.', RemoteDisconnected('Remote end closed connection without response'))': /simple/rosdepc/
```

当我们查看系统时间发现系统时间不正确时，可以使用以下命令同步系统时间：

```bash
# 自动时间同步
timedatectl # 查看 NTP service: active 是否显示为 yes
# 若为 no，则执行以下命令启用 NTP 同步
sudo timedatectl set-ntp on
# 手动时间同步
sudo apt-get install ntpdate
sudo ntpdate cn.pool.ntp.org # 从中国的 NTP 服务器同步时间
sudo hwclock -w # 将系统时间写入硬件时钟
```

## pipeline

pipeline（管道符）可以将一个命令的输出转化为标准输入，传递给后面的命令，使用`|`符号连接。例如：

```bash
ls | grep ws # 列出当前目录下所有名称包含ws的文件和文件夹
curl -s https://api.example.com/data | jq '.field' # 将curl的json输出通过jq工具提取特定字段
```

## link（软链接 & 硬链接）

链接（link）为同一个文件或目录提供多个访问入口，分为硬链接（hard link）和软链接（symbolic link，符号链接）两种。

```bash
ln 原文件 硬链接名        # 创建硬链接（默认）
ln -s 原文件 软链接名     # 创建软链接，-s 表示 symbolic
readlink 软链接名        # 查看软链接指向的路径
unlink 链接名            # 删除链接（等价于 rm，对链接本身而言）
```

|            | 硬链接（hard link）    | 软链接（symbolic link）    |
| ---------- | ----------------- | --------------------- |
| 本质         | 同一个 inode 的另一个目录项 | 独立文件，内容是目标路径字符串       |
| inode      | 与原文件**相同**        | 与原文件**不同**            |
| 创建命令       | `ln 源文件 链接名`      | `ln -s 源文件 链接名`       |
| 跨文件系统      | 不能                | 可以                    |
| 指向目录       | 普通用户不能            | 可以                    |
| 原文件删除后     | 仍可访问（数据未丢）        | 失效，成为断链               |
| `ls -l` 显示 | 看不出差别，链接计数 +1     | 显示 `l` 类型和 `链接 -> 目标` |
| 磁盘占用       | 几乎不占额外空间          | 占少量空间存路径字符串           |
> 什么是 inode？它是文件系统用来描述一个文件的数据结构（index node），记录了文件的元信息：类型、权限、所有者、大小、时间戳，以及数据块在磁盘上的位置。文件名本身并不存在 inode 里，而是存放在目录中，目录的作用就是把文件名映射到 inode 号
>
> 理解这一点，软硬链接的区别就清楚了：
> - 硬链接：，所以它们是同一个文件，只是名字不同
> - 软链接：一个新的 inode，它对应的数据内容就是另一条目标路径的字符串

### 硬链接（hard link）

硬链接是同一个 inode 的另一个目录项（也就是同一个文件的另一个名字）。它和原文件完全平等，没有"谁指向谁"的关系

- 与原文件共享同一个 inode，不占额外磁盘空间
- 删除其中一个名字，只是把 inode 的链接计数减一，数据在计数归零时才真正释放
- 不能跨文件系统，普通用户也不能给目录创建硬链接
- `ls -l` 看不出差别，只是链接计数（第二列）+1

```bash
ln report.txt report_backup.txt   # report_backup.txt 是 report.txt 的硬链接
ls -l report.txt report_backup.txt # 两者链接计数均为 2
stat report.txt                   # 查看 inode 号和 Links 计数
```

### 软链接（symbolic link）

软链接是一个独立文件，内容是目标路径的字符串，类似 Windows 的快捷方式。使用`ln -s`命令创建。例如：

```bash
ln -s /path/to/original/file /path/to/symlink # -s表示创建符号链接，第一个路径是原文件或目录的路径，第二个路径是符号链接的路径（目录）
```

- 有自己的 inode，占少量空间用于存放路径字符串
- 可以指向目录，也可以跨文件系统
- 原文件删除后，链接失效成为"断链"（dangling link）
- `ls -l` 显示为 `l` 类型，并显示 `链接 -> 目标`

## bash script

Bash 是 Linux 系统中常用的命令行解释器，Bash 脚本是一种文本文件，包含了一系列的命令，可以通过执行脚本来自动化任务

Bash 脚本以`.sh`为扩展名，第一行通常是 shebang 指令，告诉系统用哪种解释器来执行这个脚本

| shebang指令             | 含义                            |
| --------------------- | ----------------------------- |
| `#!/bin/bash`         | 强制使用 Bash 解释器                 |
| `#!/bin/sh`           | 使用系统默认的 Shell（可能是 Bash 的简化模式） |
| `#!/usr/bin/env bash` | 更兼容的写法（自动从环境变量找`bash`）        |
| `#!/usr/bin/python3`  | 使用 Python3                    |

随后是脚本的主体部分，可以包含任意的命令和逻辑

编写完成后，保存文件并赋予执行权限

运行脚本可以使用`./script.sh`命令或者`bash script.sh`命令，前者需要脚本具有执行权限，后者不需要
