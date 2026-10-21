#### 使用模型进行目标检测

```bash
yolo detect predict model=yolo11n.pt source='path/to/image.jpg' #此处选择yolo11n.pt预训练模型，第一次运行会自动下载模型到当前目录
```

也可以提前下载预训练模型[yolo11n.pt](https://github.com/ultralytics/assets/releases/download/v8.3.0/yolo11n.pt)并在模型检测时指定路径：`model = YOLO('模型路径')`

检测生成图像默认保存在`runs/detect/predict/`目录下。

- 若一次性检测多个图像，可以将`source`参数改为图像所在文件夹路径；
- 若要使用摄像头，将`source`参数改为`0`；
- 若要检测视频文件，将`source`参数改为视频文件路径；
- 若要检测电脑显示屏，将`source`参数改为`screen`。

#### 如何保存录像检测结果?

使用脚本检测图像：

```python
import cv2
import os
import time
from ultralytics import YOLO
# 加载你的模型（可以替换为你自己训练的 best.pt）
model = YOLO('模型路径')
# 设置自定义保存路径
save_folder = r'C:\\Users\\ASUS\\runs\\detect\\predict_video'
os.makedirs(save_folder, exist_ok=True)  # 如果文件夹不存在则创建
# 自动命名视频文件
timestamp = time.strftime('%Y%m%d_%H%M%S')
filename = f'yolo_output_{timestamp}.avi'
save_path = os.path.join(save_folder, filename)
# 打开摄像头
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("无法打开摄像头")
    exit()
# 获取摄像头分辨率（确保与 VideoWriter 匹配）
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
# 初始化视频写入器（XVID 编码，帧率 20）
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(save_path, fourcc, 20.0, (frame_width, frame_height))
print(f"正在录制，按 'q' 退出程序\n 视频保存位置：{save_path}")
# 实时检测并写入视频
while True:
    success, frame = cap.read()
    if not success:
        print("读取摄像头帧失败")
        break
    # 使用 YOLO 进行预测
    results = model.predict(frame, verbose=False)
    annotated_frame = results[0].plot()
    out.write(annotated_frame)
    cv2.imshow('YOLO Webcam Detection', annotated_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("检测终止，视频已保存")
        break
# 清理资源
cap.release()
out.release()
cv2.destroyAllWindows()
```

在脚本目录下运行：

```bash
conda activate yolo_env
python detect_and_save.py
```

#### 目标检测的几个参数

使用脚本进行目标检测：

```python
yolo=YOLO('yolo11n.pt',task='detect',device='cuda:0') 
# task参数可以是'detect'、'segment'、'classify'等
# device参数可以是'cpu'或'cuda:0'（如果有GPU）
result=yolo(source='path/to/image.jpg', 
            conf=0.25,  # 置信度阈值,值越低越多检测结果
            iou=0.45,   # IOU 阈值，IOU 越高，说明预测框与真实框越接近
            max_det=1000,  # 最大检测数量
            save=True, # 是否保存结果
            save_txt=True, # 是否保存为 txt 文件
            save_conf=True,
            project='保存的主目录路径', # 比如 'C:/Users/ASUS/runs/detect'
            name='自定义子文件夹名') # 比如 'my_predict')  # 是否保存置信度
```

#### 检测结果可视化

使用matplotlib绘制检测结果：

```python
import matplotlib.pyplot as plt
plt.imshow(result[0].plot()[:,:,::-1])  # 绘制检测结果
# [:,:,::-1]是为了将BGR图像转换为RGB，因为YOLO返回的图像通常是BGR格式（因为底层很多视觉库，包括 OpenCV，默认用BGR）
plt.title('YOLO Detection Result')  # 设置标题
plt.axis('off')  # 关闭坐标轴,默认显示坐标轴
plt.show() # 生成图像窗口
```
