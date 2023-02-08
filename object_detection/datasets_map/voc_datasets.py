import os
import glob
import shutil
import urllib.request
import tarfile
import xml.etree.ElementTree as ET

from common.utils import progress_print

import numpy as np
import pandas as pd


def download(data_dir, data='voc2012'):
    d = {
        'voc2012':
            'http://host.robots.ox.ac.uk/pascal/VOC/voc2012/VOCtrainval_11-May-2012.tar',
        'voc2007':
            'http://host.robots.ox.ac.uk/pascal/VOC/voc2007/VOCtest_06-Nov-2007.tar',
    }
    url = d[data]

    file = os.path.join(data_dir, os.path.basename(url))
    if not os.path.exists(file):
        print("Downloading VOC ...")
        urllib.request.urlretrieve(url, file, progress_print)
        print('\n')

    return file


def create_groundtruths(data_dir, anno_dir, label_filter=None):
    gt_dir = os.path.join(data_dir, 'groundtruths')
    if os.path.exists(gt_dir):
        return

    tmp_dir = os.path.join(data_dir, '_groundtruths')
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)

    img_dir = os.path.join(data_dir, 'images')

    print("Create VOC groundtruths ...")
    for file in glob.glob(os.path.join(anno_dir, '*.xml')):
        tree = ET.parse(file)
        root = tree.getroot()

        file_name = root.find('filename').text

        img_path = os.path.join(img_dir, file_name)
        if not os.path.exists(img_path):
            continue

        print(file_name)

        data = [[], [], [], [], []]  # label, x, y, w, h
        for node in root.findall('object'):
            label = node.find('name').text.replace(' ', '_')
            if label_filter is not None and label not in label_filter:
                continue

            bndbox = node.find('bndbox')
            xmin = bndbox.find('xmin').text
            ymin = bndbox.find('ymin').text
            xmax = bndbox.find('xmax').text
            ymax = bndbox.find('ymax').text
            data[0].append(label)
            data[1].append(xmin)
            data[2].append(ymin)
            data[3].append(int(float(xmax) - float(xmin)))
            data[4].append(int(float(ymax) - float(ymin)))

        if len(data[0]) == 0:
            os.remove(img_path)
            return

        df = pd.DataFrame(np.array(data).T)
        df.to_csv(
            os.path.join(tmp_dir, "%s.txt" % file_name.split(".")[0]),
            sep=" ",
            index=False,
            header=False,
        )

    shutil.move(tmp_dir, gt_dir)
    print('')


def prepare(data='voc2012', label_filter=None):
    name = data if label_filter is None else '%s_%s' % (data, '+'.join(label_filter))
    data_dir = os.path.join('data', name)

    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    image_dir = os.path.join(data_dir, 'images')
    gt_dir = os.path.join(data_dir, 'groundtruths')

    if not os.path.exists(image_dir) or not os.path.exists(gt_dir):
        file = download(data_dir, data)

        print("Extracting VOC images ...")
        with tarfile.open(file, 'r') as tf:
            def is_within_directory(directory, target):
                
                abs_directory = os.path.abspath(directory)
                abs_target = os.path.abspath(target)
            
                prefix = os.path.commonprefix([abs_directory, abs_target])
                
                return prefix == abs_directory
            
            def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
            
                for member in tar.getmembers():
                    member_path = os.path.join(path, member.name)
                    if not is_within_directory(path, member_path):
                        raise Exception("Attempted Path Traversal in Tar File")
            
                tar.extractall(path, members, numeric_owner=numeric_owner) 
                
            
            safe_extract(tf, path=data_dir)
        print('')

        if not os.path.exists(image_dir):
            shutil.move(os.path.join(data_dir, 'VOCdevkit', data.upper(), 'JPEGImages'), image_dir)

        create_groundtruths(
            data_dir,
            os.path.join(data_dir, 'VOCdevkit', data.upper(), 'Annotations'),
            label_filter
        )

        shutil.rmtree(os.path.join(data_dir, 'VOCdevkit'), ignore_errors=True)
