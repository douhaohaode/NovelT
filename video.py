from moviepy.editor import *
from moviepy.editor import AudioFileClip, CompositeVideoClip
import tools
from tts import audio_process
import random
import constant


class VideoProcessor:
    def __init__(self, image_file=None, text=None, size=None, transform=None, audio_file=None
                 , voice=None, rate=None, volume=None, output=None, repair=False
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
            start_scale = 1.0  # 初始大小
            end_scale = 1.1  # 目标大小
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
            transform_type = random.choice(constant.transform_list)
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
        image = tools.resize_image(self.image_file, width, height, self.repair).set_duration(audio.duration).resize(
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

        image = image.fadeout(0.1)  # 淡出

        # 字幕处理
        fade_duration = 0.5
        text = TextClip(self.text, font='./source/asset/Songti.ttc', fontsize=tools.font_size(), color='white')
        text = text.set_position(("center", 0.84), relative=True).set_duration(image.duration - 1)
        text = text.set_duration(audio.duration).crossfadein(fade_duration).crossfadeout(fade_duration)

        # 合成视频
        video = CompositeVideoClip([image.set_audio(audio), text], size=(width, height))
        output_file = tools.video_rename()
        video.write_videofile(output_file, codec='libx264', audio_codec='aac', fps=30)

        # 关闭音频和视频
        image.close()
        audio.close()
        video.close()
        return output_file

    def text_image_to_video(self):
        audio_file_output = audio_process(self.text, self.voice, self.rate, self.volume, self.output)
        if audio_file_output == None:
            return
        audioFileClip = AudioFileClip(audio_file_output)
        output_file = self.audio_image_to_video(audioFileClip)
        return output_file
