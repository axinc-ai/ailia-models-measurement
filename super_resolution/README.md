# Evaluation of super resolution

Evaluation script for ailia-models

## Evaluation settings

### Script

- [example-tflite.sh](example-tflite.sh)
- [example-onnx.sh](example-onnx.sh)

### Test dataset

|anime|photo|
|-----|-----|
|![input-anime](./anime/input.png)|![input-photo](./photo/input.png)|
|from AXELL CORPORATION|from https://pixabay.com/videos/bird-parrot-nature-animal-colorful-46026/|

### Resolution

- 128x128 -> 384x384 (espcn) (tflite)
- 128x128 -> 512x512 (srresnet, edsr, han) (onnx)
- 128x128 -> 448x448 (real-esrgan) (onnx)

## Anime dataset

|bilinear|gradia|espcn|
|-----|-----|-----|
|![bilinear](./anime/bilinear.png)|![gradia](./anime/gradia.png)|![espcn](./anime/espcn.png)|

|srresnet|edsr|han|
|-----|-----|-----|
|![srresnet](./anime/srresnet.png)|![edsr](./anime/edsr.png)|![han](./anime/han.png)|

|real-esrgan (photo)|real-esrgan (anime)|
|-----|-----|
|![real-esrgan-photo](./anime/real-esrgan-photo.png)|![real-esrgan-anime](./anime/real-esrgan-anime.png)|

## Photo dataset

|bilinear|gradia|espcn|
|-----|-----|-----|
|![bilinear](./photo/bilinear.png)|![gradia](./photo/gradia.png)|![espcn](./photo/espcn.png)|

|srresnet|edsr|han|
|-----|-----|-----|
|![srresnet](./photo/srresnet.png)|![edsr](./photo/edsr.png)|![han](./photo/han.png)|

|real-esrgan (photo)|real-esrgan (anime)|
|-----|-----|
|![real-esrgan-photo](./photo/real-esrgan-photo.png)|![real-esrgan-anime](./photo/real-esrgan-anime.png)|