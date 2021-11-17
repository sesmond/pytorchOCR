# -*- coding:utf-8 _*-
"""
@author:fxw
@file: __init__.py.py
@time: 2020/08/11
"""
import glob
import os
from abc import ABC

import numpy as np
from torch.utils import data

from ptocr.dataloader import data_reader


def get_files(data_path):
    """
    获取目录下以及子目录下的图片
    :param data_path:
    :return:
    """
    files = []
    exts = ['jpg', 'png', 'jpeg', 'JPG', 'bmp']
    for ext in exts:
        # glob.glob 得到所有文件名
        # 一层 2层子目录都取出来
        files.extend(glob.glob(os.path.join(data_path, '*.{}'.format(ext))))
        files.extend(glob.glob(os.path.join(data_path, '*', '*.{}'.format(ext))))
    return files


class DataProcessBase(data.Dataset, ABC):

    # TODO 这个是固定的
    def __init__(self):
        pass

    def get_base_information(self, train_txt_file):
        label_list = []
        img_list = []
        # 参与训练的所有图片名
        paths = open(train_txt_file, "r").readlines()
        for sel_type in paths:
            sel_type = sel_type.rstrip('\n')
            img_path, label_path, data_type = sel_type.split(" ")
            real_reader = data_reader.get_data_reader(data_type)
            image_list = np.array(get_files(img_path))
            if len(image_list) <= 0:
                continue
            for img_p in image_list:
                success, text_polys, text_tags = real_reader.get_annotation(img_p, label_path)
                if success:
                    text_polys = text_polys.reshape(len(text_polys), -1)
                    img_list.append(img_p)
                    label_list.append([text_polys, text_tags])
        return img_list, label_list
