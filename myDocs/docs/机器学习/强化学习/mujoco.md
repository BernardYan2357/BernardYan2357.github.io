# mujoco

## [mujoco_ros2_control](https://github.com/ros-controls/mujoco_ros2_control)

mujoco_ros2_control provides a ROS 2 control hardware interface for the MuJoCo physics simulator, including plugins for various sensors, RGB-D cameras, and lidar

mujoco_ros2_control包含以下组件：

- mujoco_ros2_control - 核心插件，提供ROS2 Control的接口实现
- mujoco_ros2_control_msgs - 定义了ROS2 Control接口使用的消息类型
- mujoco_ros2_control_demos - 一些使用mujoco_ros2_control的示例，包括一个简单的差速机器人和一个机械臂
- mujoco_ros2_control_tests - 测试文件
- docker/ - Dockerfile和脚本，用于运行CI/容器

### Installation

参考官方文档安装即可，依赖的安装参考[[ROS2环境管理#rosdep]]

[google-deepmind/mujoco_menagerie: A collection of high-quality models for the MuJoCo physics engine, curated by Google DeepMind.](https://github.com/google-deepmind/mujoco_menagerie)