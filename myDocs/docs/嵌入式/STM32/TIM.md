# TIM(定时器)

## TIM概念

- 定时器可以对输入的时钟进行计数，并在计数值达到设定值时触发中断
- 不仅具备基本的定时中断功能，而且还包含内外时钟源选择、输入捕获、输出比较、编码器接口、主从触发模式等多种功能

### TIM定时长度

16位计数器、预分频器、自动重装寄存器构成时基单元，在72MHz计数时钟下可以实现最大59.69s的定时

- **预分频器（Prescaler）**
  预分频器的作用是“减慢”定时器的计数速度。它会把主时钟（比如72MHz）“分频”成一个较慢的时钟信号，供定时器计数用。比如分频系数为N时，定时器每收到N个主时钟脉冲才加1（即输出频率=输入频率/N，**预分频器值+1=分频系数**，预分频器值为0时输出=输入，预分频器值为1时输出=输入/2，依次类推）。
- **自动重装寄存器（ARR）**
  自动重装寄存器决定了定时器计数到多少就“归零”并触发中断或事件。你可以把它理解为“计数的终点”。
- **计数器（Counter）**
  计数器对预分频后的计数时钟进行计数，计数时钟每来一个上升沿，计数器的值加1（从0开始，最大值为65535）。当计数器的值达到自动重装寄存器的值时，产生中断（称为更新中断）。
- 假设主时钟频率为72MHz，预分频器和自动重装寄存器都设置为最大值65536（实际寄存器最大值为65535，但这里便于理解用65536）。
  - 预分频器分频：
    72,000,000 ÷ 65536 ≈ 1098
    也就是说，定时器每收到1098个主时钟脉冲，计数器才加1。
  - 自动重装寄存器：
    计数器从0数到65536（共65536次），就会溢出并触发一次事件。
  - 总计时时间：
    65536 × (1 ÷ 1098) ≈ 59.69秒
    也就是大约每59.69秒定时器才会溢出一次。

通过定时器级联延长定时器定时长度
> 级联是指将一个定时器的输出连接到另一个定时器的输入，从而实现更长的计时周期（最大59.69*65536*65536（约8千年））

## 定时中断基本结构

![定时中断基本结构](定时中断基本结构.jpg)

- 时基单元：
  包括预分频器、自动重装寄存器和计数器，负责生成定时中断。
- 运行控制：
  包括计数器的使能、计数方向（向上或向下计数）、计数模式（单次或连续）等。
- 时钟源：
  包括内部时钟（系统时钟）和外部时钟（外部引脚输入的时钟信号）。
- 定时中断
  中断信号先在状态寄存器中置一个中断标志位，然后通过中断输出控制到NVIC申请中断

## TIM类型

根据复杂度和应用场景分为了高级定时器、通用定时器、基本定时器三种类型

| 类型     | 编号                | 总线 | 功能          |
| -------- | ------------------- | ---- | ------------ |
| 高级定时器 | TIM1、TIM8          | APB2 | 拥有通用定时器全部功能，并额外具有重复计数器、死区生成、互补输出、刹车输入等功能 |
| 通用定时器 | TIM2、TIM3、TIM4、TIM5 | APB1 | 拥有基本定时器全部功能，并额外具有内外时钟源选择、输入捕获、输出比较、编码器接口、主从触发模式等功能 |
| 基本定时器 | TIM6、TIM7          | APB1 | 拥有定时中断、主模式触发DAC（数模转换器）的功能 |

STM32F103C8T6的定时器资源: TIM1、TIM2、TIM3、TIM4。

### 基本定时器结构

![基本定时器结构](基本定时器结构.jpg)

- UI（Update Interrupt）：更新中断，计数器溢出时触发
  配置好NVIC定时器通道后使得更新中断可以被CPU响应
- U（Update）：更新事件，计数器溢出时触发
  更新事件，可以触发其他电路的工作
- 主模式（Master Mode）：主模式触发DAC（数模转换器）
  正常情况下要实现DAC的输出需要在中断函数中调用代码手动触发DAC转换，然后DAC输出；
  但使用主模式触发DAC后，定时器的更新事件被映射到TRGO（触发输出）上，TRGO直接接到DAC触发转换引脚上。从而避免干扰主程序运行，减轻CPU负担。

### 通用定时器结构

![通用定时器结构](通用定时器结构.jpg)

- 相较于基本定时器只有向上计数模式，通用定时器和高级定时器还支持向下计数模式和中央对齐模式。
- 内外时钟源选择：基本定时器只能选择内部时钟（系统频率72MHz）通用定时器可以选择内部时钟或外部时钟
- **外部时钟模式2**
  输入信号通过ETR脚，经过极性选择、分频和滤波后生成触发信号，连接到从模式控制器
- **外部时钟模式1**
  输入信号通过定时器的输入通道(TIx)，经过极性选择和滤波后生成触发信号，连接到从模式控制器
  假设当TIM3的更新事件映射到TRGO上时，初始化TIM2时选择ITR2（对应TIM3的TRGO），时钟模式选择外部时钟模式1，TIM2的计数器就会在TIM3的更新事件到来时开始计数。即实现了**定时器级联。**
- 外部时钟输入也可以是CH1引脚的边沿，CH1和CH2引脚

## 时基单元时序

> 时基单元组件简称：PSC（预分频器）、CNT（计数器）、ARR（自动重装寄存器）

### 预分频器时序

当预分频器值从0到1时，即分频参数从1变为2时，预分频器的计数时序如下图所示：

![预分频器时序](预分频器时序.jpg)

- CK_PSC：预分频器输入时钟（此处参考基本定时器结构图更易理解）
- CNT_EN：计数器使能信号，高电平表示计数器开始计数
- CK_CNT：预分频器的输出时钟，计数器的输入时钟
  可以发现，在CNT_EN信号高电平时，CK_CNT信号与CK_PSC信号相同（因为预分频系数为1），后面系数改变，CK_CNT信号的频率会变慢。
- 计数器寄存器：16位寄存器，计数器的值从0开始计数
  计数器寄存器在计数器时钟的驱动下随时钟上升沿不断自增。可以发现，在寄存器值增大至FC后计数值变为0（可以推断FC即为ARR的值），当计数值和重装值相等且下一个时钟到来时，计数值才清零。
- 更新事件（UEV）：计数器寄存器的值清零时，产生更新事件
- 下面三行时序描述了预分频寄存器的缓冲机制（在图示中带灰色阴影的元件均有缓冲机制）
  预分频寄存器实际上有两个，一个是预分频控制寄存器，供用户读写，不直接决定预分频值；
  另一个是预分频缓冲寄存器，实际控制预分频值。使得当计数器正在计数时用户修改预分频值，变化不会立刻生效，而是在本次计数周期结束，产生更新事件时生效。

由此可得：

计数器计数频率：CK_CNT = CK_PSC / (PSC + 1)

> 缓冲机制可以由用户选择是否使用，通过设置ARPE位（自动重装寄存器预装载使能位）来决定。若ARPE=1，则使用缓冲寄存器，预分频值在更新事件时生效；若ARPE=0，则不使用缓冲寄存器，预分频值立即生效。


### 计数器时序

当内部时钟分频系数为2时，计数器的计数时序如下图所示：

![计数器时序](计数器时序.jpg)

- CK_INT：内部时钟（72MHZ）
- CNT_EN：计数器使能信号，高电平表示计数器开始计数
- CK_CNT: 计数器时钟
- 计数器寄存器：16位寄存器，计数器的值从0开始计数
  计数器寄存器在计数器时钟的驱动下随时钟上升沿不断自增。当增至0036（即ARR值）时，计数器溢出，产生一个更新事件（UEV），同时置位更新中断标志位（UIF）。当标志位置1，就会申请中断，中断响应后需在中断处理函数中清除标志位。

因此有：

计数器溢出频率：CK_CNT_OV = CK_CNT / (ARR + 1) = CK_PSC / ((PSC + 1) * (ARR + 1))

!![计数器无预装时序](计数器无预装时序.jpg)

当写入新数值到ARR寄存器时，即刻生效，无需等待本次计数周期结束。

1. 如果ARR值小于当前计数器值，计数器会在下一个时钟来临时溢出
2. 如果ARR值大于当前计数器值，计数器会继续计数直到达到新的ARR值

!![计数器有预装时序](计数器有预装时序.jpg)


## 定时中断库函数

```c
// 省略 void
// 初始化函数
TIM_DeInit(TIM_TypeDef* TIMx);// 恢复初始配置
TIM_TimeBaseInit(TIM_TypeDef* TIMx, 
TIM_TimeBaseInitTypeDef*TIM_TimeBaseInitStruct);// 初始化时基单元
TIM_TimeBaseStructInit(TIM_TimeBaseInitTypeDef* TIM_TimeBaseInitStruct);// 设置时基单元的默认值
TIM_Cmd(TIM_TypeDef* TIMx, FunctionalState NewState);// 使能或禁用定时器
TIM_ITConfig(TIM_TypeDef* TIMx, uint16_t TIM_IT, FunctionalState NewState);// 使能或禁用定时器中断
// 时基单元的时钟源选择
TIM_InternalClockConfig(TIM_TypeDef* TIMx);// 内部时钟
TIM_ITRxExternalClockConfig(TIM_TypeDef* TIMx, uint16_t TIM_ITRxSource);// ITRx其他定时器
TIM_TIxExternalClockConfig(TIM_TypeDef* TIMx, uint16_t TIM_TIxExternalCLKSource, uint16_t TIM_ICPolarity, uint16_t TIM_ICFilter);// TIx捕获通道，参数2：选择TIx引脚，参数3：极性，参数4：滤波器
// 外部时钟配置
TIM_ETRClockMode1Config(TIM_TypeDef* TIMx, uint16_t TIM_ExtTRGPrescaler, uint16_t TIM_ExtTRGPolarity, uint16_t ExtTRGFilter);// ETR外部时钟，参数2：预分频系数，参数3：极性，参数4：滤波器
TIM_ETRClockMode2Config(TIM_TypeDef* TIMx, uint16_t TIM_ExtTRGPrescaler, uint16_t TIM_ExtTRGPolarity, uint16_t ExtTRGFilter);// ETR外部时钟，参数2：预分频系数，参数3：极性，参数4：滤波器
TIM_ETRConfig(TIM_TypeDef* TIMx, uint16_t TIM_ExtTRGPrescaler, uint16_t TIM_ExtTRGPolarity, uint16_t ExtTRGFilter);// 单独用来配置ETR引脚
// 单独修改配置值
TIM_PrescalerConfig(TIM_TypeDef* TIMx, uint16_t Prescaler, uint16_t TIM_PSCReloadMode);// 修改预分频器值，参数2：预分频器值，参数3：重载模式
TIM_CounterModeConfig(TIM_TypeDef* TIMx, uint16_t TIM_CounterMode);// 修改计数模式，参数2：向上计数、向下计数、中央对齐
TIM_SetCounter(TIM_TypeDef* TIMx, uint32_t Counter);// 设置计数器值
YIM_ARRPreloadConfig(TIM_TypeDef* TIMx, FunctionalState NewState);// 自动重装器预装功能配置
TIM_SetAutoreload(TIM_TypeDef* TIMx, uint16_t Autoreload);// 设置自动重装寄存器值
TIM_GetCounter(TIM_TypeDef* TIMx);// 获取计数器值
TIM_GetPrescaler(TIM_TypeDef* TIMx);// 获取预分频器值
// 中断相关
ITStatus TIM_GetITStatus(TIM_TypeDef* TIMx, uint16_t TIM_IT);// 获取中断挂起标志位
TIM_ClearITPendingBit(TIM_TypeDef* TIMx, uint16_t TIM_IT);// 清除中断挂起标志位
FlagStatus TIM_GetFlagStatus(TIM_TypeDef* TIMx, uint16_t TIM_FLAG);// 获取主程序标志位
TIM_ClearFlag(TIM_TypeDef* TIMx, uint16_t TIM_FLAG);// 清除主程序标志位
```

## 定时中断配置

在`System`文件夹下新建Timer.c和Timer.h文件

### 初始化TIM

1. RCC开启定时器时钟（APB1）
2. 选择时基单元的时钟源
3. 配置时基单元
4. 配置输出中断控制，允许更新中断输出至NVIC
5. 配置NVIC，打开定时器中断通道并设置优先级
6. 启动定时器

```c
void Timer_Init(void){
    // 1. RCC开启定时器时钟（APB1）
    RCC_APB1PeriphClockCmd(RCC_APB1Periph_TIM2,ENABLE);
    // 2. 选择时基单元的时钟源
    TIM_InternalClockConfig(TIM2);//内部时钟源
    // 3. 配置时基单元
    TIM_TimeBaseInitTypeDef TIM_TimeBaseInitStructure;
    TIM_TimeBaseInitStructure.TIM_ClockDivision=TIM_CKD_DIV1;//时钟分频系数，DIV1表示不分频。滤波器在固定频率f下采样，若连续采样n次电平均相同则认为输入信号稳定：f越低，n越大，滤波效果越好,信号延迟越大。采样频率f可来源于内部时钟或内部时钟加一个时钟分频，分频多少即由TIM_ClockDivision决定。
    TIM_TimeBaseInitStructure.TIM_CounterMode=TIM_CounterMode_Up;//计数模式，向上计数
    TIM_TimeBaseInitStructure.TIM_Period=10000-1;//10kHz为10000次每秒，周期设10000代表计数周期为1s
    TIM_TimeBaseInitStructure.TIM_Prescaler=7200-1;//对72MHz进行7200分频，得10kHZ
    TIM_TimeBaseInitStructure.TIM_RepetitionCounter=0;//重复计数器，在高级计数器中出现，若无则置0
    TIM_TimeBaseInit(TIM2,&TIM_TimeBaseInitStructure);// 初始化时基单元
    // 4. 配置输出中断控制，允许更新中断输出至NVIC
    TIM_ITConfig(TIM2,TIM_IT_Update,ENABLE);//选择更新中断
    // 5. 配置NVIC，打开定时器中断通道并设置优先级
    NVIC_PriorityGroupConfig(NVIC_PriorityGroup_2);
    NVIC_InitTypeDef NVIC_InitStructure;
    NVIC_InitStructure.NVIC_IRQChannel=TIM2_IRQn;
    NVIC_InitStructure.NVIC_IRQChannelCmd=ENABLE;
    NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority=2;
    NVIC_InitStructure.NVIC_IRQChannelSubPriority=1;
    NVIC_Init(&NVIC_InitStructure);
    TIM_Cmd(TIM2,ENABLE);
}
```

### TIM中断处理函数

计数实现方式：

- 在`main.c`中放置中断函数

  ```c
  uint16_t Num;
  void TIM2_IRQHandler(void){
    if(TIM_GetITStatus(TIM2,TIM_IT_Update)==SET){
        Num++;
      TIM_ClearITPendingBit(TIM2,TIM_IT_Update);
    }
  }
  ```

- 在`Timer.c`中放置中断函数，使用`extern`关键字声明`main.c`中的变量

  ```c
  extern uint16_t Num;
  void TIM2_IRQHandler(void){
      if(TIM_GetITStatus(TIM2,TIM_IT_Update)==SET){
          Num++;
          TIM_ClearITPendingBit(TIM2,TIM_IT_Update);
      }
  }
  ```

**如何解决程序开始时Num值为1的问题？**

问题原因：在Time_BaseInit函数定义中提到：`Generate an update event to reload the Prescaler and the Repetition counter values immediately`
由于预分频器有一个缓冲寄存器，写入的值只有在更新事件时才会起作用，为了使写入值立即生效，TIM_TimeBaseInit函数会在初始化后立即触发一次更新事件`TIMx->EGR = TIM_PSCReloadMode_Immediate;`。但由于更新事件和更新中断是同时触发的，更新中断会置更新中断标志位，因此在初始化后就会立刻触发一次中断，导致Num值为1。

解决方法：

```c
TIM_TimeBaseInit(TIM2,&TIM_TimeBaseInitStructure);// 初始化时基单元
TIM_ClearFlag(TIM2,TIM_FLAG_Update);// 添加该语句，清除更新中断标志位
```

### 外部时钟配置

初始化函数如下：

```c
void Timer_Init(void){
    RCC_APB1PeriphClockCmd(RCC_APB1Periph_TIM2,ENABLE);//开启TIM2时钟
    RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA,ENABLE);//开启GPIOA时钟
    GPIO_InitTypeDef GPIO_InitStructure;
    GPIO_InitStructure.GPIO_Pin=GPIO_Pin_0;//PA0引脚
    GPIO_InitStructure.GPIO_Mode=GPIO_Mode_IPU;//上拉输入，在输入信号功率较小时用浮空输入，避免上拉电阻对输入信号的影响
    GPIO_InitStructure.GPIO_Speed=GPIO_Speed_50MHz;//输入速度，50MHz
    GPIO_Init(GPIOA,&GPIO_InitStructure);//初始化GPIOA的PA0引脚
    // 2. 选择时基单元的时钟源
    TIM_ETRClockMode2Config(TIM2,TIM_ExtTRGPSC_OFF,TIM_ExtTRGPolarity_NonInverted,0x00);// ETR外部时钟，参数2：预分频系数，参数3：外部触发极性，参数4：滤波器，0x00表示无滤波
    // 3. 配置时基单元
    TIM_TimeBaseInitTypeDef TIM_TimeBaseInitStructure;
    TIM_TimeBaseInitStructure.TIM_ClockDivision=TIM_CKD_DIV1;//时钟分频系数
    TIM_TimeBaseInitStructure.TIM_CounterMode=TIM_CounterMode_Up;//计数模式，向上计数
    TIM_TimeBaseInitStructure.TIM_Period=10-1;//10次每秒，周期设10代表计数周期为1s
    TIM_TimeBaseInitStructure.TIM_Prescaler=1-1;//不分频
    TIM_TimeBaseInitStructure.TIM_RepetitionCounter=0;//重复计数器，在高级计数器中出现，若无则置0
    TIM_TimeBaseInit(TIM2,&TIM_TimeBaseInitStructure);// 初始化时基单元
    TIM_ClearFlag(TIM2,TIM_FLAG_Update);// 清除更新中断标志位
    TIM_ITConfig(TIM2,TIM_IT_Update,ENABLE);//选择更新中断
    NVIC_PriorityGroupConfig(NVIC_PriorityGroup_2);
    NVIC_InitTypeDef NVIC_InitStructure;
    NVIC_InitStructure.NVIC_IRQChannel=TIM2_IRQn;
    NVIC_InitStructure.NVIC_IRQChannelCmd=ENABLE;
    NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority=2;
    NVIC_InitStructure.NVIC_IRQChannelSubPriority=1;
    NVIC_Init(&NVIC_InitStructure);
    TIM_Cmd(TIM2,ENABLE);//启动定时器
}
```

## TIM捕获/比较

CCR（捕获/比较寄存器）

> CCR在输出比较模式下为比较寄存器，在输入捕获模式下为捕获寄存器。

### PWM波形

PWM（Pulse Width Modulation，脉冲宽度调制）

PWM波形是一种**数字**信号，在具有惯性的系统中，可以通过对一系列脉冲的宽度进行调制，来等效地获得所需要的**模拟**参量，常应用于电机控速等领域

> 简单来说，通过高低电平的跳变信号，给电机不断地通断电，从而实现对电机速度的控制
> LED调光也是类似的原理，通过调节高电平的时间比例来控制LED的亮度
> 可以发现，这些操作对象都需要一定的”惯性“，才能实现平滑的控制效果

![PWM波形](PWM波形.jpg)

如图，高低电平的跳变信号可以等效为一个模拟信号，当正向脉冲宽度越大，等效的模拟信号值就偏向正向，反之亦然。

![PWM参数](PWM参数.jpg)

- 频率 = $1 / \mathrm{Ts}$
  
  $\mathrm{Ts}$表示一个高低电平变换周期的时间。
  PWM频率越快，等效的模拟信号就越平稳。

- 占空比 = $\mathrm{Ton} / \mathrm{Ts}$

  $\mathrm{Ton}$表示高电平的时间。
  占空比越大，等效的模拟信号值就越大。占空比与等效电压的关系为：
  $V_{out} = V_{in} \times \text{占空比}$

- 分辨率 = 占空比变化步距

  假设占空比以0.1%为步距变化，则分辨率为0.001。
  分辨率表示PWM波形的精细程度，分辨率越高，PWM波形就越接近理想的模拟信号。
  
### TIM输出比较

OC（Output Compare，输出比较）

- 输出比较可以通过比较CNT（计数器）与CCR值的关系，来对输出电平进行置1、置0或翻转的操作，用于输出一定频率和占空比的的PWM波形
- 每个高级定时器和通用定时器都拥有4个输出比较通道
- 高级定时器的前3个通道额外拥有死区生成和互补输出的功能

#### 输出比较通道

![输出比较通道](通用定时器结构.jpg)

图中可见4个CCR（捕获/比较寄存器）和一个CNT，分别对应4个输出比较通道（OC1、OC2、OC3、OC4）。4个通道将信号通过TIMx_CH1、TIMx_CH2、TIMx_CH3、TIMx_CH4输出到GPIO引脚。

!![输出比较通道结构](输出比较通道（通用）.jpg)

以通道一为例：
1. 当CNT大于或等于CCR1时，输出模式控制器会改变它输出的OC1REF(*输出比较1参考值*)的高低电平
2. REF信号可以前往主模式控制器，但主要是前往极性选择处，给TIMx_CCER(捕获/比较使能寄存器)的CC1P(捕获/比较1输出极性选择位)设置为0，信号电平不翻转，设置为1，信号通过非门取反，电平翻转
3. 然后信号前往输出使能电路，修改CC1E（捕获/比较1输出使能位）为1，允许输出到OC1通道
4. 前往TIMx_CH1输出，根据查阅引脚定义表得知其对应引脚映射:
   - TIM2_CH1: PA0
   - TIM3_CH1: PB4
   - TIM4_CH1: PB6
5. 通过引脚重定义还可以将TIMx_CH1映射到PA15引脚上

#### 输出比较模式

即输出模式控制器的执行逻辑，模式通过TIMx_CCMR1(捕获/比较模式寄存器1)的OC1M(输出比较1模式)位来选择。

| 模式 | 描述 | 作用 |
| :---: | :---: | :---: |
| 冻结 | CNT=CCR时，REF保持为原状态 | 暂停PWM波形输出 |
| 匹配时置有效电平(高电平) | CNT=CCR时，REF置有效电平 | 定时输出一次性信号 |
| 匹配时置无效电平(低电平) | CNT=CCR时，REF置无效电平 | 定时输出一次性信号 |
| 匹配时电平翻转 | CNT=CCR时，REF电平翻转 | 输出占空比为50%的方波 |
| 强制为无效电平 | CNT与CCR无效，REF强制为无效电平 | 暂停PWM波形输出，维持低电平 |
| 强制为有效电平 | CNT与CCR无效，REF强制为有效电平 | 暂停PWM波形输出，维持高电平 |
| PWM模式1 | 向上计数：CNT<CCR时，REF置有效电平，CNT≥CCR时，REF置无效电平向下计数：CNT>CCR时，REF置无效电平，CNT≤CCR时，REF置有效电平 | 输出频率和占空比可调的PWM波形 |
| PWM模式2 | 向上计数：CNT<CCR时，REF置无效电平，CNT≥CCR时，REF置有效电平向下计数：CNT>CCR时，REF置有效电平，CNT≤CCR时，REF置无效电平 | 输出频率和占空比可调的PWM波形 |

#### 输出比较库函数

```c
// 初始化函数
void TIM_OC1Init(TIM_TypeDef* TIMx, TIM_OCInitTypeDef* TIM_OCInitStruct);
void TIM_OC2Init(TIM_TypeDef* TIMx, TIM_OCInitTypeDef* TIM_OCInitStruct);
void TIM_OC3Init(TIM_TypeDef* TIMx, TIM_OCInitTypeDef* TIM_OCInitStruct);
void TIM_OC4Init(TIM_TypeDef* TIMx, TIM_OCInitTypeDef* TIM_OCInitStruct);
void TIM_OCStructInit(TIM_OCInitTypeDef* TIM_OCInitStruct);
//TIM_OCInitStruct的成员变量说明：
//TIM_OCMode：输出比较模式
//TIM_OCPolarity：输出比较极性
//TIM_OutputState：输出使能
//TIM_Pulse：比较寄存器（CCR）值
//TIM_OCIdleState：空闲状态下的输出状态，正向或反向（仅高级定时器）
//TIM_OCNIdleState：互补输出空闲状态下的输出状态，正向或反向（仅高级定时器）
//TIM_OCNPolarity：互补输出极性，正向或反向（仅高级定时器）

// 单独修改配置值
void TIM_ForcedOC1Config(TIM_TypeDef* TIMx, uint16_t TIM_ForcedAction);
void TIM_ForcedOC2Config(TIM_TypeDef* TIMx, uint16_t TIM_ForcedAction);
void TIM_ForcedOC3Config(TIM_TypeDef* TIMx, uint16_t TIM_ForcedAction);
void TIM_ForcedOC4Config(TIM_TypeDef* TIMx, uint16_t TIM_ForcedAction);

// 设置预装功能（影子寄存器）
void TIM_OC1PreloadConfig(TIM_TypeDef* TIMx, uint16_t TIM_OCPreload);
void TIM_OC2PreloadConfig(TIM_TypeDef* TIMx, uint16_t TIM_OCPreload);
void TIM_OC3PreloadConfig(TIM_TypeDef* TIMx, uint16_t TIM_OCPreload);
void TIM_OC4PreloadConfig(TIM_TypeDef* TIMx, uint16_t TIM_OCPreload);

// 单独设置极性，函数中带N的为高级定时器的互补输出功能，OC4没有互补输出功能
void TIM_OC1PolarityConfig(TIM_TypeDef* TIMx, uint16_t TIM_OCPolarity);
void TIM_OC1NPolarityConfig(TIM_TypeDef* TIMx, uint16_t TIM_OCNPolarity);
void TIM_OC2PolarityConfig(TIM_TypeDef* TIMx, uint16_t TIM_OCPolarity);
void TIM_OC2NPolarityConfig(TIM_TypeDef* TIMx, uint16_t TIM_OCNPolarity);
void TIM_OC3PolarityConfig(TIM_TypeDef* TIMx, uint16_t TIM_OCPolarity);
void TIM_OC3NPolarityConfig(TIM_TypeDef* TIMx, uint16_t TIM_OCNPolarity);
void TIM_OC4PolarityConfig(TIM_TypeDef* TIMx, uint16_t TIM_OCPolarity);

// 单独修改输出使能参数
void TIM_CCxCmd(TIM_TypeDef* TIMx, uint16_t TIM_Channel, uint16_t TIM_CCx);
void TIM_CCxNCmd(TIM_TypeDef* TIMx, uint16_t TIM_Channel, uint16_t TIM_CCxN);

// 单独更改输出比较模式
void TIM_SelectOCxM(TIM_TypeDef* TIMx, uint16_t TIM_Channel, uint16_t TIM_OCMode);

// 运行时更改占空比
void TIM_SetCompare1(TIM_TypeDef* TIMx, uint16_t Compare1);//Compare1是CCR1寄存器的值
void TIM_SetCompare2(TIM_TypeDef* TIMx, uint16_t Compare2);
void TIM_SetCompare3(TIM_TypeDef* TIMx, uint16_t Compare3);
void TIM_SetCompare4(TIM_TypeDef* TIMx, uint16_t Compare4);
```
#### PWM输出基本结构

![PWM输出基本结构](PWM输出基本结构.jpg)

以PWM模式1为例，输出波形如图：

![PWM输出波形图](PWM输出波形图.jpg)

参数计算：
- PWM频率：	 $Freq = CK_PSC / (PSC + 1) / (ARR + 1)$
- PWM占空比：	$Duty = CCR / (ARR + 1)$
- PWM分辨率：	$Reso = 1 / (ARR + 1)$

#### 外设

##### 舵机

- 舵机是一种根据输入PWM信号占空比来控制输出角度的装置
- 输入PWM信号要求：周期为20ms，高电平宽度为0.5ms~2.5ms

| 输入信号脉冲宽度（周期20ms） | 舵机输出轴转角（方向：CW，顺时针） | 舵机输出轴转角（方向：CCW，逆时针） |
|------------------------------|-----------------------------|------------------------------|
| 0.5ms                        | 0°                          | 180°                         |
| 1ms                          | 45°                         | 135°                         |
| 1.5ms                        | 90°                         | 90°                          |
| 2ms                          | 135°                        | 45°                          |
| 2.5ms                        | 180°                        | 0°                           |

![舵机接线](舵机接线.jpg)

##### 直流电机

- 直流电机是一种将电能转换为机械能的装置，有两个电极，当电极正接时，电机正转，当电极反接时，电机反转
- 直流电机属于大功率器件，GPIO口无法直接驱动，需要配合电机驱动电路来操作
- TB6612是一款双路H桥型的直流电机驱动芯片，可以驱动两个直流电机并且控制其转速和方向

![电机驱动接线](电机驱动接线.jpg)

**引脚定义表**

| 引脚    | 定义                                   |
|---------|---------------------------------------|
| VM      | 驱动电压输入端（4.5~10V）             |
| VCC     | 逻辑电平输入端（2.7~5.5V），与控制器电源保持一致 |
| GND     | 电源地端（两个，任选一个）                     |
| STBY    | 正常工作/待机状态控制输入端（接逻辑电源VCC时芯片正常工作，接地则待机）|
| 1路电机如下：|                                  |
| PWMA    | PWM信号输入端                         |
| AIN1    | 电机控制模式输入端                     |
| AIN2    | 电机控制模式输入端                     |
| A01     | 电机驱动输出端                         |
| A02     | 电机驱动输出端                         |
| 2路电机如下：|                                   |
| PWMB    | PWM信号输入端                          |
| BIN1    | 电机控制模式输入端                     |
| BIN2    | 电机控制模式输入端                     |
| B01     | 电机驱动输出端                         |
| B02     | 电机驱动输出端                         |

**控制逻辑表**

IN1、IN2决定正反转，PWM决定是否转，STBY决定工作/待机状态

|输入| | | |输出| | |
| --- | --- | --- | --- | --- | --- | --- |
|IN1|IN2|PWM|STBY|O1|O2|模式状态|
|H|H|H/L|H|L|L|制动|
|L|H|H|H|L|H|反转|
|L|H|L|H|L|L|制动|
|H|L|H|H|H|L|正转|
|H|L|L|H|L|L|制动|
|L|L|H|H|OFF|OFF|停止|
|H/L|H/L|H/L|L|OFF|OFF|待机|

#### PWM初始化

1. RCC开启定时器时钟（APB1）
2. 配置时基单元
3. 配置输出比较单元
4. 启动计数器

```c
void PWM_Init(void){
  // 1. RCC开启定时器时钟（APB1）
	RCC_APB1PeriphClockCmd(RCC_APB1Periph_TIM2,ENABLE);
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA,ENABLE);
	
  // 2. 配置GPIO引脚
	GPIO_InitTypeDef GPIO_InitStructure;
	GPIO_InitStructure.GPIO_Mode=GPIO_Mode_AF_PP; // 复用推挽输出，想要用定时器控制引脚必须设置为复用推挽输出
	GPIO_InitStructure.GPIO_Pin=GPIO_Pin_0; // PA0引脚是TIM2_CH1的复用引脚
	GPIO_InitStructure.GPIO_Speed=GPIO_Speed_50MHz;
	GPIO_Init(GPIOA,&GPIO_InitStructure);
  
  // 3. 配置时基单元
	TIM_InternalClockConfig(TIM2);
	TIM_TimeBaseInitTypeDef TIM_TimeBaseInitStructure;
	TIM_TimeBaseInitStructure.TIM_ClockDivision=TIM_CKD_DIV1;
	TIM_TimeBaseInitStructure.TIM_CounterMode=TIM_CounterMode_Up;
	TIM_TimeBaseInitStructure.TIM_Period=100-1;
	TIM_TimeBaseInitStructure.TIM_Prescaler=720-1;
	TIM_TimeBaseInitStructure.TIM_RepetitionCounter=0;
	TIM_TimeBaseInit(TIM2,&TIM_TimeBaseInitStructure);
	
  // 4. 配置输出比较单元
	TIM_OCInitTypeDef TIM_OCInitStructure;
  //由于部分成员变量仅在高级定时器中使用，所以未初始化，故需先调用TIM_OCStructInit函数赋默认值避免出现bug
	TIM_OCStructInit(&TIM_OCInitStructure);// 设置输出比较单元的默认值
	TIM_OCInitStructure.TIM_OCMode=TIM_OCMode_PWM1;// 输出比较模式，PWM模式1
	TIM_OCInitStructure.TIM_OCPolarity=TIM_OCPolarity_High;// 输出比较极性，高电平
	TIM_OCInitStructure.TIM_OutputState=TIM_OutputState_Enable;// 输出使能
	TIM_OCInitStructure.TIM_Pulse=0; // CCR比较寄存器值
  // 计算公式：占空比 = CCR / (ARR + 1)
	TIM_OC1Init(TIM2,&TIM_OCInitStructure);

  // 5. 启动计数器
  TIM_Cmd(TIM2,ENABLE);
}
```

通过引脚重定义将TIM2_CH1映射到PA15引脚上，要使用AFIO复用IO口外设

```c
RCC_APB2PeriphClockCmd(RCC_APB2Periph_AFIO,ENABLE); // 开启AFIO时钟

GPIO_PinRemapConfig(GPIO_PartialRemap1_TIM2,ENABLE); // 将TIM2_CH1部分重映射到PA15引脚
// 由于PA15引脚默认复用为调试端口JTDI,需要关闭调试端口。
// 三个参数解除调试端口的复用功能：
// GPIO_Remap_SWJ_NoJTRST: 解除JTRST引脚复用
// GPIO_Remap_SWJ_JTAGDisable: 解除JTAG的调试端口复用
// GPIO_Remap_SWJ_Disable: 解除SWD和JTAG的调试端口复用
GPIO_PinRemapConfig(GPIO_Remap_SWJ_JTAGDisable,ENABLE);
```

#### 外设使用

##### LED呼吸灯

```c
// 封装函数修改CCR值，从而改变占空比
void PWM_SetCompare1(uint16_t Compare){
	TIM_SetCompare1(TIM2,Compare);
}
```

```c
// 在main.c中调用PWM_SetCompare1函数
void main(void){
    PWM_Init(); // 初始化PWM
    while(1){
        for(uint16_t i=0;i<100;i++){ // 从0到99，逐渐增大占空比
            PWM_SetCompare1(i); // 设置占空比
            Delay(10); // 延时10ms
        }
        for(uint16_t i=100;i>0;i--){ // 从99到0，逐渐减小占空比
            PWM_SetCompare1(i); // 设置占空比
            Delay(10); // 延时10ms
        }
    }
}
```

##### 舵机操控

![舵机接线](PWM驱动舵机.jpg)

```c
// Servo.c
void Servo_Init(void){
    PWM_Init();
}
/*
CCR->Angle
5-> -90
10-> -45
15-> 0
20-> 45
25-> 90
*/
void Servo_Angle(float Angle){
    PWM_SetCompare2(15+5*(Angle/45));
}
```

```c
// main.c
float Angle=-90;
uint8_t KeyNum;
int main(void){
	OLED_Init();
	Servo_Init();
    Key_Init();
	OLED_ShowString(1,1,"Angle:");
	OLED_ShowSignedNum(1,7,Angle,2);
    while(1){
		KeyNum=Key_GetNum();
		if(KeyNum==1){
		    Angle+=45;
			if(Angle>90){
				Angle=-90;
		    }
		}
		Servo_Angle(Angle);
		OLED_ShowSignedNum(1,7,Angle,2);
	}
}
```

##### 电机转速控制

![电机接线](PWM驱动直流电机.jpg)

```c
// Motor.c
void Motor_Init(void)
{
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA, ENABLE);
	GPIO_InitTypeDef GPIO_InitStructure;
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_Out_PP;//推挽输出,使用推挽输出模式控制电机的转向
	GPIO_InitStructure.GPIO_Pin = GPIO_Pin_4 | GPIO_Pin_5;
	GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
	GPIO_Init(GPIOA, &GPIO_InitStructure);
	PWM_Init();//初始化直流电机的底层PWM
}
void Motor_SetSpeed(int8_t Speed)
{
	if (Speed >= 0)	
	{
		GPIO_SetBits(GPIOA, GPIO_Pin_4);	//PA4置高电平
		GPIO_ResetBits(GPIOA, GPIO_Pin_5);	//PA5置低电平，设置方向为正转
		PWM_SetCompare3(Speed);				//PWM设置为速度值
	}
	else
	{
		GPIO_ResetBits(GPIOA, GPIO_Pin_4);	//PA4置低电平
		GPIO_SetBits(GPIOA, GPIO_Pin_5);	//PA5置高电平，设置方向为反转
		PWM_SetCompare3(-Speed);			//PWM设置为负的速度值，因为此时速度值为负数，而PWM只能给正数
	}
}
```

```c
// main.c
OLED_Init();
Motor_Init();
Key_Init();
OLED_ShowString(1, 1, "Speed:");
while (1)
{
	KeyNum = Key_GetNum();	
	if (KeyNum == 1)				
	{
		Speed += 20;
    if(speed>100)				
		{
			Speed = -100;//此操作会让电机旋转方向突然改变，可能会因供电不足而导致单片机复位,若出现了此现象，则应避免使用这样的操作
		}
	}
	Motor_SetSpeed(Speed);
	OLED_ShowSignedNum(1, 7, Speed, 3);
}
```

### TIM输入捕获

IC（Input Capture，输入捕获）

- 输入捕获模式下，当通道输入引脚出现指定电平跳变时，当前CNT的值将被锁存到CCR中，可用于测量PWM波形的频率、占空比、脉冲间隔、电平持续时间等参数
- 每个高级定时器和通用定时器都拥有4个输入捕获通道
- 可配置为PWMI模式，同时测量频率和占空比
- 可配合主从触发模式，实现硬件全自动测量

#### 频率测量

使用stm32测量任意波形需要先将其转换为高低电平信号。

![频率测量](频率测量.jpg)


- 测频法(适用于高频)：在闸门时间$T$内，对上升沿计次，得到$N$，则频率
  $f_x = N / T$
- 测周法（适用于低频）：两个上升沿内，以标准频率$f_c$计次，得到$N$，则频率
  $f_x = f_c / N$
- 中界频率：测频法与测周法误差相等的频率点
  由于测频法和测周法都可能存在1个计数误差，因此测频法的误差为$±1/T$，测周法的误差为$±f_c/N^2$，令两者相等可得中界频率

  $f_{m} = \sqrt{f_x*f_x} = \sqrt{(f_c/N)(N/T)} = \sqrt{f_{c}/T}$

**测周法的误差为什么是$±f_c/N^2$？**

由于计数器只能记录整数个脉冲，存在最大 $±1$ 个脉冲的量化误差。假设实际计数为 $N$，但由于量化，实际可能是 $N±1$，则测量得到的频率为：
$f_x' = \frac{f_c}{N±1}$

误差为： $\Delta f = f_x' - f_x = \frac{f_c}{N±1} - \frac{f_c}{N}$

对 $N$ 远大于 1 的情况，使用泰勒展开近似： 
$\frac{1}{N±1} \approx \frac{1}{N} \mp \frac{1}{N^2}$

所以误差近似为： $\Delta f \approx \mp \frac{f_c}{N^2}$

#### 主从触发模式

主模式，从模式，触发源选择三个功能的简称：

- 主模式：将定时器内部信号映射到TRGO
- 从模式：接收其他外设或自身外设的触发信号，用于控制自身定时器的运行
- 触发源选择：选择从模式的触发信号源，选择指定信号，得到TRGI，输入到从模式的触发输入端

| 主模式信号 | 说明           | 触发源选择 | 说明           | 从模式类型 | 说明           |
|------------|----------------|------------|----------------|------------|----------------|
| Reset      | 复位           | ITR0       | 内部触发0      | Closed     | 关闭           |
| Enable     | 使能           | ITR1       | 内部触发1      | Encoder1   | 编码器模式1    |
| Update     | 更新           | ITR2       | 内部触发2      | Encoder2   | 编码器模式2    |
| OC1        | 输出比较1      | ITR3       | 内部触发3      | Encoder3   | 编码器模式3    |
| OC1REF     | 输出比较1参考  | TI1F_ED    | 通道1边沿检测  | Reset      | 复位           |
| OC2REF     | 输出比较2参考  | TI1FP1     | 通道1滤波器1   | Gated      | 门控           |
| OC3REF     | 输出比较3参考  | TI2FP2     | 通道2滤波器2   | Trigger    | 触发           |
| OC4REF     | 输出比较4参考  | ETRF       | 外部触发       | External1  | 外部模式1      |

> 从模式参考文档：STM32F10xxx参考手册：14.4.3

#### 输入捕获通道

![输入捕获通道](通用定时器结构.jpg)

-在图中可见4个CCR（捕获/比较寄存器）和一个CNT，分别对应4个输入捕获通道（IC1、IC2、IC3、IC4）。

在TIMx_CHx引脚处，可以发现一个异或门：异或门（当三个输入电平有任何一个发生翻转，输出引脚就发生一次电平翻转）输入接在通道1，2，3端口，输出接在一个数据选择器上。当数据选择器选择上面一个，那输入捕获通道1的输入就是3个引脚的异或值，如果选择下面一个，那异或门无作用。（设计异或门的主要目的是服务于三相无刷电机）

![输入捕获通道结构](输入捕获通道结构.jpg)

以通道一为例：

- 输入滤波器和边沿检测器
  - 输入滤波器用于消除输入信号的抖动
  - 边沿检测器用于检测输入信号的上升沿或下降沿
  - 此处有**两套**滤波器和边沿检测器，分别产生两个信号：TI1FP1和TI1FP2
    且通道一二的两个信号可以交叉，其作用是：
    - 灵活切换后续捕获电路的输入
    - 把一个引脚的输入同时映射到两个捕获通道上
- 数据选择器
  三个信号：TI1FP1、TI1FP2和TRC
- 预分频器
  给信号分频
- 捕获寄存器（CCR）
  每来一个触发信号，就将当前计数器CNT的值转运到对应的捕获寄存器中，
  转运同时，会触发一个捕获事件，捕获事件会在状态寄存器设置一个标志位，也可以产生中断。

#### 输入捕获基本结构

![输入捕获基本结构](输入捕获基本结构.jpg)

- 配置好时基单元，启动定时器，CNT不断自增，标准频率$f_c = CK_PSC / (PSC + 1) / (ARR + 1)$
- GPIO口输入上升信号，选择TI1FP1作为上升沿触发，分频器选择不分频
- 当输入信号上升沿到来时，CNT的值被锁存到CCR1中，
- 同时触发源选择选中TI1FP1作为触发信号，从模式选择复位操作，这样，当输入信号上升沿到来时，CNT被清零（CNT先锁存后清零）
- 从而实现全自动测量输入信号的周期（测周法）

> 注意：
> 1. ARR值最大为65535，若输入信号频率太低，CNT会溢出，导致测量错误。
> 2. 从模式的触发源只有TI1FP1和TI1FP2，故要实现自动测量，必须使用通道1或通道2。对于通道3和通道4，只能开启捕获中断，在中断中手动清零CNT。

#### PWMI基本结构

![PWMI基本结构](PWMI基本结构.jpg)

- TI1FP1配置上升沿触发，触发捕获和清零CNT，捕获周期
- TI1FP2配置下降沿触发，通过交叉通道，触发通道二的捕获单元，此时：CNT的值被锁存到CCR2，那么占空比：$Duty = CCR2 / CCR1$

#### 输入捕获库函数

```c
// 初始化函数
void TIM_ICInit(TIM_TypeDef* TIMx, TIM_ICInitTypeDef* TIM_ICInitStruct);//初始化
void TIM_ICStructInit(TIM_ICInitTypeDef* TIM_ICInitStruct);//配置四个通道中的一个
//TIM_ICInitStruct的成员变量说明：
//TIM_Channel：选择输入捕获通道
//TIM_ICPolarity：输入捕获极性
//TIM_ICSelection：输入捕获选择
//TIM_ICPrescaler：输入捕获预分频
//TIM_ICFilter：输入捕获滤波器
void TIM_PWMIConfig(TIM_TypeDef* TIMx, TIM_ICInitTypeDef* TIM_ICInitStruct);//配置PWMI模式
// 主从触发配置函数
void TIM_SelectInputTrigger(TIM_TypeDef* TIMx, uint16_t TIM_InputTriggerSource);//选择输入触发源TRGI
void TIM_SelectOutputTrigger(TIM_TypeDef* TIMx, uint16_t TIM_OutputTriggerSource);//选择输出触发源TRGO
void TIM_SelectSlaveMode(TIM_TypeDef* TIMx, uint16_t TIM_SlaveMode);//选择从模式
void TIM_SelectIC1Prescaler(TIM_TypeDef* TIMx, uint16_t TIM_IC1Prescaler);//选择通道1的预分频
void TIM_SelectIC2Prescaler(TIM_TypeDef* TIMx, uint16_t TIM_IC2Prescaler);//选择通道2的预分频
void TIM_SelectIC3Prescaler(TIM_TypeDef* TIMx, uint16_t TIM_IC3Prescaler);//选择通道3的预分频
void TIM_SelectIC4Prescaler(TIM_TypeDef* TIMx, uint16_t TIM_IC4Prescaler);//选择通道4的预分频
uint16_t TIM_GetCapture1(TIM_TypeDef* TIMx);//获取捕获寄存器CCR1的值
uint16_t TIM_GetCapture2(TIM_TypeDef* TIMx);//获取捕获寄存器CCR2的值
uint16_t TIM_GetCapture3(TIM_TypeDef* TIMx);//获取捕获寄存器CCR3的值
uint16_t TIM_GetCapture4(TIM_TypeDef* TIMx);//获取捕获寄存器CCR4的值
```

#### 输入捕获模式测频率与占空比

1. 使用输出比较模式输出PWM波形
2. 设置调节PWM波形的频率和占空比的函数
   调节频率可以通过改变ARR的值或PSC的值来实现，但调节ARR的值会影响占空比，因此调节PSC的值更为合适。
   改频率：
   ```c
   void PWM_SetPrescaler(uint16_t Prescaler){
       TIM_PrescalerConfig(TIM2,Prescaler,TIM_PSCReloadMode_Immediate);
   }
   ```
   改占空比：
   ```c
   void PWM_SetCompare1(uint16_t Compare){
       TIM_SetCompare1(TIM2,Compare);
   }
   ```
3. 初始化IC通道1
   ```c
   //"IC.c"
   void IC_Init(void){
   // 1. RCC开启时钟
   RCC_APB1PeriphClockCmd(RCC_APB1Periph_TIM3,ENABLE);
	 RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA,ENABLE);
	 // 2. 配置GPIO引脚
	 GPIO_InitTypeDef GPIO_InitStructure;
	 GPIO_InitStructure.GPIO_Mode=GPIO_Mode_IPU;//也可以浮空输入
	 GPIO_InitStructure.GPIO_Pin=GPIO_Pin_6;//TIM3的通道1引脚
	 GPIO_InitStructure.GPIO_Speed=GPIO_Speed_50MHz;
	 GPIO_Init(GPIOA,&GPIO_InitStructure);
	 // 3. 配置时基单元
	 TIM_InternalClockConfig(TIM3);//内部时钟配置
	 TIM_TimeBaseInitTypeDef TIM_TimeBaseInitStructure;
	 TIM_TimeBaseInitStructure.TIM_ClockDivision=TIM_CKD_DIV1;
	 TIM_TimeBaseInitStructure.TIM_CounterMode=TIM_CounterMode_Up;
	 TIM_TimeBaseInitStructure.TIM_Period=65536-1;
	 TIM_TimeBaseInitStructure.TIM_Prescaler=72-1;//故标准频率为1MHz
	 TIM_TimeBaseInitStructure.TIM_RepetitionCounter=0;
	 IM_TimeBaseInit(TIM3,&TIM_TimeBaseInitStructure);
	 // 4. 配置输入捕获通道
   //通道一配置
	 TIM_ICInitTypeDef TIM_ICInitStructure;
	 TIM_ICInitStructure.TIM_Channel=TIM_Channel_1;
	 TIM_ICInitStructure.TIM_ICFilter=0xF;
	 TIM_ICInitStructure.TIM_ICPolarity=TIM_ICPolarity_Rising;//上升沿触发
	 TIM_ICInitStructure.TIM_ICPrescaler=TIM_ICPSC_DIV1;
	 TIM_ICInitStructure.TIM_ICSelection=TIM_ICSelection_DirectTI;//直连输入
   TIM_PWMIConfig(TIM3,&TIM_ICInitStructure);//配置PWMI模式
   //该函数可以快捷地把电路配置为PWMI模式的标准结构
   //也可以手动配置PWMI模式：
   /*
	 TIM_ICInit(TIM3,&TIM_ICInitStructure);
   //通道二配置
	 TIM_ICInitStructure.TIM_Channel=TIM_Channel_2;
	 TIM_ICInitStructure.TIM_ICFilter=0xF;
	 TIM_ICInitStructure.TIM_ICPolarity=TIM_ICPolarity_Falling;//下降沿触发
	 TIM_ICInitStructure.TIM_ICPrescaler=TIM_ICPSC_DIV1;
	 TIM_ICInitStructure.TIM_ICSelection=TIM_ICSelection_IndirectTI;//交叉输入
	 TIM_ICInit(TIM3,&TIM_ICInitStructure);
   */
	 // 5. 配置主从触发模式
	 TIM_SelectInputTrigger(TIM3,TIM_TS_TI1FP1);
	 TIM_SelectSlaveMode(TIM3,TIM_SlaveMode_Reset);
	 // 6. 开启定时器
	 TIM_Cmd(TIM3,ENABLE);
   }
   ```
4. 读取频率，占空比函数
   ```c
   uint32_t IC_GetFreq(void){
       return 1000000/(TIM_GetCapture1(TIM3)+1);
   }
   uint32_t IC_GetDuty(void){
    return (TIM_GetCapture2(TIM3)+1)*100/(TIM_GetCapture1(TIM3)+1);
   }
   ```

## 编码器接口

Encoder Interface

- 编码器接口可接收增量（正交）编码器的信号，根据编码器旋转产生的正交信号脉冲，自动控制CNT自增或自减，从而指示编码器的位置、旋转方向和旋转速度
- 每个高级定时器和通用定时器都拥有1个编码器接口
- 两个输入引脚借用了输入捕获的通道1和通道2

> 正交编码器：
>
> 正交编码器是一种特殊的增量编码器，具有两个输出信号A和B，相位相差90度。
>
> ![正交编码器](正交编码器.jpg)

### 编码器接口基本结构

![通用定时器结构](通用定时器结构.jpg)

![编码器接口基本结构](编码器接口基本结构.jpg)

- 编码器接口接收两个信号：TI1FP1和TI2FP2
- 编码器信号控制CNT的自增或自减

### 编码器接口工作模式

![编码器接口工作模式](编码器接口工作模式.jpg)

- 仅在TI1或TI2计数，单相计数，精度低
- 在TI1和TI2上都计数，双相计数，抗噪声，精度高
  如图：

  ![双相计数](双相计数实例图.jpg)

  如果出现一个引脚不变，另一个引脚连续跳变的毛刺信号，计数器就会加减来回摆动，最终计数值不变，避免了噪声影响。

**编码器模式下的极性选择器的作用：**

对于编码器接口，信号的上升沿和下降沿均有效，故此模式下的极性选择器不再是边沿的极性选择，而是高低电平的极性选择：
- 如果选择上升沿，那么高低电平不翻转
- 如果选择下降沿，那么高低电平翻转
  
  ![双相计数（TI1反相）](双相计数实例图（TI1反相）.jpg)

  TI1反相后，计数器的自增和自减方向发生了翻转。
  把任意一个引脚的极性翻转后，计数方向就会反转。

### 编码器接口库函数

```c
void TIM_EncoderInterfaceConfig(TIM_TypeDef* TIMx, uint16_t TIM_EncoderMode, uint16_t TIM_IC1Polarity, uint16_t TIM_IC2Polarity);
```

### 编码器接口测速

1. 初始化编码器接口
   ```c
   void Encoder_Init(void){
    RCC_APB1PeriphClockCmd(RCC_APB1Periph_TIM3,ENABLE);
	  RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA,ENABLE);
	
	  GPIO_InitTypeDef GPIO_InitStructure;
	  GPIO_InitStructure.GPIO_Mode=GPIO_Mode_IPU;//如果接在某个引脚的外部模块默认输出高电平，选择上拉输入，默认输入高电平
	  GPIO_InitStructure.GPIO_Pin=GPIO_Pin_6 | GPIO_Pin_7;
	  GPIO_InitStructure.GPIO_Speed=GPIO_Speed_50MHz;
	  GPIO_Init(GPIOA,&GPIO_InitStructure);
	
	  TIM_TimeBaseInitTypeDef TIM_TimeBaseInitStructure;
	  TIM_TimeBaseInitStructure.TIM_ClockDivision=TIM_CKD_DIV1;
	  TIM_TimeBaseInitStructure.TIM_CounterMode=TIM_CounterMode_Up;
	  TIM_TimeBaseInitStructure.TIM_Period=65536-1;//编码器模式只需要CNT计数，故ARR值给最大，同时方便换算为负数
	  TIM_TimeBaseInitStructure.TIM_Prescaler=1-1;//不分频
	  TIM_TimeBaseInitStructure.TIM_RepetitionCounter=0;
	  TIM_TimeBaseInit(TIM3,&TIM_TimeBaseInitStructure);
	
	  //编码器模式下只需要配置IC通道的滤波器和极性选择，又由于TIM_EncoderInterfaceConfig函数也会配置通道极性，故此处不配置
	  //配置通道1
	  TIM_ICInitTypeDef TIM_ICInitStructure;
	  TIM_ICStructInit(&TIM_ICInitStructure);//结构体配置不完整，先赋初始值
	  TIM_ICInitStructure.TIM_Channel=TIM_Channel_1;
	  TIM_ICInitStructure.TIM_ICFilter=0xF;
	  TIM_ICInit(TIM3,&TIM_ICInitStructure);
	  //配置通道2
	  TIM_ICInitStructure.TIM_Channel=TIM_Channel_2;
	  TIM_ICInitStructure.TIM_ICFilter=0xF;
	  TIM_ICInit(TIM3,&TIM_ICInitStructure);
	
	  TIM_EncoderInterfaceConfig(TIM3,TIM_EncoderMode_TI12,TIM_ICPolarity_Rising,TIM_ICPolarity_Rising);
	
	  TIM_Cmd(TIM3,ENABLE);
   }
   ```
2. 如何更改正反转方向？
   - 硬件层面：AB引脚互换
   - 软件层面：在编码器接口初始化时，选择TI1或TI2的极性翻转
     ```c
     TIM_EncoderInterfaceConfig(TIM3,TIM_EncoderMode_TI12,TIM_ICPolarity_Falling,TIM_ICPolarity_Rising);
     ```
3. 编码器测速
   读取CNT的值，使用TIM2的定时中断（1s）,每次中断读取CNT的值并清零，可得转速=CNT/1s
   ```c
   // Encoder.c
   int16_t Encoder_Get(void){
	 int16_t Temp;
	 Temp=TIM_GetCounter(TIM3);
	 TIM_SetCounter(TIM3,0);
   return Temp;
   }
   ```
  
   ```c
   // main.c
   int16_t Speed;
   int main(void){
	 OLED_Init();
	 Timer_Init();
	 Encoder_Init();
	 OLED_ShowString(1,1,"Speed:");
   while(1){
		OLED_ShowSignedNum(1,7,Encoder_Get(),5);
	 }
   }

   void TIM2_IRQHandler(void){
    if(TIM_GetITStatus(TIM2,TIM_IT_Update)==SET){
		  Speed=Encoder_Get();
	    TIM_ClearITPendingBit(TIM2,TIM_IT_Update);
  	}  
   }
   ```