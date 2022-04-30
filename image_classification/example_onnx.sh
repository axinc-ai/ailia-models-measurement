export dataset=imagenet

python3 prediction.py -m resnet50 -p a=resnet50.opt -d ${dataset}
python3 prediction.py -m resnet50 -p a=resnet50_pytorch -d ${dataset}
python3 prediction.py -m resnet50 -p a=resnet50_pytorch t=1_crop -d ${dataset}

python3 accuracy.py -m resnet50 -d ${dataset}__a_resnet50.opt
python3 accuracy.py -m resnet50 -d ${dataset}__a_resnet50_pytorch
python3 accuracy.py -m resnet50 -d ${dataset}__a_resnet50_pytorch_t_1_crop
