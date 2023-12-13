from moviepy.editor import AudioFileClip, concatenate_audioclips
from constant import sound_path


# def sound_effect(file_name, output_path, sounds=[("手枪", 0, 2)], _text=""):
#     # 加载现有音频文件
#     existing_audio = AudioFileClip(output_path)
#     sounds_array = []
#     i = 0
#     for content, start, end, in sounds:
#         sound = AudioFileClip(sound_path + content[1:-1] + ".mp3")
#         print(len(_text))
#         if start == 0:
#             existing_audio = concatenate_audioclips([sound, existing_audio])
#         elif start - i == len(_text):
#             existing_audio = concatenate_audioclips([existing_audio, sound])
#         elif start + 1 == len(_text):
#             existing_audio = concatenate_audioclips([existing_audio, sound])
#         else:
#             sound_effect_start_time = existing_audio.duration / len(_text) * (start - i)
#             existing_audio = concatenate_audioclips([existing_audio.subclip(0, sound_effect_start_time), sound,
#                                                      existing_audio.subclip(sound_effect_start_time, None)])
#         i = i + len(content)
#         sounds_array.append(sound)
#
#     # 保存带有音效的新音频文件
#     existing_audio.write_audiofile(output_path)
#
#     # 关闭音频剪辑对象
#     existing_audio.close()
#     for s in sounds_array:
#         s.close()
#     return output_path


from pydub import AudioSegment

def sound_effect(file_name, output_path, sounds=[("手枪", 0, 2)], _text=""):

    audio = AudioSegment.from_file(output_path)
    i = 0
    for content, start, end in sounds:
        sound_effect = AudioSegment.from_file(sound_path + content[1:-1] + ".mp3")
        if start == 0:
            audio = sound_effect + audio
        elif start - i == len(_text):
            audio = audio + sound_effect
        elif start + 1 == len(_text):
            audio = audio + sound_effect
        else:
            desired_volume = -5
            sound_effect_volume = sound_effect.set_channels(2)
            sound_effect_volume = sound_effect_volume + desired_volume
            duration_seconds = len(audio) / 1000.0
            sound_effect_start_time = duration_seconds / len(_text) * (start - i)
            sound_effect_start_time = sound_effect_start_time * 1000.0
            audio = audio.overlay(sound_effect_volume, position=sound_effect_start_time)
        i = i + len(content)

    audio.export(output_path, format="mp3")
    return output_path
