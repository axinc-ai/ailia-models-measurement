export dataset=imagenet

python3 prediction.py -m resnet50 --tflite -p float -d ${dataset}
python3 accuracy.py -m resnet50 -d ${dataset}_tflite__float
