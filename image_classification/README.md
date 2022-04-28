# TOP1 and TOP5 accuracy

Calculate TOP1 and TOP5 accuracy of image classification API

## Usage

### Dataset

Please download imagenet_object_localization_patched2019.tar.gz from kaggle.
https://www.kaggle.com/c/imagenet-object-localization-challenge/overview/description

(This subset linked from https://image-net.org/download.php)

### Prediction 

Predict labels using MODEL.

```
python3 prediction.py -m MODEL
```

### Calculate accuracy

Calculate accuracy using prediction result.

```
python3 map.py -m MODEL -d imagenet
```

### Example

See [example.sh](./example.sh).