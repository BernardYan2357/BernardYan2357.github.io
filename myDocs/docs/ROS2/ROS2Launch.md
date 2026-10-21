# ROS2Launch

- [ROS2工具 Launch](https://xiaohuzi-design.github.io/zhaoxuzuo_ros2/di-4-zhang-ros2-gong-ju-zhi-launch-rosbag2-yu-rqt.html)

在ROS2中，Launch文件可以使用Python，XML或YAML格式编写

## xml

`<node>-tag`用于表示节点
- 属性
  - pkg：功能包
  - exec：可执行文件
  - name：节点名称，如果不指定，默认为可执行文件的名称
  - namespace：命名空间
  - respawn：节点关闭后是否重启
  - args：节点的命令行参数，注意不是ROS2参数，而是命令行参数
  - output：节点的输出方式，可以选择screen, log或both，screen表示输出到终端，log表示输出到日志文件
- 子级标签
  - param，设置参数的标签，属性：
    - name：参数名称
    - value：参数值
    - from：参数文件路径
  - remap，话题重映射标签，属性：
    - from：原话题名称
    - to：新话题名称

`<executable>-tag`用于表示执行命令
- 属性
  - cmd：被执行的命令，字符串表示，例如`cmd="ros2 run pkg_name node_name"`
  - output：日志输出目的地设置，可以选择screen, log或both

`<arg>-tag`用于声明参数
- 属性
  - name：参数名称
  - default：参数默认值
- 调用方式：`$(arg arg_name)`

`<include>-tag`用于包含其他Launch文件
- 属性
  - file：被包含的Launch文件路径
  - arg：传递给被包含Launch文件的参数，格式为`<arg name="arg_name" value="arg_value"/>`

`<group>-tag`用于将多个节点组织在一起
- 子级标签
  - push_ros_namespace：可以通过该标签中的 namespace 属性设置组内节点使用的命名空间
  - node：节点标签

替换写法：
- `$(find-pkg-share package_name)`：获取功能包的路径
- `$(var <变量名>)` 读取 launch 里用`<let>`声明的参数值
- `$(xacro file_path)` 解析 xacro 文件，返回解析后的字符串
- `$(command <command_line>)` 执行命令，返回命令的输出结果
- `$(dirname)`：返回当前 launch 文件所在的目录路径
- `$(env <环境变量名>)`：读取系统环境变量（例如 `$(env HOME)`）
- `$(eval <Python表达式>)`：执行 Python 表达式，返回结果字符串

条件执行：
`if/unless`属性可以被添加到任何标签上，用于条件执行，例如：

```xml
<node pkg="pkg_name" exec="node_name" if="$(var load_controller)">
</node>
```

### 安装方式

package.xml：

```xml
<!-- 必要的依赖 -->
<exec_depend>launch</exec_depend>
<exec_depend>launch_ros</exec_depend>
<!-- 如果launch文件中使用了xacro -->
<exec_depend>xacro</exec_depend>
```

CMakeLists.txt：

```cmake
install(
  DIRECTORY config launch
  DESTINATION share/${PROJECT_NAME}/
)
```

## Python

基本结构
```python
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
	<node_name01> = Node(...) # 实例化Node类
	<node_name02> = Node(...)
    return LaunchDescription([
        <node_name01>, <node_name02>
    ])
```

节点定义
```python
<node_name> = Node(
    package='pkg_name', # 功能包名称
    executable='node_name', # 可执行文件名称
    name='custom_name', # 节点名称，如果不指定，默认为可执行文件的名称
    namespace='my_namespace', # 命名空间
    remappings=[('old_topic', 'new_topic')], # 话题重映射
    parameters=[{'param_name': value}], # 参数列表，可以是字典或参数文件路径
    arguments=['--ros-args', '--log-level', 'info'], # 命令行参数列表
    output='screen', # 输出方式，可以选择'screen'或'log'
    respawn=True # 关闭后是否重启
)
```

ROS2参数传递
```python
from launch import LaunchConfiguration
from launch.actions import DeclareLaunchArgument

my_arg = DeclareLaunchArgument('my_arg', default_value='default_val', description='This is a launch argument'),
Node(
    ...,
    parameters=[{'key': LaunchConfiguration('my_arg')}] # 使用LaunchConfiguration获取参数值
)
```

路径拼接
```python
from launch.substitutions import PathJoinSubstitution

DeclareLaunchArgument('description_path',
    default_value=PathJoinSubstitution([
        FindPackageShare('robot_description'), # 获取功能包的路径
        'urdf',
        'robot.urdf.xacro'
    ]),
    description='Path to the robot description file'),
```

包含其他Launch文件
```python
from launch.actions import IncludeLaunchDescription
from launch_ros.substitutions import PathJoinSubstitution, FindPackageShare

IncludeLaunchDescription(
    PathJoinSubstitution([
	    FindPackageShare('pkg_name'),
	    'launch',
	    'file.launch.py'
	]),
    launch_arguments={'arg1': 'value'} # 传递参数给被包含的Launch文件
)
```

条件执行
```python
from launch.conditions import IfCondition

Node(
    ...,
    condition=IfCondition(LaunchConfiguration('condition_arg')) # 只有当condition_arg为true时才执行该节点，括号里面可以使用PythonExpression放判断语句，例如：PythonExpression([LaunchConfiguration('condition_arg'), " == 'some_thing'"])
)
```

### 安装方式

setup.py：

```python
from setuptools import setup
setup(
    ...,
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
    ],
)
```

 launch.py 不要求功能包必须声明为 `ament_python`，`ament_cmake` 同样可以包含 `.launch.py` 文件。ROS2 只关心 launch 文件是否被正确安装到了 `share/<package_name>/launch/` 目录下，对于 `ament_cmake`，参考：[[ROS2Launch#安装方式]]
