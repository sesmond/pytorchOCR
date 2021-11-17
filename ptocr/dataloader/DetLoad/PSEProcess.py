# -*- coding:utf-8 _*-
"""
@author:fxw
@file: PSEProcess.py
@time: 2020/08/11
"""
import glob
import os

import cv2
import numpy as np
import torch
import torchvision.transforms as transforms
from PIL import Image
from torch.utils import data

from ptocr.utils.util_function import resize_image
from . import DataProcessBase
from .MakeSegMap import MakeSegPSE
from .transform_img import Random_Augment
from .. import data_reader


class PSEProcessTrain(DataProcessBase):
    def __init__(self, config):
        super(PSEProcessTrain, self).__init__()
        self.crop_shape = config['base']['crop_shape']
        self.TSM = Random_Augment(self.crop_shape)
        self.MSM = MakeSegPSE(config['base']['classes'], config['base']['shrink_ratio'])
        img_list, label_list = self.get_base_information(config['trainload']['train_file'])
        self.img_list = img_list
        self.label_list = label_list

    def __len__(self):
        return len(self.img_list)

    def __getitem__(self, index):
        img = cv2.imread(self.img_list[index])
        polys, dontcare = self.label_list[index]

        img, polys = self.TSM.random_scale(img, polys, self.crop_shape[0])
        img, polys = self.TSM.random_flip(img, polys)
        img, polys = self.TSM.random_rotate(img, polys)
        img, train_mask, gt_text, gt_kernels = self.MSM.process(img, polys, dontcare)

        imgs = [img, gt_text, train_mask]
        imgs.extend(gt_kernels)
        imgs = self.TSM.random_crop_pse(imgs)
        img, gt_text, train_mask, gt_kernels = imgs[0], imgs[1], imgs[2], imgs[3:]

        img = Image.fromarray(img).convert('RGB')
        img = transforms.ColorJitter(brightness=32.0 / 255, saturation=0.5)(img)
        img = self.TSM.normalize_img(img)

        gt_text = torch.from_numpy(gt_text).float()
        train_mask = torch.from_numpy(train_mask).float()
        gt_kernels = torch.from_numpy(np.array(gt_kernels)).float()

        return img, gt_text, gt_kernels, train_mask


class PSEProcessTest(data.Dataset):
    def __init__(self, config):
        super(PSEProcessTest, self).__init__()
        self.img_list = self.get_img_files(config['testload']['test_file'])
        self.TSM = Random_Augment(config['base']['crop_shape'])
        self.test_size = config['testload']['test_size']
        self.config = config

    def get_img_files(self, test_txt_file):
        img_list = []
        with open(test_txt_file, 'r', encoding='utf-8') as fid:
            lines = fid.readlines()
            for line in lines:
                line = line.strip('\n')
                img_list.append(line)
        return img_list

    def __len__(self):
        return len(self.img_list)

    def __getitem__(self, index):
        ori_img = cv2.imread(self.img_list[index])
        img = resize_image(ori_img, self.config['base']['algorithm'], self.test_size,
                           stride=self.config['testload']['stride'])
        img = Image.fromarray(img).convert('RGB')
        img = self.TSM.normalize_img(img)
        return img, ori_img
