import shutil
import sys, os
import glob
import argparse
import subprocess as sp

this_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(this_path, 'Object-Detection-Metrics'))

import _init_paths  # noqa: E402
from BoundingBox import BoundingBox  # noqa: E402
from BoundingBoxes import BoundingBoxes  # noqa: E402
from Evaluator import *  # noqa: E402
from utils import BBFormat  # noqa: E402

parser = argparse.ArgumentParser(
    description='mAP',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
parser.add_argument(
    '-m', '--model', metavar='MODEL', default='yolov4',
    help='specify the model.'
)
parser.add_argument(
    '-d', '--data', metavar='DATASET(or DIRECTORY)', default='coco2017',
    help='specify the datasets ( coco2017, coco2014, voc2012, voc2007, or custom )'
         ' or directory which has groundtruths and predictions.'
)
parser.add_argument(
    '-t', '--threshold', default=0.5,
    dest='iou', type=float,
    help='IOU threshold.'
)
args = parser.parse_args()


def getBoundingBoxes(
        directory, isGT, bbFormat, coordType,
        allBoundingBoxes=None,
        allClasses=None,
        imgSize=(0, 0),
    ):
    """Read txt files containing bounding boxes (ground truth and detections)."""
    if allBoundingBoxes is None:
        allBoundingBoxes = BoundingBoxes()
    if allClasses is None:
        allClasses = []

    # Read ground truths
    files = glob.glob(os.path.join(directory, "*.txt"))
    files.sort()

    # Check number of file
    if isGT:
        print("GT count : ",len(files))
    else:
        print("Pred count : ",len(files))
    if isGT and "coco2017" in args.data:
        if(len(files)<4952):
            print("Invalid processed frame count")
            sys.exit()

    # Read GT detections from txt file
    # Each line of the files in the groundtruths folder represents a ground truth bounding box
    # (bounding boxes that a detector should detect)
    # Each value of each line is  "class_id, x, y, width, height" respectively
    # Class_id represents the class of the bounding box
    # x, y represents the most top-left coordinates of the bounding box
    # x2, y2 represents the most bottom-right coordinates of the bounding box
    for f in files:
        nameOfImage = f.rsplit(os.sep, 1)[-1].replace(".txt", "")
        fh1 = open(f, "r")
        for line in fh1:
            line = line.strip()
            if not line:
                continue
            splitLine = line.split(" ")
            if isGT:
                idClass = (splitLine[0])  # class
                x = float(splitLine[1])
                y = float(splitLine[2])
                w = float(splitLine[3])
                h = float(splitLine[4])
                bb = BoundingBox(
                    nameOfImage, idClass,
                    x, y, w, h,
                    coordType, imgSize,
                    BBType.GroundTruth,
                    format=bbFormat)
            else:
                idClass = (splitLine[0])  # class
                confidence = float(splitLine[1])
                x = float(splitLine[2])
                y = float(splitLine[3])
                w = float(splitLine[4])
                h = float(splitLine[5])
                bb = BoundingBox(
                    nameOfImage, idClass,
                    x, y, w, h,
                    coordType, imgSize,
                    BBType.Detected,
                    confidence,
                    format=bbFormat)
            allBoundingBoxes.addBoundingBox(bb)
            if idClass not in allClasses:
                allClasses.append(idClass)

        fh1.close()

    return allBoundingBoxes, allClasses


def map(model_name, data):
    if os.path.isdir(data):
        pred_dir = os.path.join(data, 'predictions')
        gt_dir = os.path.join(data, 'groundtruths')
        result_dir = os.path.join(
            'results', model_name, data.replace(os.sep, '/').rsplit('/', 1)[-1]
        )
    else:
        pred_dir = os.path.join('evaluation', model_name, data, 'predictions')
        gt_dir = os.path.join('evaluation', model_name, data, 'groundtruths')
        result_dir = os.path.join('results', model_name, data)

    if not os.path.exists(pred_dir):
        raise Exception('Directory does not exist \'%s\'' % pred_dir)
    if not os.path.exists(gt_dir):
        raise Exception('Directory does not exist \'%s\'' % gt_dir)
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)

    coord_fmt = BBFormat.XYWH
    coord_type = CoordinatesType.Absolute
    img_size = None

    # Get groundtruth boxes
    allBoundingBoxes, allClasses = getBoundingBoxes(
        gt_dir, True, coord_fmt, coord_type, imgSize=img_size)

    # Get detected boxes
    allBoundingBoxes, allClasses = getBoundingBoxes(
        pred_dir, False, coord_fmt, coord_type, allBoundingBoxes, allClasses, imgSize=img_size)
    allClasses.sort()

    iouThreshold = args.iou
    showPlot = False
    evaluator = Evaluator()

    # Plot Precision x Recall curve
    detections = evaluator.PlotPrecisionRecallCurve(
        allBoundingBoxes,  # Object containing all bounding boxes (ground truths and detections)
        IOUThreshold=iouThreshold,  # IOU threshold
        method=MethodAveragePrecision.EveryPointInterpolation,
        showAP=True,  # Show Average Precision in the title of the plot
        showInterpolatedPrecision=False,  # Don't plot the interpolated precision curve
        savePath=result_dir,
        showGraphic=showPlot
    )

    with open(os.path.join(result_dir, 'results.txt'), 'w') as f:
        f.write('Object Detection Metrics\n')
        f.write('https://github.com/rafaelpadilla/Object-Detection-Metrics\n\n\n')
        f.write('Average Precision (AP), Precision and Recall per class:')

        acc_AP = 0
        validClasses = 0

        # each detection is a class
        for metricsPerClass in detections:
            # Get metric values per each class
            cl = metricsPerClass['class']
            ap = metricsPerClass['AP']
            precision = metricsPerClass['precision']
            recall = metricsPerClass['recall']
            totalPositives = metricsPerClass['total positives']
            total_TP = metricsPerClass['total TP']
            total_FP = metricsPerClass['total FP']

            if totalPositives > 0:
                validClasses = validClasses + 1
                acc_AP = acc_AP + ap
                prec = ['%.2f' % p for p in precision]
                rec = ['%.2f' % r for r in recall]
                ap_str = "{0:.2f}%".format(ap * 100)
                print('AP: %s (%s)' % (ap_str, cl))

                f.write('\n\nClass: %s' % cl)
                f.write('\nAP: %s' % ap_str)
                f.write('\nPrecision: %s' % prec)
                f.write('\nRecall: %s' % rec)

        if validClasses == 0:
            print("validClasses is not found. maybe prediction is failed.\n")
        else:
            mAP = acc_AP / validClasses
            mAP_str = "{0:.2f}%".format(mAP * 100)
            print('mAP: %s' % mAP_str)
            f.write('\n\n\nmAP: %s' % mAP_str)


def main():
    args.data=args.data.replace('=', '_').replace('.', '_')

    if os.path.isdir(args.data):
        print("DATA DIRECTORY:", args.data)
    else:
        print("DATASETS:", args.data)
        print("MODEL:", args.model)
    print('')

    map(args.model, args.data)


if __name__ == '__main__':
    main()
