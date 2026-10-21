# Mermaid

Mermaid 是最流行的 Markdown 图表工具之一，它使用简单的文本语法生成各种图表

使用前需要确保你的 Markdown 编辑器或渲染器支持 Mermaid 语法。可下载插件：名称: 
[Markdown Preview Mermaid Support](https://marketplace.visualstudio.com/items?itemName=bierner.markdown-mermaid)

## 支持的图表类型

- 流程图 (Flowchart)
- 序列图 (Sequence Diagram)
- 类图 (Class Diagram)
- 状态图 (State Diagram)
- 甘特图 (Gantt Chart)
- 饼图 (Pie Chart)

## 流程图

```mermaid
graph TD
    A[开始] --> B{条件判断}
    B -->|Yes| C[执行操作A]
    B -->|No| D[执行操作B]
    C --> E[结束]
    D --> E
```

- 流程图方向
  - TD 或 TB：从上到下
  - BT：从下到上
  - RL：从右到左
  - LR：从左到右
- 节点形状
  - A矩形
  - B圆角矩形
  - C菱形（决策）
  - D圆形
  - E旗帜形
- 连接线类型
  - --> 实线箭头
  - -.-> 虚线箭头
  - ==> 粗实线箭头
  - -- 实线
  - -. 虚线

示例：

```mermaid
---
config:
  theme:"neutral"
---

graph TD
    subgraph PC [上位机]
    style PC font-size:16px
        Send[发送指令: AA BB XX YY ZZ CC DD]
        Receive[接收反馈: FF EE MM 02 DD CC]
    end

    subgraph STM32System [STM32 单片机系统]
        UART[USART1 串口模块]
        Process[ProcessPacket 解析]
        Timer[TIM3 定时器中断]
        Loop[Main Loop 定时查询]
        
        GPIO_LED[GPIO 输出控制]
        GPIO_BEEP[GPIO 输出控制]
    end

    subgraph Peripherals [外围硬件]
        LED0[LED0]
        LED1[LED1]
        Buzzer[蜂鸣器]
    end

    %% Data Flow
    Send -->|RX 中断接收| UART
    UART -->|解析| Process
    Process -->|设置模式与周期| Timer
    Process -->|直接控制| GPIO_LED
    Process -->|直接控制| GPIO_BEEP
    
    Timer -->|跑马灯翻转| GPIO_LED
    
    Loop -->|读取状态| GPIO_LED
    Loop -->|读取状态| GPIO_BEEP
    Loop -->|读取ARR周期| Timer
    Loop -->|TX 1000ms反馈| Receive

    GPIO_LED --> LED0
    GPIO_LED --> LED1
    GPIO_BEEP --> Buzzer
```