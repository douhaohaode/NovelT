import os

import pytesseract
from PIL import Image
import glob
import constant


def red_image(image):
    # 使用Tesseract进行文字提取
    # result= pytesseract.image_to_string(image,)
    result = pytesseract.image_to_string(image, lang='chi_sim')
    return result
    # return re.sub(r'[\s\n]', '', result)
    # text = pytesseract.image_to_string(image, lang='jpn')
    # text = pytesseract.image_to_string(image, lang='kor')
    # text = pytesseract.image_to_string(image, lang='chi_sim')


def red_path(image_path):
    image_extensions = constant.image_extensions
    # 遍历文件夹中的图片文件
    image_files = []
    for extension in image_extensions:
        pattern = os.path.join(image_path, "*" + extension)
        image_files.extend(glob.glob(pattern))

    # 打印找到的图片文件
    result = ''
    for image_file in image_files:
        image = Image.open(image_file)
        text = pytesseract.image_to_string(image, lang='chi_sim')
        result = result + text
    # re.sub(r'[\s\n]', '', result)
    return result
