# Anaconda使用

## conda包管理器

`conda`是Anaconda的包管理器，用于安装、更新和管理Python包和环境。它可以处理Python包以及其他语言的包

相比于`pip`，`conda`具有以下优势：

- 可以管理Python包和其他语言的包（如R、Ruby等）
- 可以创建和管理虚拟环境，隔离不同项目的依赖
- 可以处理包的依赖关系，自动安装所需的依赖包

### conda命令

终端初始化：

```bash
conda init # 初始化conda
# 执行该命令后会修改shell配置文件（如.bashrc、profile.ps1等），使得新终端默认进入base环境
# 如果要取消自动进入base环境，可以执行以下命令：
conda config --set auto_activate_base false
```

```bash
conda create -n env_name python=3.9  # 创建新环境
conda env create --file # 需指定环境配置文件environment.yml
conda activate env_name              # 激活环境
conda rename -n old_env_name new_env_name # 重命名环境
conda deactivate                    # 退出当前环境
conda install package_name          # 安装包
conda update package_name           # 更新包
conda remove package_name           # 删除包
conda list                          # 列出已安装的包
conda list > requirements.txt  # 导出已安装包到文件
conda search package_name           # 搜索包
conda env list                     # 列出所有环境
conda env remove -n env_name        # 删除环境
conda clean --all                   # 清理缓存
```

## Channel是什么？

Channel是Anaconda的包源，类似于Linux的apt源。Anaconda默认使用的是`https://repo.anaconda.com/pkgs/main`

使用命令`conda config --show channels`可以查看当前的Channel列表。
> channel的优先级是从上到下的，优先使用列表中的第一个Channel。
> 通过再次执行add命令添加Channel，使得新的Channel被添加到列表的顶部。

```bash
channels:
  - defaults #官方channel
  - conda-forge #开源社区channel
```

增加和删除Channel可以使用以下命令：

```bash
conda config --add channels CHANNEL #添加Channel
conda tos accept --override-channels --channel CHANNEL #接受Channel的使用条款
conda config --remove channels CHANNEL #删除Channel
```

`--override-channels`选项用于覆盖当前的Channel设置

在下载包时选择Channel

```bash
conda install PACKAGE_NAME -c CHANNEL_NAME
```

创建环境时报错：

```bash
(base) PS C:\Users\ASUS> conda create -n pytorch_env python=3.9 -y

CondaToSNonInteractiveError: Terms of Service have not been accepted for the following >channels. Please accept or remove them before proceeding:
• https://repo.anaconda.com/pkgs/r
• https://repo.anaconda.com/pkgs/msys2
```

如果按提示允许或拒绝，anaconda只会抛出另一个报错：`CondaKeyError: 'channels': value 'https://repo.anaconda.com/pkgs/r' not present in config`

> 这就有点烦了对吧——你已经尝试移除这些 channel，但系统还是提示你没有接受它们的条款

解决方法是在创建环境时指定channel

```bash
conda create -n pytorch_env python=3.9 -y --override-channels -c conda-forge
```

在安装包时也指定channel

```bash
conda install pytorch torchvision torchaudio pytorch-cuda=11.8 \
  --override-channels \
  -c pytorch -c nvidia -c conda-forge
```

也可以选择接受

```bash
conda config --add channels https://repo.anaconda.com/pkgs/r
conda config --add channels https://repo.anaconda.com/pkgs/msys2
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/msys2
```
