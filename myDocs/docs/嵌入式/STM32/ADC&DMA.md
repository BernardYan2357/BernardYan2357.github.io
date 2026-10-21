# ADC&DMA

## ADC简介

ADC（Analog-to-Digital Converter）模拟-数字转换器

- ADC可以将引脚上连续变化的模拟电压转换为内存中存储的数字变量，建立模拟电路到数字电路的桥梁
- 12位逐次逼近型ADC，1us转换时间
- 输入电压范围：0~3.3V，转换结果范围：0~4095
- 18个输入通道，可测量16个外部和2个内部信号源
- 规则组和注入组两个转换单元，STM32的ADC可以列一个组，一次性启动一个组，连续转换多个值
- 模拟看门狗自动监测输入电压范围

STM32F103C8T6的ADC资源：ADC1、ADC2，10个外部输入通道

### ADC结构

#### 逐次逼近型ADC结构

以ADC0809芯片为例，8位逐次逼近型ADC的结构如下图所示：
（以前的单片机性能不强，需要外挂ADC芯片实现AD转换）

![逐次逼近型ADC结构](逐次逼近型ADC结构.jpg)

- 通道选择开关：选择8路通道中的一路输入
  实现方式：在地址锁存和译码处，将要选的通道号放在三个地址线上，再给一个锁存信号，锁存后送到译码器，译码器输出8路信号中对应的一路高电平，控制模拟开关导通
- 逐次逼近法：
  - DAC（数模转换器）：将输入数据转换为模拟电压
  - 电压比较器：比较输入电压和DAC输出电压的大小关系，输出高低电平指示
  - 逐次逼近寄存器SAR：使用二分法逼近，最高位先试探，依次向低位逼近：
    对于8位ADC，编码0~255：第一次取128，DAC输出对应电压，比较器比较输入电压和DAC输出电压的大小关系，然后取64，32，16，8，4，2，1。用二进制表示，这些数字正好是二进制每一位的位权。该判断过程即对二进制从高位到低位依次试探1或0的过程，大于则该位为1，否则为0，直到最低位，完成8位二进制数的转换。
- 8位三态锁存缓冲器：输出转换结果
- 外部信号：
  - EOC（End of Convert）：转换完成信号
  - START：开始转换信号
  - CLOCK：时钟信号，推动逐次逼近寄存器工作和采样
  - Vref+、Vref-：DAC参考电压，决定ADC的量化级数和输入电压范围
    VCC与Vref+相连，GND与Vref-相连，故一般情况下ADC输入电压范围与其供电电压相同

#### STM32的ADC结构

![ADC框图](ADC框图.jpg)

![ADC基本结构](ADC基本结构.jpg)

- 通道选择
  
  18路通道，通过GPIO端口输入，经过模拟多路开关：
  - 注入通道一次最多选择4路通道
  - 规则通道一次最多选择16路通道
- 触发转换
  - 软件触发：通过代码触发ADC转换
  - 硬件触发：通过外部触发器触发ADC转换，如使用定时器将更新事件选择为TRGO输出，再在ADC中配置触发源为定时器的TRGO
- 外部信号
  - VDDA，VSSA：ADC供电引脚，同时也是RC震荡器，锁相环等的供电引脚
  - Vref+、Vref-：ADC参考电压，在芯片上无这两个引脚，在内部与VDDA、VSSA相连
  - ADCCLK：ADC时钟，来自ADC预分频器（来源于RCC，参考图“RCC时钟树”），ADC预分频器支持2，4，6，8分频，又由于ADCCLK最大14MHz,故ADCCLK频率只能是12MHz（6分频）或9MHz（8分频）
- 转换标志位
  
  产生的标志位信号通过或门传递至NVIC的ADC中断
  - 转换结束标志位（EOC）
  - 注入转换结束标志位（JEOC）
  - 模拟看门狗事件（AWD）
- 转换结果
  
  转换结果放在注入通道数据寄存器或规则通道数据寄存器
  规则通道寄存器一次只能保存一个通道的转换结果，需配合DMA(Direct Memory Access)使用

##### ADC输入通道

| 通道    | ADC1   | ADC2   | ADC3         |
|---------|--------|--------|--------------|
| 通道0   | PA0    | PA0    | PA0          |
| 通道1   | PA1    | PA1    | PA1          |
| 通道2   | PA2    | PA2    | PA2          |
| 通道3   | PA3    | PA3    | PA3          |
| 通道4   | PA4    | PA4    | PF6          |
| 通道5   | PA5    | PA5    | PF7          |
| 通道6   | PA6    | PA6    | PF8          |
| 通道7   | PA7    | PA7    | PF9          |
| 通道8   | PB0    | PB0    | PF10         |
| 通道9   | PB1    | PB1    | -            |
| 通道10  | PC0    | PC0    | PC0          |
| 通道11  | PC1    | PC1    | PC1          |
| 通道12  | PC2    | PC2    | PC2          |
| 通道13  | PC3    | PC3    | PC3          |
| 通道14  | PC4    | PC4    | -            |
| 通道15  | PC5    | PC5    | -            |
| 通道16  | 温度传感器 | 温度传感器 | 温度传感器 |
| 通道17  | 内部参考电压 | 内部参考电压 | 内部参考电压 |

> 对于STM32F103C8T6，ADC1和ADC2共有10个输入通道（0~9），无ADC3

ADC1和ADC2的引脚相同，便于实现双ADC模式:

ADC1和ADC2一起工作，有同步模式和交叉模式。例如使用交叉模式对一个通道进行采样，进一步提高采样率

##### 规则组的四种转换模式

- 单次转换：转换一次后置EOC标志位，若想再次启动转换需再触发一次
- 连续转换：转换一次后不会停止，而是继续转换不停止
- 扫描模式：ADC从序列1开始，到序列n结束，需指定通道数目n
- 非扫描模式：同时选中一组的的方式退化为简单选择一个的方式，只有序列1有效

四种组合方式如下：

- 单次转换非扫描模式
  
  ![单次转换非扫描模式](单次转换非扫描模式.jpg)
- 连续转换非扫描模式

  ![连续转换非扫描模式](连续转换非扫描模式.jpg)
- 单次转换扫描模式

  ![单次转换扫描模式](单次转换扫描模式.jpg)
- 连续转换扫描模式

  ![连续转换扫描模式](连续转换扫描模式.jpg)

##### 触发控制

ADC1和ADC2用于规则通道的外部触发：

| 触发源                        | 类型                   | EXTSEL（2:0）|
|-------------------------------|-----------------------|-------------|
| TIM1_CC1事件                  | 来自片上定时器的内部信号 | 000         |
| TIM1_CC2事件                  | 来自片上定时器的内部信号 | 001         |
| TIM1_CC3事件                  | 来自片上定时器的内部信号 | 010         |
| TIM2_CC2事件                  | 来自片上定时器的内部信号 | 011         |
| TIM3_TRGO事件                 | 来自片上定时器的内部信号 | 100         |
| TIM4_CC4事件                  | 来自片上定时器的内部信号 | 101         |
| EXTI线11/TIM8_TRGO事件        | 外部引脚/来自片上定时器的内部信号| 110 |
| SWSTART                       | 软件控制位  | 111         |

##### 数据对齐

STM32的12位ADC转换结果是12位数据，而数据寄存器是16位的，需要将数据对齐

**数据右对齐：**

- 便于直接读取数据

| 0 | 0 | 0 | 0 | 0 | D11 | D10 | D9 | D8 | D7 | D6 | D5 | D4 | D3 | D2 | D1 | D0 |
|---|---|---|---|---|-----|-----|----|----|----|----|----|----|----|----|----|----|

**数据左对齐：**

- 左移四位，相当于x16
- 左对齐的意义在于：低分辨率情境下不需要读取12位数据，可以数据左对齐，读取高八位

| D11 | D10 | D9 | D8 | D7 | D6 | D5 | D4 | D3 | D2 | D1 | D0 | 0 | 0 | 0 | 0 |
|-----|-----|----|----|----|----|----|----|----|----|----|----|---|---|---|---|

##### 转换时间

AD转换的步骤：采样，保持，量化，编码
> 由于输入信号电压在不断变化，故在模数转换之前需要先采样
>
> 在通道选择开关后设置采样开关，使用小容量电容存储电压，存储好后再进行AD转换

STM32 ADC的总转换时间为：
  TCONV = 采样时间 + 12.5个ADC周期（量化编码花费时间）

例如：当ADCCLK=14MHz，采样时间为1.5个ADC周期
  TCONV = 1.5 + 12.5 = 14个ADC周期 = 1μs（理论最快时间）

##### 校准

- ADC有一个内置自校准模式。校准可大幅减小因内部电容器组的变化而造成的准精度误差。校准期间，在每个电容器上都会计算出一个误差修正码(数字值)，这个码用于消除在随后的转换中每个电容器上产生的误差
- 建议在每次上电后执行一次校准
- 启动校准前， ADC必须处于关电状态超过至少两个ADC时钟周期

### 硬件电路

![ADC硬件电路](ADC硬件电路.jpg)

- 电位器（滑动变阻器）产生可调电压
  向PA0口输出0~3.3v可调电压，电阻不能过小，KΩ级
- 传感器输出电压
  - 光敏电阻、热敏电阻、红外接收管、麦克风等等效为可变电阻N1，串联固定电阻（阻值与N1相近）分压，以此测量电压：传感器阻值变大时，下拉作用变弱，输出端受上拉电阻的作用，输出电压升高，反之同理
  - 当传感器与固定电阻对调，输出电压极性翻转
- 电压转换电路
  将0~5v电压转换为等比的0~3.3v电压

### 软件编程

#### ADC库函数

```c
//stm32f10x.rcc.h
void RCC_ADCCLKConfig(uint32_t RCC_ADCCLK);//配置ADCCLK分频器

//stm32f10x.adc.h
//ADC初始化
void ADC_DeInit(ADC_TypeDef* ADCx);//ADC初始化
void ADC_Init(ADC_TypeDef* ADCx, ADC_InitTypeDef* ADC_InitStruct);//ADC参数配置
void ADC_StructInit(ADC_InitTypeDef* ADC_InitStruct);//ADC参数结构体初始化
void ADC_Cmd(ADC_TypeDef* ADCx, FunctionalState NewState);//使能/禁止ADC,给ADC上电
void ADC_DMACmd(ADC_TypeDef* ADCx, FunctionalState NewState);//使能/禁止DMA传输
void ADC_ITConfig(ADC_TypeDef* ADCx, uint16_t ADC_IT, FunctionalState NewState);//配置ADC中断
//校准
void ADC_ResetCalibration(ADC_TypeDef* ADCx);//复位校准寄存器
FlagStatus ADC_GetResetCalibrationStatus(ADC_TypeDef* ADCx);//获取复位校准寄存器状态
void ADC_StartCalibration(ADC_TypeDef* ADCx);//开始校准
FlagStatus ADC_GetCalibrationStatus(ADC_TypeDef* ADCx);//获取开始校准状态
//软件触发
void ADC_SoftwareStartConvCmd(ADC_TypeDef* ADCx, FunctionalState NewState);//软件触发ADC转换
FlagStatus ADC_GetSoftwareStartConvStatus(ADC_TypeDef* ADCx);//获取软件触发转换状态
//间断模式
void ADC_DiscModeChannelCountConfig(ADC_TypeDef* ADCx, uint8_t Number);//每隔几个通道间断一次
void ADC_DiscModeCmd(ADC_TypeDef* ADCx, FunctionalState NewState);//使能/禁止间断模式
//规则组通道配置
void ADC_RegularChannelConfig(ADC_TypeDef* ADCx, uint8_t ADC_Channel, uint8_t Rank, uint8_t ADC_SampleTime);//配置通道
void ADC_ExternalTrigConvCmd(ADC_TypeDef* ADCx, FunctionalState NewState);//外部触发转换控制
uint16_t ADC_GetConversionValue(ADC_TypeDef* ADCx);//获取ADC转换值
uint32_t ADC_GetDualModeConversionValue(void);//获取双模式ADC转换值
//注入组配置
void ADC_AutoInjectedConvCmd(ADC_TypeDef* ADCx, FunctionalState NewState);
void ADC_InjectedDiscModeCmd(ADC_TypeDef* ADCx, FunctionalState NewState);
void ADC_ExternalTrigInjectedConvConfig(ADC_TypeDef* ADCx, uint32_t ADC_ExternalTrigInjecConv);
void ADC_ExternalTrigInjectedConvCmd(ADC_TypeDef* ADCx, FunctionalState NewState);
void ADC_SoftwareStartInjectedConvCmd(ADC_TypeDef* ADCx, FunctionalState NewState);
FlagStatus ADC_GetSoftwareStartInjectedConvCmdStatus(ADC_TypeDef* ADCx);
void ADC_InjectedChannelConfig(ADC_TypeDef* ADCx, uint8_t ADC_Channel, uint8_t Rank, uint8_t ADC_SampleTime);
void ADC_InjectedSequencerLengthConfig(ADC_TypeDef* ADCx, uint8_t Length);
void ADC_SetInjectedOffset(ADC_TypeDef* ADCx, uint8_t ADC_InjectedChannel, uint16_t Offset);
uint16_t ADC_GetInjectedConversionValue(ADC_TypeDef* ADCx, uint8_t ADC_InjectedChannel);
//模拟看门狗配置
void ADC_AnalogWatchdogCmd(ADC_TypeDef* ADCx, uint32_t ADC_AnalogWatchdog);//启动/关闭模拟看门狗
void ADC_AnalogWatchdogThresholdsConfig(ADC_TypeDef* ADCx, uint16_t HighThreshold, uint16_t LowThreshold);//配置模拟看门狗阈值
void ADC_AnalogWatchdogSingleChannelConfig(ADC_TypeDef* ADCx, uint8_t ADC_Channel);//配置模拟看门狗通道
//ADC16通道
void ADC_TempSensorVrefintCmd(FunctionalState NewState);
//标志位
FlagStatus ADC_GetFlagStatus(ADC_TypeDef* ADCx, uint8_t ADC_FLAG);//获取ADC标志位状态
void ADC_ClearFlag(ADC_TypeDef* ADCx, uint8_t ADC_FLAG);
ITStatus ADC_GetITStatus(ADC_TypeDef* ADCx, uint16_t ADC_IT);//获取ADC中断状态
void ADC_ClearITPendingBit(ADC_TypeDef* ADCx, uint16_t ADC_IT);
```

#### ADC代码实现

##### 单通道

- 单通道初始化
  ```c
  void AD_Init(void){
    //配置时钟
    RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA,ENABLE);
	  RCC_APB2PeriphClockCmd(RCC_APB2Periph_ADC1,ENABLE);//开启ADC1时钟
	  RCC_ADCCLKConfig(RCC_PCLK2_Div6);//ADCCLK分频器分频系数
	  //配置GPIO
	  GPIO_InitTypeDef GPIO_InitStructure;
    GPIO_InitStructure.GPIO_Mode=GPIO_Mode_AIN;
	  GPIO_InitStructure.GPIO_Pin=GPIO_Pin_0;
	  GPIO_InitStructure.GPIO_Speed=GPIO_Speed_50MHz;
	  GPIO_Init(GPIOA,&GPIO_InitStructure);
	  //指定ADC通道
	  ADC_RegularChannelConfig(ADC1,ADC_Channel_0,1,ADC_SampleTime_55Cycles5);//序列数：1，采样时间55.5个ADCCLK周期
	  //配置ADC
	  ADC_InitTypeDef ADC_InitStructure;
	  ADC_InitStructure.ADC_DataAlign=ADC_DataAlign_Right;//数据对齐：右对齐
	  ADC_InitStructure.ADC_ExternalTrigConv=ADC_ExternalTrigConv_None;//外部触发转换选择：软件触发
	  ADC_InitStructure.ADC_Mode=ADC_Mode_Independent;//模式，选择独立模式，即单独使用ADC1
    ADC_InitStructure.ADC_ContinuousConvMode=DISABLE;//单次转换
	  ADC_InitStructure.ADC_ScanConvMode=DISABLE;//非扫描模式
	  ADC_InitStructure.ADC_NbrOfChannel=1;//通道数，在非扫描模式下无用
	  ADC_Init(ADC1,&ADC_InitStructure);
	  //使能ADC
	  ADC_Cmd(ADC1,ENABLE);
	  //校准
	  ADC_ResetCalibration(ADC1);//复位校准
	  while(ADC_GetResetCalibrationStatus(ADC1)==SET);//检测是否复位
	  ADC_StartCalibration(ADC1);//开始校准
	  while(ADC_GetCalibrationStatus(ADC1)==SET);//检测是否校准
  }
  ```

- 单通道读取
  ```c
  //AD.c
  uint16_t AD_GetValue(void){
    ADC_SoftwareStartConvCmd(ADC1,ENABLE);//软件触发
    //如果是连续转换模式，将软件触发代码移至初始化代码最后
	  while(ADC_GetFlagStatus(ADC1,ADC_FLAG_EOC)==RESET);//判断是否转换完成
	  return ADC_GetConversionValue(ADC1);//返回DR寄存器值，自动清除标志位
  }
  ```

  ```c
  //main.c
  uint16_t AD_Value;
  float Voltage;
  int main(void){
	  OLED_Init();
	  AD_Init();
	  OLED_ShowString(1,1,"ADValue:");
	  OLED_ShowString(2,1,"Voltage:0.00V");
    while(1){
		  AD_Value=AD_GetValue();
		  Voltage=(float)AD_Value/4095*3.3;//ADC是12位的，分辨率就是2^12，所以存的数范围就是0~4095
		  OLED_ShowNum(1,9,AD_Value,4);
		  OLED_ShowNum(2,9,Voltage,1);//整数部分
		  OLED_ShowNum(2,11,(uint16_t)(Voltage*100)%100,2);//小数部分
		  Delay_ms(100);
	  }
  }
  ```

##### 多通道

1. 通过手动更改通道配置，实现多通道的ADC转换
   - GPIO初始化中添加对应输入引脚
   - 将初始化代码中的`ADC_RegularChannelConfig()`函数移至`AD_GetValue()`函数中：修改函数声明为`void AD_GetValue(uint8_t ADC_Channel)`
     ```c
     //AD.c
     uint16_t AD_GetValue(uint8_t ADC_Channel){
	      ADC_RegularChannelConfig(ADC1,ADC_Channel,1,ADC_SampleTime_55Cycles5);
        ADC_SoftwareStartConvCmd(ADC1,ENABLE);//软件触发
	      while(ADC_GetFlagStatus(ADC1,ADC_FLAG_EOC)==RESET);//判断是否转换完成
	      return ADC_GetConversionValue(ADC1);//返回DR寄存器值，自动清除标志位
     }
     ```
     ```c
     //main.c
     uint16_t AD0,AD1,AD2,AD3;
     int main(void){
	    OLED_Init();
	    AD_Init();
	    OLED_ShowString(1,1,"AD0:");
	    OLED_ShowString(2,1,"AD1:");
	    OLED_ShowString(3,1,"AD2:");
	    OLED_ShowString(4,1,"AD3:");
      while(1){
		  AD0=AD_GetValue(ADC_Channel_0);
		  AD1=AD_GetValue(ADC_Channel_1);
		  AD2=AD_GetValue(ADC_Channel_2);
		  AD3=AD_GetValue(ADC_Channel_3);
		  OLED_ShowNum(1,5,AD0,4);
		  OLED_ShowNum(2,5,AD1,4);
		  OLED_ShowNum(3,5,AD2,4);
		  OLED_ShowNum(4,5,AD3,4);
		  Delay_ms(100);
	    }
     }
     ```
2. 通过DMA实现多通道的ADC转换
   见下文

##### 解决AD值波动导致在阈值上下跳动的问题

以开关灯举例：

- 迟滞比较：
  设置两个阈值，一个上阈值，一个下阈值，当AD值大于上阈值时，开灯，当AD值小于下阈值时，关灯。
- 滤波：使AD值更平滑
  - 均值滤波：取多个阈值之间的平均值作为阈值
  - 裁剪分辨率：把数据的尾数去掉，使数据变成整数，这样可以减少噪声的影响

## DMA直接存储器存取

DMA（Direct Memory Access）直接存储器存取

- DMA可以提供外设(外设寄存器)和存储器或者存储器和存储器之间的高速数据传输，无须CPU干预，节省了CPU的资源
- 12个独立可配置的通道： DMA1（7个通道）， DMA2（5个通道）
- 每个通道都支持软件触发和特定的（每个通道的硬件触发源不同）硬件触发

STM32F103C8T6 DMA资源：DMA1（7个通道）

### 存储器映像

> STM32F103x8B数据手册：4存储器映像

| 类型 | 起始地址        | 存储器               | 用途                                   |
|------|----------------|----------------------|----------------------------------------|
| ROM  | 0x0800 0000    | 程序存储器Flash      | 存储C语言编译后的程序代码               |
| ROM  | 0x1FFF F000    | 系统存储器           | 存储BootLoader，用于串口下载            |
| ROM  | 0x1FFF F800    | 选项字节             | 存储一些独立于程序代码的配置参数        |
| RAM  | 0x2000 0000    | 运行内存SRAM         | 存储运行过程中临时变量                  |
| RAM  | 0x4000 0000    | 外设寄存器           | 存储各个外设的配置参数                  |
| RAM  | 0xE000 0000    | 内核外设寄存器       | 存储内核各个外设的配置参数              |

解释：
- ROM（只读存储器）：非易失性、掉电不丢失
  - Flash(闪存)：存储器，容量大，可擦写，常用作程序存储器
- RAM（随机存储器）：易失性、掉电丢失
  - SRAM：存储器，容量小，可擦写，常用作运行内存，类似于电脑的内存条
  - 外设寄存器：存储器，容量小，可擦写，用于配置各个外设
    > 寄存器是一种特殊的存储器，一方面CPU可以对寄存器进行读写，另一方面，寄存器每一位都连接导线，可以控制外设电路的状态

**代码验证：**

```c
//运行内存SRAM
uint8_t aa=0x66;
OLED_ShowHexNum(2,1,(uint32_t)&aa,8);//强制类型转换，uint8_t*（指针类型）转uint32_t（32位（32位二进制）无符号整数类型），显示为16进制数就是8位
//程序存储器Flash
const uint8_t bb=0x55;//常量只读，存储在Flash中
//若要定义一个很大的查找表或字库，可以定义为常量，避免浪费SRAM空间
OLED_ShowHexNum(2,5,(uint32_t)&bb,8);
//外设寄存器
OLED_ShowHexNum(2,9,(uint32_t)&ADC1->DR,8);//访问ADC1的DR（数据寄存器）地址：4001244c，使用->结构体指针成员访问运算符访问寄存器地址
```

### DMA结构

![DMA框图](DMA框图.jpg)

- 总线矩阵：
  - 总线矩阵的左端是主动单元（拥有存储器的访问权），右端是被动单元（被主动单元读写）
  - 存在仲裁器，若DMA与CPU都要访问同一目标地址，DMA优先于CPU访问
- 主动单元：
  - DCode：专门访问Flash
  - 系统总线
  - DMA：共有三条：DMA1，DMA2，以太网外设私有DMA
- DMA内部
  - 多个通道可以分别设置转运数据的源地址和目的地址，多个通道分时复用DMA总线
  - 通过仲裁器根据通道优先级决定先后
  - AHB从设备：DMA自身的配置寄存器
  - AHB从设备连接在AHB总线上，故DMA也是AHB总线上的被动单元
- DMA请求
  DMA的硬件触发源

![DMA基本结构](DMA基本结构.jpg)

- 自动重装器：决定转运模式：不重装就是单次模式，重装就是循环模式
- 传输计数器：在配置DMA时，需设置传输计数器的初值，表示本次需要传输的数据个数，每传输一次自动减一，计数器为零时传输结束，其值不能在DMA运行过程中修改
- 触发控制：由M2M（Memory to Memory）决定，给M2M位1，选择软件触发（此处软件触发相当于循环模式，不能与自动重装器同时使用），给M2M位0，选择硬件触发
  硬件触发：外设到存储器的传输
  软件触发：存储器到存储器的传输

DMA转运的条件：
- 开关控制，DMA_Cmd()函数使能
- 传输计数器>0
- 有触发信号

### DMA请求

![DMA请求映像](DMA请求映像.jpg)

### 数据宽度与对齐

![数据宽度与对齐](数据宽度与对齐.jpg)

源端数据宽度小于目标数据宽度时，高位补零
源端数据宽度大于目标数据宽度时，高位舍弃

### DMA库函数

```c
void DMA_DeInit(DMA_Channel_TypeDef* DMAy_Channelx);//恢复缺省配置
void DMA_Init(DMA_Channel_TypeDef* DMAy_Channelx, DMA_InitTypeDef* DMA_InitStruct);//初始化
void DMA_StructInit(DMA_InitTypeDef* DMA_InitStruct);//初始化结构体
void DMA_Cmd(DMA_Channel_TypeDef* DMAy_Channelx, FunctionalState NewState);//使能
void DMA_ITConfig(DMA_Channel_TypeDef* DMAy_Channelx, uint32_t DMA_IT, FunctionalState NewState);//中断输出使能
void DMA_SetCurrDataCounter(DMA_Channel_TypeDef* DMAy_Channelx, uint16_t DataNumber); //设置当前数据寄存器（设置传输寄存器的值）
uint16_t DMA_GetCurrDataCounter(DMA_Channel_TypeDef* DMAy_Channelx);//获取当前数据寄存器（返回传输计数器的值）
FlagStatus DMA_GetFlagStatus(uint32_t DMAy_FLAG);//获取标志位状态
void DMA_ClearFlag(uint32_t DMAy_FLAG);//清除标志位
ITStatus DMA_GetITStatus(uint32_t DMAy_IT);//获取中断状态
void DMA_ClearITPendingBit(uint32_t DMAy_IT);//清除中断标志位
```

### 数据转运+DMA

![数据转运+DMA](数据转运+DMA.jpg)

```c
//MyDMA.c
uint16_t MyDMA_Size;

void MyDMA_Init(uint32_t ADDrA,uint32_t ADDrB,uint16_t Size){
	MyDMA_Size=Size;
	//使能DMA时钟
  RCC_AHBPeriphClockCmd(RCC_AHBPeriph_DMA1,ENABLE);
	//初始化DMA通道1
	DMA_InitTypeDef DMA_InitStructure;
	DMA_InitStructure.DMA_PeripheralBaseAddr=ADDrA;//传输数据的起始地址
	DMA_InitStructure.DMA_PeripheralDataSize=DMA_PeripheralDataSize_Byte;//数据宽度
	DMA_InitStructure.DMA_PeripheralInc=DMA_PeripheralInc_Enable;//地址是否自增
	DMA_InitStructure.DMA_MemoryBaseAddr=ADDrB;//目的地起始地址
	DMA_InitStructure.DMA_MemoryDataSize=DMA_MemoryDataSize_Byte;//数据宽度
	DMA_InitStructure.DMA_MemoryInc=DMA_MemoryInc_Enable;//是否自增
	DMA_InitStructure.DMA_DIR=DMA_DIR_PeripheralSRC;//Direction,传输方向,此处选择外设站点作为数据源
	DMA_InitStructure.DMA_BufferSize=Size;//缓存区大小（传输计数器值）
	DMA_InitStructure.DMA_Mode=DMA_Mode_Normal;//传输模式，是否使用自动重装
	DMA_InitStructure.DMA_M2M=DMA_M2M_Enable;//选择硬件/软件触发(M2M)
	DMA_InitStructure.DMA_Priority=DMA_Priority_Medium;//优先级
	DMA_Init(DMA1_Channel1,&DMA_InitStructure);
	//先失能
	DMA_Cmd(DMA1_Channel1,DISABLE);
}
//修改DMA传输计数器值，避免传输一次后停止
void MyDMA_transfer(void){
  DMA_Cmd(DMA1_Channel1,DISABLE);//不能在DMA运行时修改计数器值
	DMA_SetCurrDataCounter(DMA1_Channel1,MyDMA_Size);//设置传输计数器值
	DMA_Cmd(DMA1_Channel1,ENABLE);//启动DMA传输
	//等待DMA传输结束
	while(DMA_GetFlagStatus(DMA1_FLAG_TC1)==RESET);
	DMA_ClearFlag(DMA1_FLAG_TC1);
}
```

```c
//main.c
uint8_t DataA[]={0x01,0x02,0x03,0x04};
uint8_t DataB[]={0,0,0,0};
int main(void){
	OLED_Init();
	MyDMA_Init((uint32_t)DataA,(uint32_t)DataB,4);
	OLED_Show(); //此处用show函数省略表示，详情在代码块文末
  while(1){
		DataA[0]++;
		DataA[1]++;
		DataA[2]++;
		DataA[3]++;
		OLED_Show();
		Delay_s(1);
		MyDMA_transfer();
		OLED_Show();
		Delay_s(1);
	}
}
//显示函数
  // OLED_ShowString(1,1,"DataA:");
	// OLED_ShowHexNum(1,8,(uint32_t)DataA,8);
	// OLED_ShowString(3,1,"DataB:");
	// OLED_ShowHexNum(3,8,(uint32_t)DataB,8);
	// OLED_ShowHexNum(2,1,DataA[0],2);
	// OLED_ShowHexNum(2,4,DataA[1],2);
	// OLED_ShowHexNum(2,7,DataA[2],2);
  // OLED_ShowHexNum(2,10,DataA[3],2);
	// OLED_ShowHexNum(4,1,DataB[0],2);
	// OLED_ShowHexNum(4,4,DataB[1],2);
	// OLED_ShowHexNum(4,7,DataB[2],2);
  // OLED_ShowHexNum(4,10,DataB[3],2);
```

### ADC扫描模式+DMA

![ADC扫描模式+DMA](ADC扫描模式+DMA.jpg)

```c
//AD.c
//ADC连续转换模式，DMA循环转运模式
uint16_t AD_Value[4];//需在头文件声明，便于外部调用
void AD_Init(void){
    RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA,ENABLE);
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_ADC1,ENABLE);//开启ADC1时钟
	RCC_AHBPeriphClockCmd(RCC_AHBPeriph_DMA1,ENABLE);//开启DMA时钟
	RCC_ADCCLKConfig(RCC_PCLK2_Div6);//ADCCLK分频器分频系数
	
	GPIO_InitTypeDef GPIO_InitStructure;
    GPIO_InitStructure.GPIO_Mode=GPIO_Mode_AIN;
	GPIO_InitStructure.GPIO_Pin=GPIO_Pin_0|GPIO_Pin_1|GPIO_Pin_2|GPIO_Pin_3;
	GPIO_InitStructure.GPIO_Speed=GPIO_Speed_50MHz;
	GPIO_Init(GPIOA,&GPIO_InitStructure);
	//配置通道对应序列
	ADC_RegularChannelConfig(ADC1,ADC_Channel_0,1,ADC_SampleTime_55Cycles5);
	ADC_RegularChannelConfig(ADC1,ADC_Channel_1,2,ADC_SampleTime_55Cycles5);
	ADC_RegularChannelConfig(ADC1,ADC_Channel_2,3,ADC_SampleTime_55Cycles5);
	ADC_RegularChannelConfig(ADC1,ADC_Channel_3,4,ADC_SampleTime_55Cycles5);
	
	ADC_InitTypeDef ADC_InitStructure;
	ADC_InitStructure.ADC_DataAlign=ADC_DataAlign_Right;//数据对齐：右对齐
	ADC_InitStructure.ADC_ExternalTrigConv=ADC_ExternalTrigConv_None;//外部触发转换选择：软件触发
	ADC_InitStructure.ADC_Mode=ADC_Mode_Independent;//模式，选择独立模式，即单独使用ADC1
    ADC_InitStructure.ADC_ContinuousConvMode=ENABLE;//连续转换
	ADC_InitStructure.ADC_ScanConvMode=ENABLE;//扫描模式
	ADC_InitStructure.ADC_NbrOfChannel=4;//通道数
	ADC_Init(ADC1,&ADC_InitStructure);
	
	DMA_InitTypeDef DMA_InitStructure;
	DMA_InitStructure.DMA_PeripheralBaseAddr=(uint32_t)&ADC1->DR;//传输数据的起始地址
	DMA_InitStructure.DMA_PeripheralDataSize=DMA_PeripheralDataSize_HalfWord;//半字节数据宽度
	DMA_InitStructure.DMA_PeripheralInc=DMA_PeripheralInc_Disable;//地址不自增
	DMA_InitStructure.DMA_MemoryBaseAddr=(uint32_t)AD_Value;//起始地址
	DMA_InitStructure.DMA_MemoryDataSize=DMA_MemoryDataSize_HalfWord;//数据宽度
	DMA_InitStructure.DMA_MemoryInc=DMA_MemoryInc_Enable;//地址自增
	DMA_InitStructure.DMA_DIR=DMA_DIR_PeripheralSRC;//Direction,传输方向,此处选择外设站点作为数据源
	DMA_InitStructure.DMA_BufferSize=4;//缓存区大小（传输计数器值）
	DMA_InitStructure.DMA_Mode=DMA_Mode_Circular;//循环模式
	DMA_InitStructure.DMA_M2M=DMA_M2M_Disable;//选择硬件触发
	DMA_InitStructure.DMA_Priority=DMA_Priority_Medium;//优先级
	DMA_Init(DMA1_Channel1,&DMA_InitStructure);//通道选择：选择ADC硬件触发对应通道（详见DMA请求）
	
	DMA_Cmd(DMA1_Channel1,ENABLE);//由于此时ADC硬件触发未配置，故此时DMA未工作
	ADC_DMACmd(ADC1,ENABLE);//配置硬件触发
	ADC_Cmd(ADC1,ENABLE);
	
	ADC_ResetCalibration(ADC1);//复位校准
	while(ADC_GetResetCalibrationStatus(ADC1)==SET);//检测是否复位
	ADC_StartCalibration(ADC1);//开始校准
	while(ADC_GetCalibrationStatus(ADC1)==SET);//检测是否校准
	
	ADC_SoftwareStartConvCmd(ADC1,ENABLE);//ADC软件触发
}
```

```c
//AD.c
//AD_GetValue函数完成了模数转换与DMA转运
//如果ADC为单次转换，DMA也是单次转运，需要此函数
uint16_t AD_GetValue(void){
	DMA_Cmd(DMA1_Channel1,DISABLE);//不能在DMA运行时修改计数器值
	DMA_SetCurrDataCounter(DMA1_Channel1,4);
	DMA_Cmd(DMA1_Channel1,ENABLE);
	
	ADC_SoftwareStartConvCmd(ADC1,ENABLE);//ADC软件触发

	while(DMA_GetFlagStatus(DMA1_FLAG_TC1)==RESET);
	DMA_ClearFlag(DMA1_FLAG_TC1);
	return 0;
}
```

```c
//main.c
//ADC连续转换模式，DMA循环转运模式
int main(void){
	OLED_Init();
	AD_Init();
	OLED_ShowString(1,1,"AD0:");
	OLED_ShowString(2,1,"AD1:");
	OLED_ShowString(3,1,"AD2:");
	OLED_ShowString(4,1,"AD3:");
    while(1){
		OLED_ShowNum(1,5,AD_Value[0],4);
		OLED_ShowNum(2,5,AD_Value[1],4);
		OLED_ShowNum(3,5,AD_Value[2],4);
		OLED_ShowNum(4,5,AD_Value[3],4);
		Delay_ms(100);
	}
}
```
