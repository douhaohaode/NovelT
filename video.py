from moviepy.editor import *
from moviepy.editor import AudioFileClip, ImageClip, CompositeVideoClip
import tools
from tts import audio_process
import random

transform_list = ["non", "let", "right", "up", "down"]

size_mapping = {
    "16:9": (1920, 1080),
    "4:3": (1024, 768),
    "1:1": (800, 800),
    "9:16": (1080, 1920),
    "21:9": (2560, 1080),
    "32:9": (2560, 1080),
}

class VideoProcessor:
    def __init__(self, image_file=None, text=None, size=None, transform=None, audio_file=None
                 , voice=None, rate=None, volume=None, output=None
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

    #  变换核心代码
    #  >>> clip.set_position(lambda t: ('center', 50+t) )

        # 音频生成文件
    def audio_image_to_video(self, audio=None):

        if audio == None :
           audio = AudioFileClip(self.audio_file)
        # 根据 self.size 获取宽度和高度
        if self.size in size_mapping:
            width, height = size_mapping[self.size]
        else:
            width, height = 1920, 1080

        # 图片处理
        image = ImageClip(self.image_file)
        scale_width = width / image.size[0]
        scale_height = height / image.size[1]
        scale = min(scale_width, scale_height)
        image = image.resize((int(image.size[0] * scale), int(image.size[1] * scale)))  # 调整图像的大小，并将其放置在视频帧中间
        image = image.set_duration(audio.duration).resize((width, height))

        transform_type = self.transform

        if self.transform is None:
            transform_type = random.choice(["non", "up", "down", "left", "right"])
        move = getattr(self, f"move_{transform_type}", self.move_non())

        image = image.set_position(("center", "center")).set_position(move)
        image = image.fadeout(0.1)  # 淡出/淡入  image = image.fadein(1.0)

        # 字幕处理
        fade_duration = 0.5
        text = TextClip(self.text, font='./source/asset/Songti.ttc', fontsize=42, color='white')
        text = text.set_position(("center", 0.85), relative=True).set_duration(image.duration - 1)
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

        # 视频生成文件
    def text_image_to_video(self):
        audio_file_output = audio_process(self.text, self.voice, self.rate, self.volume, self.output)
        if audio_file_output == None:
            return
        audioFileClip = AudioFileClip(audio_file_output)
        output_file = self.audio_image_to_video(audioFileClip)
        return output_file









# from moviepy.editor import *
# from moviepy.editor import AudioFileClip, ImageClip, CompositeVideoClip
#
#
# # 指定音频文件和图片文件
# audio_file = "1.mp3"
# image_file = "1.jpg"
#
#
# var = 100
#
# def move_up(t):  # 向上移动
#     speed = 50  # 移动的速度（像素/秒）
#     y_position = -speed * t
#     return (0, y_position)
#
# def move_down(t):  # 向下移动
#     speed = 50  # 移动的速度（像素/秒）
#     y_position = speed * t
#     return (0, y_position)
#
#
# def move_left(t):  # 向左移动
#     speed = 50  # 移动的速度（像素/秒）
#     x_position = -speed * t
#     return (x_position, 0)
#
#
# def move_right(t):  # 向左移动
#     speed = 50  # 移动的速度（像素/秒）
#     x_position = speed * t
#     return (x_position, 0)
#
# def zoom_in(t): # 在播放时间内逐渐增加缩放比例
#     return 1 + 0.2 * t
#
#
# # 打开音频文件
# audio = AudioFileClip(audio_file)
# width, height = 1280, 720
#
#
# # 打开图片文件
# image = ImageClip(image_file)
# scale_width = width / image.size[0]
# scale_height = height / image.size[1]
# scale = min(scale_width, scale_height)
# image = image.resize((int(image.size[0] * scale), int(image.size[1] * scale))) # 调整图像的大小，并将其放置在视频帧中间
# image = image.set_duration(audio.duration).resize((width, height))
# image = image.set_position(("center", "center")).set_position(move_right)
# image = image.fadeout(0.2) # 淡出 淡入#image = image.fadein(1.0)
#
#
# # 计算渐变的持续时间
# fade_duration = 0.5
# fadein_start = 0
# fadein_end = fade_duration
# fadeout_start = audio.duration - fade_duration
# fadeout_end = audio.duration
# text = TextClip("莫名其妙的被穿越到异世界首先要学会什么", font='Songti.ttc', fontsize=36, color='white')
# text = text.set_position(("center", "bottom")).set_duration(image.duration - 1)
# # 设置文字剪辑的逐渐显示和逐渐消失效果
# text = text.set_duration(audio.duration).crossfadein(fade_duration).crossfadeout(fade_duration)
#
#
# # 合成视频，将图片、音频和文字进行配合
# video = CompositeVideoClip([image.set_audio(audio), text], size=(width, height))
# output_file = "output_video.mp4"
# video.write_videofile(output_file, codec='libx264', audio_codec='aac', fps=30)
#
#
# # 关闭音频和视频
# image.close()
# audio.close()
# video.close()
