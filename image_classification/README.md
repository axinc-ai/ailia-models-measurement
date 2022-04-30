# TOP1 and TOP5 accuracy

Calculate TOP1 and TOP5 accuracy of image classification API

## Usage

### Dataset

Please download following files from kaggle.

https://www.kaggle.com/c/imagenet-object-localization-challenge/overview/description

(This subset linked from https://image-net.org/download.php)

```
imagenet_object_localization_patched2019.tar.gz : images
LOC_val_solution.csv.zip : annotation
LOC_synset_mapping.txt : class id to class no mapping
```

Unzip only val images.

```
tar -xvzf imagenet_object_localization_patched2019.tar.gz "*val*"
```

Put val files to following directoty.

```
data/imagenet/ILSVRC/Data/CLS-LOC/val/ILSVRC2012_val_00*.JPEG
data/imagenet/LOC_synset_mapping.txt
data/imagenet/LOC_val_solution.csv
```

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