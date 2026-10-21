# ROS2

## ROS2与ROS区别

![ros_vs_ros2](ros_vs_ros2.png)

- ROS2全面支持三种平台 Ubuntu，MacOSX，Windows10
- 实现了分布式架构，取消Master中央节点，实现节点的分布式发布/订阅，请求/响应通讯
- 使用新版本的编程语言：C++11，Python3.5+
- 使用了新的编译系统 Ament（ROS为Catkin），ROS1的编译命令是`catkin_make`，而ROS2的编译命令使用`colcon build`命令

## 功能包与工作空间

### 工作空间

工作空间是ROS2中存放功能包的目录结构。工作空间可以包含多个功能包，每个功能包可以包含多个节点

```bash
mkdir ~/ros2_ws # 新建ROS2工作空间
cd ~/ros2_ws
colcon build # 编译工作空间，初始化
source install/setup.bash # source 工作空间
nano ~/.bashrc # 编辑 .bashrc 文件
# source ~/ros2_ws/install/setup.bash
```

删除工作空间

```bash
rm -rf ~/ros2_ws
nano ~/.bashrc # 在.bashrc文件中删除 source 语句
```

### 功能包

#### 功能包安装

1. 安装二进制包，自动放置到系统目录，不用手动 source

   ```bash
    sudo apt install ros-<version>-package_name
   ```

2. 手动编译功能包，编译后需要手动source工作空间的install目录

#### 编译功能包

在工作空间目录下使用命令`colcon build`来编译工作空间下的所有功能包,产生三个目录：

```bash
.
├── build #存储中间文件
├── install #每个软件包将安装到的位置，默认情况下，每个包都将安装到单独的子目录中
├── log #存储编译日志
└── src #存放功能包源代码
```

Colcon的常用命令

```bash
colcon build #编译工作空间下的所有功能包
colcon build --symlink-install #使用符号链接而不是复制文件来安装功能包，这样在开发过程中修改源代码后，无需重新编译即可生效
colcon build --packages-select YOUR_PKG_NAME #编译指定的功能包
colcon build --cmake-args -DCMAKE_BUILD_TYPE=Release #以Release模式编译
colcon list #列出工作空间下的所有功能包
```

#### 功能包相关指令

```bash
ros2 pkg create <package-name>  --build-type  {cmake,ament_cmake,ament_python}  --dependencies <依赖名> #创建功能包，要在src目录下执行
ros2 pkg executables <package-name> #列出功能包的所有可执行文件
ros2 pkg list #列出所有的包
ros2 pkg prefix  <package-name> #输出某个包所在路径的前缀
ros2 pkg xml <package-name> #列出包的清单描述文件
```

#### 删除功能包

```bash
rm -rf src/<package-name> #删除功能包
rm -rf build/<package-name> install/<package-name> log
colcon build #重新编译工作空间
```
