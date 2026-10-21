# linux软件包

## 软件包管理器

不同的Linux发行版使用不同的软件包管理器，常见的有：

- **APT（Advanced Package Tool）**：主要用于Debian及其衍生版（如Ubuntu）。使用`.deb`格式的软件包。
  - 常用命令：
    - `sudo apt update`：更新软件包列表
    - `sudo apt upgrade`：升级已安装的软件包
    - `sudo apt install <package>`：安装软件包
    - `sudo apt-get install <package>`：安装软件包，`apt-get` 是传统、底层的 APT 工具，输出简洁，适合脚本
    - `sudo apt remove <package>`：删除软件包
- **YUM（Yellowdog Updater, Modified）**：主要用于Red Hat及其衍生版（如CentOS）。使用`.rpm`格式的软件包。
  - 常用命令：
    - `sudo yum check-update`：检查可用更新
    - `sudo yum update`：升级已安装的软件包
    - `sudo yum install <package>`：安装软件包
    - `sudo yum remove <package>`：删除软件包

### APT 软件源

#### PPA

PPA 是 Ubuntu 特有的个人软件包存档，适合添加单个软件

```bash
sudo add-apt-repository ppa:用户/仓库名
sudo apt update
```

## linux源码包

源码包通常以`.tar.gz`或`.tar.bz2`等格式分发，包含了软件的源代码。需要手动编译和安装

## linux二进制包

二进制包，也就是源码包经过成功编译之后产生的包

目前主要有以下 2 大主流的二进制包管理系统：

- RPM 包管理系统：很多 Linux 发行版都默认使用此机制作为软件安装的管理方式，例如 Fedora、CentOS、SuSE 等。其对应的包文件格式为 `.rpm`
- DPKG 包管理系统：由 Debian Linux 所开发的包管理机制，主要应用在 Debian 和 Ubuntu 中。其对应的包文件格式为 `.deb`

### RPM包

#### RPM包统一命名规则

`包名-版本号-发布次数-发行商-Linux平台-适合的硬件平台-包扩展名`

适合的硬件平台：

- i386 Intel 80386 架构（第三代 x86，32位）
- i586 Intel Pentium 架构（第五代 x86）
- i686 Intel Pentium Pro 及以上（第六代 x86）
- x86_64 也称amd64，是AMD芯片架构
- noarch 没有硬件限制

#### RPM包安装

```bash
sudo rpm -ivh <包全名，如终端不在包目录下，要写路径>
# -i：安装
# -v：显示安装过程
# -h：显示安装进度
# 还可以一次性安装多个软件包
sudo rpm -ivh package1.rpm package2.rpm package3.rpm
```

#### RPM包升级

```bash
sudo rpm -Uvh package.rpm
# -U：如果该软件没安装过则直接安装；若已经安装则升级至最新版本
sudo rpm -Fvh package.rpm
# -F：如果该软件没安装过则不做任何操作；若已经安装则升级至最新版本
```

#### RPM包卸载

RPM 软件包的卸载要考虑包之间的依赖性。例如，我们先安装的 httpd 软件包，后安装 httpd 的功能模块 mod_ssl 包，那么在卸载时，就必须先卸载 mod_ssl，然后卸载 httpd，否则会报错。

```bash
sudo rpm -e package.rpm
# -e：卸载
```

#### 查询RPM包

```bash
rpm -q package.rpm
# -q：查询某个软件包是否安装
rpm -qa
# -qa：查询所有已安装的软件包
rpm -qi package.rpm
# -qi：查询某个软件包的详细信息
rpm -ql package.rpm
# -ql：查询某个软件包安装了哪些文件
rpm -qf package.rpm
# -qf：查询某个文件属于哪个软件包
rpm -qR package.rpm
# -qR：查询某个软件包的依赖关系
```

### DEB包

deb 是 Unix 系统(其实主要是 Linux)下的安装包，基于 tar 包

#### DEB包的组成

deb 包本身有三部分组成：数据包，包含实际安装的程序数据，文件名为 data.tar.XXX；安装信息及控制脚本包，包含 deb 的安装说明，标识，脚本等，文件名为 control.tar.gz

#### DEB包安装

```bash
sudo dpkg -i /path/to/package.deb # 使用dpkg安装deb包
sudo apt-get install -f # 修复依赖关系
sudo apt install /path/to/package.deb # 使用apt安装deb包，可以自动处理依赖关系
```

#### DEB包升级

当需要更新已经安装的 deb 包时，可以下载新版本的 deb 包，然后重复上述的安装过程。系统会自动处理包的更新。

#### DEB包卸载

```bash
sudo dpkg -r package_name # 卸载软件包
sudo apt remove example_package # 使用apt卸载软件包
```

#### 查询DEB包

```bash
dpkg -l | grep <关键字> # 列出所有已安装的包，并通过关键字过滤
```
