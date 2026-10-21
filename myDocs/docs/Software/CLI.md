# CLI

CLI 是 Command Line Interface 的缩写，指的是通过命令行界面与计算机进行交互的方式

## Terminal 和 Shell 的区别

[控制台（Console），终端（Terminal）和Shell之间的区别究竟是什么？](https://zhuanlan.zhihu.com/p/405527391)

- 单词 **Terminal** 来源于 terminate，用于表示通信过程的“终端”，TTY（即 teletypewriter，电传打字机）是最早出现的终端。软件意义上的终端和 TTY 一样，负责显示命令行，接收输入，把 **Shell** 运行的结果展示出来，本身不执行命令。常见的 Terminal 有 Windows Terminal
- **Shell**，操作系统外壳，区别于操作系统内核。Shell 会接收你通过 **Terminal** 输入的命令并将其"翻译"成操作系统内核可以理解的语言，然后调用相应的应用程序生成输出

## Windows Terminal

Windos操作系统下，使用[Windows Terminal](https://github.com/microsoft/terminal)+[PowerShell 7](https://github.com/PowerShell/PowerShell)是最佳选择

注意：

- Windows Terminal 和 PowerShell 7 都支持跨平台，可以在 Windows、Linux 和 macOS 上使用
- Powershell 7 也不是 Windows Powershell，Windows Powershell对应的可执行文件是 `powershell.exe`，而 PowerShell 7 对应的可执行文件是 `pwsh.exe`，Windows Powershell 不再更新，并会被移除

安装：

```powershell
winget install --id Microsoft.WindowsTerminal -e
winget install --id Microsoft.PowerShell -e
```

### 快捷键

| 快捷键 | 功能 |
| --- | --- |
| Ctrl + Shift + 数字 | 打开对应数字的终端配置 |
| Ctrl + Shift + T | 打开新的标签页 |
| Ctrl + Shift + W | 关闭当前标签页 |
| Ctrl + Shift + P | 打开命令面板 |
| Alt + Shift + - | 水平分屏 |
| Alt + Shift + + | 垂直分屏 |
| Ctrl + , | 打开设置界面 |

### profile

PowerShell 的 profile 就是每次启动 Shell 时自动执行的脚本，相当于 `.bashrc` / `.zshrc`。它不是只有一份，而是按 **作用范围（用户 / 所有用户）× 主机（所有宿主 / 当前宿主）** 分成 4 个，对应的变量和路径为：

| 变量                                | 路径                                                        | 说明               |
| --------------------------------- | --------------------------------------------------------- | ---------------- |
| `$PROFILE.AllUsersAllHosts`       | `<pwsh_install_path>\7\profile.ps1`                       | 所有用户、所有宿主        |
| `$PROFILE.AllUsersCurrentHost`    | `<pwsh_install_path>\7\Microsoft.PowerShell_profile.ps1`  | 所有用户、仅当前宿主（pwsh） |
| `$PROFILE.CurrentUserAllHosts`    | `~\Documents\PowerShell\profile.ps1`                      | 当前用户、所有宿主        |
| `$PROFILE.CurrentUserCurrentHost` | `~\Documents\PowerShell\Microsoft.PowerShell_profile.ps1` | 当前用户、仅当前宿主（pwsh） |

如果安装 pwsh 时只为当前用户安装，那么只有 `CurrentUser*` 的两个文件是实际存在并被加载的。`$PROFILE` 本身指向最后一个，即 `Microsoft.PowerShell_profile.ps1`。启动时 PowerShell 会依次执行这 4 个文件（存在的才执行）

## Linux

[The 7 CLI tools I can't live without](https://www.youtube.com/watch?v=8HXQ12ff0_s)

### [WezTerm](https://github.com/wez/wezterm)

WezTerm 是一个开源的终端模拟器

### [fish_shell](https://github.com/fish-shell/fish-shell)

提供代码补全、语法高亮、自动提示等功能

### NeoVim

### LazyGit

### Tmux

Tmux 是一个终端 multiplexer，它可以将多个终端会话 multiplex 到单个窗口中，并允许在多个窗口之间进行切换

## CLI 美化

### Oh My Posh

[Oh My Posh](https://ohmyposh.dev/docs/) 把原来的 `C:\Users\You>` 提示符，变成带图标、颜色、Git 状态、路径、权限的智能状态栏

下载 Oh My Posh 与字体：

```powershell
winget install JanDeDobbeleer.OhMyPosh -s winget
winget upgrade JanDeDobbeleer.OhMyPosh --source winget # 更新
oh-my-posh font install meslo # 安装字体
```

配置终端使用 MesloLGM Nerd Font 字体，`Ctrl + Shift +` , 打开`settings.json`文件：

```json
{
    "profiles":
    {
        "defaults":
        {
            "font":
            {
                "face": "MesloLGM Nerd Font"
            }
        }
    }
}
```

配置终端使用 Oh My Posh：

```powershell
New-Item -Path $PROFILE -Type File -Force # 创建 PowerShell 配置文件
nano $PROFILE # 编辑 PowerShell 配置文件
<<<
oh-my-posh init pwsh | Invoke-Expression # pwsh 为终端配置名，如果是 bash 就改成 bash
if ($PWD.Path -eq "C:\Windows\System32") {
    Set-Location ~
} # 此举是因为设置完主题后在windows terminal中打开新终端后路径是System32，添加这个命令可以让它回到主目录
>>>
. $PROFILE # 使配置生效
```

额外的图标库配置：

```powershell
Install-Module -Name Terminal-Icons -Repository PSGallery
nano $PROFILE
<<<
Import-Module Terminal-Icons
>>>
. $PROFILE
ls # 现在就可以看到文件夹和文件的图标
```

#### VSCode 与 WSL 终端配置

在 VSCode 按 `Ctrl+Shift+P`，选择 Preferences: Open User Settings (JSON)，添加：

```json
"terminal.integrated.fontFamily": "MesloLGM Nerd Font Mono"
```

#### 主题与自定义

更换主题，在[Themes](https://ohmyposh.dev/docs/themes)或`C:\Program Files\WindowsApps\ohmyposh.cli_29.10.0.0_x64__96v55e8n804z4\themes`查看主题列表，选择喜欢的主题，复制主题名称，在 PowerShell 配置文件中添加以下内容：

```powershell
nano $PROFILE
<<<
oh-my-posh init pwsh --config '1_shell' | Invoke-Expression # 以1_shell主题为例
>>>
. $PROFILE
```

- `oh-my-posh init pwsh --config` 后面可以跟：
  - 主题名称，如 `'1_shell'`
  - 主题文件路径，如 `'C:\Users\You\my_theme.omp.json'`
  - URL，如 `'https://raw.githubusercontent.com/JanDeDobbeleer/oh-my-posh/main/themes/jandedobbeleer.omp.json'`，虽然有缓存，但是不建议

自定义主题，参考：[Customize](https://ohmyposh.dev/docs/installation/customize)与[General Configuration](https://ohmyposh.dev/docs/configuration/general)

导出当前的主题配置：

```powershell
oh-my-posh config export --config '1_shell' --output ~/.mytheme.omp.json
```

#### 常用命令

```powershell
oh-my-posh get shell # 获取当前使用的 Shell
```

#### BUG！

```powershell
Line |
   1 |  oh-my-posh init pwsh --config 'C:\Users\ASUS\OneDrive\Backup\software …
     |  ~~~~~~~~~~
     | The term 'oh-my-posh' is not recognized as a name of a cmdlet, function, script file, or executable program.
     | Check the spelling of the name, or if a path was included, verify that the path is correct and try again.
```

相似的 issue：[Issue #558 · JanDeDobbeleer/oh-my-posh](https://github.com/JanDeDobbeleer/oh-my-posh/issues/558)

原因：oh-my-posh 通过执行别名 oh-my-posh.exe（WindowsApps目录下） 提供 oh-my-posh 命令，用户 PATH 里缺少 `%LOCALAPPDATA%\Microsoft\WindowsApps` 这个目录，所以 PowerShell 加载 `oh-my-posh init pwsh ...` 时,找不到 oh-my-posh 命令 → 报 "not recognized"