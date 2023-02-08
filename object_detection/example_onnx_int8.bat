rem The map becomes higher as the detection threshold is lower.

set dataset=coco2017
python prediction.py -m yolov3-tiny -p dw=416 dh=416 th=0.01 onnx -d %dataset%
python prediction.py -m yolov3-tiny -p dw=416 dh=416 th=0.01 quantize -d %dataset%
python prediction.py -m yolox -p dw=416 dh=416 th=0.01 m=yolox_tiny_int8_per_tensor -d %dataset%
python prediction.py -m yolox -p dw=416 dh=416 th=0.01 m=yolox_tiny_int8_per_channel -d %dataset%

set iou=0.5
python map.py -m yolov3-tiny -d %dataset%__dw_416_dh_416_th_0_01_onnx -t %iou%
python map.py -m yolov3-tiny -d %dataset%__dw_416_dh_416_th_0_01_quantize -t %iou%
python map.py -m yolox -d %dataset%__dw_416_dh_416_th=0_01_m=yolox_tiny_int8_per_tensor -t %iou%
python map.py -m yolox -d %dataset%__dw_416_dh_416_th=0_01_m=yolox_tiny_int8_per_channel -t %iou%

set iou=0.75
python map.py -m yolov3-tiny -d %dataset%__dw_416_dh_416_th_0_01_onnx -t %iou%
python map.py -m yolov3-tiny -d %dataset%__dw_416_dh_416_th_0_01_quantize -t %iou%
python map.py -m yolox -d %dataset%__dw_416_dh_416_th=0_01_m=yolox_tiny_int8_per_tensor -t %iou%
python map.py -m yolox -d %dataset%__dw_416_dh_416_th=0_01_m=yolox_tiny_int8_per_channel -t %iou%
