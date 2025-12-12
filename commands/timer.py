import re
import threading
import time
from assistant.core import Command


class TimerCommand(Command):
    def matches(self, text: str) -> bool:
        super().__init__(name="поставь таймер")

    def execute(self, text: str, speaker) -> None:
        minutes = 0
        seconds = 0

        sec_match = re.search(r"(\d+)\s*секунд", text)
        if sec_match:
            seconds = int(sec_match.group(1))
        else:
            min_match = re.search(r"(\d+)(?:\s*и\s*половин[ауы])?\s*минут", text)
            if min_match:
                minutes = int(min_match.group(1))
                if "половин" in text:
                    seconds = 30

        if "45 секунд" in text:
            minutes = 0
            seconds = 45

        total_seconds = minutes * 60 + seconds

        if total_seconds == 0:
            speaker.say("Не поняла, на сколько поставить таймер.")
            return

        threading.Thread(target=self._run_timer, args=(total_seconds, speaker), daemon=True).start()

        if minutes > 0 and seconds == 0:
            speaker.say(f"Таймер на {minutes} минут запущен.")
        elif minutes > 0 and seconds == 30:
            speaker.say(f"Таймер на {minutes} с половиной минут запущен.")
        elif seconds > 0 and minutes == 0:
            speaker.say(f"Таймер на {seconds} секунд запущен.")

    def _run_timer(self, delay: int, speaker) -> None:
        time.sleep(delay)
        speaker.say("Время вышло!")
