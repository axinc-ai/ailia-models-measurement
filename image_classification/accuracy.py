import shutil
import sys, os
import glob
import argparse
import subprocess as sp

parser = argparse.ArgumentParser(
    description='Accuracy',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
parser.add_argument(
    '-m', '--model', metavar='MODEL', default='resnet50',
    help='specify the model.'
)
parser.add_argument(
    '-d', '--data', metavar='DATASET(or DIRECTORY)', default='imagenet',
    help='specify the datasets ( imagenet, or custom )'
         ' or directory which has groundtruths and predictions.'
)
args = parser.parse_args()


def accuracy(model_name, data):
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

    files = glob.glob(os.path.join(pred_dir, "*.txt"))
    files.sort()

    top1 = 0
    top5 = 0
    cnt = 0

    gt_id = 0

    for f in files:
        fh1 = open(f, "r")
        line_cnt = 0
        for line in fh1:
            class_label = line.split(" ")[0]
            class_id = int(line.split(" ")[1])
            prob = float(line.split(" ")[2])
            if class_id == gt_id:
                if line_cnt==0:
                    top1 = top1 + 1
                top5 = top5 + 1
                break
        cnt = cnt + 1

    with open(os.path.join(result_dir, 'results.txt'), 'w') as f:
        f.write('Accuracy\n')
        print('DATA CNT : %d' % cnt)
        print('TOP1 : %f' % (top1 / cnt))
        print('TOP5 : %f' % (top5 / cnt))
        f.write('DATA CNT : %d' % cnt)
        f.write('\n\TOP1 : %f' % (top1 / cnt))
        f.write('\n\TOP5 : %f' % (top5 / cnt))


def main():
    args.data=args.data.replace('=', '_').replace('.', '_')

    if os.path.isdir(args.data):
        print("DATA DIRECTORY:", args.data)
    else:
        print("DATASETS:", args.data)
        print("MODEL:", args.model)
    print('')

    accuracy(args.model, args.data)


if __name__ == '__main__':
    main()
