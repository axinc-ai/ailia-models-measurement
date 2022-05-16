python prediction.py -m resnet50 --tflite -p float -d imagenet
python prediction.py -m resnet50 --tflite -p float tflite -d imagenet
python prediction.py -m resnet50 --tflite -p float t=1_crop -d imagenet
python prediction.py -m resnet50 --tflite -p float tflite t=1_crop -d imagenet
python prediction.py -m resnet50 --tflite -p t=1_crop -d imagenet
python prediction.py -m resnet50 --tflite -p recalib t=1_crop -d imagenet
python prediction.py -m resnet50 --tflite -p recalib t=1_crop tflite -d imagenet

python accuracy.py -m resnet50 -d imagenet__float_tflite
python accuracy.py -m resnet50 -d imagenet__float_tflite_tflite
python accuracy.py -m resnet50 -d imagenet__float_t_1_crop_tflite
python accuracy.py -m resnet50 -d imagenet__float_tflite_t_1_crop_tflite
python accuracy.py -m resnet50 -d imagenet__t_1_crop_tflite
python accuracy.py -m resnet50 -d imagenet__recalib_t_1_crop_tflite
python accuracy.py -m resnet50 -d imagenet__recalib_t_1_crop_tflite_tflite
