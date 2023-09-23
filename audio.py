import edge_tts


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
