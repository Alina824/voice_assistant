import os
from assistant.core import Command
from commands.note_reader import NoteReaderCommand


class DeleteNoteCommand(Command):
    def __init__(self, note_reader: NoteReaderCommand):
        super().__init__(name="удалить заметку")
        self.help_text = ("Команда для удаления заметок. "
                          "Скажи 'удали заметку <текст>', чтобы удалить строку. "
                          "Скажи 'удали файл', чтобы удалить весь текущий файл заметок.")
        self.note_reader = note_reader

    def matches(self, text: str) -> bool:
        text = text.lower()
        return "удали файл" in text or "удали заметку" in text or "удалить файл" in text

    def execute(self, text: str, speaker) -> None:
        text = text.lower()

        current_file = self.note_reader.get_current_file()
        if not current_file:
            speaker.speak("Заметок нет.")
            return

        if "удали файл" in text or "удалить файл" in text:
            os.remove(current_file)
            speaker.speak(f"Файл {os.path.basename(current_file)} удалён.")
            self.note_reader.reset_cursor()
            return

        if "удали заметку" in text:
            parts = text.split("удали заметку", 1)
            if len(parts) < 2 or not parts[1].strip():
                speaker.speak("Не указано, какую заметку удалить.")
                return
            note_to_delete = parts[1].strip()

            with open(current_file, "r", encoding="utf-8") as f:
                lines = f.readlines()

            new_lines = []
            deleted = False
            for line in lines:
                if not deleted and note_to_delete in line.lower():
                    deleted = True
                    continue
                new_lines.append(line)

            if not deleted:
                speaker.speak("Заметка не найдена.")
                return

            with open(current_file, "w", encoding="utf-8") as f:
                f.writelines(new_lines)

            speaker.speak(f"Заметка '{note_to_delete}' удалена.")
