python prediction.py -m resnet50 --tflite -p float -d imagenet
rem python prediction.py -m resnet50 --tflite -p float tflite -d imagenet
python prediction.py -m resnet50 --tflite -p float t=1_crop -d imagenet
python prediction.py -m resnet50 --tflite -p float tflite t=1_crop -d imagenet

python accuracy.py -m resnet50 -d imagenet__float_tflite
python accuracy.py -m resnet50 -d imagenet__float_tflite_tflite
python accuracy.py -m resnet50 -d imagenet__float_t_1_crop_tflite
python accuracy.py -m resnet50 -d imagenet__float_tflite_t_1_crop_tflite
