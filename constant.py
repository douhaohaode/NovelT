voiceMap = {
    "潇潇": "zh-CN-XiaoxiaoNeural",
    "小艺": "zh-CN-XiaoyiNeural",
    "云健": "zh-CN-YunjianNeural",
    "云溪": "zh-CN-YunxiNeural",
    "云霞": "zh-CN-YunxiaNeural",
    "云烟": "zh-CN-YunyangNeural",
    "小贝": "zh-CN-liaoning-XiaobeiNeural",
    "小妮": "zh-CN-shaanxi-XiaoniNeural",
    "hiugaai": "zh-HK-HiuGaaiNeural",
    "hiumaan": "zh-HK-HiuMaanNeural",
    "wanlung": "zh-HK-WanLungNeural",
    "hsiaochen": "zh-TW-HsiaoChenNeural",
    "hsioayu": "zh-TW-HsiaoYuNeural",
    "yunjhe": "zh-TW-YunJheNeural",
}

voiceArray = ["潇潇",
              "小艺",
              "云健",
              "云溪",
              "云霞",
              "云烟",
              "小贝",
              "小妮",
              "hiugaai",
              "hiumaan",
              "wanlung",
              "hsiaochen",
              "hsioayu",
              "yunjhe"]

size_mapping = {
    "16:9": (1920, 1080),
    "4:3": (1024, 768),
    "1:1": (800, 800),
    "9:16": (1080, 1920),
    "21:9": (2560, 1080),
    "32:9": (2560, 1080),
}

merge_array = ["准备去偷鸡",
               "200块丢了明天星期一"
               ]


# merge_array = ["今天星期天",
#                "捡了200块钱",
#                "准备去偷鸡",
#                "被发现了",
#                "壮烈激战",
#                "挨了不少打",
#                "还是被我跑了",
#                "200块丢了明天星期一"
#                ]

sizeArray = ["16:9", "4:3", "1:1", "9:16", "21:9", "32:9"]

transform_list = ["默认", "随机", "左移动", "上移动", "放大"]

transform_random_list = ["left", "up", "zoom"]

transform_dict = {"默认": "non", "随机": None, "左移动": "left", "上移动": "up", "放大": "zoom"}

image_extensions = (".jpg", ".jpeg", ".png")

finish = "完成"
ocr_title = "图像识别"
ocr_subtitle = "识别文字如下:"
oct_btn_title = "开始ocr"
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
welcome_title = "欢迎使用NoveIT工具"

video_merge_title = "视频合成"
video_merge_file_title = "视频集合路径"

background_audio_title = "背景音乐"
