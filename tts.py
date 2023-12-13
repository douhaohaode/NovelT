import edge_tts
import asyncio
import novel_tools
import constant
from sound_effect import sound_effect


def audio_process(_text, voice, rate, volume, output=None):
    if _text is None and voice is None and rate is None and volume is None:
        return None
    text, sounds = novel_tools.text_process(_text)
    ####### 多人语音处理代码
    # split_result = text.split(':')
    # if len(split_result) == 2:
    #     voice, text = split_result
    for v in constant.voiceArray:
        if text.startswith(v + ":"):
            split_result = text.split(v + ":")
            if len(split_result) == 2:
                text = split_result[1]
                voice = v
                break
   ####### 多人语音处理代码

    voice_name = constant.voiceMap[voice]

    if rate is not None and rate > 0.0:
        rate_float = "+" + str(rate) + "%"
    else:
        rate_float = "-" + str(rate) + "%"
    if volume is not None and volume > 0.0:
        volume_float = "+" + str(volume) + "%"
    else:
        volume_float = "-" + str(volume) + "%"

    if output == None or output == "":
        output_path = novel_tools.audio_rename()
    else:
        output_path = output + ".mp3"

    ####### 多人语音处理代码
    # if voice != "云溪":
    #     rate_float = "+" + str(volume-10) + "%"
    ####### 多人语音处理代码

    tts_processor = TTSProcessor(text, voice_name, output_path, rate_float, volume_float)
    asyncio.run(tts_processor.text_to_speech())
    print(text)
    print(sounds)

    if len(sounds) > 0:
        return sound_effect(output, output_path, sounds, text)

    return output_path




class TTSProcessor:
    def __init__(self, text, voice, output, rate, volume):
        self.text = text
        self.voice = voice
        self.output = output
        self.rate = rate
        self.volume = volume

    async def text_to_speech(self):
        tts = edge_tts.Communicate(text=self.text, voice=self.voice, rate=self.rate, volume=self.volume)
        await tts.save(self.output)
