**LoRA（Low-Rank Adaptation）** 是一种高效的大模型微调技术，常用于大型语言模型（LLM）和扩散模型（[[机器学习词典#Diffusion Model]]）的领域适配或风格定制

### 核心思想

- 不改变预训练模型的原始权重，而是在模型层中插入可训练的低秩矩阵（通常秩 $r$ 很小，如 4、8、16）
- 推理时，将低秩矩阵与原始权重合并，因此几乎不增加额外推理延迟

### 数学表示

对于一个权重矩阵 $W \in \mathbb{R}^{d \times k}$，LoRA 的更新形式为：

$$W' = W + BA$$

其中 $B \in \mathbb{R}^{d \times r}$，$A \in \mathbb{R}^{r \times k}$，$r \ll \min(d, k)$。训练时只更新 $A$ 和 $B$，$W$ 冻结

### 优势

| 特性 | 说明 |
|------|------|
| **高效** | 参数量减少 10,000 倍以上（例如 7B 模型微调仅需几百 MB 显存） |
| **快速切换** | LoRA 权重文件通常只有几 MB ~ 几十 MB，不同任务可加载不同 LoRA 模块 |
| **避免灾难性遗忘** | 预训练知识被保留，原始权重不变 |

### 相关资源

- 原论文：[LoRA: Low-Rank Adaptation of Large Language Models](https://arxiv.org/abs/2106.09685)
- Hugging Face 的 [PEFT](https://huggingface.co/docs/peft) 库提供了 LoRA 的便捷实现
