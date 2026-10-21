# ROS2Param

参数是ROS2中用于配置节点行为的关键机制。它们允许用户在运行时动态调整节点的功能，而无需重新编译代码

## 使用

### 静态传入

使用 `declare_parameter` 方法将获取的参数传给成员变量，例如在类的构造函数中：
```cpp
class MyNode : public rclcpp::Node
{
public:
    MyNode() : Node("my_node") {
        // 声明参数并提供默认值
        value = this->declare_parameter<std::string>("param_name", "default_value");
        RCLCPP_INFO(this->get_logger(), "MyNode has been created with static parameter!");
    }
private:
    std::string value;
};
```

可以在节点运行时通过命令行或参数文件来覆盖默认值，例如：
```bash
# 通过命令行覆盖默认值
ros2 run my_package my_node --ros-args -p param_name:=new_value
# 通过参数文件覆盖默认值
ros2 run my_package my_node --ros-args --params-file path/to/params.yaml
```

### 动态传入