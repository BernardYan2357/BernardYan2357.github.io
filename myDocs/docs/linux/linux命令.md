# linux 命令

[54 Essential Linux Commands You Need To Know](https://www.youtube.com/watch?v=F7rMWdB1s08)

## 命令的命令

```bash
alias ls='ls --color=auto' # alias命令可以用来创建命令别名，简化常用命令的输入
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
Page Up/Down # 回滚终端命令历史
history # 显示命令历史，默认显示最近1000条命令，可以使用history n显示最近n条命令
```

## 文件操作

> 一切皆文件

```bash
pwd # 显示当前目录
ls # 列出当前目录下的文件和文件夹
    -l # 显示详细信息
    -lh # 显示详细信息，文件大小以人类可读的方式显示
    -a # 显示所有文件，包括隐藏文件（以.开头的文件）
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
find 目录 -name 文件名 # 在目录及其子目录中查找文件，可以使用正则表达式，例如find . -name "*.txt"查找当前目录及其子目录下所有以.txt结尾的文件
    -type f # 仅查找文件
    -type d # 仅查找目录
```

压缩和解压：

```bash
zip 文件名.zip 文件1 文件2 # 压缩文件
unzip 文件名.zip # 解压文件
    -d 目录名 # 解压到指定目录
```

文件权限管理

`ls -l`查看文件权限：`-rw-r--r--`
- 第一个字符表示文件类型，-表示普通文件，d表示目录，l表示符号链接等
- 后面9个字符分为三组，每组三个字符分别表示所有者、所属组和其他用户的权限，r表示读权限，w表示写权限，x表示执行权限，-表示没有该权限

符号模式调整`x`权限：
```bash
chmod +x update_system.sh    
# 所有用户（拥有者、组、其他）都添加执行权限
chmod u+x update_system.sh   
# 仅文件拥有者（user）添加执行权限
chmod -x update_system.sh    
# 所有用户移除执行权限
chmod u-x update_system.sh   
# 仅文件拥有者移除执行权限
```

数字模式调整`x`权限：
- 4表示读权限，2表示写权限，1表示执行权限，0表示没有权限
- 例如，权限`-rwxr-xr--`可以表示为754（4+2+1=7，4+1=5，4=4）
```bash
chmod 755 update_system.sh   # 设置权限为 rwxr-xr-x（常用）
chmod 700 update_system.sh   # 仅拥有者可执行
chmod 644 update_system.sh   # 移除所有执行权限（仅读写）
```

## 文本处理

[[linux文本编辑器]]

```bash
cat 文件名 # 显示文件内容
less 文件名 # 分页显示文件内容，按j向下翻页，按k向上翻页，按q退出
nano 文件名 # 使用nano文本编辑器编辑文件
vim 文件名 # 使用vim文本编辑器编辑文件
grep 关键词 文件名 # 在文件中搜索关键词
sed -i 's/旧字符串/新字符串/g' 文件名 # 替换文件中的字符串，-i表示直接修改文件，g表示替换所有匹配的字符串
awk '{print $1}' 文件名 # 打印文件中的某一列，例如打印第一列
```

echo 命令可以用来输出文本
```bash
echo "Hello, World!" # 输出文本
echo $PATH # $PATH是环境变量，因此可以使用echo命令输出环境变量的值
echo "Hello, World!" > file.txt # 将Hello, World!写入file.txt文件，覆盖原有内容
echo "Hello, World!" >> file.txt # 将Hello, World!追加到file.txt文件末尾
```

## 系统管理

用户和权限管理：
```bash
sudo 命令 # 以管理员权限执行命令
whoami # 显示当前用户
adduser 用户名 # 添加用户
su 用户名 # 切换用户
userdel -r 用户名 # 删除用户及其主目录
passwd 用户名 # 设置用户密码
```

系统监控和管理：
```bash
uname -a # 查看系统信息
htop # 实时显示系统资源占用情况
free -h # 显示内存使用情况，-h表示以人类可读的方式显示
df -h # 显示磁盘使用情况，-h表示以人类可读的方式显示
ps aux # 显示当前运行的进程，aux分别表示显示所有用户的进程、显示详细信息、显示进程所属的用户
kill 进程ID # 终止进程
    -9 # 强制终止进程
pkill 进程名 # 根据进程名终止进程
systemctl start 服务名 # 管理服务，start表示启动服务，stop表示停止服务，restart表示重启服务，status表示查看服务状态
```

## 网络工具

```bash
wget URL # 下载文件
curl URL # 发送HTTP请求，获取URL内容
ping IP地址或域名 # 测试网络连接
ifconfig # 查看网络接口信息
hostname -I # 查看本机IP地址
ip addr # 查看网络接口信息，ip addr show也可以
```

## pipeline

pipeline（管道符）可以将一个命令的输出作为另一个命令的输入，使用`|`符号连接。例如：
```bash
ls | grep ws # 列出当前目录下所有名称包含ws的文件和文件夹
ps aux | grep python # 列出所有运行的python进程
curl -s https://api.example.com/data | jq '.field' # 将curl的json输出通过jq工具提取特定字段
```

## 符号链接

符号链接（symbolic link）是一种特殊的文件，它包含了另一个文件或目录的路径，可以通过符号链接访问原文件或目录。使用`ln -s`命令创建符号链接。例如：
```bash
ln -s /path/to/original/file /path/to/symlink
```

## Bash脚本

Bash是Linux系统中常用的命令行解释器，Bash脚本是一种文本文件，包含了一系列的命令，可以通过执行脚本来自动化任务

Bash脚本以`.sh`为扩展名，第一行通常是shebang指令，告诉系统用哪种解释器来执行这个脚本
| shebang指令             | 含义                                     |
|:-----------------------:|:---------------------------------------:|
| `#!/bin/bash`         | 强制使用 Bash 解释器                        |
| `#!/bin/sh`           | 使用系统默认的 Shell（可能是 Bash 的简化模式）|
| `#!/usr/bin/env bash` | 更兼容的写法（自动从环境变量找`bash`）        |
| `#!/usr/bin/python3`  | 使用 Python 3                              |
随后是脚本的主体部分，可以包含任意的命令和逻辑

编写完成后，保存文件并赋予执行权限

运行脚本可以使用`./script.sh`命令或者`bash script.sh`命令，前者需要脚本具有执行权限，后者不需要