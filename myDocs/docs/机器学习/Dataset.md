# Dataset

## 数据集格式

### 数据集格式种类

- yolo：每张图片对应一个 .txt 标签文件，内容为类别编号和归一化的边界框坐标。
- voc：每张图片对应一个 .xml 标签文件，内容为类别和边界框坐标。
- coco：每张图片对应一个 .json 文件，内容为类别和边界框坐标。

### voc 格式

### coco 格式

### yolo 格式

```bash
dataset/
├── images/
│   ├── train/
│   └── val/
├── labels/
│   ├── train/
│   └── val/
└── data.yaml
```

- `images/train/` 和 `images/val/` 目录下存放训练和验证图像；
- `labels/train/` 和 `labels/val/` 目录下存放对应的标签文件，标签文件格式为 YOLO 格式（每行一个对象，格式为 `class_id center_x center_y width height`，所有值都是相对于图像宽高的比例）；
  例如：

  ```bash
    0 0.5 0.5 0.1 0.1 
    # 0是类别ID，0.5是中心点x坐标，0.5是中心点y坐标，0.1是宽度，0.1是高度
  ```

- `data.yaml` 文件包含数据集的配置信息，如类别名称和图像路径。
  
  ```yaml
  train: dataset/images/train # 训练集图像路径
  val: dataset/images/val # 验证集图像路径
  nc: 3                        # 类别数量
  names: ['cat', 'dog', 'person']  # 类别名称列表
  ```

## 数据集制作

### 数据采集

可以使用手机、相机等设备拍摄图片

图片尺寸的要求：
- 图片尺寸建议为32的倍数（如320、352、384、416、448、480、512、544、576、608、640等），因为YOLO网络结构中有多次下采样操作，使用32的倍数可以避免尺寸不匹配的问题
- YOLO训练时会自动将图片resize到imgsz参数指定的尺寸（如640×640），不需要手动统一图片大小。如果图片为1920x1080，会等比缩放为640x360，再填充成640x640，但是这样分辨率会降低，细节损失较多
- 训练和推理时的图片尺寸最好一致

### 数据集划分

一般将数据集划分为训练集、验证集，常见的比例为：训练集占80%，验证集占20%。数据集较小时，可以适当提高验证集比例，如70%训练集，30%验证集

### 数据标注

使用`LabelImg`工具制作`voc/yolo`格式数据集：

1. 下载：[LaabelImg](https://github.com/HumanSignal/labelImg/releases/tag/v1.8.1)
2. 在data目录的`predefined_classes.txt`中添加类别名称
3. 运行`LabelImg`
4. 在上方菜单栏选择`view`
   - `Auto Save mode` 当你切换到下一张图片时，就会自动把上一张标注的图片标签自动保存下来，这样就不用每标注一样图片都按`Ctrl+S`保存一下了
   - `Single Class Mode` 单一类别模式
   - `Display Labels` 标注好图片之后，会把框和标签都显示出来
   - `Show/Hide Label Panel` 显示/隐藏标签面板
   - `Advanced Mode` 专家模式：这样标注的十字架就会一直悬浮在窗口，不用每次标完一个目标，再按一次W快捷键，调出标注的十字架
5. 在右侧菜单栏选择图像路径与标签保存路径
6. 选择标注格式：`PascalVOC`或`YOLO`
7. 开始标注

| 快捷键       | 功能                | 快捷键           | 功能                        |
|--------------|---------------------|------------------|---------------------------|
| ctrl + q     | 退出软件            | ctrl + -         | 缩小                       |
| ctrl + o     | openfile            | ctrl + =         | 原始大小                   |
| ctrl + u     | openDir             | ctrl + F         | fitwindow                 |
| ctrl + r     | ChangeSaveDir       | d                | nextImg                   |
| ctrl + s     | 保存                | a                | preImg                    |
| ctrl + L     | boxlineColor        | space            | 标记当前图片已标记          |
| ctrl + J     | move and edit Boxes | w                | 画框                       |
| ctrl + D     | 复制框              | Delete           | 删除框                    |
| ctrl + H     | 隐藏所有的框        |
| ctrl + A     | 显示所有的框        |
| ctrl + +     | 放大                |

#### 数据标注自动化

使用SAM模型分割实现数据标注自动化

[SAM模型简介与下载](https://docs.ultralytics.com/zh/models/sam/#sam-comparison-vs-yolo)

SAM(Segment Anything Model), 是一种先进的图像分割模型,具有零样本迁移特性，通过给定提示词从而生成有效的分割掩码，将该模型应用于数据标注，可以实现自动画框，大大提高标注效率

使用SAM的分割功能：

分割一切（不提供提示词）：

```python
from ultralytics import SAM
# Load a model
model = SAM("sam_b.pt")
# Display model information (optional)
model.info()
# Run inference
model("path/to/image.jpg")
```

提供提示词：

```python
# 1. 使用 bbox（框）作为提示进行分割
results = model("ultralytics/assets/zidane.jpg", bboxes=[439, 437, 524, 709])
# 作用：对图片中指定的矩形区域（左上角x=439, y=437，右下角x=524, y=709）进行分割。
# 2. 使用单个点作为提示进行分割
results = model(points=[900, 370], labels=[1])
# 作用：以(900, 370)这个点为正样本（labels=1），分割包含该点的目标。
# 3. 使用多个点作为提示进行分割
results = model(points=[[400, 370], [900, 370]], labels=[1, 1])
# 作用：以两个点(400, 370)和(900, 370)为正样本，分割包含这些点的目标。
# 4. 对每个目标分别用多个点作为提示
results = model(points=[[[400, 370], [900, 370]]], labels=[[1, 1]])
# 作用：对一个目标，使用两个正样本点进行分割。
# 5. 使用正负点混合提示
results = model(points=[[[400, 370], [900, 370]]], labels=[[1, 0]])
# 作用：对一个目标，(400, 370)为正样本点，(900, 370)为负样本点，分割时会排除负样本点所在的区域。
```

### 数据增强

[YOLO数据增强参考](https://docs.ultralytics.com/zh/guides/yolo-data-augmentation/)

数据增强是通过对训练数据进行一系列变换来增加数据的多样性，从而提升模型的泛化能力

YOLO 已经内置了多种数据增强方法，在`train()`函数中指定参数即可

### 思考

- 在训练集中，单一类别数据连续时需要在训练前将训练集打乱吗？
  - 需要，因为单一类别数据连续不满足mini-batch梯度下降所依赖的“独立同分布”的基本假设，使得模型的梯度变化剧烈，难以收敛
  - 但是如果使用 yolo 的`train()`函数且不指定`shuffle=False`，则程序会自动打乱数据集