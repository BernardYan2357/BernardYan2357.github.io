# Linux优化笔记

## lolcat

一些有趣的命令行工具：
- Cowsay
- jp2a：图片转 ASCII 字符画
- Neoftech
- cbonsai
- cmartix
- pips
- aquarium

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

