from typing import List, Optional, Callable
from abc import ABC, abstractmethod

from utils import filesystem as _fs
from utils import text_files as _tf


class Command(ABC):
    def __init__(self, name: str = None):
        self._name = name or self.__class__.__name__.lower()

    @property
    def name(self) -> str:
        return self._name

    @abstractmethod
    def matches(self, text: str) -> bool:
        pass

    @abstractmethod
    def execute(self, text: str, speaker) -> None:
        pass


class FileSystemCommand(Command):
    """Базовая команда для работы с файловой системой. Использует utils.filesystem."""

    def __init__(self, base_dir: str, name: str = None):
        super().__init__(name=name)
        self._base_dir = base_dir

    def list_files(self, *extensions: str) -> List[str]:
        return _fs.list_files(self._base_dir, *extensions)

    def list_files_in(self, directory: str, *extensions: str) -> List[str]:
        """Список файлов в произвольной директории (для вложенных: сезон/серия)."""
        return _fs.list_files(directory, *extensions)

    def find_file_by_name(
        self,
        name: str,
        extensions: tuple = (".mp3",),
    ) -> Optional[str]:
        return _fs.find_file_by_name(self._base_dir, name, extensions)

    def resolve_path(self, *parts: str) -> str:
        return _fs.resolve_path(self._base_dir, *parts)

    def path_exists(self, path: str) -> bool:
        return _fs.path_exists(path)

    def ensure_directory(self, path: str) -> None:
        _fs.ensure_directory(path)

    @abstractmethod
    def matches(self, text: str) -> bool:
        pass

    @abstractmethod
    def execute(self, text: str, speaker) -> None:
        pass


class TextFileCommand(Command):
    """Базовая команда для загрузки текстовых файлов через load_lines / load_delimited."""

    def _load_lines_safe(
        self,
        filepath: str,
        speaker,
        parse_line: Optional[Callable[[str], str]] = None,
        empty_msg: str = "Файл пуст или не найден.",
    ) -> List[str]:
        data = _tf.load_lines(filepath, parse_line=parse_line)
        if not data:
            speaker.speak(empty_msg)
            return []
        return data

    def _load_delimited_safe(
        self,
        filepath: str,
        speaker,
        delimiter: str = ";",
        empty_msg: str = "Файл пуст или не найден.",
    ) -> List[tuple]:
        data = _tf.load_delimited(filepath, delimiter=delimiter)
        if not data:
            speaker.speak(empty_msg)
            return []
        return data

    @abstractmethod
    def matches(self, text: str) -> bool:
        pass

    @abstractmethod
    def execute(self, text: str, speaker) -> None:
        pass


class InteractiveCommand(Command):
    """Базовая команда с циклом recognizer.recognize() и проверкой стоп-слов."""

    def __init__(self, recognizer, name: str = None):
        super().__init__(name=name)
        self.recognizer = recognizer

    def run_until_stop(
        self,
        speaker,
        stop_phrases: list,
        prompt_fn: Callable[[], str],
        handle_response_fn: Callable[[str], bool],
    ) -> None:
        """Цикл: prompt_fn() → speak → recognize() → стоп-фразы или handle_response_fn(resp) → True для выхода."""
        while True:
            speaker.speak(prompt_fn())
            r = self.recognizer.recognize()
            if not r:
                continue
            r = r.lower().strip()
            if r in stop_phrases:
                break
            if handle_response_fn(r):
                break

    @abstractmethod
    def matches(self, text: str) -> bool:
        pass

    @abstractmethod
    def execute(self, text: str, speaker) -> None:
        pass


class WakeUpCommand(Command):
    def matches(self, text: str) -> bool:
        return text.startswith("проснись")

    def execute(self, text: str, speaker) -> None:
        speaker.speak("Я проснулся. Слушаю.")


class SleepCommand(Command):
    def matches(self, text: str) -> bool:
        return text.startswith("усни")

    def execute(self, text: str, speaker) -> None:
        speaker.speak("Я засыпаю. Позови, когда понадобится.")


class VoiceAssistant:
    def __init__(self, recognizer, speaker, wake_word: str = "привет"):
        self.recognizer = recognizer
        self.speaker = speaker
        self.wake_word = wake_word.lower()
        self.commands: List[Command] = []
        self.sleeping = False

        self.system_commands = [WakeUpCommand(), SleepCommand()]

    def add_command(self, command: Command):
        self.commands.append(command)

    def run(self):
        print(f"Ассистент запущен. Скажи '{self.wake_word}' + команда.")

        try:
            while True:
                text = self.recognizer.recognize()
                if not text:
                    continue

                text = text.lower().strip()
                print(f"Распознано: {text}")

                if not text.startswith(self.wake_word):
                    continue

                command_text = text.replace(self.wake_word, "", 1).strip()

                if not command_text:
                    self.speaker.speak("Слушаю.")
                    continue

                if self.sleeping:
                    if WakeUpCommand().matches(command_text):
                        self.sleeping = False
                        WakeUpCommand().execute(command_text, self.speaker)
                    else:
                        print("Ассистент спит, команда проигнорирована.")
                    continue

                for cmd in self.system_commands + self.commands:
                    if cmd.matches(command_text):
                        cmd.execute(command_text, self.speaker)
                        if isinstance(cmd, SleepCommand):
                            self.sleeping = True
                        break
                else:
                    self.speaker.speak("Команда не распознана.")

        except KeyboardInterrupt:
            print("\nЗавершение работы ассистента...")
            self.speaker.stop()

