from datetime import datetime
from assistant.core import Command


class TimeCommand(Command):
    def __init__(self):
        super().__init__(name="время")
        self.help_text = ("Скажи 'сколько времени', "
                          "'текущее время', "
                          "или 'скажи время'.")

    def matches(self, text: str) -> bool:
        keywords = ["время", "скажи время", "текущее время", "сколько времени"]
        return any(k in text for k in keywords)

    def execute(self, text: str, speaker) -> None:
        now = datetime.now().strftime("%H:%M")
        speaker.speak(f"Сейчас {now}")
