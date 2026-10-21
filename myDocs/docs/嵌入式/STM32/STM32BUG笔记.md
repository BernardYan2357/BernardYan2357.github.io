# STM32bug笔记

## 解决方案

- [修改Keil工程名称](https://www.cnblogs.com/Gustavo-G/p/13516205.html)

## 程序

### 变量一定要初始化

编写串口发送字符串函数时，发现以下写法会导致程序卡死在循环里

```c
void Serial_SendString(char* String){
	uint8_t i;
	while(String[i]!='\0'){
        Serial_SendByte(String[i]);
        i++;
    }
}
```

- 如果将i初始化为0，问题消失
- 尝试使用`debug`模式查看变量i的值，结果由于i是局部变量存储在堆栈中无法访问：`<not in scope>`
- 故尝试将i移至全局变量，`uint8_t i;`，问题亦消失

这样看来，全局变量若未初始化，默认值为0（这一点存疑，最好手动初始化为0），但局部变量若未初始化，为垃圾值，可能导致 BUG

如果使用for循环，在不经意间就已经将i初始化了（for循环优越性这一块）

```c
void Serial_SendString(char *String)
{
	uint8_t i;
	for (i = 0; String[i] != '\0'; i ++){
		Serial_SendByte(String[i]);
	}
}
```

## 烧录

### ST-LINK 下载程序报错的解决办法

关注输出的`Error: Flash Download failed  -  Target DLL has been cancelled`之前的错误提示：
- `No J-Link found`：如果你用的是 `ST-LINK`，说明需要更改 Keil5 的`options for target`中的 Debug 选项，选择使用 `ST-LINK Debugger`
- `Internal Command Error`：表示调试器与芯片间的 SWD 通信链路出现了故障
  - 检查核心板上的 PWR(power) 指示灯是否亮起，如果不亮说明供电存在问题，检查接线，如果使用过长线缆也会导致供电出问题，建议只用一节杜邦线连接核心板和 ST-LINK
  - 如果使用的是非原装 STM32 芯片
- `Could not load file 'WHEELTEC_PS2Demo\WHEELTEC_PS2Demo.axf'`：说明编译生成的 axf 文件不存在，可能是编译失败了，检查编译输出日志，解决编译错误后再次尝试烧录程序

通用排查办法：
- 检查 ST-LINK 接线是否正确
- 按一下核心板上的复位键，再次下载程序
- 重新插拔 ST-LINK
- 打开 STM32CubeIDE，在烧录时会检查 ST-LINK 的版本，如果版本过旧会提示更新，按照提示更新后再次尝试下载程序

### “程序文件不是0x8000000和0x20000000区域的”

使用FlyMcu串口烧录程序报错：“程序文件不是0x8000000和0x20000000区域的”

搜索到的解决方案是查看`options for target`->`Target`中`Read/Only Memory Areas`里面的 IROM1 的 Start 地址是否为 0x8000000，然而，查看后发现 IROM1 的 Start 地址的确为 0x08000000，烧录依然报错。此外，在写入程序前已经进行过Flash擦除，排除是残留程序导致的问题（未解决）