import os
from assistant.core import Command
from commands.stop_command import StopCommand


class NoteReaderCommand(Command):
    def __init__(self, notes_dir: str, recognizer):
        super().__init__(name="чтение заметок")
        self.help_text = (
            "Скажи 'прочитай заметки', чтобы прослушать содержимое заметок подряд. "
            "Доступны команды 'пауза', 'продолжить', 'стоп'."
        )
        self.notes_dir = notes_dir
        self.recognizer = recognizer

    def _chunk_text(self, text: str, size: int = 250):
        for i in range(0, len(text), size):
            yield text[i:i + size]

    def matches(self, text: str) -> bool:
        return text.lower().startswith(("прочитай заметки", "чтение заметок"))

    def execute(self, text: str, speaker) -> None:
        stop_cmd = StopCommand()

        if not os.path.exists(self.notes_dir):
            speaker.speak("Папка с заметками не найдена.")
            return

        files = [f for f in os.listdir(self.notes_dir) if f.endswith(".txt")]
        if not files:
            speaker.speak("Нет заметок.")
            return

        for name in files:
            speaker.speak(f"Читаю заметку {name.replace('.txt', '')}")

            path = os.path.join(self.notes_dir, name)
            with open(path, encoding="utf-8") as f:
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
