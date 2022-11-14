python prediction.py -m efficientnetlite --tflite -p float t=1_crop -d imagenet
python prediction.py -m efficientnetlite --tflite -p legacy t=1_crop -d imagenet
python prediction.py -m efficientnetlite --tflite -p t=1_crop -d imagenet

python accuracy.py -m efficientnetlite -d imagenet__float_t_1_crop_tflite
python accuracy.py -m efficientnetlite -d imagenet__legacy_t_1_crop_tflite
python accuracy.py -m efficientnetlite -d imagenet__t_1_crop_tflite
