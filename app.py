import os

import gradio as gr
import time

from cover import cover
from video import VideoProcessor
from tts import audio_process
import constant
import video_merge
import novel_tools
import video_effect_text
import video_effect_video
import random

def video_process(inp1=None, inp2=None, inp3=None, inp4=None, inp6=None, inp7=None, inp8=None, inp9=None, inp14=None):
    repair = False
    if len(inp9) > 0:
        repair = True
    corp = False
    if len(inp14) > 0:
        corp = True
    language = "zh"
    if inp2 in constant.voiceArray:
        language = "zh"
    if inp2 in constant.voice_array_en:
        language = "en"

    video_processor = VideoProcessor(text=inp1, voice=inp2, image_file=inp6, size=inp7, transform=inp8, rate=inp3,
                                     volume=inp4, repair=repair, corp=corp, language=language)
    file_path = video_processor.text_image_to_video()
    return file_path


def batch_process(inp2=None, inp3=None, inp4=None, inp7=None, inp8=None, inp9=None, inp10=None, inp11=None, inp12=None,
                  inp13=None, inp14=None, inp15=None, inp16=None ,inp20=None,inp21=None,inp22=None,inp23=None):
    if inp20 != None:
        cover(inp21, inp22, inp23 , inp20)
    with open(inp10, 'r') as text_file:
        lines = text_file.readlines()
        image_extensions = constant.image_extensions
        image_files = [file for file in os.listdir(inp11) if file.endswith(image_extensions)]
        image_files = sorted(image_files, key=novel_tools.extract_number)
        for line, image_file in zip(lines, image_files):
            line = line.strip()
            image_file_path = os.path.join(inp11, image_file)
            video_process(line, inp2, inp3, inp4, image_file_path, inp7, inp8, inp9, inp14)
        time.sleep(len(image_files))
        if inp15 in constant.size_mapping:
            width, height = constant.size_mapping[inp15]
        else:
            width, height = 1920, 1080

        if inp16 == "word":
            video_effect_text.text_effect(screensize=(width, height), text=inp15)
        elif inp16 == "video":
            video_effect_video.image_effect(screensize=(width, height), text=inp15)

        return video_merge.merge_video(inp12, inp13)


def merge_process(inp12=None, inp13=None):
    if inp12 == None and inp13 == None:
        return
    return video_merge.merge_video(inp12, inp13)


def text(index):
    int2 = gr.Textbox(label="文文言1违逆啊案", value=index)
    return int2

def text1(index):
    int2 = gr.Textbox(label="提示词是提示", value=index)
    return int2

def fake_gan(index):
    images = [
        (random.choice(
            [
                "http://www.marketingtool.online/en/face-generator/img/faces/avatar-1151ce9f4b2043de0d2e3b7826127998.jpg",
                "http://www.marketingtool.online/en/face-generator/img/faces/avatar-116b5e92936b766b7fdfc242649337f7.jpg",
                "http://www.marketingtool.online/en/face-generator/img/faces/avatar-1163530ca19b5cebe1b002b8ec67b6fc.jpg",
                "http://www.marketingtool.online/en/face-generator/img/faces/avatar-1116395d6e6a6581eef8b8038f4c8e55.jpg",
                "http://www.marketingtool.online/en/face-generator/img/faces/avatar-11319be65db395d0e8e6855d18ddcef0.jpg",
            ]
        ), f"label {i}")
        for i in range(3)
    ]
    return images


arra1 = ["101","201","3","4","5","6","7","8","9","10","11","12","13"]


def gallery(index):
    gallery = gr.Gallery(
        label="Generated images", show_label=False, elem_id=("gallery" + index)
        , columns=[3], rows=[1], object_fit="contain",  height=250 ) #height="auto",

    def my_select(evt: gr.SelectData):
        print(f"You selected {evt.value} at {evt.index} from {evt.target} and index {index}")
        print("调用了方法")

    gallery.select(my_select)
    return gallery




with gr.Blocks(theme='freddyaboulton/dracula_revamped') as demo:
    gr.Markdown(f"### [NovelT](https://github.com/douhaohaode/NovelT)")

    with gr.Tab("文案与图片"):
        with gr.Column():
             for a in arra1:
                 with gr.Row():
                    text(a)
                    text1(a)
                    g = gallery(a)
                    btn22 = gr.Button("Generate images", scale=0)
                    btn22.click(fn = fake_gan ,inputs = None , outputs = g)
                    # merge__video_btn.click(fn=merge_process, inputs=[inp12, inp13], outputs=merge__video_out)

    with gr.Tab(constant.video_title):
        with gr.Row():
            inp1 = gr.Textbox(placeholder=constant.title_placeholder, label=constant.text_title,
                              value=constant.welcome_title)
            with gr.Column():
                inp6 = gr.Textbox(placeholder=constant.path_subtitle, label=constant.image_path_title,
                                  value='./source/image/1.jpg')
        with gr.Row():
            with gr.Column():
                inp7 = gr.Radio(constant.sizeArray, label=constant.size_title, value=constant.sizeArray[0])
                inp8 = gr.Radio(constant.transform_list, label=constant.transform_title,
                            value=constant.transform_list[0])
            with gr.Row():
                with gr.Column():
                    inp3 = gr.Slider(-50.0, 50.0, value=0.0, label=constant.voice_title, info=constant.voice_desc)
                    inp4 = gr.Slider(-50.0, 50.0, value=0.0, label=constant.volume_title, info=constant.volume_desc)
                with gr.Column():
                    inp9 = gr.CheckboxGroup([constant.repair_title], label=constant.cartoon_title)
                    inp14 = gr.CheckboxGroup([constant.corp_title], label=constant.video_corp_title)
        # with gr.Row():
        #     with gr.Column():
        #         inp3 = gr.Slider(-50.0, 50.0, value=0.0, label=constant.voice_title, info=constant.voice_desc)
        #         inp4 = gr.Slider(-50.0, 50.0, value=0.0, label=constant.volume_title, info=constant.volume_desc)
        #         inp14 = gr.CheckboxGroup([constant.corp_title], label=constant.video_corp_title)

        with gr.Row():
            video_file_path = gr.Video(label=constant.video_title, type="filepath")

            with gr.Tab("中文"):
                inp_zh = gr.Radio(constant.voiceArray, label=constant.anchor_title,
                                  value=constant.voiceArray[0])
                video_btn = gr.Button(constant.generate_title)
                video_btn.click(fn=video_process, inputs=[inp1, inp_zh, inp3, inp4, inp6, inp7, inp8, inp9, inp14],
                                outputs=video_file_path)

            with gr.Tab("英文"):
                inp_en = gr.Radio(constant.voice_array_en, label=constant.anchor_title,
                                  value=constant.voice_array_en[0])
                video_btn = gr.Button(constant.generate_title)
                video_btn.click(fn=video_process, inputs=[inp1, inp_en, inp3, inp4, inp6, inp7, inp8, inp9, inp14],
                                outputs=video_file_path)

    with gr.Tab(constant.batch_title):
        with gr.Row():
            inp10 = gr.Textbox(placeholder=constant.path_subtitle, label=constant.text_path_title,
                               value='./source/image/1.txt')
            inp11 = gr.Textbox(placeholder=constant.path_subtitle, label=constant.image_file_path_title,
                               value='./source/image/')
        with gr.Row():
            with gr.Row():
                with gr.Column():
                    inp3 = gr.Slider(-50.0, 50.0, value=23.0, label=constant.voice_title, info=constant.voice_desc)
                    inp4 = gr.Slider(-50.0, 50.0, value=40.0, label=constant.volume_title, info=constant.volume_desc)

                with gr.Column():
                    inp7 = gr.Radio(constant.sizeArray, label=constant.size_title, value=constant.sizeArray[0])
                    inp8 = gr.Radio(constant.transform_list, label=constant.transform_title,
                                value=constant.transform_list[1])

        with gr.Row():
            with gr.Row():
                with gr.Column():
                    inp12 = gr.Textbox(placeholder=constant.path_subtitle, label=constant.video_merge_file_title,
                                       value='./source/video/')
                    inp13 = gr.Radio(constant.merge_array, label=constant.background_audio_title,
                                     value=constant.merge_array[6])
                with gr.Column():
                    inp9 = gr.CheckboxGroup([constant.repair_title], label=constant.cartoon_title)
                    inp14 = gr.CheckboxGroup([constant.corp_title], label=constant.video_corp_title)

                # with gr.Column():
                #     inp15 = gr.Textbox(placeholder=constant.title_placeholder, label=constant.sequence_title,
                #                        value=constant.welcome_title)
                #     inp16 = gr.Radio(constant.title_sequence_list, label=constant.sequence_label,
                #                      value=constant.title_sequence_list[0])

        with gr.Row():
            merge__video_out = gr.Video(label=constant.video_title, type="filepath")

            with gr.Tab("中文"):
                with gr.Column():
                    inp_zh = gr.Radio(constant.voiceArray, label=constant.anchor_title,
                                      value=constant.voiceArray[0])
                    batch_video_btn = gr.Button(constant.generate_title)
                    batch_video_btn.click(fn=batch_process,
                                          inputs=[inp_zh, inp3, inp4, inp7, inp8, inp9, inp10, inp11, inp12, inp13, inp14],
                                          outputs=merge__video_out)
            with gr.Tab("英文"):
                with gr.Column():
                    inp_en = gr.Radio(constant.voice_array_en, label=constant.anchor_title,
                                      value=constant.voice_array_en[0])
                    batch_video_btn = gr.Button(constant.generate_title)
                    batch_video_btn.click(fn=batch_process,
                                          inputs=[inp_en, inp3, inp4, inp7, inp8, inp9, inp10, inp11, inp12, inp13, inp14],
                                          outputs=merge__video_out)

demo.launch()
