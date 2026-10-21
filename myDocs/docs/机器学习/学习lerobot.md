# 学习lerobot

当前笔记对应lerobot版本: v0.4.2

## Windows配置环境

注意非必要不要混用pip和conda安装包

```bash
conda create -y -n lerobot_env python=3.10
conda activate lerobot_env
conda install ffmpeg -c conda-forge -y
git clone https://github.com/huggingface/lerobot.git
cd lerobot
pip install 'lerobot[aloha,pusht]'
```

如果手动选择pytorch版本，需要注意：

- torch >=2.2.1, <2.8.0
- torchvision >=0.21.0, <0.23.0
- Torchaudio 必须和 PyTorch 版本严格匹配
- cuda12.1 最高只提供到 torchvision 0.20.1+cu121，所以在这个 CUDA 版本下确实没有满足 lerobot 要求的 GPU 版 torchvision，因此最好选择cuda11.8

综上所述，推荐安装命令为

```bash
pip install torch==2.7.0+cu118 torchvision==0.22.0+cu118 torchaudio==2.7.0+cu118 --index-url https://download.pytorch.org/whl/cu118
```

登录huggingface

```powershell
hf auth login --token ${HUGGINGFACE_TOKEN} --add-to-git-credential
```

登录wandb

```powershell
wandb login
```

## WSL2配置环境

**失败**

当前 WSLg 图形驱动（Mesa/D3D12 转换层）缺少 rerun 需要的 GPU 特性。即使切换到 NVIDIA GPU 或强制软件渲染，WSLg 的 OpenGL/Vulkan 层仍然不支持 R32Float 纹理格式，所以 rerun 无法创建渲染上下文

## Ubuntu配置环境

在远程服务器配置环境，使用ubuntu22.04/CUDA 11.8 Miniconda3_3.10镜像，训练用

```bash
sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install -y build-essential ffmpeg
conda create -y -n lerobot_env python=3.10
conda activate lerobot_env
conda install ffmpeg -c conda-forge -y
pip install torch==2.7.0+cu118 torchvision==0.22.0+cu118 torchaudio==2.7.0+cu118 --index-url https://download.pytorch.org/whl/cu118
git clone https://github.com//huggingface/lerobot.git
cd lerobot
pip install 'lerobot[aloha,pusht]'
hf auth login --token huggingface ${access_token} --add-to-git-credential
wandb login
lerobot-train --help # 测试lerobot命令行工具是否可用
```

下载tmux，确保在SSH连接断开后，训练进程不被Kill

```bash
sudo apt-get install tmux -y
tmux new -s lerobot_train # -s指定会话名称
# ctrl+b 是一个前缀键，后续按下d键即可退出会话但保持后台运行
ctrl+b d # 退出tmux会话，保持后台运行
tmux ls # 查看当前所有会话
tmux attach -t lerobot_train # 重新连接到指定会话
```

```bash
lerobot-train --steps 50000 \
--batch_size 128 \
--dataset.repo_id lerobot/aloha_sim_transfer_cube_human \
--policy.type act \
--policy.device cuda \
--policy.push_to_hub true \
--policy.repo_id Bernard2357/lerobot-aloha-act-model2 \
--output_dir outputs/train/aloha_cube2 \
--wandb.enable true \
--save_checkpoint true \
--save_freq 5000 \
--eval_freq 5000
# 训练至200epochs即可
```

训练完成后，使用scp命令将训练结果下载到本地

```powershell
scp -P 45989 -r root@wejpnjdgg9de6be7.ssh.x-gpu.com:~/lerobot/outputs/train/aloha_cube C:\Users\ASUS\Downloads
```

## lerobot dataset

`LeRobotDataset v3.0`的核心原则是将存储与 API 分离：数据高效存储（大文件很少），而公共 API 则提供直观的 episode-level 访问

lerobot数据集包含以下组件：

- 表格数据：存储在Apache Parquet中的低维高频信号（状态、动作、时间戳）。访问通过内存映射或通过堆栈流传输
- 视觉数据：将摄像机帧串接并编码成MP4。同一集的帧被分组;视频会根据实际尺寸分片
- 元数据：描述模式（特征名称、dtype、形状）、帧率、归一化统计和剧集分割（开始/结束偏移到共享Parquet/MP4文件）的JSON/Parquet记录

目录结构：

```
lerobot-dataset/
├── meta/
│   ├── info.json # 数据集元信息（特征、形状、FPS 等）
│   ├── episodes.jsonl # 每个episode的元数据（开始/结束偏移等）
│   ├── stats.json # 归一化统计信息（整个数据集的均值、标准差等）
│   └── episodes_stats.jsonl # Per-episode统计信息
│
├── data/
│   ├── chunk-000/
│   │   ├── episode_000000.parquet
│   │   ├── episode_000001.parquet
│   │   └── ...
│   ├── chunk-001/
│   │   ├── episode_001000.parquet
│   │   ├── episode_001001.parquet
│   │   └── ...
│   └── ...
│
├── videos/
│   ├── chunk-000/
│   │   ├── observation_images.cam1/
│   │   │   ├── episode_000000.mp4
│   │   │   ├── episode_000001.mp4
│   │   │   └── ...
│   │   ├── observation_images.cam2/
│   │   │   ├── episode_000000.mp4
│   │   │   ├── episode_000001.mp4
│   │   │   └── ...
│   │   └── ...
│   ├── chunk-001/
│   │   ├── observation_images.cam1/
│   │   └── observation_images.cam2/
│   └── ...
│
└── images/
```

lerobot数据集强制使用hugging face进行存储和分发，数据集仓库地址：https://huggingface.co/datasets/lerobot

一些常用数据集：

- `lerobot/pusht`：单臂推物体，简单，适用于环境配置测试
- `lerobot/aloha_sim_transfer_cube_human`：双臂搬运立方体，中等难度，适合练习ACT协调能力
- `lerobot/aloha_sim_insertion_human`：双臂插入方块，高难度，适合进阶练习

## dataset visualize

lerobot中，数据集的可视化依赖于`lerobot-dataset-viz`命令行工具。该工具使用`rerun`进行3D可视化展示，[rerun是一个开源的实时3D可视化工具](https://www.rerun.io/)

简单示例：

```bash
lerobot-dataset-viz --help
lerobot-dataset-viz --repo-id lerobot/pusht --episode-index 0
```

- `--repo-id`：指定数据集的仓库ID
- `--episode-index`：指定要可视化的episode索引，也可以使用`--all-episodes`参数可视化所有episode
- `--root`: 指定数据集的本地存储路径
  - 数据默认存放在`~/.cache/huggingface/hub/`，在这个目录下，会按照 repo_id（比如 lerobot/pusht）建立子目录，存放下载的文件

## train a policy

使用`lerobot-train`命令行工具进行训练

简单示例：

```bash
lerobot-train --help
lerobot-train --steps 20000 --dataset.repo_id lerobot/pusht --policy.type act --policy.device cuda --policy.push_to_hub true --policy.repo_id ${HF name}/lerobot-pusht-act-model --output_dir outputs/train/pusht --wandb.enable true --save_checkpoint true --save_freq 10000
```

- dataset.repo_id：指定训练使用的数据集仓库ID
- policy.type：指定训练的策略类型（如act、bc等）
- policy.device：指定训练使用的设备（如cuda或cpu）
- policy.push_to_hub：是否将训练好的模型推送到hugging face hub
- policy.repo_id：指定推送到hugging face hub的模型ID
- policy.use_amp：是否启用自动混合精度训练，混合精度训练可以加速训练过程并减少显存占用
- batch_size：训练批次大小
- steps：最大训练步数
- 
- output_dir：指定训练输出目录
- save_freq：模型保存频率（每隔多少步保存一次模型）
- eval_freq：评估频率（每隔多少步进行一次评估）
- save_checkpoint：是否保存训练检查点
- wandb.enable：是否启用wandb进行训练日志记录，可以在wandb官网查看训练过程和结果
- 其他参数可以通过`--help`查看详细说明和配置选项

> 一些误区：
>
> 在输入--policy.max_steps时报错：PreTrainedConfig: The fields `max_steps` are not valid for ACTConfig
> 
> 在输入--max_steps时报错：lerobot-train: error: unrecognized arguments: --max_steps 20000
>
> 依照--help说明，max_steps应该是policy下的参数，但是这样写还是报错，正确的写法是`--steps 20000`，需要对照源码查看具体参数名称

此外，lerobot支持恢复训练功能，前提是打开了`save_checkpoint`并指定`save_freq`。在某次训练中断后，可以通过开启`--resume`参数，传入`train_config.json`路径，继续从上次中断的地方进行训练。例如：

```bash
lerobot-train --config_path outputs/train/pusht/train_config.json --resume true --output_dir outputs/train/pusht --steps 40000 --wandb.enable true
```

- `--output_dir` 必须与之前的路径保持一致

训练结果分析：

- checkpoint目录下保存了训练过程中的模型权重文件，可以用于后续的模型评估或推理
  - 000XX目录下保存了每次保存的模型权重文件
    - pretrained_model目录下保存了模型的权重文件，可以直接用于推理
      - model.safetensors：**模型权重文件**
      - config.json：模型结构和参数配置文件
      - policy_postprocessor.json：策略后处理器配置
      - policy_preprocessor.json：策略预处理器配置
      - train_config.json：完整训练配置
    - training_state目录下保存了训练状态文件，可以用于恢复训练
      - optimizers.param_groups.json：优化器参数组文件
      - optimizers_state.safetensors：优化器状态文件
      - rng_state.safetensors：随机数生成器状态文件
      - training_step.json：训练步数文件
- wandb目录下保存了训练日志文件，可以在wandb官网查看训练过程和结果

如果在训练后想推送模型到hugging face该怎么办？

示例：

```python
from huggingface_hub import HfApi

api = HfApi()
api.create_repo(repo_id="Bernard2357/lerobot-pusht-act-model", exist_ok=True)
api.upload_folder(
    repo_id="Bernard2357/lerobot-pusht-act-model",
    folder_path="outputs/train/pusht/checkpoints/020000/pretrained_model",
    path_in_repo="",  # 上传整个文件夹内容到根目录
)
```

## evaluate model

使用`lerobot-eval`命令行工具进行模型评估

简单示例：

```bash
lerobot-eval --help
lerobot-eval `
  --env.type aloha `
  --env.task AlohaTransferCube-v0 `
  --policy.type act `
  --policy.pretrained_path 025000/pretrained_model `
  --policy.device cuda `
  --eval.n_episodes 50 `
  --output_dir outputs/eval/aloha_cube2/025000
```

- `env.type`：指定评估使用的环境类型
- `env.task`：指定评估使用的具体任务
  - 在Aloha环境中，可以指定不同的任务，下面是常用的两个：
    - gym_aloha/AlohaInsertion-v0
    - gym_aloha/AlohaTransferCube-v0
- `policy.type`：指定评估使用的策略类型
- `policy.pretrained_path`：指定预训练模型的路径
- `policy.device`：指定评估使用的设备（如cuda或cpu）
- `eval.n_episodes`：指定评估的episode数量
- `output_dir`：指定评估输出目录

注意：

- 如果要评估线上模型，可以将`--policy.pretrained_path`替换为`--policy.repo_id MODEL_REPO_ID`
- `policy.pretrained_path` 必须指向包含 `model.safetensors` 和 `config.json` 的目录
- 不存在`--wandb.enable`参数

评估完成后，结果会保存在`--output_dir`指定的目录下，包括评估日志和视频等文件