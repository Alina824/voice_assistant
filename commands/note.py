import os
import re
from datetime import datetime
from assistant.core import Command


class NoteCommand(Command):
    def __init__(self, notes_dir: str = "D:/User/Notes"):
        super().__init__(name="добавить заметку")
        self.help_text = ("Скажи 'добавь заметку <текст>', чтобы записать в файл. "
                          "Скажи 'добавь заметку новая заметка', чтобы создать новый файл. "
                          "Можно сразу добавить текст в новую заметку.")
        self.notes_dir = notes_dir
        os.makedirs(self.notes_dir, exist_ok=True)

    def matches(self, text: str) -> bool:
        return "добавь заметку" in text.lower() or "добавить заметку" in text.lower() or "давай заметку" in text.lower()

    def execute(self, text: str, speaker) -> None:
        text = text.lower().strip()

        match = re.search(r"(?:добавь|добавить) заметку\s*(.*)", text)
        if not match:
            speaker.speak("Не поняла текст заметки.")
            return

        note_text = match.group(1).strip()

        if note_text.startswith("новая заметка"):
            remainder = note_text.replace("новая заметка", "", 1).strip()
            file_path = self._create_new_file()
            if remainder:
                self._append_to_file(file_path, remainder)
                speaker.speak(f"Создана новая заметка и добавлено: {remainder}")
            else:
                speaker.speak("Создана новая пустая заметка.")
        else:
            file_path = self._get_last_or_new_file()
            self._append_to_file(file_path, note_text)
            speaker.speak(f"Добавлено в заметку: {note_text}")

    def _create_new_file(self) -> str:
        today = datetime.now().strftime("%d-%m-%Y")
        existing = [
            f for f in os.listdir(self.notes_dir)
            if f.startswith(today)
        ]
        next_num = len(existing) + 1
        filename = f"{today}-{next_num}.txt"
        file_path = os.path.join(self.notes_dir, filename)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("")
        return file_path

    def _get_last_or_new_file(self) -> str:
        files = sorted(os.listdir(self.notes_dir))
        if not files:
            return self._create_new_file()
        return os.path.join(self.notes_dir, files[-1])

    def _append_to_file(self, file_path: str, text: str) -> None:
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(text + "\n")