# Linux优化笔记

## 磁盘空间清理

### 找出空间被谁占用

```bash
df -h # 查看各分区使用情况
du -sh /* 2>/dev/null | sort -h # 查看根目录下各文件夹大小（按大小排序）
du -h --max-depth=1 / | sort -h # 同上，只显示一层目录
```

更推荐安装交互式工具 `ncdu`，方向键进入目录、`d` 删除文件：

```bash
sudo apt install ncdu
ncdu / # 扫描根目录，也可指定如 ncdu ~
```

查找大于 500MB 的单个文件：

```bash
sudo find / -xdev -type f -size +500M -exec ls -lh {} \;
```

> `-xdev` 表示不跨文件系统，避免扫描到 /proc、挂载的其他盘

### 清理包管理器缓存与无用依赖

```bash
sudo apt autoremove --purge    # 删除不再需要的依赖和旧内核（最常用）
sudo apt clean                 # 清空 /var/cache/apt/archives 的 deb 包缓存
sudo apt autoclean             # 只清理已无法下载的旧包
sudo rm -rf /var/lib/snapd/cache/* # 清理 snap 的包缓存
sudo snap set system refresh.retain=2 # 限制 snap 保留版本数
```

### 清理系统日志

`systemd` 系统的日志常占几个 GB：

```bash
journalctl --disk-usage                  # 查看日志占用
sudo journalctl --vacuum-size=100M       # 只保留 100MB
sudo journalctl --vacuum-time=7d         # 只保留最近 7 天
```

### 清理 Docker

```bash
docker system df               # 先查看镜像/容器/卷占用
docker system prune            # 删除停止的容器、悬空镜像、无用网络
docker system prune -a --volumes  # 连未使用的镜像和数据卷一起删（谨慎！）
```

### 清理用户目录

```bash
# 回收站
rm -rf ~/.local/share/Trash/*

# 各应用缓存（可安全删除，需要时会重新生成）
du -sh ~/.cache/* | sort -h
rm -rf ~/.cache/<对应程序>

# pip / conda 缓存
pip cache purge
conda clean --all # 详见 Anaconda 笔记
```

### 其他

- `/tmp`：临时文件，重启一般自动清空，也可手动删除其中的旧文件

> WSL2 注意：在 Linux 内删除文件后，Windows 上的 `.vhdx` 虚拟磁盘文件**不会自动缩小**，需要在 PowerShell 中压缩，见 [[WSL2]]

## lolcat

一些有趣的命令行工具：
- Cowsay
- jp2a：图片转 ASCII 字符画
- cbonsai
- cmartix
- pips
- aquarium

## Fastfetch

安装：
```bash
sudo add-apt-repository ppa:zhangsongcui3371/fastfetch
sudo apt update
sudo apt install fastfetch
```

使用：
```bash
fastfetch
fastfetch --logo small
```

每天显示一次：
```bash
# ~/.bashrc
FASTFETCH_STAMP="$HOME/.cache/fastfetch_last_run"
TODAY=$(date +%Y-%m-%d)
if [ ! -f "$FASTFETCH_STAMP" ] || [ "$(cat "$FASTFETCH_STAMP" 2>/dev/null)" != "$TODAY" ]; then
    mkdir -p "$HOME/.cache"
    fastfetch --logo small
    echo "$TODAY" > "$FASTFETCH_STAMP"
fi
```

## gnome-tweaks

使用该工具调整字体、图标等外观设置

安装
```bash
sudo apt install gnome-tweaks
```

使用
```bash
gnome-tweaks
```

## Terminator

安装
```bash
sudo apt install terminator
```

配置
- 打开Terminator，右键`配置文件首选项`，进行配置
- 或者者编辑配置文件`~/.config/terminator/config`

建议配置项：
- 打开`选中即复制`

快捷键
- Ctrl+Shift+E 垂直分割窗口
- Ctrl+Shift+O 水平分割窗口

设为默认终端
```bash
sudo update-alternatives --config x-terminal-emulator
```

此方法只能改变用快捷键`Ctrl+Alt+T`打开的终端

右键菜单中添加"open_in_Terminator"选项方式：在右键菜单中添加一个脚本，当点击脚本选项时，打开Terminator并切换到当前目录
```bash
gedit ~/.local/share/nautilus/scripts/open_in_terminator
# 在文件中添加以下内容
# #!/bin/bash
# terminator --working-directory="$PWD"
chmod +x ~/.local/share/nautilus/scripts/open_in_terminator
nautilus -q  # 重启nautilus
```
> nautilus是Gnome桌面的文件管理器
> `$PWD`是当前目录的路径

之后进入你要在终端打开的目录，右键点击其中的文件或文件夹，选择`脚本 -> open_in_terminator`即可
> 在文件夹的空白处右键可能不会显示

