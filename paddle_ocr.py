from paddleocr import PaddleOCR

import cv2
import numpy as np
import constant

import os
from PIL import Image
import glob
from collections import OrderedDict

ocr = PaddleOCR()


def process_text(result, n='\n'):
    text = ""
    if result and result[0]:
        for re in result[0]:
            text = text + re[1][0] + n
    print(text)
    return text


def red_image(image):
    image_np = np.array(image)
    return process_text(ocr.ocr(image_np))


def red_path(image_path):
    # 遍历文件夹中的图片文件
    image_files = []
    image_extensions = constant.image_extensions
    for extension in image_extensions:
        pattern = os.path.join(image_path, "*" + extension)
        image_files.extend(glob.glob(pattern))

    sorted_image_files = sorted(image_files)
    # 打印找到的图片文件
    result_text = ''
    for image_file in sorted_image_files:
        image_np = np.array(Image.open(image_file))
        text = process_text(ocr.ocr(image_np))
        result_text = result_text + text
    return result_text


def red_voide(video):
    cap = cv2.VideoCapture(video)

    video_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # 设置底部区域的坐标
    y_start = video_height - 200
    y_end = video_height

    frame_skip = 60  # 每隔30帧处理一次
    frame_count = 0

    result_text_dict = OrderedDict()

    while True:
        ret, frame = cap.read()

        if not ret:
            break
        frame_count += 1
        # 跳过指定数量的帧
        if frame_count % frame_skip != 0:
            continue
            # 截取底部区域
        bottom_area = frame[y_start:y_end, :]
        image_np = np.array(bottom_area)
        text = process_text(ocr.ocr(image_np), '')
        if text not in result_text_dict:
            result_text_dict[text] = None
    cap.release()
    cv2.destroyAllWindows()
    result_text = '\n'.join(result_text_dict.keys())
    return result_text
