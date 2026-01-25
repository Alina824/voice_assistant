import time
from assistant.core import Command
from utils.numeric import parse_number


class ManulCounterCommand(Command):
    def __init__(self, recognizer, speaker, timeout=12):
        super().__init__(name="манул")
        self.recognizer = recognizer
        self.speaker = speaker
        self.active = False
        self.expected_user_number = 1
        self.expected_bot_number = 2
        self.timeout = timeout
        self.last_time = None

    def matches(self, text: str) -> bool:
        text = text.lower()
        if "манул" in text and ("один" in text or "раз" in text):
            return True
        return self.active

    def format_manuls(self, n: int) -> str:
        if n % 10 == 1 and n % 100 != 11:
            return f"{n} манул"
        elif 2 <= n % 10 <= 4 and not (12 <= n % 100 <= 14):
            return f"{n} манула"
        else:
            return f"{n} манулов"

    def execute(self, text: str, speaker) -> None:
        t = text.lower().strip()

        if "хватит" in t and self.active:
            speaker.speak("Игра завершена.")
            self.active = False
            return

        if not self.active and "манул" in t:
            n = parse_number(t)
            if n == 1:
                self.active = True
                self.expected_user_number = 1
                self.expected_bot_number = 2
                self.last_time = time.time()
                speaker.speak(self.format_manuls(self.expected_bot_number))
                return

        if not self.active:
            return

        if time.time() - self.last_time > self.timeout:
            speaker.speak("Слишком долго нет ответа. Игра окончена.")
            self.active = False
            return

        n = parse_number(t)
        if n is None:
            speaker.speak("Не поняла число.")
            return

        if n < self.expected_user_number:
            speaker.speak("Слишком мало манулов.")
            speaker.speak(self.format_manuls(self.expected_user_number))
        elif n > self.expected_user_number:
            speaker.speak("Слишком много манулов.")
            speaker.speak(self.format_manuls(self.expected_user_number))

        speaker.speak(self.format_manuls(self.expected_bot_number))
        self.expected_user_number += 2
        self.expected_bot_number += 2
        self.last_time = time.time()
