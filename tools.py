import os
import re
import time
from PIL import Image
from moviepy.editor import ImageClip
import real_gan


def path(path_name, type):
    directory = os.path.dirname(os.path.abspath(__file__))
    timestamp = int(time.time())
    file_path = f"source/{path_name}/{timestamp}.{type}"
    file_name = os.path.join(directory, file_path)
    return file_name


def video_rename():
    return path("video", "mp4")


def audio_rename():
    return path("audio", "mp3")


def image_rename():
    return path("image", "jpg")


def resize_image(image_path, w, h, repair=False):
    target_ratio = w / h
    # 打开图像
    image = Image.open(image_path)

    # 获取图像的原始宽度和高度
    original_width, original_height = image.size

    # 计算图像的原始宽高比和目标宽高比
    original_ratio = original_width / original_height

    # 计算剪裁后的目标尺寸
    if target_ratio > original_ratio:
        # 如果目标宽高比大于原始宽高比，需要剪裁左右边缘
        new_width = int(original_height * target_ratio)
        new_height = original_height
    else:
        # 如果目标宽高比小于原始宽高比，需要剪裁顶部和底部
        new_width = original_width
        new_height = int(original_width / target_ratio)

    # 计算剪裁的坐标位置（居中剪裁）
    left = (original_width - new_width) // 2
    top = (original_height - new_height) // 2
    right = (original_width + new_width) // 2
    bottom = (original_height + new_height) // 2

    # 执行剪裁
    cropped_image = image.crop((left, top, right, bottom))
    cropped_image = cropped_image.convert("RGB")
    new_image_path = image_rename()
    cropped_image.save(new_image_path)
    if repair == True:
        real_gan.inference_gan(new_image_path)
    image_clip = ImageClip(new_image_path)
    os.remove(new_image_path)
    return image_clip


def font_size():
    if 16 / 9:
        return 44
    if 4 / 3:
        return 36
    if 1 / 1:
        return 32
    if 16 / 9:
        return 44
    if 16 / 9:
        return 50
    if 32 / 9:
        return 50
    return 44

def background_audio(title):
    directory = os.path.dirname(os.path.abspath(__file__))
    file_path = f"source/asset/mp3/{title}.mp3"
    file_name = os.path.join(directory, file_path)
    return file_name



# 自定义排序函数，从文件名中提取数字并进行比较
def extract_number(filename):
    # 使用正则表达式从文件名中提取数字部分
    match = re.search(r'\d+', filename)
    if match:
        return int(match.group())
    else:
        return 0  # 如果文件名中没有数字，则返回0