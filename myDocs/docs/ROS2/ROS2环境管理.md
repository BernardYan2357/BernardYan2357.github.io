# ROS2环境管理

## ROS2 Setup

设置系统Locale，确保系统支持UTF-8编码

```bash
sudo apt update && sudo apt install locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8
locale # 检查当前locale设置
```

使用脚本安装

```bash
sudo apt install python3-colcon-common-extensions # 安装colcon构建工具
wget http://fishros.com/install -O fishros && . fishros
```

安装完成后，测试

```bash
# 终端1：启动C++发布者节点
ros2 run demo_nodes_cpp talker
# 终端2：启动Python订阅者节点
ros2 run demo_nodes_py listener
# 小海龟仿真示例
ros2 run turtlesim turtlesim_node
ros2 run turtlesim turtle_teleop_key
```

## rosdep

rosdep 是 ROS 的依赖安装工具。它会读取你工作空间里的 package.xml 等信息，帮你查出这个 ROS 工程缺哪些系统依赖，然后自动用 apt 等方式安装

安装：

```bash
sudo apt install python3-rosdep
sudo rosdep init
```

使用：

```bash
rosdep update # 更新 rosdep 数据库
cd ~/ros2_ws
rosdep install --from-paths src --ignore-src -r -y
```

- --from-paths src：指定要解析的源码路径
- --ignore-src：跳过前面指定的路径里已存在的源码包，只安装它们的系统依赖。如果你有别处源码包，要把路径也放进 --from-paths，例如：`rosdep install --from-paths src ~/moveit2/src --ignore-src -r -y`
- -r：继续处理后续依赖，即使某些依赖失败

### rosdepc

在国内使用 rosdep 可能会遇到网络问题，建议使用 rosdepc，安装：

```bash
wget http://fishros.com/install -O fishros && . fishros # 选3安装rosdepc
# 或者
sudo pip install rosdepc
sudo rosdepc init
```

除了要把命令改成`rosdepc`，其他用法和 rosdep 一样
