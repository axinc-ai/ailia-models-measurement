export dataset=coco2017
python3 prediction.py -m yolox -p dw=640 dh=640 th=0.01 m=yolox_s -d ${dataset}
python3 prediction.py -m yolox -p dw=416 dh=416 th=0.01 m=yolox_tiny -d ${dataset}
python3 prediction.py -m yolox -p dw=416 dh=416 th=0.01 m=yolox_nano -d ${dataset}
python3 prediction.py -m yolov3 -p dw=416 dh=416 th=0.01 -d ${dataset}
python3 prediction.py -m yolov3_tiny -p dw=416 dh=416 th=0.01 -d ${dataset}
python3 prediction.py -m yolov4 -p dw=416 dh=416 th=0.01  -d ${dataset}
python3 prediction.py -m yolov4_tiny -p dw=641640 416=640 th=0.01 -d ${dataset}
python3 prediction.py -m yolov5 -p dw=640 dh=640 th=0.01 a=yolov5s -d ${dataset}
python3 prediction.py -m yolov5 -p dw=640 dh=640 th=0.01 a=yolov5s6 e=0 -d ${dataset}

export iou=0.5
python3 map.py -m yolox -d ${dataset}__dw_640_dh_640_th=0_01_m=yolox_s -th ${iou}
python3 map.py -m yolox -d ${dataset}__dw_416_dh_416_th=0_01_m=yolox_tiny -th ${iou}
python3 map.py -m yolox -d ${dataset}__dw_416_dh_416_th=0_01_m=yolox_nano -th ${iou}
python3 map.py -m yolov3 -d ${dataset}__dw_416_dh_416_th=0_01 -th ${iou}
python3 map.py -m yolov3_tiny -d ${dataset}__dw_416_dh_416_th=0_01 -th ${iou}
python3 map.py -m yolov4 -d ${dataset}__dw_416_dh_416_th=0_01 -th ${iou}
python3 map.py -m yolov4_tiny -d ${dataset}__dw_416_dh_416_th=0_01 -th ${iou}
python3 map.py -m yolov5 -d ${dataset}__dw_640_dh_640_th=0_01_a=yolov5s -th ${iou}
python3 map.py -m yolov5 -d ${dataset}__dw_640_dh_640_th=0_01_a=yolov5s6_e=0 -th ${iou}
