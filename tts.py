import edge_tts
import asyncio
import tools
import constant


def audio_process(text, voice, rate, volume, output=None):
    if text is None and voice is None and rate is None and volume is None:
        return None

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
        output_path = tools.audio_rename()
    else:
        output_path = output + ".mp3"
    tts_processor = TTSProcessor(text, voice_name, output_path, rate_float, volume_float)
    asyncio.run(tts_processor.text_to_speech())
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
