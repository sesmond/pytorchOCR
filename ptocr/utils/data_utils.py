import logging

import numpy as np

logger = logging.getLogger(__name__)


def read_labeled_image_list(label_file_name, limit=None):
    f = open(label_file_name, 'r')

    filenames = []
    labels = []
    for line in f:
        filename, _, label = line.strip().partition(' ')  # partition函数只读取第一次出现的标志，分为左右两个部分
        filenames.append(filename)
        labels.append(label)

    logger.info("样本标签数量[%d],样本图像数量[%d]", len(labels), len(filenames))

    if limit:
        image_labels = list(zip(filenames, labels))
        np.random.shuffle(image_labels)
        logger.info("实际返回%d个样本", limit)
        return zip(*image_labels[0:limit])
    f.close()

    return filenames, labels
