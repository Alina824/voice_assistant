import queue
import sounddevice as sd
import vosk
import json
import numpy as np
import tempfile
import wave
import whisper


class VoskRecognizer:
    def __init__(self, model_path="model", samplerate=16000):
        self.model = vosk.Model(model_path)
        self.samplerate = samplerate
        self.q = queue.Queue()
        self.device = None

    def recognize(self) -> str:
        with sd.RawInputStream(samplerate=self.samplerate, blocksize=8000,
                               dtype="int16", channels=1, callback=self.callback):
            rec = vosk.KaldiRecognizer(self.model, self.samplerate)
            while True:
                data = self.q.get()
                if rec.AcceptWaveform(data):
                    result = json.loads(rec.Result())
                    return result.get("text", "").lower()

    def callback(self, indata, frames, time, status):
        if status:
            print(status)
        self.q.put(bytes(indata))


class WhisperRecognizer:
    def __init__(self, model_name="small", samplerate=16000):
        self.model = whisper.load_model(model_name)
        self.samplerate = samplerate
        self.channels = 1
        self.duration = 5

    def recognize(self) -> str:
        print("Запись...")
        audio = sd.rec(int(self.duration * self.samplerate),
                       samplerate=self.samplerate,
                       channels=self.channels,
                       dtype='int16')
        sd.wait()

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            filename = f.name
        with wave.open(filename, "wb") as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(2)
            wf.setframerate(self.samplerate)
            wf.writeframes(audio.tobytes())

        result = self.model.transcribe(filename, fp16=False, language="ru")
        return result["text"].strip().lower()
