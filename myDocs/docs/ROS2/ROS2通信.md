# ROS2通信

Prerequisites:

- [[计算机基础#通信]]

在 ROS 时代，开发者习惯于这样理解系统：节点就是独立的功能单元，通过 Topic 连接在一起，整个系统就是这些节点的集合。这种模型在简单场景下是成立的，但在复杂系统中，它会迅速失效

原因在于，真实系统并不是节点的集合，而是强耦合的执行链。例如一个移动机器人，从传感器、感知、定位到规划和控制，每一个环节都依赖前一个环节的数据。如果其中任意一环出现延迟或阻塞，整个系统就会受到影响。这就意味着，问题不再是某个节点是否正常，而是整个系统是否被正确调度。而调度，正是 ROS2 相比 ROS1 最大的变化之一

## ROS2通信机制

![ros2_architecture_overview](ros2_architecture_overview.png)

### DDS

数据分发服务（Data Distribution Service, DDS）是对象管理组织（OMG）制定的中间件协议和 API 标准，是一种去中心化的，基于发布-订阅模式的数据通信协议

DDS 是 ROS2 中默认的通信中间件，是 ROS2 通信的基础设施。DDS 有多种实现，ROS2 通过 ROS2 Middleware Interface (RMW) 层来抽象和支持不同的 DDS 实现，常用的 DDS 实现包括：

- eProsima’s Fast DDS：默认的DDS实现，功能全面，适用于大多数应用场景
- Eclipse’s Cyclone DDS：轻量级，低延迟，适用于嵌入式系统
- RTI’s Connext DDS：工业级，高可靠性，商业许可证

要换用其他DDS实现，参考：[Working with multiple RMW implementations](https://docs.ros.org/en/humble/How-To-Guides/Working-with-multiple-RMW-implementations.html)

#### Domain ID

在 DDS 中，不同逻辑网络共享物理网络的主要机制称为域(Domain) ID。同一域上的 ROS2 节点可以自由地相互发现并发送消息，而不同域上的 ROS2 节点则不能

所有ROS 2节点默认使用域ID为0。为了避免在同一网络上运行ROS 2的不同计算机组之间互相干扰，应为每组设置不同的域ID，要设置域ID，参考：[详细解释如何选择域ID](http://dev.ros2.fishros.com/doc/Concepts/About-Domain-ID.html#choosing-a-domain-id-long-version)

#### Qos

- [一文搞懂Qos](https://mp.weixin.qq.com/s/J63fO4c_QIseLGQd5W2fAw)
- [About-Quality-of-Service-Settings](https://docs.ros.org/en/humble/Concepts/Intermediate/About-Quality-of-Service-Settings.html)

在ROS1中，节点间的通信是基于TCP的。因为TCP的失败重传机制，在一些网络不稳定的场景，通信会出现延时严重的问题

Qos（Quality of Service）是 DDS 中的一个重要概念，用于描述通信的质量和可靠性要求。在 ROS2 中，针对节点特定的工作负载和使用场景，有倾向地配置Qos将可以使通信质量达到最佳。我们可以为每个节点单独配置 Qos ，但是需要注意的是，只有当通信双方的 Qos 配置兼容时，节点间的通信才能建立成功

Qos 配置项有：

- History
  - Keep last: 只保留最多 N 个样本，N 可通过 queue depth 选项配置
  - Keep all: 保留所有样本，但受限于底层中间件的资源限制
- Depth
  - Queue size: 仅当 history 策略设置为 keep last 时才会生效
- Reliability
  - Best effort: 尝试传递样本，但在网络不稳定时可能会丢失
  - Reliable: 保证样本会被传递，可能会多次重试
- Durability
  - Transient local: 发布者会负责为“后加入”的订阅者持久保存样本
  - Volatile: 不尝试持久保存样本
- Deadline
  - Duration: 发布到某个 topic 的相邻两条消息之间，允许的最大时间间隔
- Lifespan
  - Duration: 消息从发布到接收之间允许的最大时间；如果超过这个时间，消息会被视为陈旧或过期，过期消息会被静默丢弃，实际上不会被接收
- Liveliness
  - Automatic: 当节点的任意一个 publisher 发布消息时，系统会认为该节点的所有 publisher 在接下来的 lease duration 内仍然存活
  - Manual by topic: 当 publisher 通过 publisher API 手动声明自己仍然存活时，系统会认为该 publisher 在接下来的 lease duration 内仍然存活
- Lease Duration
  - Duration: publisher 在被系统判定为失去 liveliness 之前，允许声明自己仍然存活的最长时间；失去 liveliness 可能表示发生了故障

下表显示了Qos的不同策略及其兼容性：

![Qos_Compatibility|537](Qos_Compatibility.png)

表中的x表示人为设定了某个值，Default值根据不同的DDS有不同的设定。通常是下面两种：

```cpp
#define RMW_DURATION_INFINITE {9223372036LL, 854775807LL}
#define RMW_DURATION_UNSPECIFIED {0LL, 0LL}
```

查询话题的Qos配置：

```bash
ros2 topic info <topic_name> --verbose
```

rclcpp 还提供了一些常用的[预设 Qos](https://docs.ros.org/en/humble/p/rclcpp/generated/classrclcpp_1_1QoS.html)，本质上是把常见的 DDS 配置封装成现成的类型，方便直接使用。常见的有：

- `rclcpp::SystemDefaultsQoS()`：使用底层 RMW/DDS 的默认配置
- `rclcpp::SensorDataQoS()`：适合相机、雷达、IMU 这类传感器数据，通常更偏向低延迟和 best effort
- `rclcpp::ServicesQoS()`：适合服务通信
- `rclcpp::ParametersQoS()` 和 `rclcpp::ParameterEventsQoS()`：适合参数相关通信
- `rclcpp::RosoutQoS()`：适合 ROS 日志输出
- `rclcpp::ClockQoS()`：适合时钟消息

### 消息回调

#### Executor

- [ros2回调调度原理](https://fishros.org.cn/forum/topic/1783/ros2回调调度原理-调用-spin-时-ros-2-都在做什么)

在 ROS2 中，执行管理由执行器（Executor）来处理。执行器使用底层操作系统的一个或多个线程来调用订阅、定时器、服务服务器、动作服务器等的回调，以响应传入的消息和事件。明确的执行器类在rclcpp的 `executor.hpp`中，rclpy的`executors.py`中

Executor的基本用法是 `spin()` 函数，其内部会创建一个默认的单线程执行器，并将节点添加到该执行器中，然后调用执行器的`spin()`方法来处理回调函数

- `rclcpp::spin(node)`会阻塞当前线程并持续处理节点的回调函数，直到节点被关闭或程序退出
  - 其等价于以下代码：

  ```cpp
  rclcpp::executors::SingleThreadedExecutor executor;
  executor.add_node(node);
  executor.spin();
  ```

- `rclcpp::spinOnce(node)`会处理一次回调函数后返回，不会持续阻塞线程

![Executor](executor.png)

结合上图来看，执行器调用 `spin()` 之后，工作流程可以理解成三步：

1. `wait`：执行器先在等待集上阻塞，等待 `/goal`、`/cmd`、`/odom` 这些来源里出现新消息，或者等待定时器到期
2. `take`：一旦某个消息或事件就绪，执行器就从中间件里把它取出来
3. `execute`：最后执行器调用对应的回调函数，比如 `onGoal`、`nextCmd`、`processOdom`

这里和 ROS1 的一个重要区别是，ROS2 的客户端库不会自己再维护消息队列，而是尽量让消息留在中间件中，由[[ROS2通信#Qos]]决定如何暂存和交付。等待集就是执行器用来统一监听这些消息源和定时器的机制：你可以把它理解成一个“事件通知集合”，每个对象都有一个二进制标志，标志为 1 表示已经就绪，可以被执行器处理

某些情况下，用户可能需要直接使用执行器来更细粒度地控制回调的处理，例如将处理回调的线程与主线程分离，避免回调函数阻塞主线程，或者在多线程环境中同时处理多个回调函数，这时`spin()`就不够用了，需直接使用执行器，例如，创建一个单线程执行器来处理回调函数：

```cpp
int main(int argc, char * argv[]) {
    rclcpp::init(argc, argv);
    auto node = std::make_shared<MyNode>();
    rclcpp::executors::SingleThreadedExecutor executor; // 创建一个单线程执行器
    executor.add_node(node); // 将节点添加到执行器中
    auto spinner = std::thread([&executor]() {executor.spin();}); // 在一个单独的线程中运行执行器，这里使用lambda表达式将executor作为参数传递给线程函数
    // 在主线程中执行其他任务
    rclcpp::shutdown(); // 关闭ROS2，停止执行器
    spinner.join(); // 等待执行器线程结束
    return 0;
}
```

rclcpp 提供了三种执行器类型，它们派生自一个共享的父类`rclcpp::Executor`

![executor_types](executor_types.png)

- 多线程执行器创建可配置数量的线程，以允许并行处理多个消息或事件
- 静态单线程执行器优化了扫描节点结构的运行时成本，添加节点时，它仅执行一次对节点订阅、计时器、service、action的扫描，而其他两个执行程序会定期扫描此类更改。因此，静态单线程执行器应仅与在初始化期间创建所有订阅、计时器等的节点一起使用

其它executor相关函数:

```cpp
rclcpp::executors::SingleThreadedExecutor executor; // 创建一个单线程执行器
rclcpp::executors::MultiThreadedExecutor executor( // 创建一个多线程执行器
    rclcpp::ExecutorOptions(),
    4  // 线程数，默认为 CPU 核心数
);
rclcpp::executors::StaticSingleThreadedExecutor executor; // 创建一个静态单线程执行器
executor.remove_node(node); // 从执行器中移除一个节点，停止处理该节点的回调函数
executor.cancel(); // 取消正在执行的回调函数
executor.spin_some(std::chrono::milliseconds(10)); // 处理当前可用的回调函数，但不会阻塞线程
```

也可以使用指针来创建执行器：

```cpp
std::shared_ptr<rclcpp::Executor> executor = std::make_shared<rclcpp::executors::MultiThreadedExecutor>();
executor->add_node(node);
executor->spin();
```

#### Callback Group

Callback Group（回调组）是 ROS2 中用于管理和组织回调函数的一种机制。在 ROS2 中，每一个回调（订阅、定时器、服务等）都可以被分配到不同的 Callback Group 中。不同 Group 之间可以并行执行，而同一个 Group 内的回调则可以被限制为互斥执行

合理的使用 Callback Group 可以有效避免回调函数之间的资源竞争和死锁问题，同时也能提升系统的响应速度和稳定性。很多莫名其妙的卡死问题，本质上都是 Callback Group 使用不当导致的。例如两个互相依赖的回调被放在同一个互斥组中，就可能形成死锁；而多个高频回调如果没有合理分组，又可能导致线程资源被耗尽

回调组有两种类型：

- Mutually Exclusive（互斥组）：同一组内的回调函数不会并行执行，适用于需要保护共享资源的回调
- Reentrant（可重入组）：同一组内的回调函数可以并行执行，适用于没有资源竞争的回调

不同回调组的回调可以并行执行。多线程执行器使用其线程作为池，根据这些条件尽可能并行处理尽可能多的回调

在 rclcpp 中，可以通过 Node 类的`create_callback_group()`函数创建这样一个回调组。在 rclpy 中，可以通过调用特定回调组类型的构造函数来完成相同的操作。回调组必须在节点的执行过程中保留（例如作为类成员），否则执行者将无法触发回调。然后，在创建订阅、定时器等时可以指定此回调组，例如，通过订阅选项：

```cpp
my_callback_group = create_callback_group(rclcpp::CallbackGroupType::MutuallyExclusive);
rclcpp::SubscriptionOptions options; // 创建订阅选项对象
options.callback_group = my_callback_group; // 将回调组分配给订阅选项
my_subscription = create_subscription<Int32>("/topic", rclcpp::SensorDataQoS(), callback, options);
// 在创建订阅时指定QoS，同时将回调组分配给订阅选项
```

所有没有指定回调组的订阅、定时器等都被分配到默认回调组。可以通过`NodeBaseInterface::get_default_callback_group()`(rclcpp)和 `Node.default_callback_group`(rclpy)查询默认回调组

在 rclcpp 中，Executor 基类还具有函数`add_callback_group()`，可以将回调组分配给不同的执行器。通过使用操作系统调度器配置底层线程，可以使特定的回调优先于其他回调。例如，可以将控制循环的订阅和定时器优先于节点的所有其他订阅和标准服务。`examples_rclcpp_cbg_executor` package 提供了该机制的演示

#### Scheduling Semantics

> 调度语义（Scheduling Semantics）指的是系统或程序在分配任务、资源或事件时，所遵循的逻辑规则与行为准则

如果回调函数的处理时间短于消息和事件发生的周期，执行器基本上按照先进先出（FIFO）的顺序处理它们。然而，如果某些回调函数的处理时间较长，消息和事件将在堆栈的较低层次上排队。等待集机制对这些队列向执行器仅报告了非常少的信息。具体而言，它只报告某个主题是否有任何消息。执行器使用这些信息以循环轮询的方式处理消息（包括服务和动作），而不是按照先进先出的顺序。下面的流程图可视化了这种调度语义

![Scheduling Semantics](Scheduling_Semantics.png)

## ROS2节点通信

### 话题

![话题通信示意图](ROS2/image/ROS2通信/Topic.jpg)

话题（Topic）是ROS2中用于发布和订阅消息的通信机制。它允许节点之间以异步方式交换数据

发布者使用接口类创建消息 ➤ 序列化（将结构化数据转化为字节流） ➤ 发送，订阅者接收字节流 ➤ 反序列化 ➤ 得到可读消息内容

同一个话题，所有的发布者和接收者必须使用相同消息接口

#### ROS2话题工具

- GUI工具：Node Graph （不是`rqt_graph`，这个是ROS里面的）
    打开`rqt`后，选择插件`Introspection` ➤ `Node Graph`，可以查看当前系统中所有节点和话题的关系图
- CLI工具：ros2 topic
  - 查看帮助：`ros2 topic -h`
  - 查看当前系统中的所有话题：`ros2 topic list`
  - 查看某个话题的详细信息：`ros2 topic info <topic_name>` `-v` 表示展示详细信息
  - 查看消息类型的具体信息`ros2 interface show <msg_type>` （例如：`ros2 interface show std_msgs/msg/String`）
  - 查看某个话题的消息内容：`ros2 topic echo <topic_name>`，只读取一条消息：`ros2 topic echo <topic_name> --once`
  - 手动发布消息到某个话题：`ros2 topic pub <topic_name> <msg_type> <msg_data>` （例如：`ros2 topic pub /chatter std_msgs/msg/String 'data: "123"'`）

#### 使用RCLCPP实现话题通信

假设：

- 控制节点创建一个话题发布者，发布控制命令（command）话题，接口类型为字符串（string），控制接点通过发布者发布控制命令（前进、后退、左转、右转、停止）。
- 被控节点创建一个订阅者，订阅控制命令，收到控制命令后根据命令内容打印对应速度出来。

[相关函数文档](https://docs.ros2.org/latest/api/rclcpp/classrclcpp_1_1Node.html)

##### 编写c发布者节点

- 修改CMakeLists.txt

  ```cmake
  find_package(rclcpp REQUIRED)
  find_package(std_msgs REQUIRED)

  add_executable(topic_publisher_01 src/topic_publisher_01.cpp)
  ament_target_dependencies(topic_publisher_01 rclcpp std_msgs) # 添加依赖
  install(TARGETS
  topic_publisher_01
  DESTINATION lib/${PROJECT_NAME}
  )
  ```

- 在package.xml中添加依赖

  ```xml
  <depend>rclcpp</depend>
  <depend>std_msgs</depend>
  ```

- 编写发布者节点

  ```cpp
  #include "rclcpp/rclcpp.hpp"
  #include "std_msgs/msg/string.hpp"

  class TopicPublisher01 : public rclcpp::Node // 创建节点类
  {
    public:
    // 构造函数,有一个参数为节点名称
    TopicPublisher01(std::string name) : Node(name)
    {
      RCLCPP_INFO(this->get_logger(), "大家好，我是%s.", name.c_str());
      // 创建发布者
      command_publisher_ = this->create_publisher<std_msgs::msg::String>("command", 10);
      // 创建定时器，500ms为周期，定时发布
      timer_ = this->create_wall_timer(std::chrono::milliseconds(500), std::bind(&TopicPublisher01::timer_callback, this));
    }

    private:
      void timer_callback()
      {
        // 创建消息
        std_msgs::msg::String message;
        message.data = "forward";
        // 日志打印
        RCLCPP_INFO(this->get_logger(), "Publishing: '%s'", message.data.c_str());
        // 发布消息
        command_publisher_->publish(message);
      }
      // 声名定时器指针
      rclcpp::TimerBase::SharedPtr timer_;
      // 声明话题发布者指针
      rclcpp::Publisher<std_msgs::msg::String>::SharedPtr command_publisher_;
  };

  int main(int argc, char **argv)
    {
      rclcpp::init(argc, argv);
      /*创建对应节点的共享指针对象*/
      auto node = std::make_shared<TopicPublisher01>("topic_publisher_01");
      /* 运行节点，并检测退出信号*/
      rclcpp::spin(node); // spin循环节点
      rclcpp::shutdown();
      return 0;
    }
  ```

##### 编写c订阅者节点

- 修改CMakeLists.txt
- 在package.xml中添加依赖
- 编写发布者节点
  
  ```cpp
  #include "rclcpp/rclcpp.hpp"
  #include "std_msgs/msg/string.hpp"

  class TopicSubscribe01 : public rclcpp::Node
  {
    public:
    TopicSubscribe01(std::string name) : Node(name)
    {
      RCLCPP_INFO(this->get_logger(), "大家好，我是%s.", name.c_str());
      // 创建一个订阅者订阅话题
      command_subscribe_ = this->create_subscription<std_msgs::msg::String>("command", 10, std::bind(&TopicSubscribe01::command_callback, this, std::placeholders::_1));
    }

    private:
    // 声明一个订阅者
    rclcpp::Subscription<std_msgs::msg::String>::SharedPtr command_subscribe_;
    // 收到话题数据的回调函数
    void command_callback(const std_msgs::msg::String::SharedPtr msg)
    {
      double speed = 0.0f;
      if(msg->data == "forward")
      {
        speed = 0.2f;
      }
      RCLCPP_INFO(this->get_logger(), "收到[%s]指令，发送速度 %f", msg->data.c_str(),speed);
    }
  };

  int main(int argc, char **argv)
  {
    rclcpp::init(argc, argv);
    /*创建对应节点的共享指针对象*/
    auto node = std::make_shared<TopicSubscribe01>("topic_subscribe_01");
    /* 运行节点，并检测退出信号*/
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
  }
  ```

##### c测试

```bash
ros2 run example_topic_rclcpp topic_subscribe_01 # 运行订阅者节点
ros2 run example_topic_rclcpp topic_publisher_01 # 运行发布者节点
ros2 topic list # 查看当前系统中的所有话题
ros2 topic echo /command # 查看/command话题的消息内容
ros2 topic pub /command std_msgs/msg/String "{data: forward}" # 手动发布消息到/command话题
rqt #查看话题关系图
```

#### 使用RCLPY实现话题通信

[相关函数文档](https://docs.ros2.org/latest/api/rclpy/api/node.html)

修改`setup.py`文件，添加节点入口：

```python
entry_points={
  'console_scripts': [
    "topic_publisher_02 = example_topic_rclpy.topic_publisher_02:main",
    "topic_subscribe_02 = example_topic_rclpy.topic_subscribe_02:main"
  ],
},"topic_publisher_02 = example_topic_rclpy.topic_publisher_02:main",
    "topic_subscribe_02 = example_topic_rclpy.topic_subscribe_02:main"
```

#### 编写py发布者节点

```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class NodePublisher02(Node):
    def __init__(self,name):
        super().__init__(name)
        self.get_logger().info("大家好，我是%s!" % name)
        self.command_publisher_ = self.create_publisher(String,"command", 10) 
        self.timer = self.create_timer(0.5, self.timer_callback)
    
    def timer_callback(self):
        """
        定时器回调函数
        """
        msg = String()
        msg.data = 'backup'
        self.command_publisher_.publish(msg) 
        self.get_logger().info(f'发布了指令：{msg.data}')    #打印一下发布的数据

def main(args=None):
    rclpy.init(args=args) # 初始化rclpy
    node = NodePublisher02("topic_publisher_02")  # 新建一个节点
    rclpy.spin(node) # 保持节点运行，检测是否收到退出指令（Ctrl+C）
    rclpy.shutdown() # 关闭rclpy
```

##### 编写py订阅者节点

```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class NodeSubscribe02(Node):
    def __init__(self,name):
        super().__init__(name)
        self.get_logger().info("大家好，我是%s!" % name)
        # 创建订阅者
        self.command_subscribe_ = self.create_subscription(String,"command",self.command_callback,10)
    def command_callback(self,msg):
        speed = 0.0
        if msg.data=="backup":
            speed = -0.2
        self.get_logger().info(f'收到[{msg.data}]命令，发送速度{speed}')

def main(args=None):
    rclpy.init(args=args) # 初始化rclpy
    node = NodeSubscribe02("topic_subscribe_02")  # 新建一个节点
    rclpy.spin(node) # 保持节点运行，检测是否收到退出指令（Ctrl+C）
    rclpy.shutdown() # 关闭rclpy
```

##### py测试

```bash
ros2 run example_topic_rclpy topic_publisher_02
ros2 run example_topic_rclpy topic_subscribe_02
```

### 服务

![服务通信示意图](ROS2/image/ROS2通信/Service.jpg)

服务（Service）是ROS2中用于请求-响应式通信的机制。它允许节点之间进行同步通信。
相较于话题，服务是双向的，客户端发送请求，服务端响应请求。

客户端发送请求 ➤ 序列化 ➤ 发送 ➤ 服务端接收请求 ➤ 反序列化 ➤ 处理请求 ➤ 返回响应 ➤ 客户端接收响应

注意：

- 同一个服务（名称相同）有且只能有一个节点来提供
- 同一个服务可以被多个客户端调用

#### ROS2服务工具

- GUI工具：Service Graph
  打开`rqt`后，选择插件`Introspection` ➤ `Service Graph`，可以查看当前系统中所有服务和节点的关系图。
- CLI工具：ros2 service

  ```bash
  ros2 service list # 查看当前系统中的所有服务
  ros2 service type <service_name> # 查看某个服务的类型
  ros2 service find example_interfaces/srv/AddTwoInts # 查找某个服务的提供者
  ros2 service call <service_name> <service_type> <request_data> # 手动调用某个服务
  ```

#### 服务相关函数

**create_service()**：

```cpp
this->create_service<<Service类型>>(
  "<服务名称>",
  std::bind(&<类名>::<回调函数>, this, std::placeholders::_1, std::placeholders::_2),
  <QoS配置>,  // 可省略，默认即可
  <回调组>    // 可省略，默认即可
);
```

**create_client()**：

```cpp
this->create_client<<Service类型>>(
  "<服务名称>",
  <QoS配置>,  // 可省略，默认即可
  <回调组>    // 可省略，默认即可
);
```

**async_send_request**：

```cpp
<客户端对象指针>->async_send_request(
  <请求对象指针>,
  std::bind(&<类名>::<回调函数名>, this, std::placeholders::_1)
);
```

**wait_for_service()**：

```cpp
<客户端对象指针>->wait_for_service(
  std::chrono::seconds(10) // 等待服务的超时时间
);
```

#### 使用RCLCPP实现服务通信

假设：

因为还没有学习如何自定义接口，所以我们先借着上一节的两数相加的示例接口，利用rclcpp提供的接口实现两数相加的服务端和客户端

##### 编写c服务端节点

1. 编写一个简单的节点
2. 导入接口

## 动作

Services 通信存在以下弊端，在长耗时的请求与响应过程中：

- 客户端不能确定请求是否成功发送到服务端
- 服务端无法向客户端发送反馈
- 客户端无法取消请求

针对以上问题，ROS2引入了动作（Action）通信机制，它是基于服务和话题通信机制之上的一种更高级的通信方式，适用于需要长时间执行的任务

Action的三大组成部分：

- 目标（Goal）：即Action客户端告诉服务端要做什么，服务端针对该目标要有响应
- 反馈（Feedback）：服务端在执行目标过程中，可以向客户端发送反馈信息，告知当前进展情况
- 结果（Result）：服务端在完成目标后，向客户端发送最终结果

![动作通信示意图](Action.gif)

一个Action = 三个服务+两个话题

- 三个服务分别是：1.目标传递服务 2.结果传递服务 3.取消执行服务
- 两个话题：1.反馈话题（服务端发布，客户端订阅） 2.状态话题（服务端发布，客户端订阅）

### action cli

```bash
ros2 action list # 查看当前系统中的所有动作
  -t # 查看动作类型
ros2 action info <action_name> # 查看某个动作的详细信息
ros2 action send_goal <action_name> <action_type> <goal_data> # 手动发送一个目标
  --feedback # 显示反馈信息
```

#### 自定义动作接口

在功能包`example_interfaces`中创建一个`action`文件夹，在该文件夹中创建一个后缀为`.action`的文件，写入消息类型，顺序必须是goal、result、feedback，每个部分之间用`---`分隔开，例如：

```action
# SumInts.action
# goal
int64 num
---
# result
int64 sum
---
# feedback
float64 progress
```

packages.xml

```xml
<depend>action_msgs</depend>
<depend>rosidl_default_generators</depend>
<member_of_group>rosidl_interface_packages</member_of_group>
```

CMakeLists.txt

```txt
find_package(rosidl_default_generators REQUIRED)
rosidl_generate_interfaces(${PROJECT_NAME}
  "action/SumInts.action"
)
```

编译后会在`install/example_interfaces/include`或`install/example_interfaces/local/lib/python3.10`目录下生成相应的接口文件

#### RCLCPP实现

- [Action API](https://docs.ros2.org/latest/api/rclcpp_action/)

功能包需要依赖`rclcpp`、`rclcpp_action`和`example_interfaces`（因为我们之前的接口是放在example_interfaces包中的）：

```cpp
#include "rclcpp/rclcpp.hpp"
#include "rclcpp_action/rclcpp_action.hpp"
#include "example_interfaces/action/sum_ints.hpp"
```

##### Action Server

服务端编写的一般步骤：

1. 创建一个继承自`rclcpp::Node`的类，在构造函数中创建一个动作服务器，绑定处理目标请求、取消请求和接受目标请求的回调函数
2. 在处理目标请求的回调函数中，判断请求是否合法，返回接受或拒绝
3. 在处理取消请求的回调函数中，返回接受或拒绝
4. 在处理(已接受的目标请求)的回调函数中，将执行目标的函数放到一个新的线程中，避免阻塞主线程，导致无法处理新的请求和取消请求
5. 在执行目标的函数中，执行具体的任务逻辑，定期检查是否有取消请求，发布反馈信息，最后返回结果

```cpp
using namespace std::placeholders;
using SumInts = example_interfaces::action::SumInts;
using GoalHandleProgress = rclcpp_action::ServerGoalHandle<SumInts>;

class ActionServer : public rclcpp::Node
{
public:
    ActionServer() : Node("action_server")
    {
        action_server_ = rclcpp_action::create_server<SumInts>(
            this,
            "sum_ints", // 动作名称
            std::bind(&ActionServer::handle_goal, this, _1), // 处理目标请求的回调函数
            std::bind(&ActionServer::handle_cancel, this, _1), // 处理取消请求的回调函数
            std::bind(&ActionServer::handle_accepted, this, _1) // 处理接受目标请求的回调函数
        );
    }
```

- action_server_是一个动作服务器指针，指向创建的动作服务器对象，需要在类的成员变量中声明
- 这里使用了`std::bind`将成员函数绑定为回调函数，并使用占位符`_1`表示回调函数的参数，同时将this排除出回调函数的参数列表，因为成员函数会隐式地接受一个指向类实例的指针（即this指针）

类的私有成员变量和函数

```cpp
private:
    rclcpp_action::Server<SumInts>::SharedPtr action_server_; // 声明一个动作服务器指针
    void handle_goal(const std::shared_ptr<SumInts::Goal> goal) // 处理目标请求的回调函数
    {
        if (goal->num < 1) {
        return rclcpp_action::GoalResponse::REJECT;
        }
        return rclcpp_action::GoalResponse::ACCEPT_AND_EXECUTE;
    };
    void handle_cancel(const std::shared_ptr<SumInts::Goal> goal) // 处理取消请求的回调函数
    {
        return rclcpp_action::CancelResponse::ACCEPT;
    };
```

- 处理目标请求的回调函数`handle_goal`接受一个指向目标请求的智能指针作为参数，需指定消息类型（即`<SumInts::Goal>`）
- 处理取消请求的回调函数`handle_cancel`接受一个指向目标请求的智能指针作为参数
- `GoalResponse`和`CancelResponse`是`rclcpp_action`命名空间下的枚举类，请自行点击查看具体定义

```cpp
    void handle_accepted(const std::shared_ptr<SumInts::Goal> goal) // 处理接受目标请求的回调函数
    {
      std::thread{std::bind(&ActionServer::execute, this, _1), goal}.detach(); // 将执行放到一个新的线程中，避免阻塞主线程，导致无法处理新的请求和取消请求
    };
    void execute(const std::shared_ptr<GoalHandleSumInts> goal_handle)
    {
        rclcpp::Rate loop_rate(10.0); // 设置循环频率为10Hz，即每100ms执行一次循环
        const auto goal = goal_handle->get_goal(); // 获取目标请求
        auto feedback = std::make_shared<SumInts::Feedback>(); //  SumInts::Feedback是action接口中定义的feedback类型
        auto result = std::make_shared<SumInts::Result>(); // SumInts::Result是 action接口中定义的result类型
        int64_t sum= 0;
        for (int i = 1; (i <= goal->num) && rclcpp::ok(); i++){
            sum += i;
            if (goal_handle->is_canceling()) { // 检测是否有取消请求
                result->sum = sum;
                goal_handle->canceled(result); // 将当前结果返回给客户端，告知任务取消了
                RCLCPP_INFO(this->get_logger(), "任务取消");
                return;
            }
            feedback->SumInts = (double_t)i / goal->num;
            goal_handle->publish_feedback(feedback);
            RCLCPP_INFO(this->get_logger(), "连续反馈中，进度：%.2f", feedback->SumInts);
            loop_rate.sleep();
        }
        if (rclcpp::ok()){
            result->sum = sum;
            goal_handle->succeed(result);
            RCLCPP_INFO(this->get_logger(), "任务完成！");
        }
    };
};
```

- `get_goal()`函数用于获取目标请求的内容
- `publish_feedback(feedback)`函数用于发布反馈信息，参数为一个指向反馈消息的智能指针，反馈消息会被封装在一个`WrappedFeedback`对象中发送给客户端，客户端可以通过回调函数获取反馈消息的内容
- `succeed(result)`函数用于向客户端发送结果，参数为一个指向结果消息的智能指针，result消息会被封装在一个`WrappedResult`对象中发送给客户端，客户端可以通过回调函数获取结果消息的内容
- 需要在`execute`函数中定期检查是否有取消请求，如果有则调用`canceled()`函数向客户端发送当前结果，并告知任务取消了

main函数

```cpp
int main(int argc, char ** argv)
{
  rclcpp::init(argc, argv);
  auto action_server = std::make_shared<ActionServer>();
  rclcpp::spin(action_server);
  rclcpp::shutdown();
  return 0;
}
```

##### Action Client

客户端编写的一般步骤：

1. 创建一个继承自`rclcpp::Node`的类，在构造函数中创建一个动作客户端
2. 编写一个发送目标的函数，检查客户端是否初始化，等待服务端上线，构造目标消息，配置发送目标的回调函数，异步发送目标
3. 在目标响应回调函数中，判断目标请求是否被接受，如果被接受则等待结果中，如果被拒绝则打印错误信息
4. 在反馈回调函数中，处理服务端发送的反馈信息，例如打印当前进度
5. 在结果回调函数中，判断结果状态，如果任务执行成功则打印最终结果，如果任务被中止或取消则打印错误信息

```cpp
using namespace std::placeholders;
using SumInts = example_interfaces::action::SumInts;
using GoalHandleSumInts = rclcpp_action::ClientGoalHandle<SumInts>;

class ActionClient : public rclcpp::Node
{
public:
  ActionClient() : Node("action_client")
  {
    action_client_ = rclcpp_action::create_client<SumInts>(
      this,"sum_ints"
    );
  }
  void send_goal(int64_t num)
  {
    if (!action_client_){ // 检查客户端是否初始化
      return;
    }
    if (!action_client_->wait_for_action_server(std::chrono::seconds(10))) { // 等待服务端上线
      return;
    }
    auto goal_msg = SumInts::Goal(); // 构造目标消息
    goal_msg.num = num;
    // 配置发送目标的回调
    auto send_goal_options = rclcpp_action::Client<SumInts>::SendGoalOptions();
    send_goal_options.goal_response_callback = std::bind(&ActionClient::goal_response_callback, this, _1);
    send_goal_options.feedback_callback = std::bind(&ActionClient::feedback_callback, this, _1, _2);
    send_goal_options.result_callback = std::bind(&ActionClient::result_callback, this, _1);
    // 异步发送目标
    auto goal_handle_future = action_client_->async_send_goal(goal_msg, send_goal_options);
  }
```

- `action_client_`是一个动作客户端指针，指向创建的动作客户端对象，需要在类的成员变量中声明
- `wait_for_action_server()`函数用于等待服务端上线，参数为一个表示等待超时时间的`std::chrono`对象，如果在指定时间内服务端没有上线则返回false
- `SendGoalOptions`结构体用于配置发送目标的回调函数，包括目标响应回调、反馈回调和结果回调，分别对应服务端接受或拒绝目标请求、服务端发送反馈信息和服务端发送结果的情况
- `async_send_goal()`函数用于异步发送目标，参数为目标消息和发送选项，返回一个`std::shared_future`对象，可以通过该对象获取发送目标的结果，例如是否成功发送目标请求以及服务端的响应情况

类的私有成员变量和函数

```cpp
private:
  rclcpp_action::Client<SumInts>::SharedPtr action_client_;
  void goal_response_callback(GoalHandleSumInts::SharedPtr goal_handle) // 目标响应回调
  {
    if (!goal_handle) {
      // 目标请求被拒绝
    } else {
      // 目标请求被接受，等待结果中
    }
  }
  void feedback_callback(GoalHandleSumInts::SharedPtr, const std::shared_ptr<const SumInts::Feedback> feedback)
  {
    int32_t progress = static_cast<int32_t>(feedback->SumInts * 100);
    RCLCPP_INFO(this->get_logger(), "当前进度: %d%%", progress);
  }
  void result_callback(const GoalHandleSumInts::WrappedResult & result)
  {
    switch (result.code) {
      case rclcpp_action::ResultCode::SUCCEEDED:
        break;
      case rclcpp_action::ResultCode::ABORTED:
        return;
      case rclcpp_action::ResultCode::CANCELED:
        return;
      default:
        return;
    }
  }
};
```

main函数

```cpp
int main(int argc, char ** argv)
{
  rclcpp::init(argc, argv);
  auto action_client = std::make_shared<ActionClient>();
  int64_t num = 10; // 目标请求的参数，例如要求服务端计算1到10的和
  action_client->send_goal(num);
  rclcpp::spin(action_client);
  rclcpp::shutdown();
  return 0;
}
```

##### package.xml

```xml
<depend>rclcpp</depend>
<depend>rclcpp_action</depend>
<depend>my_interfaces</depend>
```

##### CMakeLists.txt

```cmake
find_package(rclcpp REQUIRED)
find_package(rclcpp_action REQUIRED)
find_package(my_interfaces REQUIRED)

add_executable(action_server src/action_server.cpp)
ament_target_dependencies(action_server rclcpp rclcpp_action my_interfaces)

add_executable(action_client src/action_client.cpp)
ament_target_dependencies(action_client rclcpp rclcpp_action my_interfaces)

install(TARGETS
  action_server
  action_client
  DESTINATION lib/${PROJECT_NAME}
)
```

#### RCLPY实现

```python
import time
import rclpy
import rclpy.action
from rclpy.node import Node
from example_interfaces.action import SumInts
```

##### Action Server in RCLPY

相较于RCLCPP，RCLPY的API设计更为简洁，使用起来也更为方便，服务端编写的一般步骤：

1. 创建一个继承自`rclpy.node.Node`的类，在构造函数中创建一个动作服务器，只需绑定`execute_callback`回调函数
2. 在`execute_callback`中实现目标请求处理逻辑，执行具体的任务逻辑，定期检查是否有取消请求，发布反馈信息，最后返回结果

```py
class ActionServer(Node):
    def __init__(self):
        super().__init__('action_server') # super()函数用于调用父类的构造函数，初始化节点名称为'action_server'
        self._action_server = ActionServer(
            self,SumInts,'sum_ints',self.execute_callback)
    def execute_callback(self, goal_handle):
        feedback_msg = SumInts.Feedback()
        sum = 0
        for i in range(1, goal_handle.request.num + 1):
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                return SumInts.Result()
            sum += i
            feedback_msg.progress = i / goal_handle.request.num
            goal_handle.publish_feedback(feedback_msg)
            time.sleep(1)
        goal_handle.succeed()
        result = SumInts.Result()
        result.sum = sum
        return result

def main(args=None):
    rclpy.init(args=args)
    action_server = ActionServer()
    rclpy.spin(action_server)
    rclpy.shutdown()
if __name__ == '__main__':
    main()
```

##### Action Client in RCLPY

Python版本的Action Client反而比Server更复杂一些，客户端编写的一般步骤：

```py
class ActionClient(Node):
    def __init__(self):
        super().__init__('action_client')
        self._action_client = ActionClient(self, SumInts, 'sum_ints')
    def send_goal(self, num):
        goal_msg = SumInts.Goal()
        goal_msg.num = num
        self._action_client.wait_for_server()
        self._send_goal_future = self._action_client.send_goal_async(goal_msg, feedback_callback=self.feedback_callback)
        self._send_goal_future.add_done_callback(self.goal_response_callback)
    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            return
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)
    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info('最终计算结果：sum = %d' % result.sum)
        rclpy.shutdown()
    def feedback_callback(self, feedback_msg):
        feedback = (int)(feedback_msg.feedback.progress * 100)

def main(args=None):
    rclpy.init(args=args)
    action_client = ActionClient()
    action_client.send_goal(10)
    rclpy.spin(action_client)
    rclpy.shutdown()
if __name__ == '__main__':
    main()
```

- `send_goal_async()`函数用于异步发送目标，参数为目标消息和反馈回调函数，返回一个`Future`对象，可以通过该对象获取发送目标的结果
- `add_done_callback()`函数用于为`Future`对象添加回调函数，当`Future`对象的状态发生变化时会调用相应的回调函数，例如当发送目标请求完成后会调用`goal_response_callback`函数，当获取结果完成后会调用`get_result_callback`函数
- `goal_response_callback`函数用于处理目标响应，判断目标请求是否被接受，如果被接受则等待结果中，如果被拒绝则打印错误信息
- `get_result_callback`函数用于处理结果，判断结果状态，如果任务执行成功则打印最终结果，如果任务被中止或取消则打印错误信息
- `feedback_callback`函数用于处理服务端发送的反馈信息，例如打印当前进度

##### Setup.py

`setup.py`内容省略，请参考前面章节中RCLPY实现话题通信的setup.py文件，添加相应的依赖和节点入口即可
