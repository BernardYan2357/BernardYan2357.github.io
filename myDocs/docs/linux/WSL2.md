# WSL2

## WSL相关命令

发行版管理相关：
- `wsl --list --online` 列出可用发行版
- `wsl --install -d <发行版名称>` 安装指定发行版
- `wsl --unregister <发行版名称>` 卸载指定发行版
- `wsl --list --verbose` 查看已安装的发行版
- `wsl --set-default-version 2` 设置默认启动版本
- `wsl -d <发行版名称>` 进入指定发行版

- `wsl --shutdown` 关闭WSL2实例，相当于关机，可用于重启WSL2
- `wsl` 启动默认发行版

## WSL+WSLg

WSLg是WSL的一个扩展，允许在WSL2中运行Linux GUI应用程序

声明环境变量从而使用NVIDIA显卡进行渲染

```bash
export MESA_D3D12_DEFAULT_ADAPTER_NAME=NVIDIA
glxinfo | grep "renderer string" # 查看渲染器信息
```

可以使用的Linux GUI应用程序包括：

- Gedit：文本编辑器
    - Gnome Terminal：终端模拟器
- GIMP：图像编辑器
- Nautilus：文件管理器
- VLC：VLC媒体播放器
- X11 apps：X11应用程序
- Google Chrome

使用apt安装即可

## VSCode 连接 WSL2

使用VSCode远程连接至WSL，需确保本机跟WSL在同一个网络下，也就是能ping通，可以通过WSL setting设置

点击VSCode左下角图标，选择“连接到WSL”，即可连接到WSL2

## 双系统文件访问

- 访问 Windows 文件：
  - `cd /mnt/c`
  - `mnt` 文件夹是挂载点，在 WSL2 中这里挂载了 C 盘
- 访问 WSL2 文件：
  - 直接用资源管理器查看

## 网络配置

网络模式：
- None: 无网络连接
- NAT
- Mirrored
- VirtioProxy

## 配置代理

- Mirriored模式下，只需打开 WSL Setting，找到`已启用自动代理`选项，打开，重启后WSL就能够使用Windows的HTTP代理信息，再开启VPN全局模式