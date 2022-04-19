for dataset in anime photo
do
cd ../ailia-models/super_resolution/
cd srresnet
python3 srresnet.py --padding -i ../../../super_resolution/${dataset}/input.png -s ../../../super_resolution/${dataset}/srresnet.png
cd ../han
python3 han.py --scale 4 -i ../../../super_resolution/${dataset}/input.png -s ../../../super_resolution/${dataset}/han.png
cd ../edsr
python3 edsr.py --scale 4 -i ../../../super_resolution/${dataset}/input.png -s ../../../super_resolution/${dataset}/edsr.png
cd ../real-esrgan
python3 real_esrgan.py -i ../../../super_resolution/${dataset}/input.png -s ../../../super_resolution/${dataset}/real-esrgan-photo.png
python3 real_esrgan.py -m RealESRGAN_anime -i ../../../super_resolution/${dataset}/input.png -s ../../../super_resolution/${dataset}/real-esrgan-anime.png
cd ../../../super_resolution/
done