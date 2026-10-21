# UART

References: [UART：了解通用异步接收器/发送器的硬件通信协议 | 亚德诺半导体](https://www.analog.com/cn/resources/analog-dialogue/articles/uart-a-hardware-communication-protocol.html)

UART，即**通用异步接收器/发送器**，是微控制器（MCU）内部负责收发串行数据的物理电路模块，它采用的通信协议称为UART协议，一般被称为串口通信

## 帧协议

![[帧协议.jpg]]

帧协议由多个UART数据包组成，一个数据包传输 8bit（1byte），所以帧协议的基本单位是 1byte

### Data

帧协议的主体是其上的多字节数据 Data\[N\]，Data\[n\] 是一个字节，通常表示为两位十六进制数：0x00~0xFF，将要传输的数据 EData\[M\] 依附于这些多字节数据之上：

- 最原始的方法就是一一对应，令 N=M，那么 EData\[m\] 数据类型为 `uint8_t`，可以表示 0~255 的十进制范围。这种方法也适用于发送文本（ASCII 码用一个字节表示一个字符）
- 当我要传输多位数或浮点数时 0~255 显然不够用，比如我们的 EData\[m\] 是舵机角度，范围是 3.142~-3.142：
	- 我们可以设定 EData\[m\] 数据类型为 `float32_t`，那么 EData\[m\] 就需要4个字节表示，N=4M
	- 我们还可以设置定点值（fixed-point value），约定只保留3位小数，那么 EData\[m\] 就要乘以1000（缩放因子），从而将浮点数转换为整数，这样 EData\[m\] 数据类型就可以用 `int16_t`，需要2个字节表示，N=2M。相较于 `float32_t` 少了2字节，传输效率更高

传输 Data 时还需要选择[[通信#端序]]

