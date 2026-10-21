# Gazebo

## Setup Gazebo Env

为一个机器人模型搭建 Gazebo 仿真环境

前提：你已经有了 `robot_description`, `robot_hardware`, `robot_bringup` 等功能包

### 让 URDF 兼容 Gazebo

`robot_description` 中的 URDF/Xacro 必须满足 Gazebo 的仿真要求：

- 每个 `<link>` 必须包含 `<inertial>` 标签（质量和惯性矩阵），否则 Gazebo 会忽略该 link 或报错，如果原始 URDF 不包含惯性参数，可以使用宏（如 `xacro:macro`）从质量生成近似惯性矩阵，或者用 SolidWorks/MeshLab 等工具计算
- 每个 `<joint>` 应设置合理的限位、摩擦、阻尼（可选但影响仿真真实度）
- **碰撞模型**：如果模型复杂，应用简化网格或基本几何体作为 `<collision>`，减少物理计算开销

### 配置 Gazebo 插件与 ros2_control

对于使用 ros2_control 的机器人，需要在 URDF 中添加 `gazebo_ros2_control` 插件

在 URDF 的 `<robot>` 元素内插入：

```xml
<gazebo>
  <plugin name="gazebo_ros2_control" filename="libgazebo_ros2_control.so">
    <parameters>$(find robot_description)/config/ros2_control_sim.yaml</parameters>
  </plugin>
</gazebo>
```

然后在 `robot_simulation` 包的 `config` 目录下创建 `ros2_control_sim.yaml`，内容与真实硬件的 `ros2_control.yaml` 类似，但 `hardware` 部分改用仿真实现：

```yaml
controller_manager:
  ros__parameters:
    update_rate: 100  # Hz

    joint_state_broadcaster:
      type: joint_state_broadcaster/JointStateBroadcaster

    diff_drive_controller:
      type: diff_drive_controller/DiffDriveController

    # ... 其他控制器

joint_state_broadcaster:
  ros__parameters:
    # ...

diff_drive_controller:
  ros__parameters:
    # ...
```

**关键区别**：在 URDF 中，针对每个要仿真的 joint，通过 `<ros2_control>` 标签定义接口和硬件组件，并指定 `hardware_type="gazebo_ros2_control/GazeboSystem"`（或其他仿真实现）。例如：

```xml
<ros2_control name="GazeboSystem" type="system">
  <hardware>
    <plugin>gazebo_ros2_control/GazeboSystem</plugin>
  </hardware>
  <joint name="left_wheel_joint">
    <command_interface name="velocity"/>
    <state_interface name="position"/>
    <state_interface name="velocity"/>
  </joint>
  <!-- 其他关节 -->
</ros2_control>
```

这个配置告诉 ros2_control：不要试图连接真实硬件，而是由 Gazebo 插件从仿真中读取状态、发送命令

注意：

```xml
    <xacro:if value="${ros2_control_hardware_type == 'sim_gazebo' and controllers_yaml_path != ''}">
      <gazebo>
        <plugin filename="gz_ros2_control-system" name="gz_ros2_control::GazeboSimROS2ControlPlugin">
          <parameters>${controllers_yaml_path}</parameters>
          <ros>
            <remapping>/mecanum_drive_controller/tf_odometry:=/tf</remapping>
            <remapping>/mecanum_drive_controller/reference_unstamped:=/cmd_vel</remapping>
          </ros>
        </plugin>
      </gazebo>
    </xacro:if>
```

`mecanum_drive_controller` 不是由 launch 直接启动的，而是由 URDF 中的 `gz_ros2_control` 插件在 Gazebo 内部创建的。因此：

- `bringup.launch.py` 中的 `Node(remappings=...)` 只适用于独立运行的 `ros2_control_node`
- `gazebo.launch.py` 不能直接给 Gazebo 内部创建的 controller 设置 remap
- 将 `<ros><remapping>...</remapping></ros>` 放在 Gazebo 插件中，正是该插件的运行时配置方式

## 仿真时间

MoveIt 执行失败：仿真时间不一致

日志：

```
Requested time 1786431325.204913
latest received state has time 73.640000
```

MoveIt 使用了系统时间，而 `/joint_states` 使用 Gazebo 仿真时间，所以 MoveIt 认为关节状态已经过期，最终：

```
Solution found but controller failed during execution
```