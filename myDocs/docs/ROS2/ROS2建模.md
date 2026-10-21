# ROS2URDF

## URDF

URDF（Unified Robot Description Format）是 ROS 中描述机器人模型的 XML 格式文件

### `<robot>-tag`

根标签

属性
- name：机器人的名称，通常与文件名对应

示例：
```xml
<robot name="my_robot">
  <!-- 内部包含 link 和 joint -->
</robot>
```

### `<material>-tag` 

表示材质属性

属性
  - name：材质名称（可选，定义后可被其他 `<visual>` 通过 `name` 引用）
子级标签
  - `<color>`：定义颜色及透明度
    - 属性：`rgba="r g b a"`
      - r/g/b：红绿蓝分量，取值 0.0 ~ 1.0
      - a：不透明度，0.0（完全透明）~ 1.0（完全不透明）
  - `<texture>`：定义纹理贴图（较少使用）
    - 属性：`filename="package://pkg_name/path/to/image.png"`

示例：
```xml
<material name="SemiRed">
      <color rgba="1 0 0 0.5"/>
</material>
```


### `<link>-tag` 

表示连杆（刚体）

属性
  - name：连杆的唯一名称
子级标签，定义几何体（一个link可以有多个几何体）
  - `<visual>`：可视化外观
    - `<geometry>`：形状几何体
	    - `<box>`
	    - `<cylinder>`
	    - `<mesh>`，具有属性：`filename="package://<pkg_name>/meshes/<mesh_name>.stl"
		    - URDF 中长度单位统一是米（m）。STL 格式本身不保存单位，RViz 会把 STL 顶点里的数值直接当作米
		    - 如果使用的 STL模型是以 mm 为单位导出的，可以使用属性 `scale="0.001 0.001 0.001"` 进行缩放
		    - URDF 不会自动计算 STL 的中心。它直接使用 STL 顶点坐标所在处作为中心，在 origin 为0时，STL 顶点坐标与 link 的原点重合
    - `<origin>`：位姿偏移（`xyz` 和 `rpy` 属性）
    - `<material>`：颜色/纹理（包含`color` 子标签或通过 `name` 引用外部`<material>`）
  - `<collision>`：碰撞检测几何体，结构与 visual 类似，visaul 和 collision 的 geometry 可以相同，也可以不同，一般要求 collision 的几何体比 visual 的几何体更简单，简化计算
  - `<inertial>`：惯性参数
    - `<mass>`：质量（`value` 属性）
    - `<origin>`：质心位姿偏移
    - `<inertia>`：惯性张量（`ixx, ixy, ixz, iyy, iyz, izz`）

### `<joint>-tag` 

表示关节（连接两个连杆）

属性
- name：关节唯一名称
- type：关节类型，常用：
	- `fixed`：固定连接
	- `revolute`：旋转关节，有角度限制
	- `continuous`：无限旋转关节
	- `prismatic`：滑动关节
	- `planar`、`floating`（较少使用）
子级标签
- `<parent link="父连杆名称"/>`
- `<child link="子连杆名称"/>`
- `<origin xyz="x y z" rpy="roll pitch yaw"/>`：定义子连杆相对于父连杆的变换
- `<axis xyz="1 0 0"/>`：定义旋转轴或滑动轴（对 revolute/prismatic 必需）
- `<limit>`：关节运动范围限制
	- `lower`：下限（rad 或 m）
	- `upper`：上限
	- `effort`：最大力矩/力（Nm 或 N）
	- `velocity`：最大速度
- `<dynamics>`：阻尼、摩擦（`damping`, `friction`）
- `<mimic>`：模仿其他关节（`joint` 属性指定要模仿的关节名，`multiplier` 倍数（-1表示相反），`offset` 偏移）

### 两个`<origin>`的区别

`<link>` 内部的 `<origin>`
- 含义：该部件的外观中心或质心相对于该 link 自身坐标系（自身坐标系的位置即全局坐标系中joint内部`<origin>`定义的相对于父坐标系的变换后的坐标系位置）的位置和姿态
- 例如：
  ```xml
  <link name="base_link">
    <visual>
      <origin xyz="0.1 0 0.2" rpy="0 0 0.5"/>
      <geometry><box size="0.1 0.1 0.05"/></geometry>
    </visual>
  </link>
  ```
表示视觉长方体的中心位于 link 原点前方 0.1 m、上方 0.2 m，并绕 z 轴旋转 0.5 弧度

`<joint>` 内部的 `<origin>`
- 出现在 `<joint>` 标签里。
- 含义：子 link 坐标系相对于父 link 坐标系的初始相对位姿（当关节值为 0 时）
- 例如：
  ```xml
  <joint name="joint1" type="revolute">
    <parent link="base_link"/>
    <child link="arm_link"/>
    <origin xyz="0.2 0 0" rpy="0 0 0"/>
    <axis xyz="0 0 1"/>
  </joint>
  ```
表示 `arm_link` 的原点位于 `base_link` 前方 0.2 m 处，无旋转

## XACRO

Xacro（XML Macros）是 ROS 中处理 URDF 的 XML 宏语言，允许使用变量、宏、条件等，减少重复，提高机器人模型的可维护性

### 基本语法

#### 基本结构

```xml
<?xml version="1.0"?>
<robot name="my_robot" xmlns:xacro="http://www.ros.org/wiki/xacro">
  <!-- 属性定义 -->
  <xacro:property name="length" value="0.5"/>
  <!-- 宏定义 -->
  <xacro:macro name="my_macro" params="param1 param2:=default">
    <!-- 宏内容，使用 ${param1} -->
  </xacro:macro>
  <!-- 调用宏或直接编写 link/joint -->
  <xacro:my_macro param1="${length}" param2="some_value"/>
</robot>
```

#### 属性（property）

声明和调用：

```xml
<xacro:property name="wheel_radius" value="0.05"/>

<link name="wheel">
  <visual>
    <geometry>
      <cylinder radius="${wheel_radius}" length="0.02"/> <!-- 调用方式：${属性名} -->
    </geometry>
  </visual>
</link>
```

在 `${}` 内也可以进行数学运算，例如：

```xml
${pi/2.0}
${wheel_radius*2}
```

属性也可以在 xacro 命令行里面指定 value，详见：[[ROS2建模#XACRO的解析]]

#### 参数（Arg）

不同于 `property` 是文件内固定常量，`arg` 允许从外部传入参数值并覆盖默认值。可在调用 xacro 时通过命令行传入：

```xml
<xacro:arg name="use_sim" default="false"/>
<xacro:arg name="prefix" default=""/>

<!-- 在xacro中的调用方式与property一致-->
```

```python
robot_description = {
    'robot_description': ParameterValue(
        Command([
            'xacro ', description_path,
            ' use_sim:=', use_sim, # use_sim = LaunchConfiguration('use_sim')
            ' prefix:=', prefix, # prefix = LaunchConfiguration('prefix')
        ]),
        value_type=str
    )
}
```

#### 宏（Macro）

相当于可复用的模板：

```xml
<xacro:macro name="wheel" params="name x y"> <!-- 也可以写成 <属性名>=“...” 的形式 -->
   <link name="${name}_wheel_link">
     <visual>
       <origin rpy="${pi/2.0} 0 0"/>
       <geometry>
         <cylinder radius="${wheel_radius}" length="${wheel_width}"/>
       </geometry>
       <material name="wheel_black"/>
     </visual>
     <collision>
		...
     </collision>
   </link>
</xacro:macro>
```

宏的调用：

```xml
<xacro:wheel params="name x y"/>
```

#### 包含（Include）

可用于拆分模型文件：

```xml
<xacro:include filename="chassis.xacro"/> <!-- 相对路径 -->
<xacro:include filename="arm.xacro"/>
```

#### 条件判断（if）

```xml
<xacro:if value="${use_gpu}">
  <!-- 条件为真时包含 -->
</xacro:if>
<xacro:unless value="${standalone}">
  <!-- 条件为假时包含 -->
</xacro:unless>
```

value 中可以放属性（property）或运算式

### XACRO的解析

Prerequisites: [[ROS2Launch]]

XACRO 文件并不能直接作为 URDF 文件调用，必须通过 `xacro` 命令解析为 urdf 文件：

- 在 launch 文件中用 `xacro` 命令解析并作为 `robot_description` 参数：
	```xml
	<param name="robot_description"
       command="$(find xacro)/xacro $(find-pkg-share <pkg_name>)/urdf/robot.xacro"/>
	```
	
- Python launch 中可用 `Command` 调用 `xacro` 子进程：
```python
Node(
    package='robot_state_publisher',
    executable='robot_state_publisher',
    name='robot_state_publisher',
    parameters=[{
        'robot_description': Command(['xacro ', 
        LaunchConfiguration('description_path'),
        ' <key>:=', LaunchConfiguration('<value对应的ROS2参数名>')])
    }]
),
```

- 在终端使用 `xacro` 命令生成纯 URDF：`xacro model.xacro > model.urdf`

## 建模规范

对于车辆模型，一般需要指定 base_link（机器人本体坐标系）和 base_footprint（机器人投影坐标系），即 base_link 在地面的 2D 投影，坐标系命名规范参考：[[TF2#坐标系规范]]

### Soildworks 导出 URDF

注意事项：
- 设置坐标之前先摆正模型，防止导出的 Axis 是歪的
- 导出前确认导出器没有用装配体原点 Origin_global
- 导出器似乎不能导出无mesh的link，会报错

## 模型展示

编写一套启动 joint_state_publisher_gui、robot_state_publisher、rviz2 的 launch 文件，例如：

```python
from launch import LaunchDescription
from launch.substitutions import Command, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    description_path = PathJoinSubstitution([
        FindPackageShare('openrover_description'),
        'urdf',
        'openrover.urdf.xacro'
    ])

    robot_description = {
        'robot_description': ParameterValue(
            Command([
                'xacro', ' ', description_path
            ]),
            value_type=str,
        )
    } # robot_description 里的 URDF 输出需要用 ParameterValue 明确其为 string 而不是 yaml，防止 robot_state_publisher 理解错误导致报错

    return LaunchDescription([
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[robot_description]
        ),
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            name='joint_state_publisher_gui',
            output='screen'
        ),
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen',
        )
    ])
```

Launch 文件编写参考 [[ROS2Launch]]。启动后需要在 RVIZ2 中配置 fixed frame 为 `base_footprint`，添加 RobotModel，设置 topic 为 `/robot_description`