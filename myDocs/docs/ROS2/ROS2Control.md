# ROS2 Control

References:

- [ROS2 Control Documentation](https://control.ros.org/humble/doc/ros2_control/doc/index.html)
- [ROS2 Control Wiki | ZRead.AI](https://zread.ai/ros-controls/ros2_control)
- [ROS2 Control 视频教程 | Edouard](https://www.udemy.com/course/ros2_control/)
- [ros2_control 视频教程 | WMGIII](https://www.bilibili.com/video/BV1ku411G7UR)

## Why ROS2 Control?

要控制硬件（电机，传感器等），我们第一时间想到的方法是使用一个节点与硬件通信，再通过 Topic/Service/Action 等方式让其它节点与这个节点通信，来控制硬件的行为。但是这套方法往往只适用于简单的硬件控制，或者说是一些不需要实时性的控制

在实际的机器人控制中，我们对实时性有很高要求（100 Hz），在高速控制中，ROS2 的通信机制会引入较大的延迟，这时我们就需要一个专门的框架来处理这些问题，即 ROS2 Control

```mermaid
flowchart LR
    A[Your ROS 2 App] <-->|Topic/Service/Action| B[ros2_control]
    B <-->|Direct communication| C[Hardware]
```

- High performance
- Lots of modularity
- Can use lots of existing controllers
- Compatibility with stacks such as Nav2 and Moveit2

## Install

```bash
sudo apt install ros-humble-ros2-control ros-humble-ros2-controllers
```

## CLI Tools

```bash
sudo apt install ros-humble-ros2controlcli
ros2 control --help
# 常用命令
list_controller_types         # 列出所有已安装且可用的controller类型
list_controllers              # 列出当前加载的controller，包括它们的状态和类型
list_hardware_components      # 列出当前的硬件组件，就是我们在urdf中定义的ros2_control组件
list_hardware_interfaces      # 列出当前加载的硬件接口，分为command和state两类
view_controller_chains        # 在/tmp目录下生成controller链的pdf文件
# 卸载controller，即将节点状态从active切换到inactive
unload_controller <controller_name>
# 加载controller，即将节点状态从inactive切换到active
load_controller <controller_name>
```

## How ROS2 Control works?

![ROS2 Control Architecture](ros2control_architecture.png)

- **Controller Manager**  
    ROS2 Control 的主组件，负责 ​controllers 的生命周期管理（loads, activates, deactivates, unloads）并执行控制循环 
    在每个周期中，CM 会：
  1. 通过 Resource Manager 的 `read()` 从硬件组件读取最新状态
  2. 调用所有 active controllers 的 `update()` 计算新指令
  3. 通过 Resource Manager 的 `write()` 将指令写入硬件组件
- **Resource Manager**  
    负责抽象物理硬件和底层 driver，也就是 ros2_control 中的 Hardware Components。RM 通过 [[ROS2Pluginlib]] 加载 Hardware Components，管理它们的生命周期，以及它们导出的 command interfaces 和 state interfaces。Controller Manager 基于这些接口完成 controller 与 hardware interface 的匹配、访问授权和冲突检查
- **Hardware Component**  
    物理硬件的抽象模块，以 plugin 的形式实现（继承自 SystemInterface、ActuatorInterface 或 SensorInterface）
    每个 Hardware Component 会注册它能够提供的 Hardware Interfaces（即具体的 command Interface 和 State Interface，如 `wheel_left_joint/velocity`），并实现真正的硬件通信（`read()` / `write()`）

### Why ROS2 Control faster?

ROS2 Control 的 `ControllerManager`、`Controller` 和 `HardwareInterface` 运行在**同一个进程**内。控制指令无需通过 Topic 传递，而是直接读写内存地址。这样绕过了 DDS 通信，减少内存开销和通信抖动，从而实现实时控制
## Setup ROS2 Control

### <bot_name>.ros2_control.xacro

要想将 ros2_control 集成到我们的机器人中，必须在 URDF 中添加一个`<ros2_control>-tag`。这个 tag 用来声明 Resource Manager 将要加载的 hardware components。在实践中，开发者通常会把这段 `<ros2_control>` 标签单独抽取到一个 `<bot_name>.ros2_control.xacro` 文件里，然后在 `<bot_name>.urdf.xacro` 中引用进来（这是为了方便让ros2_control_node从/robot_description话题中读到<ros2_control>）下面是一个两轮差速机器人配置示例：

```xml
<?xml version="1.0"?>
<robot xmlns:xacro="http://www.ros.org/wiki/xacro">
    <ros2_control name="MobileBaseHardwareInterface" type="system"> <!-- name 仅做标识用 -->
        <hardware>
            <plugin>mock_components/GenericSystem</plugin>
            <param name="calculate_dynamics">true</param> <!-- mock plugin 的参数，true 表示在模拟中启用简单的动力学计算 -->
        </hardware>
        <joint name="base_right_wheel_joint">
            <command_interface name="velocity"/>
            <state_interface name="position"/>
            <state_interface name="velocity"/>
        </joint>
        <joint name="base_left_wheel_joint">
            <command_interface name="velocity"/>
            <state_interface name="position"/>
            <state_interface name="velocity"/>
        </joint>
    </ros2_control>
</robot>
```

- `<ros2_control>-tag`：其下标签和参数实际上都对应着[hardware_interface/hardware_info.hpp](https://github.com/ros-controls/ros2_control/blob/master/hardware_interface/include/hardware_interface/hardware_info.hpp)中的结构体参数
  - name：hardware component 的实例名，供 Resource Manager 识别。通常是 `<robot_name>HardwareInterface`
  - type：hardware component 的类型，只能是 system、actuator 或 sensor
    - system：可同时拥有 command interface 和 state interface，通常用于需要同时读写多个关节、传感器和 GPIO 的整体系统
    - actuator：只能有 command_interface，用于单独的执行器
    - sensor：只能有 state_interface，用于纯传感器读数
- `<hardware>-tag`：定义 hardware component 和其参数
  - `<plugin>-tag`：hardware component 注册的插件名，如我们上文所说，Resource Manager 通过插件名加载 hardware component，可以选择现成的插件，也可以自定义插件。这里使用了一个虚拟插件：`mock_components/GenericSystem`
  - `<param>-tag`：传递给插件硬件的自定义参数，键值对形式。例如 `calculate_dynamics` 等，具体含义取决于插件的文档
- `<joint>-tag`：在 URDF 中选取想要控制的关节
	- name：这个 joint 的名称，必须与 URDF 中的 `<joint>` 名称一致
	- `<command_interface>-tag`：每个 `<command_interface>` 的标签名（如 position、velocity、effort）会存入 `InterfaceInfo::name`。可选属性：min、max、initial_value、data_type 等，分别对应 `InterfaceInfo` 的同名字段
	- `<state_interface>`：结构与 `<command_interface>` 类似，但用于声明硬件可读回的状态数据（position、velocity、effort）
	- `<param>-tag`：该关节的额外参数，如减速比、偏移等

可以使用 xacro 中的条件判断标签实现多个 hardware components 的加载：

```xml
    <xacro:property name="use_mock_hw" value="false">
    <xacro:property name="sim_gazebo" value="false">
    <ros2_control name="OpenRoverHardwareInterface" type="system">
        <hardware>
            <xacro:if value="${use_mock_hw}">
                <plugin>mock_components/GenericSystem</plugin>
                <param name="calculate_dynamics">true</param>
            </xacro:if>
            <xacro:if value="${sim_gazebo}">
                <plugin>gazebo_ros2_control/GenericSystem</plugin>
            </xacro:if>
```

### <bot_name>_controllers.yaml

在 ROS2 Control 中，我们需要定义一个`<robot_name>_controllers.yaml`文件来描述 controllers 的信息

首先填写 controller_manager 的配置，我们需要指定 controller_manager 的更新频率并注册 controller：

```yaml
controller_manager:
    ros__parameters:
        update_rate: 50
        joint_state_broadcaster:
            type: joint_state_broadcaster/JointStateBroadcaster
        <controller_name>:
            type: <controller_type>/<ControllerType>
```

- update_rate：controller_manager的更新频率，单位为Hz
- controller_name：controller的名称，可以自定义
- controller_type：controller的类型，在[github ros2_controllers](https://github.com/ros-controls/ros2_controllers)中获取现成的控制器，注意根据当前的ROS2版本选择对应的分支。获取方式：在目录中选择要使用的控制器，点击查看文件夹内的`xxx_plugin.xml`文件，复制class标签的name属性值

然后填写controller的参数，不同的controller有不同的参数，在[github ros2_controllers](https://github.com/ros-controls/ros2_controllers)各控制器目录下的`src/xxx_parameter.yaml`文件中查看参数的名称和默认值，进行修改，下面是一个两轮差速控制器的配置示例：

```yaml
joint_state_broadcaster:
  ros__parameters:
    publish_rate: 50

diff_drive_controller:
  ros__parameters:
    left_wheel_names: ["base_left_wheel_joint"]
    right_wheel_names: ["base_right_wheel_joint"]
    wheel_separation: 0.45
    wheel_radius: 0.1
    odom_frame_id: "odom"
    base_frame_id: "base_footprint"
    linear.x.max_velocity: 1.0
    linear.x.min_velocity: -1.0
    angular.z.max_velocity: 1.0
    angular.z.min_velocity: -1.0
```

### Launch ROS2 Control

通过命令行启动熟悉流程：

```bash
# 启动robot_state_publisher节点，发布/robot_description，需要将robot_description参数设置为<bot_name>.urdf.xacro（里面要包含ros2_control.xacro）的路径
ros2 run robot_state_publisher robot_state_publisher --ros-args -p robot_description:="$(xacro <path_to_urdf_xacro>)"
# 启动controller_manager节点，加载controller
# 注意，ros2_control_node订阅的话题是/controller_manager/robot_description，而不是/robot_description，所以需要重映射一下
ros2 run controller_manager ros2_control_node --ros-args -r /controller_manager/robot_description:=/robot_description --params-file <path_to_controllers_yaml>
# 启动controller_manager的spawner节点，启动controller，有几个controller就启动几个
ros2 run controller_manager spawner <controller_name>
# 启动rviz2节点，查看机器人状态
ros2 run rviz2 rviz2 -d <path_to_rviz_config> # rviz2中应该设置 fixed frame 为 /odom
# 启动teleop节点，控制机器人运动
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r /cmd_vel:=/diff_drive_controller/cmd_vel -p stamped:=true
```

之后便可以按照上述流程编写一个Launch文件来启动整个系统，编写参考 [[ROS2Launch]]

如果发现 rviz 启动后显示 `Frame [odom] doesn't exist`，需要知道 `/odom -> /base_footprint` 的TF是由 controller 发布的，应该查看选择的 controller 是否将TF话题发布到 /tf，例如 mecanum_drive_controller 的 TF 话题就发布到了/mecanum_drive_controller/tf_odometry，需要重映射，重映射应该加在 ros2_control_node 下面，毕竟 controllers 由它统一管理

#### 多 spawner 并发导致的启动竞态

在 launch 文件中我们使用 多个 spawner 分别启动各 controller 容易导致多个 `controller_manager/spawner` 并发调用同一个 `controller_manager`，导致控制器加载和配置出现竞态，从而出现个别 controller 启动失败的问题（这是因为launch文件中各节点并行启动）

解决方法是让一个 spawner 启动所有 controllers，添加 `--activate-as-group` 参数：

```python
def generate_launch_description():
	...
    controller_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=[
            'joint_state_broadcaster',
            'mecanum_drive_controller',
            'arm_controller',
            'gripper_controller',
            '--controller-manager', '/controller_manager',
            '--controller-manager-timeout', '60.0',
            '--service-call-timeout', '10.0',
            '--activate-as-group',
        ],
        output='screen',
    )
    ...
    return LaunchDescription([
		...
	    controller_spawner,
		...
    ])
```

#### Controller 重复加载造成的配置失败

启动 launch 文件时出现报错：

```bash
[spawner-4] [WARN] [1786428829.228647348] [spawner_joint_state_broadcaster]: Controller already loaded, skipping load_controller
[spawner-4] [ERROR] [1786428829.230820209] [spawner_joint_state_broadcaster]: Failed to configure controller
```

这种情况是 Controller 重复加载导致的，为了避免这一情况，应该：

- 保证同一机器人只有一个 controller manager
	对于 Gazebo，它的 `gz_ros2_control` 插件本身就会创建管理器，因此仿真时应使用它提供的管理器，避免再启动 `ros2_control_node`。对于多机器人则配置独立命名空间
- 正确管理退出时的进程和重新加载时的冲突
	- 退出 launch 进程时 spawner 和管理器会同时开始退出；spawner 想调用卸载服务时，管理器可能已经停止响应，导致 spawner 等待或清理失败；同时 Linux 不保证父进程退出时自动终止所有子孙进程，未退出的子进程可能继续运行；此外，错误的退出方式（如直接关闭终端）会导致进程残留
	- 可以使用 spawner 的 `--unload-on-kill` 参数，wait until this application is interrupted and unload controller；终极的解决方案是编写一个管理 launch 文件启动的脚本，退出时跟踪进程树，按 `SIGINT → SIGTERM → SIGKILL` 的顺序清理进程；启动前检查残留进程，并用文件锁阻止重复启动

## Write Hardware Component

前面使用 ​`mock_components/GenericSystem`​ 时，ROS2 Control 只是在电脑里模拟硬件接口。要让 ROS2 控制真实硬件，就需要把 Mock Hardware Component 换成我们自己的 Hardware Component

为此，我们一般会新建一个功能包：`<bot_name>_hardware`，目录如下：
  ```bash
  <bot_name>_hardware/
  ├── include/<bot_name>_hardware/
  │   ├── <bot_name>_driver.hpp
  │   └── <bot_name>_hardware_interface.hpp
  ├── src/
  │	  ├── <bot_name>_driver.cpp
  │   └── <bot_name>_hardware_interface.cpp
  ├── <bot_name>_hardware_interface.xml # 插件注册文件
  ├── CMakeLists.txt
  └── package.xml
  ```

下面我们以一个底层通信为串口，Hardware Component 类型为 system 的麦轮小车 Openrover 为例，编写 Hardware Interface 和 Hardware Driver。
> 如果一个小车还装有机械臂，那么机械臂的 Hardware Component 是否和底盘放在一起取决于两者的控制渠道是否一致（例如它们是否共用同一个控制板 / 串口协议）

### Write Hardware Interface

实现一个 System 类型的 Hardware Interface，需要编写一个继承自 `hardware_interface::SystemInterface` 的 `<bot_name>HardwareInterface`类，并且 override 以下方法：

| 函数                              | 作用                                                           |
| ------------------------------- | ------------------------------------------------------------ |
| `on_init(info)`                 | 初始化硬件组件，读取 `<ros2_control>-tag`  中的配置                        |
| `export_state_interfaces()`     | 导出硬件提供的状态接口，比如 `wheel_joint/position`、`wheel_joint/velocity` |
| `export_command_interfaces()`   | 导出硬件可接收的命令接口，比如 `wheel_joint/velocity`                       |
| `on_configure(previous_state)`  | 配置硬件资源，比如创建 driver、打开串口/CAN、检查设备是否存在                         |
| `on_activate(previous_state)`   | 激活硬件，开始接受 controller 命令，通常会清零命令、使能电机                         |
| `on_deactivate(previous_state)` | 停用硬件，通常会发送停止命令、失能电机                                          |
| `read(time, period)`            | 从真实硬件读取状态，并更新 state interface 对应的变量                          |
| `write(time, period)`           | 把 command interface 中的命令写入到真实硬件                              |
由于 SystemInterface 继承自 rclcpp_lifecycle::node_interfaces::LifecycleNodeInterface 所以上面有 `on_init()`，`on_activate() `等函数，lifecycleNode 相关知识参考：[[ROS2Node#Lifecycle Node]]

#### openrover_hardware_interface.hpp

```cpp
#ifndef OPENROVER_HARDWARE__OPENROVER_HARDWARE_INTERFACE_HPP_
#define OPENROVER_HARDWARE__OPENROVER_HARDWARE_INTERFACE_HPP_

#include ...

namespace openrover_hardware
{
class OpenRoverHardwareInterface : public hardware_interface::SystemInterface
{
public:
  RCLCPP_SHARED_PTR_DEFINITIONS(OpenRoverHardwareInterface) // ROS2 提供的宏，它的作用是自动为类生成一个共享指针的类型别名，等于 using SharedPtr = std::shared_ptr<OpenRoverHardwareInterface>;
  
  hardware_interface::CallbackReturn on_init(
    const hardware_interface::HardwareInfo & info) override;
    
  std::vector<hardware_interface::StateInterface> export_state_interfaces() override;
  std::vector<hardware_interface::CommandInterface> export_command_interfaces() override;

  hardware_interface::CallbackReturn on_configure(
    const rclcpp_lifecycle::State & previous_state) override;
  hardware_interface::CallbackReturn on_activate(
    const rclcpp_lifecycle::State & previous_state) override;
  hardware_interface::CallbackReturn on_deactivate(
    const rclcpp_lifecycle::State & previous_state) override;
  
  hardware_interface::return_type read(
    const rclcpp::Time & time, const rclcpp::Duration & period) override;
  hardware_interface::return_type write(
    const rclcpp::Time & time, const rclcpp::Duration & period) override;

private:
  static constexpr std::size_t kWheelCount = 4;
  std::array<std::string, kWheelCount> wheel_joint_names_ = {
    "front_left_wheel_joint",
    "front_right_wheel_joint",
    "rear_left_wheel_joint",
    "rear_right_wheel_joint"};
  std::array<double, kWheelCount> hw_positions_ = {0.0, 0.0, 0.0, 0.0};
  std::array<double, kWheelCount> hw_velocities_ = {0.0, 0.0, 0.0, 0.0};
  std::array<double, kWheelCount> hw_commands_ = {0.0, 0.0, 0.0, 0.0};
  std::unique_ptr<OpenRoverDriver> driver_; // 声明 driver 实例指针
  std::string port_name_ = "/dev/ttyUSB0";
  int baudrate_ = 115200;
  int write_timeout_ms_ = 20;
  bool active_ = false;
};
} // namespace openrover_hardware
#endif // OPENROVER_HARDWARE__OPENROVER_HARDWARE_INTERFACE_HPP_
```

#### openrover_hardware_interface.cpp

在 `SystemInterface` 基类中，存在 `info_` 这一数据成员是由框架直接提供的。它在 `on_init()` 被调用之前就已经由 Resource Manager 填充好，包含 URDF 中整个 `<ros2_control>` 标签解析后的所有信息

```cpp
#include ...

namespace openrover_hardware
{
namespace
{
const rclcpp::Logger LOGGER = rclcpp::get_logger("OpenRoverHardwareInterface");
std::string get_param_or( // 获取硬件参数，若未指定则返回默认值（避免重复查找）
  const hardware_interface::HardwareInfo & info,
  const std::string & name,
  const std::string & default_value)
{
  const auto it = info.hardware_parameters.find(name);
  return it == info.hardware_parameters.end() ? default_value : it->second;
}
} // namespace

hardware_interface::CallbackReturn OpenRoverHardwareInterface::on_init(
  const hardware_interface::HardwareInfo & info)
{
  if (hardware_interface::SystemInterface::on_init(info) != hardware_interface::CallbackReturn::SUCCESS)
  {
    return hardware_interface::CallbackReturn::ERROR;
  }
  // 此处可添加判断是否有 info_.joints.size() == kWheelCount
  for (std::size_t i = 0; i < kWheelCount; ++i) {
    wheel_joint_names_[i] = info_.joints[i].name;
	// 此处可添加判断 joint[i] 是否有 command 和 state interface
  }
  
  port_name_ = get_param_or(info_, "port_name", port_name_);
  baudrate_ = std::stoi(get_param_or(info_, "baudrate", std::to_string(baudrate_)));
  write_timeout_ms_ = std::stoi(
    get_param_or(info_, "write_timeout_ms", std::to_string(write_timeout_ms_)));

  std::fill(hw_positions_.begin(), hw_positions_.end(), 0.0);
  std::fill(hw_velocities_.begin(), hw_velocities_.end(), 0.0);
  std::fill(hw_commands_.begin(), hw_commands_.end(), 0.0);
  std::fill(arm_joint_commands_.begin(), arm_joint_commands_.end(), 0.0F);
  
  RCLCPP_INFO(LOGGER, "Initialized OpenRover hardware for %s at %d baud",
    port_name_.c_str(), baudrate_);
  return hardware_interface::CallbackReturn::SUCCESS;
}

std::vector<hardware_interface::StateInterface>
OpenRoverHardwareInterface::export_state_interfaces()
{
  std::vector<hardware_interface::StateInterface> state_interfaces;
  state_interfaces.reserve(kWheelCount * 2);
  for (std::size_t i = 0; i < kWheelCount; ++i) {
    state_interfaces.emplace_back(
      wheel_joint_names_[i], hardware_interface::HW_IF_POSITION, &hw_positions_[i]);
    state_interfaces.emplace_back(
      wheel_joint_names_[i], hardware_interface::HW_IF_VELOCITY, &hw_velocities_[i]);
  }
  return state_interfaces;
}

std::vector<hardware_interface::CommandInterface>
OpenRoverHardwareInterface::export_command_interfaces()
{
  std::vector<hardware_interface::CommandInterface> command_interfaces;
  command_interfaces.reserve(kWheelCount);
  for (std::size_t i = 0; i < kWheelCount; ++i) {
    command_interfaces.emplace_back(
      wheel_joint_names_[i], hardware_interface::HW_IF_VELOCITY, &hw_commands_[i]);
  }
  return command_interfaces;
}

hardware_interface::CallbackReturn OpenRoverHardwareInterface::on_configure(
  const rclcpp_lifecycle::State & previous_state)
{
  (void)previous_state;
  driver_ = std::make_unique<OpenRoverDriver>(port_name_, baudrate_, write_timeout_ms_); // 初始化 driver
  if (!driver_->open()) {
    RCLCPP_ERROR(LOGGER, "Failed to open OpenRover driver: %s", driver_->last_error().c_str());
    return hardware_interface::CallbackReturn::ERROR;
  }
  RCLCPP_INFO(LOGGER, "OpenRover serial driver configured");
  return hardware_interface::CallbackReturn::SUCCESS;
}

hardware_interface::CallbackReturn OpenRoverHardwareInterface::on_activate(
  const rclcpp_lifecycle::State & previous_state)
{
  (void)previous_state;
  active_ = true;
  std::fill(hw_commands_.begin(), hw_commands_.end(), 0.0);
  RCLCPP_INFO(LOGGER, "OpenRover hardware activated");
  return hardware_interface::CallbackReturn::SUCCESS;
}

hardware_interface::CallbackReturn OpenRoverHardwareInterface::on_deactivate(
  const rclcpp_lifecycle::State & previous_state)
{
  (void)previous_state;
  active_ = false;
  if (driver_ && driver_->is_open()) {
    driver_->send_command(0.0F, 0.0F, 0.0F, 0.0F, arm_joint_commands_);
  }
  RCLCPP_INFO(LOGGER, "OpenRover hardware deactivated");
  return hardware_interface::CallbackReturn::SUCCESS;
}

hardware_interface::return_type OpenRoverHardwareInterface::read(
  const rclcpp::Time & time, const rclcpp::Duration & period) // 从硬件读取当前关节状态（此处为模拟：速度=上次指令，位置=积分）
{
  (void)time;
  for (std::size_t i = 0; i < kWheelCount; ++i) {
    hw_velocities_[i] = hw_commands_[i];
    hw_positions_[i] += hw_velocities_[i] * period.seconds();
  }
  return hardware_interface::return_type::OK;
}

hardware_interface::return_type OpenRoverHardwareInterface::write(
  const rclcpp::Time & time, const rclcpp::Duration & period)
{
  (void)time;
  (void)period;
  if (!active_) {
    return hardware_interface::return_type::OK;
  }
  if (!driver_ || !driver_->is_open()) {
    RCLCPP_ERROR(LOGGER, "OpenRover driver is not open");
    return hardware_interface::return_type::ERROR;
  }
  if (!driver_->send_command(
      static_cast<float>(hw_commands_[0]),
      static_cast<float>(hw_commands_[1]),
      static_cast<float>(hw_commands_[2]),
      static_cast<float>(hw_commands_[3]),
      arm_joint_commands_))
  {
    RCLCPP_ERROR(LOGGER, "Failed to write OpenRover command: %s", driver_->last_error().c_str());
    return hardware_interface::return_type::ERROR;
  }
  return hardware_interface::return_type::OK;
}

} // namespace openrover_hardware
PLUGINLIB_EXPORT_CLASS(
  openrover_hardware::OpenRoverHardwareInterface, hardware_interface::SystemInterface) // 将本类注册为 SystemInterface 类型的 plugin，供 Resource Manager 动态加载
```

### Write Hardware Driver

Hardware Driver 通过底层通信协议（如串口、CAN 等）与硬件通信，实现对硬件的控制和状态的读取，并提供接口函数，用于在 Hardware Interface 中调用。串口库使用 boost

#### openrover_driver.hpp

```cpp
#ifndef OPENROVER_HARDWARE__OPENROVER_DRIVER_HPP_
#define OPENROVER_HARDWARE__OPENROVER_DRIVER_HPP_

#include <string>
#include <vector>
#include <boost/asio/io_context.hpp>
#include <boost/asio/serial_port.hpp>

namespace openrover_hardware
{
class OpenRoverDriver
{
public:
  static constexpr std::size_t kWheelCount = 4;
  static constexpr std::size_t kPayloadFloatCount = kWheelCount;
  static constexpr std::size_t kFrameSize = 2 + kPayloadFloatCount * sizeof(float);

  OpenRoverDriver() = default;
  OpenRoverDriver(std::string port_name, int baudrate, int write_timeout_ms);
  ~OpenRoverDriver();

  OpenRoverDriver(const OpenRoverDriver &) = delete;
  OpenRoverDriver & operator=(const OpenRoverDriver &) = delete;

  bool open();
  void close();
  bool is_open() const;

  bool send_command(
    float front_left_speed,
    float front_right_speed,
    float rear_left_speed,
    float rear_right_speed);

  const std::string & last_error() const;

private:
  bool configure_port();
  bool write_all(const std::uint8_t * data, std::size_t size);
  std::vector<std::uint8_t> make_command_frame(
    float front_left_speed,
    float front_right_speed,
    float rear_left_speed,
    float rear_right_speed) const;

  std::string port_name_ = "/dev/ttyUSB0";
  int baudrate_ = 115200;
  int write_timeout_ms_ = 20;
  boost::asio::io_context io_context_;
  boost::asio::serial_port serial_port_{io_context_};
  std::string last_error_;
};
} // namespace openrover_hardware

#endif // OPENROVER_HARDWARE__OPENROVER_DRIVER_HPP_
```

#### openrover_driver.cpp

```cpp
#include "openrover_hardware/openrover_driver.hpp"
#include <boost/asio/write.hpp>
#include <cstring>
#include <exception>
#include <utility>

namespace openrover_hardware
{
namespace
{
void append_float_le(std::vector<std::uint8_t> & frame, const float value) // 将一个float值按小端字节序（低位在前）追加到std::vector<uint8_t>中
{
  static_assert(sizeof(float) == sizeof(std::uint32_t), "OpenRover protocol expects 32-bit floats");
  std::uint32_t bits = 0;
  std::memcpy(&bits, &value, sizeof(float));
  frame.push_back(static_cast<std::uint8_t>(bits & 0xFF));
  frame.push_back(static_cast<std::uint8_t>((bits >> 8) & 0xFF));
  frame.push_back(static_cast<std::uint8_t>((bits >> 16) & 0xFF));
  frame.push_back(static_cast<std::uint8_t>((bits >> 24) & 0xFF));
}
} // namespace

OpenRoverDriver::OpenRoverDriver(
  std::string port_name, const int baudrate, const int write_timeout_ms)
: port_name_(std::move(port_name)),
  baudrate_(baudrate),
  write_timeout_ms_(write_timeout_ms)
{
}

OpenRoverDriver::~OpenRoverDriver()
{
  close();
}

bool OpenRoverDriver::open()
{
  if (is_open()) {
    return true;
  }
  try {
    serial_port_.open(port_name_);
    return configure_port();
  } catch (const std::exception & e) {
    last_error_ = "Failed to open " + port_name_ + ": " + e.what();
    return false;
  }
}

void OpenRoverDriver::close()
{
  if (!serial_port_.is_open()) {
    return;
  }
  boost::system::error_code error;
  serial_port_.cancel(error);
  serial_port_.close(error);
  if (error) {
    last_error_ = "Failed to close " + port_name_ + ": " + error.message();
  }
}

bool OpenRoverDriver::is_open() const
{
  return serial_port_.is_open();
}

bool OpenRoverDriver::send_command(
  const float front_left_speed,
  const float front_right_speed,
  const float rear_left_speed,
  const float rear_right_speed
{
  if (!is_open()) {
    last_error_ = "Serial port is not open";
    return false;
  }
  const auto frame = make_command_frame(
    front_left_speed, front_right_speed, rear_left_speed, rear_right_speed);
  return write_all(frame.data(), frame.size());
}

const std::string & OpenRoverDriver::last_error() const
{
  return last_error_;
}

bool OpenRoverDriver::configure_port()
{
  boost::system::error_code error;
  serial_port_.set_option(boost::asio::serial_port_base::baud_rate(baudrate_), error);
  if (error) {
    last_error_ = "Failed to set baud rate on " + port_name_ + ": " + error.message();
    return false;
  }
  serial_port_.set_option(boost::asio::serial_port_base::character_size(8), error);
  if (error) {
    last_error_ = "Failed to set character size on " + port_name_ + ": " + error.message();
    return false;
  }
  serial_port_.set_option(
    boost::asio::serial_port_base::parity(boost::asio::serial_port_base::parity::none), error);
  if (error) {
    last_error_ = "Failed to set parity on " + port_name_ + ": " + error.message();
    return false;
  }
  serial_port_.set_option(
    boost::asio::serial_port_base::stop_bits(boost::asio::serial_port_base::stop_bits::one),
    error);
  if (error) {
    last_error_ = "Failed to set stop bits on " + port_name_ + ": " + error.message();
    return false;
  }
  serial_port_.set_option(
    boost::asio::serial_port_base::flow_control(
      boost::asio::serial_port_base::flow_control::none),
    error);
  if (error) {
    last_error_ = "Failed to set flow control on " + port_name_ + ": " + error.message();
    return false;
  }
  return true;
}

bool OpenRoverDriver::write_all(const std::uint8_t * data, const std::size_t size)
{
  boost::system::error_code error;
  boost::asio::write(serial_port_, boost::asio::buffer(data, size), error);
  if (error) {
    last_error_ = "Serial write failed: " + error.message();
    return false;
  }
  return true;
}

std::vector<std::uint8_t> OpenRoverDriver::make_command_frame(
  const float front_left_speed,
  const float front_right_speed,
  const float rear_left_speed,
  const float rear_right_speed
{
  std::vector<std::uint8_t> frame;
  frame.reserve(kFrameSize);
  frame.push_back(0xAA);
  frame.push_back(0x55);
  append_float_le(frame, front_left_speed);
  append_float_le(frame, front_right_speed);
  append_float_le(frame, rear_left_speed);
  append_float_le(frame, rear_right_speed);
  return frame;
}
} // namespace openrover_hardware
```

### openrover_hardware_interface.xml

```xml
<library path="openrover_hardware_interface">
  <class
    name="openrover_hardware/OpenRoverHardwareInterface"
    type="openrover_hardware::OpenRoverHardwareInterface"
    base_class_type="hardware_interface::SystemInterface">
    <description>
      ros2_control SystemInterface for OpenRover over a serial motor controller.
    </description>
  </class>
</library>
```

### CMakeLists.txt

find 依赖：

```CMake
find_package(ament_cmake REQUIRED)
find_package(hardware_interface REQUIRED)
find_package(pluginlib REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclcpp_lifecycle REQUIRED)
find_package(Boost REQUIRED COMPONENTS system)
```

把 driver 和 hardware interface 编译成一个共享库：

```cmake
add_library(openrover_hardware_interface SHARED
  src/openrover_driver.cpp
  src/openrover_hardware_interface.cpp
)
```

这是必要的，因为 ros2_control 通过 pluginlib 动态加载 hardware interface，所以它必须是 SHARED library

包含头文件路径和链接依赖,以便让编译器找到`#include "openrover_hardware/openrover_driver.hpp"`：

```CMake
target_include_directories(openrover_hardware_interface PUBLIC
$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>
)
```

链接 ROS2 依赖：

```CMake
ament_target_dependencies(openrover_hardware_interface
  hardware_interface
  pluginlib
  rclcpp
  rclcpp_lifecycle
)
```

Boost 单独链接：

```CMake
target_link_libraries(openrover_hardware_interface
  Boost::system
)
```

还要导出 pluginlib 描述文件：

```cmake
pluginlib_export_plugin_description_file(
  hardware_interface openrover_hardware_interface.xml
)
```

### package.xml

需要声明依赖：

```xml
<depend>boost</depend>
<depend>hardware_interface</depend>
<depend>pluginlib</depend>
<depend>rclcpp</depend>
<depend>rclcpp_lifecycle</depend>
```

### Test

当前只有上位机的控制指令，没有反馈帧，因此适合使用虚拟串口进行测试：

```bash
socat -d -d \
  pty,raw,echo=0,link=/tmp/tty_driver \ # 给 driver 使用
  pty,raw,echo=0,link=/tmp/tty_monitor # 用于观察 driver 写出的字节
```

监听串口：

```bash
stty -F /tmp/tty_monitor raw -echo # 修改终端属性，方便显示串口字节流
hexdump -Cv < /tmp/tty_monitor # 设置 hex+ASCII 的显示模式
```
