# ESP32

ESP32 是乐鑫科技（Espressif）推出的一款**低功耗**、高性能的微控制器芯片
- **集成 Wi-Fi 和蓝牙功能**，广泛用于物联网、智能家居、可穿戴设备等项目
- 内置 SRAM 和 Flash，支持丰富的外设接口（UART、SPI、I2C、ADC、DAC、PWM 等）
- 支持低功耗模式，适合电池供电场景，且价格低廉、生态成熟

## 芯片型号辨识

芯片系列：`SP32-S3` 
-  双核 Xtensa
- 支持 Wi-Fi + BLE
- 面向 AI/语音/USB/IoT 应用
- 比老款 ESP32 更适合做 USB 设备、图形、传感器和外设控制

模组（把芯片、Flash、天线相关部分封装好的成品模块）：
- `ESP32-S3-WROOM-1`：`WROOM` 是 Espressif 的模组系列名；`-1` 表示采用PCB板载天线
- `ESP32-S3-WROOM-1U`：`-1U` 表示采用连接器连接外部天线

开发板（board，包含模组）：`esp32-s3-devkitc-1`
- 模组和开发板的名称后面往往还会加上一些外设/板级参数：
	- `N16` = 16MB Flash
	- `R8` = 8MB PSRAM

## 开发环境

ESP IDF 即乐鑫物联网开发框架，可为在Windows、Linux 和macOS 系统平台上开发ESP32 应用程序提供工具链、API、组件和工作流程的支持

### Arduino IDE

- 封装了 ESP IDF 的API，使用C++编程，简化了很多复杂概念，适合新手入门
- 拥有丰富的开源库、外设库

配置ESP32开发环境：[ESP32开发环境搭建（保姆级）](https://zhuanlan.zhihu.com/p/695154124)

#### 下载库遇到的网络问题

已经开启了本地代理，但是在下载库时还是遇到了网络问题，在 **“文件->首选项”** 中设置代理：
![[下载库遇到的网络问题.png]]

同时需要添加用户环境变量（不添加这个没用）：

```powerhell
setx HTTP_PROXY http://127.0.0.1:10808
setx HTTPS_PROXY https://127.0.0.1:10808
```

但是添加上面的全局环境变量会导致其它软件默认走代理，从而导致大模型API连接失败和NPM下载失败等一堆问题，参考这篇反馈：[Rant about IDE 2.X proxy issues on Windows (but also on Linux and MacOS) ](https://forum.arduino.cc/t/rant-about-ide-2-x-proxy-issues-on-windows-but-also-on-linux-and-macos/1406669)，这可能是Arduino的一个BUG

本来以为 Arduino IDE 会是一个很新手友好的、方便的IDE，结果它给我的第一印象很差

### PlatformIO

PlatformIO 是一个跨平台的嵌入式开发工具链和生态系统。它支持多种微控制器（如 ESP32、STM32 等）、多种开发框架（Arduino、ESP-IDF等）以及多个 IDE（VS Code、CLion 等）。PlatformIO 提供统一的项目配置、库管理、编译、烧录、调试和单元测试功能，能大幅简化嵌入式开发和环境配置的复杂度

使用 **Platform IO+VSCode** 的组合可以拥有比Arduino IDE更快的编译、上传代码速度，同时也可以使用VSCode丰富的插件来提高编码效率

配置环境：[DFRobot ESP32 PlatformIO教程](https://wiki.dfrobot.com.cn/ESP32_Platform_IO)

文件结构：

- .pio：工程编译产生的文件
- .vscode：VSCode配置文件
- include：头文件
- lib：库文件
- src：源码文件
- test：测试文件
- .gitignore：git仓库文件
- platformio.ini：项目配置文件

#### 导入外部库

三种方法：

- 在 platformio.ini 里声明 Git 依赖，PlatformIO 会自动下载并管理库版本。在 platformio.ini 中添加：
```ini
lib_deps =
	https://github.com/madsci1016/Arduino-PS2X.git # 以 PS2 库为例
```
- 把库放进项目的 lib 目录，适合离线开发，或者改库源码的情况。把仓库克隆后放到项目目录，PlatformIO 会自动扫描，不需要额外配置
-  PlatformIO Library Registry：如果库已经发布到了 PlatformIO 注册表，可以在 PIO Home -> Libraries 中搜索库，点击添加到项目

#### 修改 Serial Monitor 的默认配置

Serial Monitor 可以用来监听调试串口的日志，要自定义端口号与波特率，在 platformio.ini 里设置：

```ini
monitor_speed = 115200
monitor_port = COM6
monitor_filters = time,default
```