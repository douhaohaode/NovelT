

voiceArray = ["芊芊",
              "君常笑",
              "李青阳",
              "马长老",
              "李家主",
              "系统",
              "老刀疤",
              "虎啸宗执事",
              "大刀帮长老",
              "群众",
              "吃瓜群众",
              "娇声公主二号",
              "温柔女主三号",
              "温柔女主四号",
              "管家",
              "苏锦",
              "女子",
              "子吟",
              "赵熙悦",
              "姚月",
              "韦一怒",
              "旁白",
              "路人甲"]


voice_map_en = {
    "JennyNeural": "en-US-JennyNeural",
    "GuyNeural": "en-US-GuyNeural",
    "AriaNeural": "en-US-AriaNeural",
    "DavisNeural": "en-US-DavisNeural",
    "ChristopherNeural": "en-US-ChristopherNeural",
    "EricNeural": "en-US-EricNeural",
    "MichelleNeural": "en-US-MichelleNeural",
    "RogerNeural": "en-US-RogerNeural",
    "SteffanNeural": "en-US-SteffanNeural",
}
voice_array_en = [
              "JennyNeural",
              "GuyNeural",
              "AriaNeural",
              "DavisNeural",
              "ChristopherNeural",
              "EricNeural",
              "MichelleNeural",
              "RogerNeural",
              "SteffanNeural",
            ]


size_mapping = {
    "16:9": (1920, 1080),
    "4:3": (1024, 768),
    "1:1": (800, 800),
    "9:16": (1080, 1920),
    "21:9": (2560, 1080),
    "32:9": (2560, 1080),
}

merge_array = ["今天星期天",
               "捡了200块钱",
               "准备去偷鸡",
               "被发现了",
               "壮烈激战",
               "挨了不少打",
               "跑了",
               "200块丢了明天星期一",
               ]

sizeArray = ["16:9", "4:3", "1:1", "9:16", "21:9", "32:9"]

transform_list = ["默认", "随机", "左移动", "上移动", "放大"]

transform_random_list = ["left", "up", "zoom"]

transform_dict = {"默认": "non", "随机": None, "左移动": "left", "上移动": "up", "放大": "zoom"}

image_extensions = (".jpg", ".jpeg", ".png", ".PNG")



title_sequence_list = ["None", "word", "video"]


finish = "完成"
pytesseract_title = "pytesseract"
image_title = "图片"
path_subtitle = "请输入路径"
path_title = "路径"
image_path_title = "图片路径"
text_path_title = "文本文件路径"
image_file_path_title = "图片文件路径"
tts_title = "文本转语音"
title_placeholder = "输入要转换的文字?"
text_title = "文本"
anchor_title = "主播"
voice_title = "音速"
voice_desc = "加速-50到+50"
volume_title = "音量"
volume_desc = "加速-50到+50"
file_placeholder_title = "文件以及文件名称"
file_title = "文件名称"
audio_title = "生成的音频"
generate_title = "生成"
video_title = "生成视频"
batch_title = "批量生成"
progress_title = "进度"
size_title = "选择尺寸"
transform_title = "图片特效"
cartoon_title = "卡通图片"
repair_title = "超清"
video_corp_title = "尺寸裁剪"
corp_title = "裁剪"
welcome_title = "欢迎使用NoveIT工具"
video_merge_title = "视频合成"
video_merge_file_title = "视频集合路径"
background_audio_title = "背景音乐"
sequence_label = "片头特效"
sequence_title = "片头文本"



audio_path = "./source/audio/"
video_path = "./source/video/"
effcet_path = "./source/effcet/"
sound_path = "./source/asset/sound/"