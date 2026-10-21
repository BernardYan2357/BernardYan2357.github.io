# GPIO(通用输入与输出口)

STM32的组成可分为：核心(core)与外设(Peripherals)

GPIO(General Purpose Input/Output)是最基本、最常用的外设之一。它的功能相对简单：

1. 输入 (Input)： 读取外部引脚的电平状态（高电平或低电平），例如读取按键状态。

2. 输出 (Output)： 控制外部引脚输出高电平或低电平，例如点亮LED。

3. 复用功能 (Alternate Function): GPIO引脚可以被“借给”其他更复杂的外设使用，作为该外设的输入或输出通道。例如，一个GPIO引脚可以被配置为串口(UART)的发送(TX)引脚。

## GPIO的常见函数

```c
void GPIO_DeInit(GPIO_TypeDef* GPIOx); //复位指定外设
void GPIO_AFIODeInit(void); //复位AFIO外设
void GPIO_Init(GPIO_TypeDef* GPIOx, GPIO_InitTypeDef* GPIO_InitStruct); //初始化各参数，需先定义一个结构体
void GPIO_StructInit(GPIO_InitTypeDef* GPIO_InitStruct); //给结构体变量赋默认值
//以下为读写函数
uint8_t GPIO_ReadInputDataBit(GPIO_TypeDef* GPIOx, uint16_t GPIO_Pin);
uint16_t GPIO_ReadInputData(GPIO_TypeDef* GPIOx);
uint8_t GPIO_ReadOutputDataBit(GPIO_TypeDef* GPIOx, uint16_t GPIO_Pin);
uint16_t GPIO_ReadOutputData(GPIO_TypeDef* GPIOx);
void GPIO_SetBits(GPIO_TypeDef* GPIOx, uint16_t GPIO_Pin); //将指定端口设置为高电平
void GPIO_ResetBits(GPIO_TypeDef* GPIOx, uint16_t GPIO_Pin); //将指定端口设置为低电平
void GPIO_WriteBit(GPIO_TypeDef* GPIOx, uint16_t GPIO_Pin, BitAction BitVal); //根据第三个参数设置指定端口的电平
void GPIO_Write(GPIO_TypeDef* GPIOx, uint16_t PortVal); //将指定端口的所有引脚设置为PortVal的值
```

## 操作GPIO口的3个步骤

1. 使用RCC开启GPIO时钟
2. 使用`GPIO_init`函数初始化GPIO
3. 使用输出或输入函数控制GPIO口

### 使用RCC开启GPIO时钟

详见`STM32的时钟系统`

### GPIO的初始化

STM32F103C8初始化代码示例：

```c
GPIO_InitTypeDef GPIO_initStructure;
GPIO_initStructure.GPIO_Mode=GPIO_Mode_Out_PP;//推挽输出
/*
GPIO_Mode_AIN = 0x0, (Analog IN, 模拟输入)
GPIO_Mode_IN_FLOATING = 0x04, (浮空输入)
GPIO_Mode_IPD = 0x28, (In Pull Down, 下拉输入)
GPIO_Mode_IPU = 0x48, (In Pull up, 上拉输入)
GPIO_Mode_Out_OD = 0x14, (Out Open Drain, 开漏输出)
GPIO_Mode_Out_PP = 0x10, (Out Push Pull, 推挽输出)
GPIO_Mode_AF_OD = 0x1C, (Aft Open Drain, 复用开漏)
GPIO_Mode_AF_PP = 0x18 (Aft Push Pull, 复用推挽)
*/
GPIO_initStructure.GPIO_Pin=GPIO_Pin_0;//操作GPIOA外设0号引脚
//引脚编号0~15，操作所有引脚则写：GPIO_Pin_All
GPIO_initStructure.GPIO_Speed=GPIO_Speed_50MHz;//GPIO的输出速度，在输入模式下无效
/*
GPIO_Speed_10MHz
GPIO_Speed_2MHz
GPIO_Speed_50MHz
*/
GPIO_Init(GPIOA,&GPIO_initStructure);
```

### GPIO输出

在推挽模式下，高低电平均具有驱动能力；
在开漏模式下，只有低电平具有驱动能力，高电平时引脚处于高阻态。

使用`GPIO_SetBits`和`GPIO_ResetBits`函数控制GPIO口的电平：

```c
GPIO_SetBits(GPIOA,GPIO_Pin_0); //将GPIOA的0号引脚设置为高电平
GPIO_ResetBits(GPIOA,GPIO_Pin_0); //将GPIOA的0号引脚设置为低电平
```

使用`GPIO_WriteBit`函数可以根据第三个参数设置指定端口的电平：

```c
GPIO_WriteBit(GPIOA, GPIO_Pin_0, Bit_SET); //将GPIOA的0号引脚设置为高电平
GPIO_WriteBit(GPIOA, GPIO_Pin_0, Bit_RESET); //将GPIOA的0号引脚设置为低电平
```

使用`GPIO_Write`函数可以将指定端口的所有引脚设置为PortVal的值：

```c
GPIO_Write(GPIOA, 0x0001); //将GPIOA的所有引脚设置为0x0001的值，0x0001表示第0号引脚为高电平，其余引脚为低电平
GPIO_Write(GPIOA, ~0x0001); //将GPIOA的所有引脚设置为~0x0001的值，~0x0001中的“~”表示按位取反，即第0号引脚为低电平，其余引脚为高电平
```

#### 使用GPIO输出操作LED与蜂鸣器

引脚输出低电平LED亮起，蜂鸣器发声；输出高电平LED熄灭，蜂鸣器静音。

### GPIO输入

```c
//读取GPIO输入数据寄存器某个端口的输入值
uint8_t GPIO_ReadInputDataBit(GPIO_TypeDef* GPIOx, uint16_t GPIO_Pin);
uint16_t GPIO_ReadInputData(GPIO_TypeDef* GPIOx);//读取整个输入数据寄存器的值

//读取GPIO输出数据寄存器某个端口的输出值
uint8_t GPIO_ReadOutputDataBit(GPIO_TypeDef* GPIOx, uint16_t GPIO_Pin);
uint16_t GPIO_ReadOutputData(GPIO_TypeDef* GPIOx);//读取整个输出数据寄存器的值
```
#### 输入模式的选择

GPIO输入模式有四种：浮空输入、上拉输入、下拉输入、模拟输入。

- 如果接在某个引脚的外部模块默认输出高电平，选择上拉输入，默认输入高电平
- 如果默认输出低电平，配置下拉输入，默认输入低电平
- 如果不确定外部模块的默认电平或者外部模块输出功率小，选择浮空输入
   
  浮空输入的缺点是当引脚悬空时没有默认电平，输入就会受噪声干扰，不断跳变
- 模拟输入：通过ADC模块读取模拟信号，输出模拟电压值。

#### C语言stdint.h头文件和ST（意法半导体公司）对变量的重命名

| 关键字                        |位数| stdint关键字 | ST关键字  |
| ---------------------------  | ---| ------------ | -------- |
| char(在单片机中通常用来存放整数)| 8  | int8_t       | s8       |
| unsigned char                | 8  | uint8_t      | u8       |
| short                        | 16 | int16_t      | s16      |
| unsigned short               | 16 | uint16_t     | u16      |
| int                          | 32 | int32_t      | s32      |
| unsigned int                 | 32 | uint32_t     | u32      |
| long                         | 32 |              |          |
| unsigned long                | 32 |              |          |
| long long                    | 64 | int64_t      |          |
| unsigned long long           | 64 | uint64_t     |          |
| float                        | 32 |              |          |
| double                       | 64 |              |          |

> 枚举类型的数据类型用BitAction表示，包含两个值：Bit_RESET（0）和Bit_SET（1）。

#### 使用GPIO输入读取按键信号

按键按下导通，松开断开。
需注意的是按键存在抖动现象（按键内部使用机械式弹簧片通断），在高低电平转换时会有短暂的抖动，导致读取到多个高低电平变化。
因此需要在读取按键状态时进行消抖处理。

按键的几种接法：

1. **上拉输入**：按键未按下时引脚处于高电平，按下时引脚接地为低电平。此时引脚可配置为上拉输入或浮空输入。（也可舍弃图中的电阻与VCC，但引脚只能设置为上拉输入）

![上拉输入](上拉输入.jpg)

1. **下拉输入**：按键未按下时引脚处于低电平，按下时引脚接VCC为高电平。此时引脚可配置为下拉输入或浮空输入。（也可舍弃图中的电阻与GND，但引脚只能设置为下拉输入）

![下拉输入](下拉输入.jpg)

**封装函数读取按键状态**：

```c
uint8_t Key_Num(void) {
    uint8_t KeyNum = 0;//定义键码
    if(GPIO_ReadInputDataBit(GPIOB,GPIO_Pin_1)==0)//上拉输入按下时为低电平
    {
        Delay_ms(20);
        while(GPIO_ReadInputDataBit(GPIOB,GPIO_Pin_1)==0);
        Delay_ms(20);//消抖
        KeyNum=1;//多个按键时可定义不同的键码
    }
    return KeyNum;//返回按键状态
}
```

从而可以在主函数中调用`Key_Num()`函数来获取按键状态。

```c
KeyNum = Key_Num();
if(KeyNum == 1) {
    ... //按键按下时执行的操作
}
if(KeyNum == 2) {
    ... //其他按键按下时执行的操作
}
```

#### 使用GPIO输入读取传感器信号

传感器元件（光敏电阻/热敏电阻/红外接收管等）的电阻值会随外界环境变化而变化，通过与定值电阻分压即可得到模拟电压输出，再通过电压比较器进行二值化处理即可得到数字电压输出。

接法：

![传感器输入](传感器输入.jpg)

> 光敏传感器：遮住光敏电阻时输出高电平，光照时输出低电平。
> DO数字输出接口接GPIO引脚，AO模拟输出接口暂时不涉及。
