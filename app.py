import os
import gradio as gr
import ocr

from video import VideoProcessor
from tts import audio_process
import constant
import video_merge

def video_process(inp1=None, inp2=None, inp3=None, inp4=None, inp6=None, inp7=None, inp8=None, inp9=None):
    repair = False
    if len(inp9) > 0:
        repair = True
    video_processor = VideoProcessor(text=inp1, voice=inp2, image_file=inp6, size=inp7, transform=inp8, rate=inp3,
                                     volume=inp4, repair=repair)
    file_path = video_processor.text_image_to_video()
    return file_path


def batch_process(inp2=None, inp3=None, inp4=None, inp7=None, inp8=None, inp9=None, inp10=None, inp11=None):
    with open(inp10, 'r') as text_file:
        lines = text_file.readlines()
        image_extensions = constant.image_extensions
        image_files = [file for file in os.listdir(inp11) if file.endswith(image_extensions)]
        sorted_image_files = sorted(image_files)

        for line, image_file in zip(lines, sorted_image_files):
            line = line.strip()
            image_file_path = os.path.join(inp11, image_file)
            print(line)
            print(image_file_path)
            video_process(line, inp2, inp3, inp4, image_file_path, inp7, inp8, inp9)
        return constant.finish


def merge_process(inp12=None, inp13=None):
     if inp12==None and inp13==None :
         return
     return video_merge.merge_video(inp12, inp13)


with gr.Blocks(theme='freddyaboulton/dracula_revamped') as demo:
    gr.Markdown(f"### [NovelT](https://github.com/douhaohaode/NovelT)")
    with gr.Tab(constant.ocr_title):
        with gr.Row():
            inp_pil = gr.Image(type="pil", label=constant.image_title)
            out_text = gr.Textbox(label=constant.ocr_subtitle)
        btn1 = gr.Button(constant.oct_btn_title)
        btn1.click(fn=ocr.red_image, inputs=inp_pil, outputs=out_text)

        with gr.Row():
            inp = gr.Textbox(placeholder=constant.path_title, label=constant.path_title)
            out = gr.Textbox(label=constant.ocr_subtitle,max_lines=9999)
        btn = gr.Button(constant.oct_btn_title)
        btn.click(fn=ocr.red_path, inputs=inp, outputs=out)

    with gr.Tab(constant.tts_title):
        with gr.Row():
            inp1 = gr.Textbox(placeholder=constant.title_placeholder, label=constant.text_title)
            inp2 = gr.Radio(constant.voiceArray, label=constant.anchor_title)
            with gr.Column():
                inp3 = gr.Slider(-50.0, 50.0, value=0.0, label=constant.voice_title, info=constant.voice_desc)
                inp4 = gr.Slider(-50.0, 50.0, value=0.0, label=constant.volume_title, info=constant.volume_desc)
            inp5 = gr.Textbox(placeholder=constant.file_placeholder_title, label=constant.file_title)
            out = gr.Audio(label=constant.audio_title, type="filepath")
        btn = gr.Button(constant.generate_title)
        btn.click(fn=audio_process, inputs=[inp1, inp2, inp3, inp4, inp5], outputs=out)
        live = True

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
                inp9 = gr.CheckboxGroup([constant.repair_title], label=constant.cartoon_title)
        with gr.Row():
            with gr.Column():
                inp2 = gr.Radio(constant.voiceArray, label=constant.anchor_title, value=constant.voiceArray[0])
                inp3 = gr.Slider(-50.0, 50.0, value=0.0, label=constant.voice_title, info=constant.voice_desc)
                inp4 = gr.Slider(-50.0, 50.0, value=0.0, label=constant.volume_title, info=constant.volume_desc)
            video_file_path = gr.Video(label=constant.video_title, type="filepath")
        with gr.Row():
            video_btn = gr.Button(constant.generate_title)
            video_btn.click(fn=video_process, inputs=[inp1, inp2, inp3, inp4, inp6, inp7, inp8, inp9],
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
                    inp3 = gr.Slider(-50.0, 50.0, value=22.0, label=constant.voice_title, info=constant.voice_desc)
                    inp4 = gr.Slider(-50.0, 50.0, value=20.0, label=constant.volume_title, info=constant.volume_desc)
        with gr.Row():
            with gr.Row():
                inp7 = gr.Radio(constant.sizeArray, label=constant.size_title, value=constant.sizeArray[0])
                inp8 = gr.Radio(constant.transform_list, label=constant.transform_title,
                                value=constant.transform_list[1])
            inp9 = gr.CheckboxGroup([constant.repair_title], label=constant.cartoon_title)
        batch_video_btn = gr.Button(constant.generate_title)
        batch_out = gr.Textbox(label=constant.progress_title)
        batch_video_btn.click(fn=batch_process, inputs=[inp2, inp3, inp4, inp7, inp8, inp9, inp10, inp11],
                              outputs=batch_out)

        with gr.Row():
            with gr.Column():
                inp12 = gr.Textbox(placeholder=constant.path_subtitle, label=constant.video_merge_file_title,
                                   value='./source/video/')
                inp13 = gr.Radio(constant.merge_array, label=constant.background_audio_title,
                                 value=constant.merge_array[6])

            merge__video_out = gr.Video(label=constant.video_title, type="filepath")

        merge__video_btn = gr.Button(constant.generate_title)
        merge__video_btn.click(fn=merge_process, inputs=[inp12, inp13], outputs=merge__video_out)

demo.launch()
