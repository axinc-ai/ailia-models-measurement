#The map becomes higher as the detection threshold is lower.

export dataset=coco2017
python3 prediction.py -m yolov3-tiny -p th=0.01 --tflite -d ${dataset}
python3 prediction.py -m yolox -p th=0.01 --tflite -d ${dataset}

export iou=0.5
python3 map.py -m yolov3-tiny -d ${dataset}__th=0_01_tflite -t ${iou}
python3 map.py -m yolox -d ${dataset}__th=0_01_tflite -t ${iou}
