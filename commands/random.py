import random
import re
from assistant.core import Command

class RandomNumberCommand(Command):
    def __init__(self):
        super().__init__("random_number")
        self.pattern = re.compile(r"от\s+(-?\d+)\s+до\s+(-?\d+)")
        self.triggers = [
            "случайное число",
            "рандомное число",
            "рандом",
            "выбери число",
            "число от",
            "число в диапазоне",
        ]

    def matches(self, text: str) -> bool:
        t = text.lower()
        return any(trigger in t for trigger in self.triggers)

    def execute(self, text: str, speaker):
        t = text.lower().strip()

        match = self.pattern.search(t)
        if not match:
            speaker.speak("Не понял диапазон. Скажи, например: от 1 до 10.")
            return

        a = int(match.group(1))
        b = int(match.group(2))

        if a > b:
            speaker.speak(f"Неверный диапазон: {a} больше {b}.")
            return

        result = random.randint(a, b)
        speaker.speak(f"Случайное число: {result}")
