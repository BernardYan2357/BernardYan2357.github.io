# Windows体验优化指北

## 功能增强

使用PowerToys增强Windows功能：
[PowerToys 官方文档](https://learn.microsoft.com/zh-cn/windows/powertoys/)

提供一系列实用工具来提升Windows的使用体验

## 卸载程序优化

在电脑上运行软件安装包时，安装程序会生成一些程序文件、后台服务和注册表项等，用以支持软件的正常运行。但是，在卸载软件时，一些软件的卸载程序卸载不干净，甚至不提供卸载程序
可能会导致：

- 卸载不彻底，残留文件和注册表项
- 系统垃圾文件增多，影响性能
- 可能导致软件无法重新安装或出现冲突

使用控制面板中的卸载程序可以解决大部分程序的卸载，然而若要更干净彻底地卸载程序，可以采用:

**Geek Uninstaller** 官网地址：[Geek Uninstaller - 下载](https://geekuninstaller.com/download)

> 谨慎使用Geek Uninstaller，存在过度清理注册表的风险，建议使用前备份注册表或创建系统还原点

系统还原点创建方法：

1. 在搜索栏中输入“创建还原点”，打开系统属性窗口
2. 在“系统保护”选项卡中，选择要创建还原点的驱动器（通常是C盘），创建还原点
3. 创建完成后点击“关闭”按钮，完成还原点创建
4. 在需要恢复时，打开“系统属性”窗口，点击“系统还原”，选择之前创建的还原点进行恢复

## 在默认打开方式设置中去掉已失效/已删除的应用选项

> 可以先下载一个Registry Workshop，查找更方便

打开注册表编辑器，定位到以下路径：
`HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\FileExts\(后缀名)`

- 删除`UserChoice`项下的`Progid`字符串值或者填上你想要的默认程序的ProgID值（可以在`HKEY_CLASSES_ROOT`中找到对应程序的ProgID值）
- 删除`OpenWithList`项下的对应程序的字符串值

## 界面美化

- **[WindHawk](https://windhawk.net/)**，Windows 的通用脚本化界面增强工具，可直接在Microsoft Store下载
- **[TranslucentTB](https://translucenttb.github.io/)**，一个轻量级实用程序，使 Windows 任务栏半透明/透明
- **[NileSoft](https://nilesoft.org)**，管理右键菜单的工具，可以自定义右键菜单的样式和功能，配置修改方式: [文档](https://nilesoft.org/docs)

## 更新推迟

`win+R`呼出运行窗口，输入`regedit`打开注册表，注册表目录：`HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\Update\UX\Settings`。在该目录下右键创建新的DWORD(32位)值，名称为`FlightSettingsMaxPauseDays`，数值为`20000`

关闭，再打开windows更新页面，选择推迟日期

> 2025/8/19更新：该注册表项找不到了，可能被微软删了🤬
> 
> 不慌，直接命令行添加注册表项：
> 
> `reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\WindowsUpdate\UX\Settings" /v FlightSettingsMaxPauseDays /t reg_dword /d 10000 /f`

## 软件推荐

- **[Geek Uninstaller](https://geekuninstaller.com/)**：一款强大的卸载工具，可以彻底清除软件残留文件和注册表项
- **[Everything](https://www.voidtools.com/)**：快速文件搜索工具，几乎瞬间找到所需文件
- **[MPC-HC](https://mpc-hc.org/)**：轻量级媒体播放器，支持多种格式和字幕
- **[7-Zip](https://www.7-zip.org/)**：免费开源的压缩软件，支持多种格式和高压缩率
- **[InputTip](https://inputtip.abgox.com/zh-CN/)**：一个输入法状态管理工具。支持实时提示，窗口自动切换，按键快捷切换。基于 AutoHotkey 开发，仅支持 Windows 系统
- **[freefilesync](https://freefilesync.org/)**：一款免费的文件同步工具，支持多平台和多种同步方式
- **[Registry Workshop](https://www.torchsoft.com/en/rw_information.html)**：一款注册表编辑工具，提供更友好的界面和功能
- **[ASCII Art Studio](https://www.torchsoft.com/en/aas_information.html)**：一款ASCII艺术创作工具，支持多种字体和效果
- **[sandboxie](https://github.com/sandboxie-plus/Sandboxie/releasesm/)**：一款沙箱软件

## 软件避雷

- **EasyConnect**：纯纯流氓软件，卸载了还是偷偷在后台运行。由于软硬件配套，你还只能用它，但是可以用docker容器替代它：[docker-easyconnect](https://github.com/Hagb/docker-easyconnect)