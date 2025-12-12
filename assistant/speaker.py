import pyttsx3
import multiprocessing as mp


def _tts_once(text: str, voice_id=None):
    engine = pyttsx3.init()
    engine.setProperty("rate", 175)
    if voice_id is not None:
        engine.setProperty("voice", voice_id)
    engine.say(text)
    engine.runAndWait()


class PyttsxSpeaker:
    def __init__(self):
        self.pool = mp.get_context("spawn").Pool(1)
        self.voice_id = None

    def list_voices(self):
        engine = pyttsx3.init()
        voices = engine.getProperty("voices")
        for i, v in enumerate(voices):
            print(f"{i}: {v.name} ({v.id})")
        return voices

    def set_voice(self, index: int):
        engine = pyttsx3.init()
        voices = engine.getProperty("voices")
        if 0 <= index < len(voices):
            self.voice_id = voices[index].id
            print(f"Голос изменён на: {voices[index].name}")
        else:
            print("Неверный индекс голоса!")

    def speak(self, text: str):
        self.pool.apply_async(_tts_once, (text, self.voice_id))

    def stop(self):
        self.pool.close()
        self.pool.join()
