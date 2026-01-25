import subprocess
import shutil
import socket

from assistant.core import FileSystemCommand
from utils.numeric import words_to_numbers


class CartoonCommand(FileSystemCommand):
    def __init__(self, videos_dir="D:/User/Videos", recognizer=None, speaker=None):
        super().__init__(base_dir=videos_dir, name="мультфильм")
        self.proc = None
        self.sock = None
        self.recognizer = recognizer
        self.speaker = speaker

        self.current_cartoon = None
        self.current_season = None
        self.current_index = None
        self.current_files = []

    def matches(self, text: str) -> bool:
        return any(word in text for word in (
            "мультфильм", "мультик", "сезон", "серия",
            "стоп", "пауза", "продолжи", "продолжить",
            "следующая", "предыдущая"
        ))

    def execute(self, text: str, speaker=None):
        self.handle(text)

    def _start_vlc(self):
        if shutil.which("vlc") is None:
            if self.speaker:
                self.speaker.speak("VLC не найден в PATH.")
            return False

        self.proc = subprocess.Popen(
            [
                "vlc",
                "--intf", "dummy",
                "--extraintf", "rc",
                "--rc-host", "127.0.0.1:4212",
                "--quiet",
            ],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect(("127.0.0.1", 4212))
            return True
        except Exception as e:
            print("Ошибка подключения к VLC:", e)
            if self.speaker:
                self.speaker.speak("Не удалось подключиться к VLC.")
            return False

    def _send_cmd(self, cmd: str):
        if not self.sock:
            return None
        try:
            self.sock.sendall((cmd + "\n").encode("utf-8"))
            data = self.sock.recv(4096).decode("utf-8", errors="ignore")
            print(f"VLC << {cmd}")
            print(f"VLC >> {data.strip()}")
            return data
        except Exception as e:
            print("Ошибка управления VLC:", e)
            return None

    def _stop_vlc(self):
        if self.sock:
            try:
                self._send_cmd("quit")
                self.sock.close()
            except Exception:
                pass
            self.sock = None
        if self.proc:
            try:
                self.proc.terminate()
            except Exception:
                pass
            self.proc = None

    def _play_file(self, video_path: str, index: int):
        uri = "file:///" + video_path.replace("\\", "/")

        if not self.proc:
            if not self._start_vlc():
                return

        self._send_cmd(f"add {uri}")
        self.current_index = index

    def handle(self, text: str):
        text = words_to_numbers(text.lower())

        if "мультфильм" in text or "мультик" in text:
            parts = text.split()
            cartoon = parts[-1]
            cartoon_dir = self.resolve_path(cartoon)
            if not self.path_exists(cartoon_dir):
                if self.speaker:
                    self.speaker.speak(f"Не нашла мультфильм {cartoon}.")
                return

            self.current_cartoon = cartoon
            self.current_season = None
            self.current_files = []
            self.current_index = None
            if self.speaker:
                self.speaker.speak(f"Выбрала мультфильм {cartoon}. Какой сезон включить?")

        elif "сезон" in text and self.current_cartoon:
            parts = text.split()
            try:
                season_num = int(parts[0])
            except ValueError:
                season_num = None

            if not season_num:
                if self.speaker:
                    self.speaker.speak("Не поняла номер сезона.")
                return

            season_dir = self.resolve_path(self.current_cartoon, f"{season_num}.сезон")
            if not self.path_exists(season_dir):
                if self.speaker:
                    self.speaker.speak(f"Сезон {season_num} не найден.")
                return

            self.current_season = f"{season_num}.сезон"
            self.current_files = sorted(self.list_files_in(season_dir))
            self.current_index = None
            if self.speaker:
                self.speaker.speak(f"Выбрала {season_num} сезон. Какая серия?")

        elif "серия" in text and self.current_cartoon and self.current_season:
            parts = text.split()
            try:
                series_num = int(parts[0])
            except ValueError:
                series_num = None

            if not series_num:
                if self.speaker:
                    self.speaker.speak("Не поняла номер серии.")
                return

            season_dir = self.resolve_path(self.current_cartoon, self.current_season)
            if series_num > len(self.current_files) or series_num <= 0:
                if self.speaker:
                    self.speaker.speak(f"Серии {series_num} нет.")
                return

            video_path = self.resolve_path(self.current_cartoon, self.current_season, self.current_files[series_num - 1])
            self._play_file(video_path, series_num - 1)
            if self.speaker:
                self.speaker.speak(f"Включаю {series_num} серию.")

        elif "следующая" in text and self.current_files and self.current_index is not None:
            if self.current_index + 1 < len(self.current_files):
                video_path = self.resolve_path(self.current_cartoon, self.current_season, self.current_files[self.current_index + 1])
                self._play_file(video_path, self.current_index + 1)
                if self.speaker:
                    self.speaker.speak("Включаю следующую серию.")
            else:
                if self.speaker:
                    self.speaker.speak("Это последняя серия в сезоне.")

        elif "предыдущая" in text and self.current_files and self.current_index is not None:
            if self.current_index - 1 >= 0:
                video_path = self.resolve_path(self.current_cartoon, self.current_season, self.current_files[self.current_index - 1])
                self._play_file(video_path, self.current_index - 1)
                if self.speaker:
                    self.speaker.speak("Включаю предыдущую серию.")
            else:
                if self.speaker:
                    self.speaker.speak("Это первая серия в сезоне.")

        elif "пауза" in text:
            self._send_cmd("pause")
            if self.speaker:
                self.speaker.speak("Поставила на паузу.")

        elif "продолжи" in text or "продолжить" in text:
            self._send_cmd("pause")
            if self.speaker:
                self.speaker.speak("Продолжаю воспроизведение.")

        elif "стоп" in text or "выключи" in text or "выключить" in text or "закрой мультфильм" in text:
            self._stop_vlc()
            if self.speaker:
                self.speaker.speak("Остановила мультфильм.")
