from moviepy.editor import *
from moviepy.editor import AudioFileClip, CompositeVideoClip
import novel_tools
from tts import audio_process
import random
import constant
from PIL import ImageFont
import re
class VideoProcessor:
    def __init__(self, image_file=None, text=None, size=None, transform=None, audio_file=None
                 , voice=None, rate=None, volume=None, output=None, repair=False, corp=False, language=None
                 ):
        self.audio_file = audio_file
        self.image_file = image_file
        self.text = text
        self.size = size
        self.transform = transform
        self.voice = voice
        self.rate = rate
        self.volume = volume
        self.output = output
        self.repair = repair
        self.corp = corp
        self.language = language

        # 音频生成文件

    def audio_image_to_video(self, audio=None):

        def move_up(t):
            speed = 50
            y_position = -speed * t
            return (0, y_position)

        def move_down(t):
            speed = 50
            y_position = speed * t
            return (0, y_position)

        def move_left(t):
            speed = 50
            x_position = -speed * t
            return (x_position, 0)

        def move_right(t):
            speed = 50
            x_position = speed * t
            return (x_position, 0)

        def move_non(t):
            return (0, 0)

        def move_zoom(t, duration):
            start_scale = 1.05  # 初始大小
            end_scale = 1.2  # 目标大小
            return start_scale + (end_scale - start_scale) * t / duration

        if audio == None:
            audio = AudioFileClip(self.audio_file)
        # 根据 self.size 获取宽度和高度
        if self.size in constant.size_mapping:
            width, height = constant.size_mapping[self.size]
        else:
            width, height = 1920, 1080

        # 对image大小的处理
        transform_type = constant.transform_dict[self.transform]
        if transform_type is None:
            transform_type = random.choice(constant.transform_random_list)
        image_width = width
        image_height = height
        if transform_type == "left":
            image_width = width + 200
        if transform_type == "up":
            image_height = height + 200
        if transform_type == "zoom":
            image_height = height - 100
            image_width = width - 100

        # 图片处理
        image = novel_tools.resize_image(self.image_file, width, height, self.repair, self.corp).set_duration(audio.duration).resize(
            (image_width, image_height))

        if transform_type == "non":
            image = image.set_position(("center", "center")).set_position(move_non)
        if transform_type == "left":
            image = image.set_position(("center", "center")).set_position(move_left)
        if transform_type == "right":
            image = image.set_position(("center", "center")).set_position(move_right)
        if transform_type == "up":
            image = image.set_position(("center", "center")).set_position(move_up)
        if transform_type == "down":
            image = image.set_position(("center", "center")).set_position(move_down)
        if transform_type == "zoom":
            image = image.set_position(("center", "center")).fx(vfx.resize, lambda t: move_zoom(t, image.duration))

        #image = image.fadeout(0.1)  # 淡出

        text, sounds = novel_tools.text_process(self.text)
        # 字幕处理
        fade_duration = 0.5
        sentences = re.split(r'(?<=[.?!。？！，,])', text)
        sentences = [s.strip() for s in sentences if s.strip()]

        text_clips = []

        for c_text in sentences:
            rendering_text = remove_trailing_punctuation(c_text)
            text_clip = TextClip(rendering_text, font='./source/asset/Songti_1.ttc', fontsize=novel_tools.font_size(),
                            color='white', stroke_color="lightblue", bg_color="black", stroke_width=0.8)
            text_clip = text_clip.set_duration(test_time(self.text, c_text, audio.duration)).crossfadein(fade_duration).crossfadeout(fade_duration)
            text_clip = text_clip.set_position(("center", 0.84), relative=True)
            text_clips.append(text_clip)
            pass
        # 合成文本剪辑
        text_video = concatenate_videoclips(text_clips).set_position(("center", 0.84), relative=True)
        # 合成视频
        video = CompositeVideoClip([image.set_audio(audio), text_video], size=(width, height))
        output_file = novel_tools.video_rename()
        video.write_videofile(output_file, codec='libx264', audio_codec='aac', fps=40)

        # 关闭音频和视频
        image.close()
        audio.close()
        video.close()
        return output_file

    def text_image_to_video(self):
        audio_file_output = audio_process(self.text, self.voice, self.rate, self.volume, self.output, self.language)
        if audio_file_output == None:
            return
        audioFileClip = AudioFileClip(audio_file_output)
        output_file = self.audio_image_to_video(audioFileClip)
        return output_file


def test_time(text, c_text, duration):
    num_sentences = len(text)
    time_per_sentence = duration / num_sentences
    return time_per_sentence * len(c_text)
    pass


def remove_trailing_punctuation(text):
    # 使用正则表达式匹配末尾的标点符号（.?!。？！，,）
    pattern = r'[.?!。？！，,]+$'
    match = re.search(pattern, text)

    if match:
        # 如果找到匹配的标点符号，去掉它
        text = text[:match.start()]

    return text
