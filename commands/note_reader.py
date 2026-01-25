from typing import Optional

from assistant.core import FileSystemCommand
from commands.stop_command import StopCommand


class NoteReaderCommand(FileSystemCommand):
    def __init__(self, notes_dir: str, recognizer):
        super().__init__(base_dir=notes_dir, name="чтение заметок")
        self.help_text = (
            "Скажи 'прочитай заметки', чтобы прослушать содержимое заметок подряд. "
            "Доступны команды 'пауза', 'продолжить', 'стоп'."
        )
        self.recognizer = recognizer
        self._current_file: Optional[str] = None

    def get_current_file(self) -> Optional[str]:
        """Последний прочитанный в этой сессии файл. Для DeleteNoteCommand."""
        return self._current_file

    def reset_cursor(self) -> None:
        """Сброс состояния текущего файла после удаления."""
        self._current_file = None

    def _chunk_text(self, text: str, size: int = 250):
        for i in range(0, len(text), size):
            yield text[i:i + size]

    def matches(self, text: str) -> bool:
        return text.lower().startswith(("прочитай заметки", "чтение заметок"))

    def execute(self, text: str, speaker) -> None:
        stop_cmd = StopCommand()

        if not self.path_exists(self._base_dir):
            speaker.speak("Папка с заметками не найдена.")
            return

        files = self.list_files(".txt")
        if not files:
            speaker.speak("Нет заметок.")
            return

        for name in files:
            self._current_file = self.resolve_path(name)
            speaker.speak(f"Читаю заметку {name.replace('.txt', '')}")

            with open(self._current_file, encoding="utf-8") as f:
                content = f.read().strip()

            if not content:
                speaker.speak("Заметка пустая.")
                continue

            for chunk in self._chunk_text(content):
                speaker.speak(chunk)

            choice = self.recognizer.recognize()
            if choice and stop_cmd.matches(choice.lower()):
                speaker.speak("Останавливаю чтение заметок.")
                return
