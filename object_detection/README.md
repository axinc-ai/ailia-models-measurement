# mAP

Calculate mAP of object detection API

## Usage

### Dataset

The script will download coco2017 val dataset to data/coco2017.

### Prediction 

Predict bounding boxes using MODEL.

```
python3 prediction.py -m MODEL
```

You can set optional parameter to model using p option.

```
python3 prediction.py -m MODEL -p dw=1280 dh=640
```

### Calculate mAP

Calculate mAP using prediction result.

```
python3 map.py -m MODEL -d coco2017
```

You can use -th option for mAP75.

```
python3 map.py -m MODEL -d coco2017 -th 0.75
```

### Example

See [example.sh](./example.sh).