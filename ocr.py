import os
import re

import pytesseract
from PIL import Image
import glob
import constant
import cv2
import numpy as np


def preprocess_image(image):
    # 图像预处理
    image_np = np.array(image)
    # 反色处理
    image_np = cv2.bitwise_not(image_np)

    gray_image = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
    _, threshold_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # 去噪处理
    denoised_image = cv2.fastNlMeansDenoising(threshold_image, None, 10, 7, 21)
    return denoised_image


def resize_image(image, scale_factor):
    # 图像分辨率处理
    new_height = int(image.shape[0] * scale_factor)
    new_width = int(image.shape[1] * scale_factor)
    resized_image = cv2.resize(image, (new_width, new_height))
    return resized_image


def red_image(image, lang):
    preprocessed_image = preprocess_image(image)
    # scaled_image = resize_image(preprocessed_image, scale_factor=2.0)
    lang = constant.ocrArray[lang]
    custom_config = f'--psm 6 -l {lang}'
    result = pytesseract.image_to_string(preprocessed_image, config=custom_config)
    return ' '.join(result.split())


def red_path(image_path, lang):
    lang = constant.ocrArray[lang]
    image_extensions = constant.image_extensions
    # 遍历文件夹中的图片文件
    image_files = []
    for extension in image_extensions:
        pattern = os.path.join(image_path, "*" + extension)
        image_files.extend(glob.glob(pattern))

    sorted_image_files = sorted(image_files)
    # 打印找到的图片文件
    result = ''
    for image_file in sorted_image_files:
        image = Image.open(image_file)
        preprocessed_image = preprocess_image(image)
        scaled_image = resize_image(preprocessed_image, scale_factor=2.0)
        custom_config = f'--psm 6 -l {lang}'
        text = pytesseract.image_to_string(scaled_image, config=custom_config)
        result = result + text + '\n'
    return result
    # return re.sub(r'[\s\n]', '', result)
