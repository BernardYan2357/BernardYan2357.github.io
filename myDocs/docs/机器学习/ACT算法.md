# ACT算法

参考：

[Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware](https://arxiv.org/abs/2304.13705)

[【精析】ACT模型 | ALOHA | Action Chunking Transformer](https://www.bilibili.com/video/BV1xGF3eeEjB/?spm_id_from=333.337.search-card.all.click&vd_source=33c42ba9bbe0f4b068a28731fdb9bc58)

[调了3天还抓不准！ACT算法到底哪出了问题？](https://www.bilibili.com/video/BV1xS32zRESp/?spm_id_from=333.337.search-card.all.click&vd_source=33c42ba9bbe0f4b068a28731fdb9bc58)

[VAE变分自编码器原理解析](https://www.bilibili.com/video/BV1op421S7Ep/?vd_source=33c42ba9bbe0f4b068a28731fdb9bc58)


ACT 算法（Action Chunking with Transformers）是斯坦福 ALOHA 团队在 2023 年提出的一种 模仿学习（Imitation Learning）方法，主要用于机器人精细操作任务。它的核心思想是将连续的动作序列分块（chunk）后一次性生成多个动作，并利用 Transformer 进行时序建模，从而提升生成效率与动作一致性

## ALOHA

一个低成本的硬件系统（A Low-cost Open-source Hardware Architecture）

![ALOHA](ALOHA_system.png)

ALOHA系统组成：

- 主动机械臂：由人控制，记录关节信息（action），将信号实时传递至从动臂
- 从动机械臂：末端有七自由度，位置+旋转+夹爪，电机通过pid控制达到信号目标位置，记录从臂关节坐标和相机信息（Observation）
- 两个摄像头：依附于从臂

模型以Observation作为输入，预测主动臂的关节信息Action

## Action Chunking

- single-step policy:
  - 一次预测一个动作
  - $\pi(a_t|s_t)$: 给定当前状态$s_t$，预测当前动作$a_t$
  - 单步策略假设环境具有马尔可夫性（Markovian），即当前状态能够完全概括过去的所有信息，未来的状态的预测只依赖于当前状态，但实际中，很多任务具有时序连续性，单步策略难以捕捉长期依赖关系，导致动作不连贯
- action chunking policy:
  - 一次预测多个动作
  - $\pi(a_{t:t+k}|s_t)$: 给定当前状态$s_t$，预测未来$k$个动作$a_{t:t+k}$
  - 动作分块策略通过一次性生成多个动作，这个动作序列内部具有时序连续性，能够提高动作的连贯性和一致性，同时，相较于history-conditional policy可能会引入“因果混淆”问题（即模型可能会错误地归因于历史中的某些状态），action chunking通过直接从当前状态预测未来动作，减少了对历史状态的依赖，从而降低了因果混淆的风险

## Temporal Ensemble

简单的action chunking会出现这样的问题：模型基于$s_t$预测未来$k$个动作，设$k$步执行完毕后状态为$s_{t+k}$，此时模型再次基于$s_{t+k}$预测未来$k$个动作，这样会导致动作之间缺乏连续性，无法保证动作序列的平滑过渡

为了解决这个问题，ACT引入了Temporal Ensemble（时序集成）机制：

![Temporal Ensemble](Temporal_Ensemble.png)

对于一个时间步的动作，会有过k次预测，使用加权的方式对这k次预测做平均，权重的设计为：$w_i=exp(-m \times i)$，其中$m$是一个超参数，控制权重的衰减速度，$i$表示预测的时间步数。这是一个以i为变量，单调递减的函数，预测发生的越久，其权重越大，m控制融合新信息的速度，m越小，融合的越快

## ACT模型架构

### AE (Autoencoder)

自编码器（Autoencoder，AE）是一种无监督学习模型，它由两个主要部分组成：编码器（Encoder）和解码器（Decoder）。输入数据被编码器转化为一个编码向量，其中编码向量的每个维度表示一些学到的关于数据的特征，每个维度上的取值代表输入数据在该特征上的表现

随后，解码器网络接收编码向量的这些值并尝试重构原始输入

AE的目标是最小化输入数据与重构数据之间的差异，通常使用均方误差（Mean Squared Error，MSE）作为损失函数

### VAE (Variational Autoencoder)

变分自编码器（Variational Autoencoder，VAE）与传统的AE不同，VAE用“取值的概率分布”代替原先的单值来描述输入向量在潜在特征上的表现，将输入数据映射到潜在空间中的一个分布（通常是高斯分布），而不是一个固定的点

当从潜在状态解码时，我们将从每个潜在状态分布中随机采样，生成一个隐变量向量$Z$作为解码器模型的输入，解码器则从这个分布中采样潜在变量，并将其映射回原始数据空间

VAE的训练目标不仅包括重构误差，还包括一个正则化项，通常是Kullback-Leibler（KL）散度，用于衡量潜在分布与预定义先验分布（通常是标准正态分布）之间的差异，通过引入KL散度，引入了噪声，保证了模型的生成能力

### CVAE (Conditional Variational Autoencoder)

条件变分自编码器（Conditional Variational Autoencoder，CVAE）是在VAE的基础上引入条件变量的一种模型。CVAE不仅考虑输入数据本身，还引入了额外的条件信息（如标签或其他相关特征），在采样时，不再是从潜在分布$P(z)$中随机采样，而是从条件分布$P(z|c)$中采样，其中$c$表示条件变量

在解码阶段，解码器接收潜在变量$z$和条件变量$c$，并尝试重构原始输入数据，所以encodeer和decoder都需要输入条件变量

CVAE的训练目标同样包括重构误差和KL散度，但KL散度现在衡量的是潜在分布$P(z|c)$与条件先验分布之间的差异

### ACT中的CVAE应用

人类示教数据常带有很多噪声：人会用不同的轨迹完成同一个任务，也会对精度要求不高的任务，做出随机性很强的行为。对此，作者将action chunking policy设置为一个生成式模型，以CVAE的形式来训练模型，根据输入观测值，生成预测动作

- CVAE Encoder:
  - 引入了 CVAE结构，目的是捕捉人类演示数据中的“风格”或多模态性（例如，同一个抓取动作可以有快有慢，或者从不同角度接近）
  - 输入：
    - 【CLS】: 这是一个特殊的Token，用于聚合整个序列的信息
    - joints: 从臂当前的关节状态（本体感知信息）
    - action sequence + PosEmb: 这里输入的是Ground Truth（真实标签），即人类演示的未来一系列动作序列，加上位置编码（Positional Embeddings）
  - 输出：隐变量$z$的分布参数（均值和方差）
- ACT Policy Stage
  - 这是模型在实际执行任务时（以及训练时的解码部分）的主要架构。它是一个基于 Transformer 的 Encoder-Decoder 结构
  - 输入层 (Detailed Inputs)
    - 模型接收三种主要类型的输入：
    - 视觉输入 (Vision):
      - 来源: 4个视角的相机图像（例如：顶视图、前视图、左手腕相机、右手腕相机）
      - 预处理: 每张图片（尺寸 $480 \times 640 \times 3$）都经过 ResNet 提取特征，并加入位置编码 (PosEmb) 来保留空间信息
      - 结果: 生成视觉特征序列（图中 cam 1 ... cam 4）
    - 本体感知输入 (Proprioception):
      - joints: 机器人当前的物理状态，对于双臂有14个自由度，组成14维特征向量
    - 风格变量 ($Z$):
      - 来源:
        - 训练时: 从 CVAE 编码器的输出分布中采样得到
        - 推理时: 设置为零（均值），或者根据需要采样，以此来获得确定性或多样性的动作
  - Transformer Encoder
    - 功能: 多模态融合
    - 它将（视觉特征, 关节特征, 风格变量 $Z$） 拼接在一起作为输入序列
    - 通过自注意力机制（Self-Attention），模型学习图像特征与关节状态之间的关联（例如：从图像中定位物体，并结合当前手臂位置规划路径）
  - Transformer Decoder
    - 输入: 
      - Position Embeddings (fixed)这是预设的、固定的位置嵌入，充当 Transformer 的 Query。它的长度决定了预测动作序列的长度（Chunk Size，例如 $k$ 步）
    - 交叉注意力 (Cross-Attention): 
      - Decoder 使用这些固定的 Query 去“查询” Encoder 输出的丰富特征（Key/Value）。意思就是：“为了预测第 $t+1$ 步的动作，我需要关注图像的哪里和关节的哪个状态？”
    - 输出: 
      - Action Sequence
      - 这是一个维度为 $k \times d$ 的张量，代表未来 $k$ 个时间步的动作（$k$ 是块的大小，$d$ 是动作维度，如关节目标位置）

在训练时，通过模型预测的动作序列与演示动作序列计算重构损失（Reconstruction Loss），同时将隐变量$Z$分布与先验分布的KL散度纳入损失函数，进行反向传播