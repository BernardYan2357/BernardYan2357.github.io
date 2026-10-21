# REF

- [C语言实现控制算法](https://space.bilibili.com/10758282/lists?sid=6997272&spm_id_from=333.788.0.0)

使用 Matlab Simulink 进行仿真，使用 C 语言进行实现，并将结果与 Simulink 仿真结果进行对比

## 理论知识

### 动态系统

动态系统的状态值随时间变化
> 状态：描述系统当前状态的变量，取决于之前的状态与系统的其他属性(物理属性、外部输入等)，也决定了系统的输出

动态系统分为连续系统和离散系统
- 连续系统(continuous)：状态值随时间连续变化，使用微分方程描述
  - 用x(t)表示连续时间t的状态值，u(t)表示输入，y(t)表示输出
  - 连续系统的状态方程：dx/dt = f(x, u)，输出方程：y = g(x, u)
- 离散系统(discrete)：状态值在离散时间点变化，使用差分方程描述
  - 用x[n]表示离散时间点n的状态值，u[n]表示输入，y[n]表示输出
  - 离散系统的状态方程：x[n+1] = f(x[n], u[n])，输出方程：y[n] = g(x[n], u[n])

## Simulink

离散方程建模
- 排列方程，使最新的状态位于方程的左侧，其余的项位于右侧
- 确定所需的 Unit Delay 模块的数量，看有几个状态变量
  - 例如：$x[n] = x[n-1] + x[n-2]$，需要两个 Unit Delay 模块
- 添加 Unit Delay 模块并对其信号加标签
- 构造方程的右侧
- 连接方程的右侧到 Unit Delay 模块的输入，构造相等性
- 设置初始条件

连续方程建模
- 排列方程，使最高阶导数单独放在方程的左侧，其余项在右侧
- 确定所需的 Integrator 模块的数量，看有几次积分
  - 例如：$\frac{d^2y}{dt^2} + 3\frac{dy}{dt} + 2y = 0$，需要两个 Integrator 模块
- 添加 Integrator 模块并对其信号加标签
- 构造方程的右侧
- 连接方程的右侧到 Integrator 模块的输入，构造相等性
- 设置初始条件

## C语言实现控制算法

### 入门

**配置 Matlab 使用 MinGW 编译器**

- [MinGW-w64的下载与安装](https://zhuanlan.zhihu.com/p/26143367916)
- [I already have MinGW on my computer. How do I configure it to work with MATLAB?](https://www.mathworks.com/matlabcentral/answers/313298-i-already-have-mingw-on-my-computer-how-do-i-configure-it-to-work-with-matlab)

由于之前下载过 MSYS2，所以已经安装了 MinGW 编译器

添加系统变量，变量名：`MW_MINGW64_LOC`，变量值：`C:\msys64\mingw64`

重启 Matlab，输入 `mex -setup`，此时可以选择 MinGW 编译器来编译 C 语言代码了