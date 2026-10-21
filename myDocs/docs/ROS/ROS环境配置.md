# 安装ROS

```bash
wget http://fishros.com/install -O fishros && . fishros
# 测试安装是否成功
source /opt/ros/noetic/setup.bash
roscore
```

# ROS&ROS2共存方法

- Ubuntu版本: 22.04
- ROS版本: Noetic
- ROS2版本: Humble

下面记录安装方法：

ROS2 Humble安装不用赘述

ROS Noetic只支持到Ubuntu 20.04，要在Ubuntu 22.04安装Noetic，需要自己编译，解决数量众多的库依赖和 C++ 版本兼容问题

## 使用非官方包安装ROS

Autolabor官方编译的一个ros noetic安装包，经测试可用

> 需要注意的是：此版本将无法使用他人编写的ROS包，因为在从源码编译时会报错

```bash
echo "deb [trusted=yes arch=amd64] http://deb.repo.autolabor.com.cn jammy main" | sudo tee /etc/apt/sources.list.d/autolabor.list
sudo apt update
sudo apt install ros-noetic-autolabor
```

当出现`ros-noetic-autolabor installed`的字样，意味着安装已经完成

## 环境变量配置

`gedit ~/.bashrc`

```bash
echo "ros:humble(1) noetic(2) ?"
read choose
case $choose in
1) source /opt/ros/humble/setup.bash
   source ~/ros2_ws/install/setup.bash
   ;;
2) source /opt/ros/noetic/setup.bash
   source ~/catkin_ws/devel/setup.bash
   ;;
esac
```

# 使用VScode开发ROS

## 在Ubuntu下使用VSCode开发ROS

安装VSCode后，安装以下插件：
- C/C++ (ms-vscode.cpptools)
- Python (ms-python.python)
- Catkin Tools (ms-iot.catkin-tools)
- Robot Developer Extension for ROS 1
- Robot Developer Extension for ROS 2
> 不要安装ROS插件，已经失效

新建工作空间和src，然后catkin_make编译

在该目录下CLI输入code . 打开VSCode

打开终端，选择ROS版本

输入#include "ros/ros.h"测试

### 创建ROS包

右键src文件夹，选择`create catkin package`，输入包名和依赖，即可创建包

`crtl+shift+b`编译

## 使用VSCode远程连接至虚拟机开发ROS

远程连接即可

启动QT程序的命令可能无法使用