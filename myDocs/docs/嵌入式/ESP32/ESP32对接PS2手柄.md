# ESP32对接PS2手柄

## PS2手柄通信方式

PS2手柄的通信分为两段：

1. 手柄本体与接收器之间通信  
   无线手柄通常通过 2.4G 私有无线协议通信；有线手柄则没有这一段无线链路

2. 接收器与 MCU 之间通信  
   这部分取决于接收器类型，常见有两种：

- PS2 接收器：通过 PS2 手柄协议与 MCU 通信，电气连接通常为 `CLK`、`CMD`、`ATT/CS`、`DAT`，形式上类似 SPI
- USB 接收器：通过 USB HID 协议与 MCU 通信，电气连接为 `USB D+`、`USB D-`、`5V`、`GND`，MCU 需要具备 USB Host 能力

## PS2X

对于 PS2 接收器，可以使用 [madsci1016/Arduino-PS2X](https://github.com/madsci1016/Arduino-PS2X) 这类库模拟 PS2 手柄协议，参考：[Arduino 結合 PS2 無線手把簡單上手](https://blog.jmaker.com.tw/ps2x/)

## USB HID

HID 即 Human Interface Device，人机接口设备。USB HID 是 USB 协议中的一个设备类别，常见的HID设备包括键盘、鼠标、游戏手柄、摇杆、遥控器等

对于 USB 接收器，MCU 不能像 PS2 接收器那样通过 GPIO 模拟时序读取数据，而是需要作为 USB Host 工作。USB Host 需要完成设备枚举、读取设备描述符、识别 HID 接口，并周期性接收 HID Report

USB HID 手柄的数据通常以 Report 的形式发送，例如按键状态、摇杆 X/Y 轴、扳机值等。不同手柄或不同接收器的 Report 格式可能不完全相同，因此适配时通常需要先打印原始 HID Report，再根据实际变化关系解析出按键和摇杆数据
