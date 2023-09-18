import os
import re

import pytesseract
from PIL import Image
import glob
import gradio as gr


def redImage(image):
    # 使用Tesseract进行文字提取
    result= pytesseract.image_to_string(image,)
    # result= pytesseract.image_to_string(image, lang='chi_sim')
    return result
    # return re.sub(r'[\s\n]', '', result)
    # text = pytesseract.image_to_string(image, lang='jpn')
    # text = pytesseract.image_to_string(image, lang='kor')
    # text = pytesseract.image_to_string(image, lang='chi_sim')

def redPath(image_path):
    image_extensions = ["*.jpg", "*.jpeg", "*.png", ]
    # 遍历文件夹中的图片文件
    image_files = []
    for extension in image_extensions:
        pattern = os.path.join(image_path, extension)
        image_files.extend(glob.glob(pattern))

    # 打印找到的图片文件
    result = ''
    for image_file in image_files:
        image = Image.open(image_file)
        text = pytesseract.image_to_string(image, lang='chi_sim')
        result = result + text
    return re.sub(r'[\s\n]', '', result)


# text = redPath("/Users/wangjian/Desktop/110")
# cleaned_text = re.sub(r'[\s\n]', '', text)
# print(cleaned_text)

with gr.Blocks() as demo:
    gr.Markdown("# OCR工具")

    with gr.Row():
        inp1 = gr.Image(type="pil", label="图片")
        out1 = gr.Textbox(label="识别文字如下:")
    btn1 = gr.Button("开始ocr")
    btn1.click(fn=redImage, inputs=inp1, outputs=out1)

    with gr.Row():
        inp = gr.Textbox(placeholder="请输入路径", label="路径")
        out = gr.Textbox(label="识别文字如下:")
    btn = gr.Button("开始ocr")
    btn.click(fn=redPath, inputs=inp, outputs=out)



demo.launch()
