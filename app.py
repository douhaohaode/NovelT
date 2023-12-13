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


def video_process(inp1=None, inp2=None, inp3=None, inp4=None, inp6=None, inp7=None, inp8=None, inp9=None, inp14=None):
    repair = False
    if len(inp9) > 0:
        repair = True
    corp = False
    if len(inp14) > 0:
        corp = True
    video_processor = VideoProcessor(text=inp1, voice=inp2, image_file=inp6, size=inp7, transform=inp8, rate=inp3,
                                     volume=inp4, repair=repair, corp=corp)
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


with gr.Blocks(theme='freddyaboulton/dracula_revamped') as demo:
    gr.Markdown(f"### [NovelT](https://github.com/douhaohaode/NovelT)")

    with gr.Tab(constant.video_title):
        with gr.Row():
            inp1 = gr.Textbox(placeholder=constant.title_placeholder, label=constant.text_title,
                              value=constant.welcome_title)
            with gr.Column():
                inp6 = gr.Textbox(placeholder=constant.path_subtitle, label=constant.image_path_title,
                                  value='./source/image/1.jpg')
                inp7 = gr.Radio(constant.sizeArray, label=constant.size_title, value=constant.sizeArray[0])
                inp8 = gr.Radio(constant.transform_list, label=constant.transform_title,
                                value=constant.transform_list[0])
                with gr.Row():
                    inp9 = gr.CheckboxGroup([constant.repair_title], label=constant.cartoon_title)
                    inp14 = gr.CheckboxGroup([constant.corp_title], label=constant.video_corp_title)

        with gr.Row():
            with gr.Column():
                inp2 = gr.Radio(constant.voiceArray, label=constant.anchor_title, value=constant.voiceArray[0])
                inp3 = gr.Slider(-50.0, 50.0, value=0.0, label=constant.voice_title, info=constant.voice_desc)
                inp4 = gr.Slider(-50.0, 50.0, value=0.0, label=constant.volume_title, info=constant.volume_desc)
            video_file_path = gr.Video(label=constant.video_title, type="filepath")
        with gr.Row():
            video_btn = gr.Button(constant.generate_title)
            video_btn.click(fn=video_process, inputs=[inp1, inp2, inp3, inp4, inp6, inp7, inp8, inp9, inp14],
                            outputs=video_file_path)

    with gr.Tab(constant.batch_title):
        with gr.Row():
            inp10 = gr.Textbox(placeholder=constant.path_subtitle, label=constant.text_path_title,
                               value='./source/image/1.txt')
            inp11 = gr.Textbox(placeholder=constant.path_subtitle, label=constant.image_file_path_title,
                               value='./source/image/')
        with gr.Row():
            with gr.Row():
                inp2 = gr.Radio(constant.voiceArray, label=constant.anchor_title, value=constant.voiceArray[3])
                with gr.Column():
                    inp3 = gr.Slider(-50.0, 50.0, value=23.0, label=constant.voice_title, info=constant.voice_desc)
                    inp4 = gr.Slider(-50.0, 50.0, value=40.0, label=constant.volume_title, info=constant.volume_desc)
        with gr.Row():
            with gr.Row():
                inp7 = gr.Radio(constant.sizeArray, label=constant.size_title, value=constant.sizeArray[0])
                inp8 = gr.Radio(constant.transform_list, label=constant.transform_title,
                                value=constant.transform_list[1])
            with gr.Row():
                with gr.Row():
                    inp9 = gr.CheckboxGroup([constant.repair_title], label=constant.cartoon_title)
                    inp14 = gr.CheckboxGroup([constant.corp_title], label=constant.video_corp_title)
                with gr.Column():
                    inp15 = gr.Textbox(placeholder=constant.title_placeholder, label=constant.sequence_title,
                                       value=constant.welcome_title)
                    inp16 = gr.Radio(constant.title_sequence_list, label=constant.sequence_label,
                                     value=constant.title_sequence_list[0])

        with gr.Row():
            with gr.Column():
                inp12 = gr.Textbox(placeholder=constant.path_subtitle, label=constant.video_merge_file_title,
                                   value='./source/video/')
                inp13 = gr.Radio(constant.merge_array, label=constant.background_audio_title,
                                 value=constant.merge_array[6])

            merge__video_out = gr.Video(label=constant.video_title, type="filepath")

        with gr.Row():
            inp20 = gr.Textbox(placeholder=constant.path_subtitle, label="封面图路径",
                               value='')
            inp21 = gr.Textbox(label="标题1", value='打造最强宗门')
            inp22 = gr.Textbox(label="标题1", value='第一集')
            inp23 = gr.Textbox(label="标题1", value='弟子数十万 个个是妖孽')


        batch_video_btn = gr.Button(constant.generate_title)
        # batch_out = gr.Textbox(label=constant.progress_title)
        batch_video_btn.click(fn=batch_process,
                              inputs=[inp2, inp3, inp4, inp7, inp8, inp9, inp10, inp11, inp12, inp13, inp14, inp15,
                                      inp16, inp20, inp21, inp22, inp23],
                              outputs=merge__video_out)

        # merge__video_btn = gr.Button(constant.generate_title)
        # merge__video_btn.click(fn=merge_process, inputs=[inp12, inp13], outputs=merge__video_out)

demo.launch()
