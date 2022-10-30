python prediction.py -m mobilenetv1 --tflite -p float t=1_crop -d imagenet
python prediction.py -m mobilenetv1 --tflite -p legacy t=1_crop -d imagenet
python prediction.py -m mobilenetv1 --tflite -p t=1_crop -d imagenet

python accuracy.py -m mobilenetv1 -d imagenet__float_t_1_crop_tflite
python accuracy.py -m mobilenetv1 -d imagenet__legacy_t_1_crop_tflite
python accuracy.py -m mobilenetv1 -d imagenet__t_1_crop_tflite

python prediction.py -m mobilenetv2 --tflite -p float t=1_crop -d imagenet
python prediction.py -m mobilenetv2 --tflite -p legacy t=1_crop -d imagenet
python prediction.py -m mobilenetv2 --tflite -p t=1_crop -d imagenet

python accuracy.py -m mobilenetv2 -d imagenet__float_t_1_crop_tflite
python accuracy.py -m mobilenetv2 -d imagenet__legacy_t_1_crop_tflite
python accuracy.py -m mobilenetv2 -d imagenet__t_1_crop_tflite
