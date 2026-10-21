# Windows优化指南

## 创建系统还原点

在优化系统之前，你应该掌握创建系统还原点的方法🤗

1. 在搜索栏中输入“创建还原点”，打开系统属性窗口
2. 在“系统保护”选项卡中，选择要创建还原点的驱动器（通常是C盘），创建还原点
3. 创建完成后点击“关闭”按钮，完成还原点创建
4. 在需要恢复时，打开“系统属性”窗口，点击“系统还原”，选择之前创建的还原点进行恢复

## 磁盘空间清理

使用WizTree分析磁盘空间，查找一些大文件：

- hiberfil.sys：用于系统休眠的大文件，一般有十几个G左右，管理员运行 `powercfg.exe /hibernate off` 关闭休眠功能，释放hiberfil.sys占用的磁盘空间

使用系统自带的`磁盘清理`工具：
![[磁盘清理目录.png]]

## 推迟系统更新

- `win+R`呼出运行窗口，输入`regedit`打开注册表，找到注册表目录：`HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\Update\UX\Settings`
- 在该目录下右键创建新的DWORD(32位)值，名称为`FlightSettingsMaxPauseDays`，数值为`20000`
- 关闭，再打开windows更新页面，选择推迟日期

2025/8/19更新：该注册表项找不到了，可能被微软删了😅。不慌，直接命令行添加注册表项：

```powerShell
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\WindowsUpdate\UX\Settings" /v FlightSettingsMaxPauseDays /t reg_dword /d 10000 /f
```

## 界面美化

- **[WindHawk](https://windhawk.net/)**，Windows 的通用脚本化界面增强工具，可直接在Microsoft Store下载
- **[TranslucentTB](https://translucenttb.github.io/)**，一个轻量级实用程序，使 Windows 任务栏半透明/透明
- **[NileSoft](https://nilesoft.org)**，管理右键菜单的工具，可以自定义右键菜单的样式和功能，配置修改方式: [文档](https://nilesoft.org/docs)

## CLI美化

[[CLI#CLI 美化]]

## 软件推荐

系统管理工具：

- **[CPU-Z](https://www.cpuid.com/softwares/cpu-z.html)**：系统信息检测工具，可以查看CPU、主板、内存等硬件信息
- [WizTree](https://wiztree.en.lo4d.com/windows) ：磁盘空间分析工具，可以快速扫描磁盘并将文件和文件夹的大小图形化显示，帮助用户清理磁盘空间
- **[Mem Reduct](https://github.com/henrypp/memreduct)**：极低占用的内存清理工具，支持自动清理
- **[Registry Workshop](https://www.torchsoft.com/en/rw_information.html)**：一款注册表编辑工具，提供更友好的界面和功能

系统功能增强：

- **[PowerToys 官方文档](https://learn.microsoft.com/zh-cn/windows/powertoys/)**：微软官方提供的Windows增强工具，包含多种实用工具
- **[Geek Uninstaller](https://geekuninstaller.com/)**：一款强大的卸载工具，可以彻底清除软件残留文件和注册表项
- **[File Converter](https://github.com/Tichau/FileConverter)**：一款免费的文件转换工具
- **[Everything 1.5](https://www.voidtools.com/everything-1.5/)**：快速文件搜索工具
- **[7-Zip](https://www.7-zip.org/)**：压缩软件
- **[InputTip](https://inputtip.abgox.com/zh-CN/)**：一个输入法状态管理工具

实用工具：

- **[ASCII Art Studio](https://www.torchsoft.com/en/aas_information.html)**：一款ASCII艺术创作工具，支持多种字体和效果
- **[sandboxie](https://github.com/sandboxie-plus/Sandboxie/releasesm/)**：一款沙箱软件
- **[MPC-HC](https://mpc-hc.org/)**：轻量级媒体播放器，支持多种格式和字幕
- **[freefilesync](https://freefilesync.org/)**：一款免费的文件同步工具，支持多平台和多种同步方式