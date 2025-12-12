import threading
import time
import random

from assistant.core import Command


class SneezingCommand(Command):
    def __init__(self, speaker):
        super().__init__(name="чихание")
        self.speaker = speaker
        self.last_sneeze_time = 0
        self.waiting_for_bless = False

        t = threading.Thread(target=self._random_sneeze_loop, daemon=True)
        t.start()

    def matches(self, text: str) -> bool:
        return text in ["апчхи", "будь здоров"]

    def execute(self, text: str, speaker) -> None:
        text = text.lower().strip()

        if text == "апчхи":
            speaker.speak("Будь здоров")
            return

        if text == "будь здоров":
            if self.waiting_for_bless:
                self.waiting_for_bless = False
                speaker.speak("Спасибо")
            else:
                speaker.speak("Спасибо, но я не чихал.")
            return

    def _random_sneeze_loop(self):
        while True:
            time.sleep(random.randint(200, 5000))

            self.speaker.speak("Апчхи")
            self.waiting_for_bless = True

            time.sleep(random.randint(5, 8))

            if self.waiting_for_bless:
                self.waiting_for_bless = False
