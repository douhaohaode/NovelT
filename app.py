import os
import re
import pytesseract
from PIL import Image
import glob
import gradio as gr

from video import VideoProcessor
from tts import audio_process
import constant

def red_image(image):
    result = pytesseract.image_to_string(image, lang='chi_sim')
    return re.sub(r'[\s\n]', '', result)
    # return re.sub(r'[\s\n]', '', result)
    # text = pytesseract.image_to_string(image, lang='jpn')
    # text = pytesseract.image_to_string(image, lang='kor')
    # text = pytesseract.image_to_string(image, lang='chi_sim')


def red_path(image_path):
    image_extensions = ["*.jpg", "*.jpeg", "*.png", ]
    image_files = []
    for extension in image_extensions:
        pattern = os.path.join(image_path, extension)
        image_files.extend(glob.glob(pattern))

    result = ''
    for image_file in image_files:
        image = Image.open(image_file)
        text = pytesseract.image_to_string(image, lang='chi_sim')
        result = result + text
    return re.sub(r'[\s\n]', '', result)


def generate(inp1=None, inp2=None, inp3=None, inp4=None, inp6=None, inp7=None, inp8=None):
    # 1.输入要转换的文字 2.主播选择 3.音速 4. 音量 5.文件路径以及文件名称 6.图片路径 7.选择尺寸 8.图片特效
    video_processor = VideoProcessor(text=inp1, voice=inp2, image_file=inp6, size=inp7, transform=inp8, rate=inp3,
                                     volume=inp4)
    file_path = video_processor.text_image_to_video()
    return file_path


with gr.Blocks(theme='freddyaboulton/dracula_revamped') as demo:
    with gr.Tab("图像识别"):
        gr.Markdown("图像识别")
        with gr.Row():
            inp_pil = gr.Image(type="pil", label="图片")
            out_text = gr.Textbox(label="识别文字如下:")
        btn1 = gr.Button("开始ocr")
        btn1.click(fn=red_image, inputs=inp_pil, outputs=out_text)

        with gr.Row():
            inp = gr.Textbox(placeholder="请输入路径", label="路径")
            out = gr.Textbox(label="识别文字如下:")
        btn = gr.Button("开始ocr")
        btn.click(fn=red_path, inputs=inp, outputs=out)

    with gr.Tab("文本转语音"):
        gr.Markdown("文本转音频")
        with gr.Row():
            inp1 = gr.Textbox(placeholder="输入要转换的文字?", label="文本")
            inp2 = gr.Radio(constant.voiceArray, label="主播选择")
            with gr.Column():
                inp3 = gr.Slider(-50.0, 50.0, value=0.0, label="音速", info="加速-50到+50")
                inp4 = gr.Slider(-50.0, 50.0, value=0.0, label="音量", info="加速-50到+50")
            inp5 = gr.Textbox(placeholder="文件以及文件名称", label="文件名称")
            out = gr.Audio(label="生成的音频", type="filepath")
        btn = gr.Button("Run")
        btn.click(fn=audio_process, inputs=[inp1, inp2, inp3, inp4, inp5], outputs=out)
        live = True  # 启用队列，允许后台运行处理函数并启用进度跟踪

    with gr.Tab("生成视频"):
        with gr.Row():
            inp1 = gr.Textbox(placeholder="输入要转换的文字?", label="文本", value="欢迎使用NoveIT工具")
            with gr.Column():
                inp6 = gr.Textbox(placeholder="请输入路径", label="图片路径", value='./source/image/1.jpg')
                inp7 = gr.Radio(constant.sizeArray, label="选择尺寸", value=constant.sizeArray[0])
                inp8 = gr.Radio(constant.transform_list, label="图片特效", value=constant.transform_list[0])
        with gr.Row():
            with gr.Column():
                inp2 = gr.Radio(constant.voiceArray, label="主播选择", value=constant.voiceArray[0])
                inp3 = gr.Slider(-50.0, 50.0, value=0.0, label="音速", info="加速-50到+50")
                inp4 = gr.Slider(-50.0, 50.0, value=0.0, label="音量", info="加速-50到+50")
            video_file_path = gr.Video(label="生成的视频", type="filepath")
        with gr.Row():
            video_btn = gr.Button("Run")
            video_btn.click(fn=generate, inputs=[inp1, inp2, inp3, inp4, inp6, inp7, inp8], outputs=video_file_path)
    with gr.Tab("一键生成"):
        gr.Markdown("一键生成")

demo.launch()
