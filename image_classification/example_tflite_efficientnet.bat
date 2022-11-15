python prediction.py -m efficientnet_lite --tflite -p float t=1_crop -d imagenet
python prediction.py -m efficientnet_lite --tflite -p legacy t=1_crop -d imagenet
python prediction.py -m efficientnet_lite --tflite -p t=1_crop -d imagenet

python accuracy.py -m efficientnet_lite -d imagenet__float_t_1_crop_tflite
python accuracy.py -m efficientnet_lite -d imagenet__legacy_t_1_crop_tflite
python accuracy.py -m efficientnet_lite -d imagenet__t_1_crop_tflite
