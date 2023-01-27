rem The map becomes higher as the detection threshold is lower.

set dataset=coco2017
python prediction.py -m yolox -p dw=416 dh=416 th=0.01 m=yolox_tiny quantize -d %dataset%

set iou=0.5
python map.py -m yolox -d %dataset%__dw_416_dh_416_th=0_01_m=yolox_tiny_quantize -t %iou%

set iou=0.75
python map.py -m yolox -d %dataset%__dw_416_dh_416_th=0_01_m=yolox_tiny_quantize -t %iou%
