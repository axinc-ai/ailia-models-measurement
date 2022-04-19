import os
import shutil
import json
import urllib.request
import zipfile

from common.utils import progress_print

import numpy as np
import pandas as pd


def download(data_dir, data='coco2017'):
    d = {
        'coco2017': (
            'http://images.cocodataset.org/zips/val2017.zip',
            'http://images.cocodataset.org/annotations/annotations_trainval2017.zip',
        ),
        'coco2014': (
            'http://images.cocodataset.org/zips/val2014.zip',
            'http://images.cocodataset.org/annotations/annotations_trainval2014.zip',
        ),
    }
    img_url, anno_url = d[data]

    image_file = os.path.join(data_dir, os.path.basename(img_url))
    if not os.path.exists(image_file):
        print("Downloading MSCOCO val images ...")
        urllib.request.urlretrieve(img_url, image_file, progress_print)
        print('\n')

    anno_file = os.path.join(data_dir, os.path.basename(anno_url))
    if not os.path.exists(anno_file):
        print("Downloading MSCOCO train/val annotations ...")
        urllib.request.urlretrieve(anno_url, anno_file, progress_print)
        print('\n')

    return image_file, anno_file


def create_groundtruths(data_dir, anno_file, label_filter=None):
    gt_dir = os.path.join(data_dir, 'groundtruths')
    if os.path.exists(gt_dir):
        return

    tmp_dir = os.path.join(data_dir, '_groundtruths')
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)

    with open(anno_file) as f:
        info = json.load(f)

    img_dir = os.path.join(data_dir, 'images')
    img_info = info["images"]
    anno_info = info["annotations"]
    cat_info = info["categories"]

    img_info = {d["id"]: d for d in img_info}
    cat_info = {d["id"]: d["name"] for d in cat_info}

    df = pd.DataFrame()
    df["image_id"] = [d["image_id"] for d in anno_info]
    df["category_id"] = [d["category_id"] for d in anno_info]
    df["bbox"] = [d["bbox"] for d in anno_info]
    df = df.sort_values(by=["image_id", "category_id"])

    def func(df):
        image_id = df.iloc[0].image_id

        if not image_id in img_info:
            return

        info = img_info[image_id]
        file_name = info["file_name"]
        # h = info["height"]
        # w = info["width"]

        img_path = os.path.join(img_dir, file_name)
        if not os.path.exists(img_path):
            return

        print(file_name)

        data = [[], [], [], [], []]  # label, x, y, w, h
        for row in df.itertuples():
            label = cat_info[row.category_id].replace(' ', '_')
            if label_filter is not None and label not in label_filter:
                continue

            bbox = row.bbox
            data[0].append(label)
            data[1].append(bbox[0])
            data[2].append(bbox[1])
            data[3].append(bbox[2])
            data[4].append(bbox[3])

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

    print("Create MSCOCO groundtruths ...")
    df.groupby("image_id", as_index=False).apply(func)
    shutil.move(tmp_dir, gt_dir)
    print('')


def prepare(data='coco2017', label_filter=None):
    d = {
        'coco2017': (
            'val2017',
            'instances_val2017.json',
        ),
        'coco2014': (
            'val2014',
            'instances_val2014.json',
        ),
    }
    val, json_file = d[data]

    name = data if label_filter is None else '%s_%s' % (data, '+'.join(label_filter))
    data_dir = os.path.join('data', name)

    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    image_dir = os.path.join(data_dir, 'images')
    anno_dir = os.path.join(data_dir, 'annotations')
    gt_dir = os.path.join(data_dir, 'groundtruths')

    if not os.path.exists(image_dir) or not os.path.exists(gt_dir):
        image_file, anno_file = download(data_dir, data)

        if not os.path.exists(image_dir):
            print("Extracting MSCOCO val images ...")
            with zipfile.ZipFile(image_file) as existing_zip:
                existing_zip.extractall(data_dir)
            print('')
            shutil.move(os.path.join(data_dir, val), image_dir)

        if not os.path.exists(anno_dir):
            print("Extracting MSCOCO train/val annotations ...")
            with zipfile.ZipFile(anno_file) as existing_zip:
                existing_zip.extractall(data_dir)
            print('')

        create_groundtruths(data_dir, os.path.join(anno_dir, json_file), label_filter)

        shutil.rmtree(anno_dir, ignore_errors=True)
