import vosk
import sounddevice as sd
import queue
import json

class STTModule:
    def __init__(self):
        self.model = vosk.Model("../voice/en-us-0.22-lgraph") # Take the models from kr37t1k/deepseekakronvoice or from http://alphacephei.com/
        print('Speech-to-text module initialized.')
        self.samplerate = 16000
        self.audio_queue = queue.Queue()
        self.enabled = False
    def _callback(self, indata, frames, time, status):
        if status:
            print(f"Audio status: {status}")
        self.audio_queue.put(bytes(indata))

    def stop(self):
        self.enabled = False
        print("STT Module state disabled now.")
    def start(self):
        self.enabled = True
        print("STT Module state enabled now.")
    def recognize(self):
        with sd.RawInputStream(
                samplerate=self.samplerate,
                blocksize=8000,
                dtype='int16',
                channels=1,
                callback=self._callback
        ):
            recognizer = vosk.KaldiRecognizer(self.model, self.samplerate)
            try:
                while not self.enabled: pass
                while self.enabled:
                    data = self.audio_queue.get()

                    if recognizer.AcceptWaveform(data):
                        result = json.loads(recognizer.Result())
                        text = result.get('text', '').strip()

                        if text:
                            print(f"🎤 You: {text}")
                            return text
                        else:
                            return ""
            except KeyboardInterrupt:
                self.stop()
                exit()
