import sys, os
import glob
import shutil
import argparse
import subprocess as sp

from datasets_map import coco_datasets, voc_datasets

parser = argparse.ArgumentParser(
    description='Prediction',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
parser.add_argument(
    '-m', '--model', metavar='MODEL', default='yolov4',
    help='specify the model.'
)
parser.add_argument(
    '-d', '--data', metavar='DATASET', default='coco2017',
    help='specify the datasets. (coco2017, coco2014, voc2012, voc2007, or custom)'
)
parser.add_argument(
    '-f', '--filter', metavar='CATEGORY', default=None, nargs='*',
    help='Select the category for which you want to create data.'
)
parser.add_argument(
    '-p', '--param', metavar='KEY=VALUE', default=[], nargs='*',
    help='Add a model parameter.'
)
parser.add_argument(
    '-t', '--tflite', action='store_true',
    help='use tflite model'
)
args = parser.parse_args()


def prepare_datasets(data='coco2017', label_filter=None):
    if data in ('coco2017', 'coco2014'):
        coco_datasets.prepare(data, None)
    elif data in ('voc2012', 'voc2007'):
        voc_datasets.prepare(data, None)
    else:
        data_dir = os.path.join('data', data)
        if not os.path.exists(os.path.join(data_dir, 'images')) and not os.path.exists(os.path.join(data_dir, 'images.txt')):
            raise FileNotFoundError(os.path.join(data_dir, 'images'))
        if not os.path.exists(os.path.join(data_dir, 'groundtruths')):
            raise FileNotFoundError(os.path.join(data_dir, 'groundtruths'))


def predict(model_name, data, label_filter=None):
    data_dir = os.path.join('data', data)
    name = data if label_filter is None else '%s_%s' % (data, '+'.join(label_filter))
    name2 = name if not args.param else '%s__%s' % (name, '_'.join([x.replace('=', '_').replace('.', '_') for x in args.param]))
    name2 = name2 if not args.tflite else '%s_tflite' % name2
    pred_dir = os.path.join('evaluation', model_name, name2, 'predictions')
    gt_dir = os.path.join('evaluation', model_name, name2, 'groundtruths')
    gt_src_dir = os.path.join('data', data, 'groundtruths')

    if not os.path.exists(pred_dir):
        os.makedirs(pred_dir)

    if args.tflite:
        work_dir = os.path.join('../ailia-models-tflite', 'object_detection', model_name)
    else:
        work_dir = os.path.join('../ailia-models', 'object_detection', model_name)
    if os.path.exists(os.path.join(data_dir, 'images.txt')) :
        with open(os.path.join(data_dir, 'images.txt')) as f:
            src_path = f.read()
    else:
        src_path = os.path.join('data', data, 'images')
    cmd = [
        sys.executable,
        '%s.py' % model_name,
        '-v' if os.path.isfile(src_path) else '-i',
        os.path.abspath(src_path),
        '-s',
        os.path.abspath(pred_dir),
        '--write_prediction',
    ]
    for kv in args.param:
        if '=' in kv:
            key, value = kv.split('=')
            cmd.extend(['-%s' % key, value])
        else:
            cmd.extend(['--%s' % kv])

    print("Predicting images ...")
    try:
        cmdline = " ".join(cmd)
        sp.check_call(cmdline, cwd=work_dir, shell=True)
    except sp.CalledProcessError:
        pass

    if not os.path.exists(gt_dir):
        os.makedirs(gt_dir)

    for res_path in sorted(glob.glob(os.path.join(pred_dir, '*_res.txt'))):
        file_path = res_path.replace('_res.txt', '.txt')
        shutil.move(res_path, file_path)

        file_name = file_path.rsplit(os.sep, 1)[-1]
        gt_file = os.path.join(gt_dir, file_name)
        gt_src_file = os.path.join(gt_src_dir, file_name)
        if not os.path.exists(gt_src_file):
            continue
        
        shutil.copyfile(gt_src_file, gt_file)

    print('\nPrediction complete.')
    print('Predict output name:', name2)


def main():
    print("DATASETS:", args.data)
    print("MODEL:", args.model)
    print('')

    try:
        prepare_datasets(args.data, args.filter)
        predict(args.model, args.data, args.filter)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
