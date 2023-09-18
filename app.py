from audio import TTSProcessor
import asyncio
import gradio as gr

import os
import re
import pytesseract
from PIL import Image
import glob


voiceMap = {
    "潇潇": "zh-CN-XiaoxiaoNeural",
    "小艺": "zh-CN-XiaoyiNeural",
    "云健": "zh-CN-YunjianNeural",
    "云溪": "zh-CN-YunxiNeural",
    "云霞": "zh-CN-YunxiaNeural",
    "云烟": "zh-CN-YunyangNeural",
    "小贝": "zh-CN-liaoning-XiaobeiNeural",
    "小妮": "zh-CN-shaanxi-XiaoniNeural",
    "hiugaai": "zh-HK-HiuGaaiNeural",
    "hiumaan": "zh-HK-HiuMaanNeural",
    "wanlung": "zh-HK-WanLungNeural",
    "hsiaochen": "zh-TW-HsiaoChenNeural",
    "hsioayu": "zh-TW-HsiaoYuNeural",
    "yunjhe": "zh-TW-YunJheNeural",
}

voiceArray = ["潇潇",
              "小艺",
              "云健",
              "云溪",
              "云霞",
              "云烟",
              "小贝",
              "小妮",
              "hiugaai",
              "hiumaan",
              "wanlung",
              "hsiaochen",
              "hsioayu",
              "yunjhe"]


def redImage(image):
    # 使用Tesseract进行文字提取
    #result= pytesseract.image_to_string(image,)
    result= pytesseract.image_to_string(image, lang='chi_sim')
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

def process(text, voice, rate, volume, output):
    voice_name = voiceMap[voice]
    if rate is not None and rate > 0.0 :
        rate_float = "+" + str(rate) + "%"
    else:
        rate_float = "-" + str(rate) + "%"
    if volume is not None and volume > 0.0:
        volume_float = "+" + str(volume) + "%"
    else:
        volume_float = "-" + str(volume) + "%"
    output_path = output + ".mp3"
    tts_processor = TTSProcessor(text, voice_name, output_path, rate_float, volume_float)
    asyncio.run(tts_processor.text_to_speech())
    return output_path

with gr.Blocks(theme='freddyaboulton/dracula_revamped') as demo:
    gr.Markdown("图像识别")

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

    gr.Markdown("文本转音频")

    with gr.Row():
        inp1 = gr.Textbox(placeholder="输入要转换的文字?", label="文本")
        inp2 = gr.Radio(voiceArray, label="主播选择")
        with gr.Column():
           inp3 = gr.Slider(-50.0, 50.0, value=0.0, label="音速", info="加速-50到+50")
           inp4 = gr.Slider(-50.0, 50.0, value=0.0, label="音量", info="加速-50到+50")
        inp5 = gr.Textbox(placeholder="文件以及文件名称", label="文件名称")
        out = gr.Audio(label="生成的音频", type="filepath")
    btn = gr.Button("Run")
    btn.click(fn=process, inputs=[inp1, inp2, inp3, inp4, inp5], outputs=out)
    live = True  # 启用队列，允许后台运行处理函数并启用进度跟踪

demo.launch()
