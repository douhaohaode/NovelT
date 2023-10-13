import novel_tools
from moviepy.editor import *
import random


def add_white_border(clip, border_width):
    w, h = clip.size
    color = random.randint(0, 255)
    border_color = (color, color, color)
    white_bg = ColorClip((w + 2 * border_width, h + 2 * border_width), color=border_color)
    final_clip = CompositeVideoClip(
        [white_bg.set_duration(clip.duration), clip.set_position((border_width, border_width))])
    return final_clip


def image_effect(screensize=(1920, 1080), text="穿越到异世界首先要学会什么"):
    w, h = screensize

    effcet_folder = "./source/video"
    file_list = os.listdir(effcet_folder)

    mp4_files = [file for file in file_list if file.endswith(".mp4")]
    first_six_mp4_files = [os.path.join(effcet_folder, file) for file in mp4_files[:7]]

    clips = [VideoFileClip(n, audio=False).subclip(1, 5) for n in
             first_six_mp4_files]

    sizes = [(w, h),
             (w / 3, h / 3),
             (w / 3.5, h / 3.5),
             (w / 4, h / 4),
             (w / 4, h / 4),
             (w / 3.5, h / 3.5),
             (w / 3, h / 3)]

    center_x, center_y = w // 2 - w / 6, h // 2 - h / 6

    spacing = h / 12

    regions = [(0, 0),
               (int(center_x - sizes[1][0] // 2 - spacing), int(center_y - sizes[1][1] // 2 - spacing)),
               (int(center_x + sizes[1][0] // 2 + spacing), int(center_y - sizes[1][1] // 2 - spacing)),
               (-50, center_y + spacing),
               (w - w / 3.5, center_y),  # Right
               (int(center_x - sizes[2][0] // 2 - spacing), int(center_y + sizes[2][1] // 2 + 2 * spacing)),
               (int(center_x + sizes[3][0] // 2 + spacing), int(center_y + sizes[3][1] // 2 + 2 * spacing))]

    comp_clips = []

    for c, s, r in zip(clips, sizes, regions):
        c = c.resize(s)
        bordered_clip = add_white_border(c, 10)
        comp_clips.append(bordered_clip.set_position(r))

    txtClip = TextClip(text, color='yellow', font='./source/asset/Songti.ttc',
                       kerning=5, fontsize=60).set_duration(2.5)

    comp_clips.append(txtClip.set_pos('center'))

    cc = CompositeVideoClip(comp_clips, size=screensize).set_duration(5)

    # 集成背景音乐
    background_music = AudioFileClip(novel_tools.background_audio('准备去偷鸡'))

    if background_music.duration > 5 or background_music.duration == 5:
        background_music = background_music.subclip(0, 5)
    else:
        background_music = afx.audio_loop(background_music, duration=5)

    background_music = background_music.volumex(0.5)
    cc = cc.set_audio(background_music)

    output_file = "./source/effcet/effect_video.mp4"

    cc.write_videofile(output_file, fps=30, codec='libx264', audio_codec="aac")
