import numpy as np

from moviepy.editor import *
from moviepy.video.tools.segmenting import findObjects

import novel_tools

rotMatrix = lambda a: np.array([[np.cos(a), np.sin(a)],
                                [-np.sin(a), np.cos(a)]])


def vortex(screenpos, i, nletters):
    d = lambda t: 1.0 / (0.3 + t ** 8)  # damping
    a = i * np.pi / nletters  # angle of the movement
    v = rotMatrix(a).dot([-1, 0])
    if i % 2: v[1] = -v[1]
    return lambda t: screenpos + 400 * d(t) * rotMatrix(0.5 * d(t) * a).dot(v)


def cascade(screenpos, i, nletters):
    v = np.array([0, -1])
    d = lambda t: 1 if t < 0 else abs(np.sinc(t) / (1 + t ** 4))
    return lambda t: screenpos + v * 400 * d(t - 0.20 * i)

def arrive(screenpos, i, nletters):
    v = np.array([-1, 0])
    d = lambda t: max(0, 3 - 3 * t)
    return lambda t: screenpos - 400 * v * d(t - 0.2 * i)


def vortexout(screenpos, i, nletters):
    d = lambda t: max(0, t)  # damping
    a = i * np.pi / nletters  # angle of the movement
    v = rotMatrix(a).dot([-1, 0])
    if i % 2: v[1] = -v[1]
    return lambda t: screenpos + 400 * d(t - 0.1 * i) * rotMatrix(-0.2 * d(t) * a).dot(v)

def moveLetters(letters, funcpos):
    return [letter.set_pos(funcpos(letter.screenpos, i, len(letters)))
            for i, letter in enumerate(letters)]


def text_effect(screensize=(1920, 1080), text="修行苦练掌握强大的力量"):

    # 穿越异不世界当王者
    txtClip = TextClip(text, color="yellow",
                             kerning= 15 , font='./source/asset/Songti.ttc', fontsize=35)

    cvc = CompositeVideoClip([txtClip.set_pos('center')],size=screensize)

    letters = findObjects(cvc)  # a list of ImageClips

    final_clip = CompositeVideoClip(moveLetters(letters, cascade), size=screensize).set_duration(5)


    background_music = AudioFileClip(novel_tools.background_audio('准备去偷鸡'))

    if background_music.duration > final_clip.duration or background_music.duration == final_clip.duration:
        background_music = background_music.subclip(0, final_clip.duration)
    else:
        background_music = afx.audio_loop(background_music, duration=final_clip.duration)

    output_file = "./source/effcet/effect_video.mp4"

    video = CompositeVideoClip([final_clip.set_audio(background_music.volumex(0.5))])

    video.write_videofile(output_file, fps=30, codec='libx264', audio_codec="aac")

    return output_file
