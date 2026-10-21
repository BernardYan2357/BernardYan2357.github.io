# ROS2 编程

## Colcon

### COLCON_IGNORE

`COLCON_IGNORE`文件是一个特殊的标记文件，当 colcon 在构建过程中遇到这个文件时，会忽略包含该文件的目录及其子目录中的所有包。这对于临时排除某些包或目录非常有用，而不需要修改`CMakeLists.txt`或`package.xml`文件

## ROS2 API

### 日志 API

常用的日志级别包括：

- `RCLCPP_DEBUG`
- `RCLCPP_INFO`
- `RCLCPP_ERROR`
- `RCLCPP_FATAL`

日志输出的基本用法如下：

```cpp
RCLCPP_INFO(this->get_logger(), "This is an info message");
```

也可以构建logger对象来发送日志：

```cpp
auto logger = rclcpp::get_logger("my_logger");
RCLCPP_ERROR(logger, "This is an error message");
```

构建logger对象的好处是同一个logger对象的日志信息都有相同的前缀，方便过滤和区分日志来源

### 时间API

### NodeOptions

## 包与构建配置

ROS2 工程通常会同时涉及包元信息、C++ 构建配置和 Python 安装配置，三者分别负责不同层面的工程组织

- `package.xml`：声明包名、版本、作者、许可证和依赖关系
- `CMakeLists.txt`：管理 C++ 目标、依赖查找、编译和安装
- `setup.py`：管理 Python 包安装、入口点和控制台命令

### package.xml

`package.xml` 用于声明包的基础信息和依赖。常见字段包括 `<depend>`、`<build_depend>` 和 `<exec_depend>`，在 ROS2 中很多情况下直接写 `<depend>` 就可以同时表示构建和运行都需要该依赖

### CMakeLists.txt

通过 `CMakeLists.txt` 完成依赖查找、可执行文件创建和安装

例如：

```cmake
cmake_minimum_required(VERSION 3.8)
project(example_cpp_pkg)

# 如果编译器不是 gcc，需要开启 C++17 支持
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 17)
  set(CMAKE_CXX_STANDARD_REQUIRED ON)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# 1. find_package：查找本包直接依赖的依赖包
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)

# 2. add_executable：把源文件编译成可执行目标
add_executable(topic_publisher_01 src/topic_publisher_01.cpp)
add_executable(topic_subscribe_01 src/topic_subscribe_01.cpp)

# 3. ament_target_dependencies：为每个目标指定依赖，ament 会据此补上头文件路径、链接库和导出信息
ament_target_dependencies(topic_publisher_01 rclcpp std_msgs)
ament_target_dependencies(topic_subscribe_01 rclcpp std_msgs)

# 4. install：安装编译产物和运行时资源，install 之后 ros2 run 才找得到
install(TARGETS
  topic_publisher_01
  topic_subscribe_01
  DESTINATION lib/${PROJECT_NAME}
)

# launch、config、urdf、rviz 这类运行时资源同样要装到 share/<pkg> 下
install(
  DIRECTORY launch config
  DESTINATION share/${PROJECT_NAME}/
)

ament_export_dependencies(rclcpp std_msgs)
ament_package()
```

注意事项：

- `add_executable()` 里写的是源文件路径，`ament_target_dependencies()` 里写的是依赖包名，两者要一一对应，漏写 `ament_target_dependencies()` 通常表现为找不到头文件
- `install(TARGETS ...)` 的 `DESTINATION lib/${PROJECT_NAME}` 是固定约定，`ros2 run <pkg> <exec>` 就是按这个路径去找可执行文件的，写成 `bin` 会导致 `ros2 run` 找不到
- 一个包里有多个可执行文件时，可以像上面这样写多个 `add_executable()` / `ament_target_dependencies()`，再统一放到一个 `install(TARGETS ...)` 里

如果包里还有[[ROS2通信#自定义动作接口|自定义接口]]（msg/srv/action），额外需要：

```cmake
find_package(rosidl_default_generators REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "action/SumInts.action"
)

# 使用这些接口的目标要把接口包作为依赖传进去
ament_target_dependencies(action_server rclcpp rclcpp_action example_interfaces)
```

### setup.py

Python 包通过 `setup.py` 声明入口脚本和安装方式。`entry_points` 里的 `console_scripts` 常用来把节点函数暴露成 `ros2 run` 可以直接执行的命令

例如：

```python
import os
from glob import glob
from setuptools import setup

package_name = 'example_py_pkg'

setup(
    name=package_name,                     # 包名，需要和 package.xml 中的 <name> 一致
    version='0.0.1',
    packages=[package_name],               # 要安装的 Python 包目录
    data_files=[
        # ament 索引资源，标记该目录是一个 ROS2 包，必须要有
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        # 安装 package.xml，ros2 pkg 相关命令依赖它
        ('share/' + package_name, ['package.xml']),
        # 安装 launch 文件，ros2 launch <pkg> <file>.launch.py 才能找到
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        # 安装参数、rviz 配置等运行时资源
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='your_name',
    maintainer_email='',
    description='ROS2 Python package example',
    license='',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            # 格式：可执行文件名 = 模块名.文件名:函数名
            # 左边是 ros2 run 时使用的名字，右边是实际要调用的 main 函数
            'topic_publisher_02 = example_py_pkg.topic_publisher_02:main',
            'topic_subscribe_02 = example_py_pkg.topic_subscribe_02:main',
        ],
    },
)
```

注意事项：

- `entry_points` 左侧的名字才是 `ros2 run example_py_pkg topic_publisher_02` 里的可执行文件名，右侧冒号后面的 `main` 必须和源文件里定义的函数名一致；写错了会出现 `No executable found`
- `data_files` 里 launch 文件的 glob 要匹配实际后缀，如果文件名是 `xxx.launch.py`，用 `glob('launch/*.launch.py')`，用 `glob('launch/*.py')` 一般也能覆盖
- 源文件要放在与包名同名的目录下（这里是 `example_py_pkg/`），并由 `packages=[package_name]` 安装；Python 节点文件不需要可执行权限

## 编程方法

### 两种带节点类的构造方式

常见的一种方式是类继承`rclcpp::Node`，在构造函数中直接调用基类构造函数来创建节点

```cpp
class MyNode : public rclcpp::Node
{
public:
    MyNode() : Node("my_node") {
        RCLCPP_INFO(this->get_logger(), "MyNode has been created!");
    }
private:
};
int main(int argc, char * argv[]) {
    rclcpp::init(argc, argv);
    auto node = std::make_shared<MyNode>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}
```

另一种方式是将节点作为成员变量，在构造函数中使用`std::shared_ptr<rclcpp::Node>`来创建节点实例（也可以写`rclcpp::Node::SharedPtr`）

```cpp
class MyNode
{
public:
    explicit MyNode(const std::shared_ptr<rclcpp::Node>& node) : node_(node) {
        // 使用explicit关键字可以防止隐式类型转换
        // 使用const & 可以避免一次不必要的 shared_ptr 拷贝
        // 使用初始化列表来初始化成员变量 node_，这是 C++ 中推荐的做法
        RCLCPP_INFO(node_->get_logger(), "MyNode has been created!");
    }
private:
    std::shared_ptr<rclcpp::Node> node_;
};
int main(int argc, char * argv[]) {
    rclcpp::init(argc, argv);
    auto node = std::make_shared<rclcpp::Node>("my_node");
    auto my_node = MyNode(node);
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}
```

这种写法适用于需要将节点作为参数传递给其他类或函数的情况，例如 Moveit2 中的规划器插件通常需要接受一个节点指针来访问 ROS2 功能

也可以类内自己创建节点实例，不用外部传入

```cpp
class MyNode
{
public:
    MyNode() {
        node_ = std::make_shared<rclcpp::Node>("my_node");
        RCLCPP_INFO(node_->get_logger(), "MyNode has been created!");
    }
    std::shared_ptr<rclcpp::Node> get_node() const { return node_; } // 提供一个公共方法来访问节点指针
private:
    std::shared_ptr<rclcpp::Node> node_;
};
int main(int argc, char * argv[]) {
    rclcpp::init(argc, argv);
    auto my_node = std::make_shared<MyNode>();
    rclcpp::spin(my_node->get_node());
    rclcpp::shutdown();
    return 0;
}
```


TODO 好的 main() 该怎么写

```python
def main(args=None):
    rclpy.init(args=args)
    node = None
    result = 0
    try:
        node = StereoNode()
        rclpy.spin(node)
    except (KeyboardInterrupt, rclpy.executors.ExternalShutdownException):
        pass
    except (OSError, ValueError, KeyError, cv2.error, yaml.YAMLError) as error:
        rclpy.logging.get_logger('stereo_node').error(str(error))
        result = 1
    finally:
        if node is not None:
            node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()
    return result
```