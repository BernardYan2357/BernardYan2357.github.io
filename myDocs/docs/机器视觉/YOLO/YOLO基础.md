# yolo基础

## yolo安装

安装`anaconda`，然后创建一个新的环境`yolov11_env`,python版本选择`3.10`

```bash
conda create -n yolov11_env python=3.10
conda activate yolov11_env # 激活环境
conda install -c pytorch -c nvidia -c conda-forge pytorch torchvision pytorch-cuda=11.8 ultralytics
```

在同一命令中安装`ultralytics`,`pytorch`和`pytorch-cuda`。这样可以通过`conda`软件包管理器自动解析和处理它们之间可能存在的版本冲突或依赖关系不兼容问题。

打开命令行输入`yolo version`，如果显示版本号，则安装成功。

## yolo设置

通过CLI检查设置：`yolo settings`

详细信息可以通过[官方文档](https://docs.ultralytics.com/zh/quickstart/#use-ultralytics-with-python)查看。

## YOLO模型的任务与模式

从`runs`目录结构可以看出：

```bash
runs/
├── detect/              # 目标检测任务
│   ├── train/           # 训练结果
│   └── predict/         # 预测结果
```

模式从属于任务，单个模型只能执行一种任务，却有多种模式。

## 任务(task)

YOLOv11支持以下任务：

- `detect`：目标检测任务
  识别图像或视频帧中的物体，并用边界框框出。
- `segment`：图像分割任务
  将图像按照物体区域进行像素级切分，每个区域带有标签。
- `classify`：图像分类任务
  对整张图像进行类别判断，例如识别产品种类或动植物类型。
- `pose`：姿态估计任务
  检测图像或视频中的关键点，如人体关节、面部特征等。
- `OBB`：方向边界框任务（Oriented Bounding Box）
  检测旋转物体，通过增加方向角，更准确地定位不规则物体。

## 模式(mode)

YOLOv11支持以下模式：

- `train`：训练模式
  训练模型，调整参数。
- `val`：验证模式
  训练完成后评估模型性能。
- `predict`：预测模式
  使用已训练的模型进行图像或视频的目标检测推理。
- `export`：模型导出模式
  将训练好的模型导出为不同平台可部署格式（如ONNX、CoreML等）。
- `track`：跟踪模式
  实现对象在视频流中的持续追踪。
- `benchmark`：基准测试模式
  分析各部署格式模型的速度和准确性。