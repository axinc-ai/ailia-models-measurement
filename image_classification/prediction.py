import sys, os
import glob
import shutil
import argparse
import subprocess as sp

parser = argparse.ArgumentParser(
    description='Prediction',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
parser.add_argument(
    '-m', '--model', metavar='MODEL', default='resnet50',
    help='specify the model (resnet50, resnet18, mobilenetv2).'
)
parser.add_argument(
    '-d', '--data', metavar='DATASET', default='imagenet',
    help='specify the datasets. (imagenet, or custom)'
)
parser.add_argument(
    '-t', '--tflite', action='store_true',
    help='use tflite model'
)
parser.add_argument(
    '-p', '--param', metavar='KEY=VALUE', default=[], nargs='*',
    help='Add a model parameter.'
)
args = parser.parse_args()


def prepare_datasets(data='imagenet'):
    data_dir = os.path.join('data', data)
    if not os.path.exists(os.path.join(data_dir, 'ILSVRC/Data/CLS-LOC/val')):
        raise FileNotFoundError(os.path.join(data_dir, 'ILSVRC/Data/CLS-LOC/val'))


def predict(model_name, data):
    data_dir = os.path.join('data', data)
    name = data
    name2 = name if not args.param else '%s__%s' % (name, '_'.join([x.replace('=', '_').replace('.', '_') for x in args.param]))
    name2 = name2 if not args.tflite else '%s_tflite' % name2

    pred_dir = os.path.join('evaluation', model_name, name2, 'predictions')

    if not os.path.exists(pred_dir):
        os.makedirs(pred_dir)

    if args.tflite:
        work_dir = os.path.join('../ailia-models-tflite', 'image_classification', model_name)
    else:
        work_dir = os.path.join('../ailia-models', 'image_classification', model_name)
    src_path = os.path.join('data', data, 'ILSVRC/Data/CLS-LOC/val')
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

    for res_path in sorted(glob.glob(os.path.join(pred_dir, '*_res.txt'))):
        file_path = res_path.replace('_res.txt', '.txt')
        shutil.move(res_path, file_path)

    print('\nPrediction complete.')
    print('Predict output name:', name2)


def main():
    print("DATASETS:", args.data)
    print("MODEL:", args.model)
    print('')

    try:
        prepare_datasets(args.data)
        predict(args.model, args.data)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
