import glob
import logging
import os
import sys

import cv2
import lmdb
import numpy as np
import six
import torch
from PIL import Image, ImageFile

from ptocr.utils import data_utils

ImageFile.LOAD_TRUNCATED_IMAGES = True
from torch.utils.data import Dataset
import torchvision.transforms as transforms
from ptocr.dataloader.RecLoad.DataAgument import transform_img_shape, DataAugment
from ptocr.utils.util_function import create_module, PILImageToCV, CVImageToPIL

logger = logging.getLogger(__name__)


def get_img(path, is_gray=False):
    img = Image.open(path).convert('RGB')
    if (is_gray):
        img = img.convert('L')
    return img


class CRNNProcessLmdbLoad(Dataset):
    """
    Lmdb 格式样本读取
    """

    def __init__(self, config, lmdb_type):
        self.config = config
        self.lmdb_type = lmdb_type

        if lmdb_type == 'train':
            lmdb_file = config['trainload']['train_file']
            workers = config['trainload']['num_workers']
        elif lmdb_type == 'val':
            lmdb_file = config['valload']['val_file']
            workers = config['valload']['num_workers']
        else:
            assert 1 == 1
            raise ('lmdb_type error !!!')

        self.env = lmdb.open(lmdb_file, max_readers=workers, readonly=True, lock=False, readahead=False, meminit=False)

        if not self.env:
            print('cannot creat lmdb from %s' % (lmdb_file))
            sys.exit(0)

        with self.env.begin(write=False) as txn:
            nSamples = int(txn.get('num-samples'.encode('utf-8')))
            self.nSamples = nSamples

        self.transform_label = create_module(config['label_transform']['label_function'])
        # TODO 这只是一个函数，但是在里边初始化了

        self.bg_img = []
        for path in glob.glob(os.path.join(config['trainload']['bg_path'], '*')):
            self.bg_img.append(path)

    def __len__(self):
        return self.nSamples

    def __getitem__(self, index):
        assert index <= len(self), 'index range error'
        index += 1
        with self.env.begin(write=False) as txn:
            img_key = 'image-%09d' % index
            imgbuf = txn.get(img_key.encode('utf-8'))

            buf = six.BytesIO()
            buf.write(imgbuf)
            buf.seek(0)
            try:
                img = Image.open(buf).convert('RGB')
            except IOError:
                print('Corrupted image for %d' % index)
                return self[index + 1]

            label_key = 'label-%09d' % index
            label = txn.get(label_key.encode('utf-8')).decode()
        # TODO 这里是为了统一大小写
        label = self.transform_label(label, char_type=self.config['label_transform']['char_type'],
                                     t_type=self.config['label_transform']['t_type'])
        # TODO 这个给用坏了，
        if self.config['base']['is_gray']:
            img = img.convert('L')
        img = PILImageToCV(img, self.config['base']['is_gray'])
        if self.lmdb_type == 'train':
            try:
                bg_index = np.random.randint(0, len(self.bg_img))
                bg_img = PILImageToCV(get_img(self.bg_img[bg_index]), self.config['base']['is_gray'])
                img = transform_img_shape(img, self.config['base']['img_shape'])
                img = DataAugment(img, bg_img, self.config['base']['img_shape'])
                img = transform_img_shape(img, self.config['base']['img_shape'])
            except IOError:
                print('Corrupted image for %d' % index)
                return self[index + 1]
        elif self.lmdb_type == 'val':
            img = transform_img_shape(img, self.config['base']['img_shape'])
        img = CVImageToPIL(img, self.config['base']['is_gray'])
        img = transforms.ToTensor()(img)
        img.sub_(0.5).div_(0.5)
        return (img, label)


class CRNNProcessTxtLoad(Dataset):
    """
    txt 格式样本读取:
    都继承自Dataset，只要实现 __getitem__,__len__ 两个方法即可，其他的在初始化之后做好。
    """

    def __init__(self, config, data_type):
        """
        初始化方法
        @param config: 配置参数
        @param data_type: 数据类型(train/val)
        """
        self.config = config
        self.data_type = data_type
        if data_type == 'train':
            label_file = config['trainload']['train_file']
            workers = config['trainload']['num_workers']
            self.data_path = os.path.join(os.path.dirname(label_file), "train")
            # self.img_path =

        elif data_type == 'val':
            label_file = config['valload']['val_file']
            workers = config['valload']['num_workers']
            self.data_path = os.path.join(os.path.dirname(label_file), "validate")
        else:
            assert 1 == 1
            raise ('data_type error !!!')

        image_file_names, labels = data_utils.read_labeled_image_list(label_file)
        if len(image_file_names) == 0:
            raise ValueError("数据集不能为空！")
        self.nSamples = len(image_file_names)
        self.image_names = image_file_names
        self.image_labels = labels

        self.transform_label = create_module(config['label_transform']['label_function'])
        self.bg_img = []
        for path in glob.glob(os.path.join(config['trainload']['bg_path'], '*')):
            self.bg_img.append(path)

    def __len__(self):
        return self.nSamples

    def __getitem__(self, index):
        assert index < len(self), 'index range error'
        img_key = self.image_names[index]
        img_path = os.path.join(self.data_path, os.path.basename(img_key))
        # label = txn.get(label_key.encode('utf-8')).decode()
        label = self.image_labels[index]
        # TODO 这个在DataAgument里 为了统一英文大小写，这里不统一了因为要放在一起训练
        # label = self.transform_label(label, char_type=self.config['label_transform']['char_type'],
        #                              t_type=self.config['label_transform']['t_type'])
        # print("样本标签：", img_key, label)
        img = cv2.imread(img_path)
        if self.config['base']['is_gray']:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        if self.data_type == 'train':
            try:
                # TODO !! 增强
                bg_index = np.random.randint(0, len(self.bg_img))
                bg_img = PILImageToCV(get_img(self.bg_img[bg_index]), self.config['base']['is_gray'])
                img = transform_img_shape(img, self.config['base']['img_shape'])
                img = DataAugment(img, bg_img, self.config['base']['img_shape'])
                img = transform_img_shape(img, self.config['base']['img_shape'])
            except IOError:
                print('Corrupted image for %d' % index)
                return self[index + 1]
        elif self.data_type == 'val':
            img = transform_img_shape(img, self.config['base']['img_shape'])

        img = CVImageToPIL(img, self.config['base']['is_gray'])
        img = transforms.ToTensor()(img)
        img.sub_(0.5).div_(0.5)
        # print("shape：", img_path, img.shape)
        # TODO !! 这里有些=1的估计是黑白的图片，这里要处理一下，统一转化成rgb三通道
        return (img, label)


class alignCollate(object):
    def __init__(self, ):
        pass

    def __call__(self, batch):
        images, labels = zip(*batch)
        images = torch.stack(images, 0)
        return images, labels
