import pygame
import time
from assistant.core import FileSystemCommand


class MusicCommand(FileSystemCommand):
    def __init__(self, music_dir: str, recognizer):
        super().__init__(base_dir=music_dir, name="музыка")
        self.help_text = ("Скажи 'включи музыку <название>', чтобы запустить трек. "
                          "Во время воспроизведения можно говорить названия других треков, "
                          "или 'пауза', 'продолжить', 'стоп'.")
        self.recognizer = recognizer
        pygame.mixer.init()

    def matches(self, text: str) -> bool:
        return "включи музыку" in text.lower()

    def execute(self, text: str, speaker) -> None:
        track_name = text.lower().replace("включи музыку", "").strip()
        if not track_name:
            speaker.speak("Скажи название трека")
            return

        file_path = self.find_file_by_name(track_name, extensions=(".mp3",))
        if not file_path:
            speaker.speak(f"Не нашла трек {track_name}")
            return

        self.play_track(file_path, speaker)

        while True:
            speaker.speak("Что дальше?")
            response = self.recognizer.recognize()

            if not response:
                continue
            response = response.lower()

            if response in ["стоп", "всё"]:
                speaker.speak("Останавливаю музыку")
                pygame.mixer.music.stop()
                break

            if response in ["пауза", "останови"]:
                pygame.mixer.music.pause()
                speaker.speak("Пауза. Скажи 'продолжить', чтобы возобновить.")
                continue

            if response in ["продолжить", "дальше"]:
                pygame.mixer.music.unpause()
                speaker.speak("Продолжаю воспроизведение.")
                continue

            next_track = self.find_file_by_name(response, extensions=(".mp3",))
            if not next_track:
                speaker.speak(f"Не нашла трек {response}")
                continue

            self.play_track(next_track, speaker)

    def play_track(self, file_path: str, speaker) -> None:
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.5)
