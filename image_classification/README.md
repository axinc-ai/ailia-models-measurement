# TOP1 and TOP5 accuracy

Calculate TOP1 and TOP5 accuracy of image classification API

## Usage

### Dataset

Please download following files from kaggle.

https://www.kaggle.com/c/imagenet-object-localization-challenge/overview/description

(This subset linked from https://image-net.org/download.php)

```
imagenet_object_localization_patched2019.tar.gz : images
LOC_val_solution.csv.zip : annotation
LOC_synset_mapping.txt : class id to class no mapping
```

Unzip only val images.

```
tar -xvzf imagenet_object_localization_patched2019.tar.gz "*val*"
```

Put val files to following directoty.

```
data/imagenet/ILSVRC/Data/CLS-LOC/val/ILSVRC2012_val_00*.JPEG
data/imagenet/LOC_synset_mapping.txt
data/imagenet/LOC_val_solution.csv
```

### Prediction 

Predict labels using MODEL.

```
python3 prediction.py -m MODEL
```

### Calculate accuracy

Calculate accuracy using prediction result.

```
python3 map.py -m MODEL -d imagenet
```

### TTA

By default, the aspect ratio is ignored and the image size is resized to 224x224. When CenterCrop is enabled, it maintains the aspect ratio, resizes the short side to 256, and then crops to 224x224. (1-crop-testing)

### Example

- [example_onnx.sh](./example_onnx.sh).
- [example_tflite.bat](./example_tflite.bat).

## Evaluation Result

ImageNet 50000 Validation Images

|model|Format|InferenceEngine|TTA|TOP1|TOP5|
|-----|-----|-----|-----|-----|-----|
|resnet50.opt (chainer)|ONNX|ailia SDK 1.2.11|None|0.7241|0.9103|
|resnet50_pytorch|ONNX|ailia SDK 1.2.11|None|0.6852|0.8869|
|resnet50_pytorch|ONNX|ailia SDK 1.2.11|1-crop|0.7532|0.9253|
|resnet50 (float)|tflite|ailia TFLite Runtime 1.1.1|None|N/A|N/A|
|resnet50 (float)|tflite|TensorFlowLite|None|N/A|N/A|
|resnet50 (int8)|tflite|ailia TFLite Runtime 1.1.1|None|N/A|N/A|
|resnet50 (int8)|tflite|TensorFlowLite|None|N/A|N/A|

## Official Benchmark

|model|InferenceEngine|TTA|TOP1|TOP5|
|-----|-----|-----|-----|-----|
|resnet50|pytorch|1-crop|0.7592|0.9281|
|resnet50|Keras|1-crop|0.759|0.929|

Reference :
- https://pytorch.org/vision/stable/models.html
- https://keras.io/ja/applications/

