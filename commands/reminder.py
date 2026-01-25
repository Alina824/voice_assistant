import re
import threading
from datetime import datetime, timedelta

from assistant.core import Command
from utils.numeric import words_to_numbers


class ReminderCommand(Command):
    def __init__(self):
        super().__init__(name="напоминание")
        self.help_text = ("Форматы: "
                          "'Поставь напоминание ужин на 17', "
                          "'Поставь напоминание бильярд на 17 05', "
                          "'Напоминание встреча на 18 30'.")

    def matches(self, text: str) -> bool:
        return "напоминание" in text

    def execute(self, text: str, speaker) -> None:
        cleaned = words_to_numbers(text.lower())

        cleaned = cleaned.replace("поставь", "").replace("напоминание", "").strip()

        match = re.search(r"(.+?) на (\d{1,2})(?:[:\s](\d{1,2}))?", cleaned)
        if not match:
            speaker.speak("Не поняла время для напоминания.")
            return

        message = match.group(1).strip()
        hour = int(match.group(2))
        minute = int(match.group(3)) if match.group(3) else 0

        now = datetime.now()
        reminder_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)

        if reminder_time <= now:
            reminder_time += timedelta(days=1)

        delay = (reminder_time - now).total_seconds()

        speaker.speak(f"Напоминание '{message}' установлено на {reminder_time.strftime('%H:%M')}.")

        def notify():
            speaker.speak(f"Напоминание: {message}")

        t = threading.Timer(delay, notify)
        t.daemon = True
        t.start()
