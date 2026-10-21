# PID

references：
- [通俗易懂的 PID 控制算法讲解](https://www.bilibili.com/video/BV1et4y1i7Gm/)
- [PID控制原理与增量式PID算法 · 给新手的两轮自平衡小车开发实战指南](https://c.miaowlabs.com/E08.html)

## PID 概念

PID算法是一种常用的自动控制方法，可以让系统输出快速、平稳地接近目标值

PID 含义：
- P(proportional)：比例
- I(integral)：积分
- D(derivative)：微分

PID 传递函数：

$$ G(s) = K_p + \frac{K_i}{S} + K_d \cdot S$$

PID 时域表达式：

$$ u(t) = K_p \cdot e(t) + K_i \cdot \int e(t) dt + K_d \cdot \frac{d e(t)}{dt} $$

## 数字 PID 控制

### 位置式 PID 算法

由于计算机控制是一种采样控制，它只能根据采样时刻的偏差计算控制量，因此需要对 PID 公式进行离散化处理：



### 增量式 PID 算法

增量式 PID 是指数字控制器的输出只是控制量的增量



### 调参

kp 决定系统的响应速度，ki 决定系统的稳态误差，kd 决定系统的稳定性

调参步骤：

- 将 kd, ki 设置为0
- 逐渐增加 kp 直到系统开始轻微振荡
- 然后增加 kd 来抑制振荡，最后增加 ki 来消除稳态误差

