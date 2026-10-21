# STM32概览

## 命名规则

![命名规则](命名规则.jpg)

## 系统结构

![系统结构](系统结构.jpg)

## STM32的组成

### STM32的时钟系统

#### 时钟与时钟系统

时钟是单片机运行的基础，时钟信号推动单片机内各个部分执行相应的指令。

时钟系统就是CPU的脉搏，决定cpu速率，

STM32为了低功耗，他将所有的外设时钟都设置为disable(不使能)，用到什么外设，只要打开对应外设的时钟就可以
其他的没用到的可以还是disable(不使能)，这样耗能就会减少
这就是不管你配置什么功能都需要先打开对应的时钟的原因

STM32时钟系统主要的目的就是给相对独立的外设模块提供时钟，也是为了降低整个芯片的耗能。

#### RCC

stm32的RCC是reset and clock control（复位和时钟控制）模块的缩写。RCC模块是STM32微控制器中的一个重要模块，用于管理复位和时钟信号。RCC模块包括多个寄存器，用于配置系统时钟、外设时钟和时钟源等参数。

常用函数有：

```c
void RCC_AHBPeriphClockCmd(uint32_t RCC_AHBPeriph, FunctionalState NewState);
void RCC_APB2PeriphClockCmd(uint32_t RCC_APB2Periph, FunctionalState NewState);
void RCC_APB1PeriphClockCmd(uint32_t RCC_APB1Periph, FunctionalState NewState);
```

##### RCC时钟树

RCC时钟树描述了STM32微控制器中各种时钟源和它们之间的关系。


![RCC时钟树](RCC时钟树.jpg)

###### 时钟输入端

在main函数执行之前，会先执行SystemInit()函数，配置系统时钟为HSI（8MHz），并开启FLASH预取功能。

- SystemInit()函数首先启动内部时钟HSI，选择HSI作为系统时钟源，
- 然后再启动HSE（4~16MHz，一般为8MHz），HSE信号经由PLL锁相环进行倍频（倍频系数为9），时钟频率达到72MHz，
- 等到PLL锁相环稳定后，切换系统时钟源为PLL输出的72MHz。

此外，当外部时钟源HSE失效时，CSS（Clock Security System）会自动切换回HSI时钟源，确保系统的稳定运行。

###### 时钟输出端

- 输出的72MHz时钟信号首先经过AHB总线分频器（AHB Prescaler），分频系数为1，输出的时钟频率仍为72MHz。
  - APB1总线分频器（APB1 Prescaler）将AHB总线的时钟频率分频为36MHz。
    需注意的是，对于定时器2~7，如果APB1总线分频系数为2，则定时器的时钟频率为APB1总线的时钟频率乘2；如果分频系数为1，则不变。
  - APB2总线分频器（APB2 Prescaler）将AHB总线的时钟频率分频为72MHz。

## 引脚定义

![引脚定义](引脚定义表.jpg)

## 面包板布局

[参考文献](http://www.taichi-maker.com/homepage/reference-index/circuit-reference-index/breadboard/)

![面包板布局](面包板布局.jpg)

然而，需要注意的是，有的面包板电源轨中间断开，如果需要电源的外设接在了没有stm32系统板的一边，就会因无电源而工作异常。解决方法如下图，用跳线将两边电源轨连接起来。

![面包板注意事项](面包板注意事项.jpg)