# YOLO 验证

## IOU算法

目标领域通常使用IOU（Intersection over Union）算法评价两个框的接近程度

例如，现在yolo模型在验证集上预测出物体位置并绘制识别框，识别框与标记框的交集面积计为$S_{交集}$，识别框与标记框的并集面积计为$S_{并集}$，那么：

$$IOU=\frac{S_{交集}}{S_{并集}}$$

即Intersection over Union，交集在并集上，交并比

一般认为$IOU\geq0.5$时预测正确

## 准确率与召回率

对于多分类问题，取其中一类，认为其它类别为反例

则真实情况与预测结果的关系可分为四种：

|                | 预测为正例      | 预测为反例      |
| -------------- |   ----------   |   ----------   |
| 实际为正例      | True Positive  | False Negative |
| 实际为反例      | False Positive | True Negative  |

上面的表格一般称为混淆矩阵（Confusion Matrix）

基于混淆矩阵数值，得出精确率（Precision）与召回率（Recall）定义：

$$Precision=\frac{TP}{TP+FP}=\frac{正确预测}{预测总数}$$

$$Recall=\frac{TP}{TP+FN}=\frac{正确预测}{实际总数}$$

基于以上两个指标，可以计算F1分数：

$$F1=2\times\frac{P\times{R}}{P+R}$$

F1分数是准确率与召回率的调和平均数，综合考虑了两者的表现

除了F1，还有F2、F0.5等指标，它们的通用公式为：

$$F_{\beta}=(1+\beta^2)\times\frac{P\times{R}}{\beta^2\times{P}+R}$$

其中$\beta$表示对召回率的重视程度，$\beta>1$时更重视召回率，$\beta<1$时更重视准确率，$\beta=1$时即F1分数，准确率与召回率同等重要

## P、R与conf的关系

置信度（confidence）是模型对预测结果的确信程度，通常表示为一个概率值，范围在0到1之间

置信度越高，准确率通常越高，但召回率会下降；置信度越低，召回率通常越高，但准确率会下降

分析P-conf、R-conf曲线、F1-conf曲线，我们无法改变曲线的变化趋势，但是我们期望P、R、F1都有较高的均值。在实际运用中，我们往往取F1最高点对应的conf值作为最终的置信度阈值，并称F1的最大值为模型的F1分数，对应的P、R值即为模型的精确率与召回率

## PR曲线与mAP

PR曲线（Precision-Recall Curve）展示了在不同置信度阈值下模型的精确率与召回率的关系

PR曲线下的面积即为平均精确率（Average Precision，AP），AP值的大小，主要取决于P-conf、R-conf曲线的形状，当两曲线绘制于同一坐标系中，如果两曲线交点高度较高，则AP值较大，反之则较小

综上，PR曲线靠外，AP值较大，代表了能够找到一个conf使得P、R都较高

现在，对于模型预测的所有类别，都绘制出各自的PR曲线，并计算出各自的AP值，最后对所有类别的AP值取平均，即为mAP（mean Average Precision，平均精确率）

同时，我们知道我们通过IOU阈值来判断预测是否正确，当IOU变大时，模型预测正确的难度也变大，因此mAP通常会随着IOU阈值的增大而减小，因此我们通常会计算多个IOU阈值下的mAP值，并标注出来，例如mAP@0.5表示IOU阈值为0.5时的mAP值，mAP@0.5:0.95表示IOU阈值从0.5到0.95，步长为0.05时的mAP均值

## fitness

fitness是YOLO模型训练过程中用于评价模型性能的指标，作为模型的loss，目标是使fitness值最小化

fitness是P、R、mAP@0.5、mAP@0.5:0.95四个指标的加权和，默认情况下，fitness的计算公式为：

$$fitness=0\times{P}+0\times{R}+0\times{mAP@0.5}+1.0\times{mAP@0.5:0.95}$$

如果要修改权重，修改`ultralytics/utils/metrics.py`文件中的`fitness`函数即可