import random
from assistant.core import Command

class CoinFlipCommand(Command):
    def __init__(self):
        super().__init__("coin_flip")
        self.triggers = [
            "орёл или решка",
            "орел или решка",
            "подбрось монету",
            "брось монету",
            "подбрось монетку",
            "брось монетку",
            "монета",
            "монетку",
        ]

    def matches(self, text: str) -> bool:
        t = text.lower()
        return any(trigger in t for trigger in self.triggers)

    def execute(self, text: str, speaker):
        result = "Орёл" if random.random() < 0.5 else "Решка"
        speaker.speak(result)
