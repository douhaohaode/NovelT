import os
import time


def path(path_name,type):
    directory = os.path.dirname(os.path.abspath(__file__))
    timestamp = int(time.time())
    file_path =  f"source/{path_name}/{timestamp}.{type}"
    file_name = os.path.join(directory, file_path)
    return file_name

def video_rename():
    return path("video", "mp4")


def audio_rename():
    return path("audio", "mp3")


def image_rename():
    return path("image", "jpg")
