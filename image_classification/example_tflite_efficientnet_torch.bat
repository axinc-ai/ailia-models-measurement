python prediction.py -m efficientnet_lite --tflite -p float t=1_crop torch -d imagenet
python prediction.py -m efficientnet_lite --tflite -p t=1_crop torch -d imagenet

python accuracy.py -m efficientnet_lite -d imagenet__float_t_1_crop_torch_tflite
python accuracy.py -m efficientnet_lite -d imagenet__t_1_crop_torch_tflite
