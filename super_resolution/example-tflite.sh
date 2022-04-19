for dataset in anime photo
do
cd ../ailia-models-tflite/super_resolution/
cd espcn
python3 espcn.py -i ../../../super_resolution/${dataset}/input.png -s ../../../super_resolution/${dataset}/espcn.png --float
cd ../../../super_resolution/
done