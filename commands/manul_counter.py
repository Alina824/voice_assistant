import time
from assistant.core import Command


class ManulCounterCommand(Command):
    def __init__(self, recognizer, speaker, timeout=12):
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

        if self.active:
            return True

        return False

    def parse_number(self, text: str):
        t = text.lower().strip()

        words_to_num = {
            "ноль": 0,
            "один": 1, "одна": 1,
            "два": 2, "две": 2,
            "три": 3,
            "четыре": 4,
            "пять": 5,
            "шесть": 6,
            "семь": 7,
            "восемь": 8,
            "девять": 9,
            "десять": 10,
        }

        for token in t.split():
            if token.isdigit():
                return int(token)

        for w, n in words_to_num.items():
            if w in t:
                return n

        return None

    def format_manuls(self, n: int) -> str:
        if n % 10 == 1 and n % 100 != 11:
            return f"{n} манул"
        elif 2 <= n % 10 <= 4 and not (12 <= n % 100 <= 14):
            return f"{n} манула"
        else:
            return f"{n} манулов"

    def execute(self, text: str):
        t = text.lower().strip()

        if "хватит" in t and self.active:
            self.speaker.say("Игра завершена.")
            self.active = False
            return

        if not self.active and ("манул" in t):
            n = self.parse_number(t)
            if n == 1:
                self.active = True
                self.expected_user_number = 1
                self.expected_bot_number = 2
                self.last_time = time.time()
                self.speaker.say(self.format_manuls(self.expected_bot_number))
                return

        if not self.active:
            return

        if time.time() - self.last_time > self.timeout:
            self.speaker.say("Слишком долго нет ответа. Игра окончена.")
            self.active = False
            return

        n = self.parse_number(t)
        if n is None:
            self.speaker.say("Не поняла число.")
            return

        if n < self.expected_user_number:
            self.speaker.say("Слишком мало манулов.")
            self.speaker.say(self.format_manuls(self.expected_user_number))
        elif n > self.expected_user_number:
            self.speaker.say("Слишком много манулов.")
            self.speaker.say(self.format_manuls(self.expected_user_number))
        else:
            pass

        self.speaker.say(self.format_manuls(self.expected_bot_number))

        self.expected_user_number += 2
        self.expected_bot_number += 2
        self.last_time = time.time()
