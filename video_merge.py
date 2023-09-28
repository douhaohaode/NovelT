
from moviepy.editor import *
import tools


def merge_video(video_folder_path, background_audio_name):
    # 获取文件夹中的所有视频文件并按文件名升序排序
    video_files = sorted([f for f in os.listdir(video_folder_path) if f.endswith(".mp4")])

    # 创建一个 VideoFileClip 列表，用于存储每个视频文件的 VideoFileClip
    video_clips = [VideoFileClip(os.path.join(video_folder_path, file)) for file in video_files]

    # 提取每个视频剪辑的音频部分，并将其存储在一个列表中
    audio_clips = [AudioFileClip(os.path.join(video_folder_path, file)) for file in video_files]

    # 使用 clips_array 函数将视频剪辑合成成一个视频
    final_video = concatenate_videoclips(video_clips, method="compose")

    # 使用 concatenate_audioclips 函数将音频剪辑连接在一起
    final_audio = concatenate_audioclips(audio_clips)


    # 集成背景音乐
    background_music = AudioFileClip(tools.background_audio(background_audio_name))

    if background_music.duration > final_video.duration or background_music.duration == final_video.duration:
        background_music = background_music.subclip(0, final_video.duration)
    else:
        # num_repeats = int(final_video.duration / background_music.duration) + 1
        # background_music = background_music.fx("audio_loop", n=num_repeats)
        background_music = afx.audio_loop(background_music, duration=final_audio.duration)

    video = CompositeVideoClip([final_video.set_audio(final_audio), final_video.set_audio(background_music.volumex(0.15))])

    # 将背景音乐添加到视频剪辑上
   # video_with_audio = final_video.set_audio(background_music)
    # 保存合成的视频
    output_file = tools.video_rename()
    video.write_videofile(output_file, codec="libx264", audio_codec="aac")
    return output_file

