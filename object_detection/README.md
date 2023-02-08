# mAP

Calculate mAP of object detection API

## Usage

### Dataset

The script will download coco2017 val dataset to data/coco2017.

### Prediction 

Predict bounding boxes using MODEL.

```
python3 prediction.py -m MODEL
```

You can set optional parameter to model using p option.

```
python3 prediction.py -m MODEL -p dw=1280 dh=640
```

### Calculate mAP

Calculate mAP using prediction result.

```
python3 map.py -m MODEL -d coco2017
```

You can use -th option for mAP75.

```
python3 map.py -m MODEL -d coco2017 -th 0.75
```

## Result

### ONNX

|Model|Format|Accuracy|mAP75|mAP50|
|-----|-----|-----|-----|-----|
|yolov3_tiny|ONNX|float|12.27|34.93|
|yolov3_tiny|ONNX|int8 (per_tensor)|6.33|32.16|
|yolox_tiny|ONNX|float|31.36|47.04|
|yolox_tiny|ONNX|int8 (per_tensor)|28.20|45.15|
|yolox_tiny|ONNX|int8 (per_channel)|28.78|44.83|

### tflite

|Model|Format|Accuracy|mAP75|mAP50|
|-----|-----|-----|-----|-----|
|yolov3_tiny|tflite|float|11.98|34.96|
|yolov3_tiny|tflite|int8|9.68|33.62|
|yolox_tiny|tflite|float|32.17|47.16|
|yolox_tiny|tflite|int8|31.08|46.57|

### Example

- [example_onnx.sh](./example_onnx.sh).
- [example_tflite.sh](./example_tflite.sh).