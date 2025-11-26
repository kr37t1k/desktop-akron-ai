from stts.silero_tts import SileroTTS

class TTSModule(SileroTTS):
    def __init__(self):
        super().__init__(
        model_id="v3_en",
        language="en",
        speaker="en_5",
        sample_rate=48000,
        device="cpu",
        )

    def synth(self, text):
        self.tts(text, "temp.wav")
