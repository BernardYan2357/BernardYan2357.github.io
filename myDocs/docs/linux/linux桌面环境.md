# Linux桌面环境

桌面环境（desktop environment）是一组组件，提供常见的图形用户界面（GUI）元素，大多数桌面环境都有集成的应用程序和工具，使得操作系统风格统一。没有桌面环境，你的Linux系统就只有一个终端式的工具，你只能用命令来操作

## 常见的桌面环境

- GNOME：臃肿，wayland图形协议
- KDE
- XFCE：轻量简洁，占用少，x11图形协议
- Cinnamon
- i3
- sway
- Hyprland
- AwesomeWM
- dwm
- Xmonad
- sexwm

## 桌面环境的安装

### GNOME->XFCE

安装XFCE
```bash
sudo apt update
sudo apt install xfce4 xfce4-goodies lightdm
# 核心组件说明：
# xfwm4：XFCE 窗口管理器，负责窗口管理和主题渲染
# xfce4-panel：任务栏面板，可添加应用启动器、系统托盘等插件
# xfce4-settings：系统设置中心（外观、显示、电源管理等）
# xfce4-goodies：拓展工具集
# 在弹出的界面中选择 lightdm 作为默认显示管理器，如果没有弹出界面，可以使用以下命令手动设置：
sudo dpkg-reconfigure lightdm
# 重启，在登录界面选择 XFCE4 会话
```

配置 NoMachine 使用 xfce 作为默认桌面环境
```bash
echo "exec startxfce4" > ~/.xsession
chmod +x ~/.xsession
# 重启远程服务
sudo /usr/NX/bin/nxserver --restart
```

重启，选择XFCE会话，再次连接 NoMachine，确认能够连接后，卸载GNOME
```bash
sudo apt purge ubuntu-desktop gnome-shell gnome-session gdm3 # 卸载 gnome 桌面环境
sudo apt purge gnome-terminal nautilus gnome-control-center gnome-software # 卸载 gnome 相关组件
sudo apt autoremove --purge
```

在XFCE桌面环境下，todesk可能会报错，无法打开文件管理器，无法访问todesk的配置文件，导致todesk无法正常使用：
```bash
open Todesk_Printer failed!!! 
mkdir: cannot create directory ‘/tmp/fuse’: File exists
sh: 1: nautilus: not found
```

解决方法
```bash
sudo ln -s /usr/bin/thunar /usr/bin/nautilus # 创建符号链接，将nautilus指向thunar
rm -rf ~/tmp/fuse # 删除/tmp/fuse目录
rm -rf ~/.local/share/todesk/ # 删除todesk的配置文件
sudo apt install libcanberra-gtk-module libcanberra-gtk3-module # 安装缺失的依赖库
sudo systemctl restart todeskd.service # 重启todesk服务
```

删除 xfce 锁屏组件，防止远程连接时自动锁屏
```bash
sudo apt purge xfce4-screensaver light-locker 
sudo gpasswd -a sunrise shadow # 将当前用户添加到 shadow 组
sudo nano /etc/lightdm/lightdm.conf
# 添加以下行，禁用屏幕保护和自动锁屏
[Seat:*]
autologin-user=sunrise
autologin-user-timeout=0
```

### GNOME

安装 Ubuntu Desktop，也是 GNOME 桌面环境：
```bash
sudo apt update
sudo apt install ubuntu-desktop gdm3
# 在弹出的界面中选择 gdm3 作为默认显示管理器，如果没有弹出界面，可以使用以下命令手动设置：
sudo dpkg-reconfigure gdm3
# 重启，在登录界面选择 Ubuntu 会话
```

禁用自动锁屏与屏幕保护：
```bash
# 禁用屏保
gsettings set org.gnome.desktop.screensaver idle-activation-enabled false
# 禁用自动锁屏
gsettings set org.gnome.desktop.screensaver lock-enabled false
# 保持屏幕常亮
gsettings set org.gnome.desktop.session idle-delay 0
# 禁用GNOME会话锁定
nano /etc/gdm3/custom.conf
# 取消注释并设置为 false
AutomaticLoginEnable=false
```

## 问题

### NoMachine 连接一小段时间后锁屏

1. 禁用自动锁屏与屏幕保护（见上文）
2. 编辑`/etc/NX/node.conf`，添加或修改：
  ```bash
  SessionLogLevel 1
  EnableUnixSharedMemory 0
  ```

### NoMachine 连接后显示黑屏/灰屏

