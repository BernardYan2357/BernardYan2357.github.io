# YOLO模型训练

## 使用CLI训练模型

```bash
yolo task=detect mode=train model='D:\code_file\YOLO_Project\Project_1\models\detect\yolo11s.pt' data='D:\code_file\YOLO_Project\Project_1\VehiclesDetectionDataset\dataset.yaml' epochs=150 imgsz=416 workers=8 batch=16
```

详细参数说明：
- `task=detect`：任务类型为目标检测；
- `mode=train`：训练模式；
- `model=yolo11n.pt`：使用的预训练模型路径，最好为绝对路径；
- `data=data.yaml`：数据集配置文件路径，最好为绝对路径；
- `epochs=100`：训练轮数；
- `imgsz=416`：输入图像大小；
- `workers=8`：数据加载的工作线程数，通常设置为 CPU 核心数；
- `batch=16`：批次大小。批次大小指的是每次训练中使用的图像数量，通常取决于显存大小。

训练过程中可能会下载‘yolo11n.pt’预训练模型（即便你并没有使用该模型训练），这是AMP（自动混合精度）检查时自动下载的官方轻量模型，仅用于AMP环境的兼容性测试。

训练完成后，最后与最佳模型权重会保存在`runs/train/exp/weights/best.pt`。

##### 使用Python脚本训练模型

```python
from ultralytics import YOLO
model = YOLO("D:/code_file/YOLO_Project/competition_project/model/basic.pt")
model.train(
    data="D:/code_file/YOLO_Project/competition_project/dataset/dataset.yaml", # 数据集配置文件路径
    epochs=150,        # 训练轮数
    batch=16,          # 批次大小
    imgsz=640,         # 输入图片尺寸
    device=0           # 指定GPU
)
```

train()函数的参数与CLI命令行参数类似，更多参数可以参考[官方文档](https://docs.ultralytics.com/zh/usage/cfg/#train-settings)

#### 模型评估图表解读

模型训练完成后，`\runs\detect\train`目录下会生成一些评估图表和日志文件。
>精确率（Precision）是指模型预测为正类的样本中，实际为正类的比例。
>召回率（Recall）是指实际为正类的样本中，模型预测为正类的比例。
>F1分数（F1-score）是**精确率（Precision）和召回率（Recall）**的调和平均值，是衡量模型分类或检测性能的一个综合指标。
>F1分数越高，说明模型的精确率和召回率都较高，整体检测效果越好。

- `F1-Confidence Curve`：F1分数与置信度的关系图，显示不同置信度阈值下模型对各类别以及平均的F1分数曲线。F1分数越高，说明模型在该阈值下的检测效果越好。
  重点关注`all class at 0.25`，表示在置信度阈值为0.25时，有最高平均F1分数。
- `Precision-Confidence Curve`：精确率与置信度的关系图，显示不同置信度阈值下模型对各类别以及平均的精确率曲线。置信度越高，精确率通常越高，但召回率会下降。用于选择合适的置信度阈值。
- `Recall-Confidence Curve`：召回率与置信度的关系图，显示不同置信度阈值下模型对各类别以及平均的召回率曲线。置信度越低，召回率越高，但精确率会下降。用于分析模型漏检情况。
- `Precision-Recall Curve`：精确率与召回率的关系图，显示不同置信度阈值下模型对各类别以及平均的精确率和召回率曲线。曲线下的面积就是AP（平均精度），AP越大模型越好。
- `Confusion Matrix`：混淆矩阵，显示模型在各类别上的预测情况。对角线上的值表示正确预测的样本数，其他位置表示误分类的样本数。可以帮助分析模型在哪些类别上表现较差。
- `confusion Matrix Normalized`：归一化的混淆矩阵，和上面类似，但每一行（或每一列）做了归一化，数值变成了百分比（0~1）。
- `labels.jpg`：标签分布图，显示每个类别的样本数量。可以帮助分析数据集是否平衡。
- `results.png`：训练结果的统计图表，显示训练过程中的损失函数变化、精确率、召回率等指标随时间的变化情况。用于观察模型训练是否收敛、是否过拟合，以及最终检测效果。
