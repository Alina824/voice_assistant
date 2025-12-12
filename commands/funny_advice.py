import random
from assistant.core import Command

class AdviceCommand(Command):
    def __init__(self, advices_file, speaker):
        self.advices_file = advices_file
        self.speaker = speaker
        self.advices = self.load_advices()

    def load_advices(self):
        advices = []
        try:
            with open(self.advices_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        if line[0].isdigit() and "." in line:
                            line = line.split(".", 1)[1].strip()
                        advices.append(line)
        except FileNotFoundError:
            print(f"[AdviceCommand] Файл не найден: {self.advices_file}")
        return advices

    def matches(self, text: str) -> bool:
        text = text.lower()

        return (
            "совет" in text
            or "вредный совет" in text
            or ("дай" in text and "совет" in text)
        )

    def execute(self, text: str):
        if not self.advices:
            self.speaker.say("Файл советов пуст или не найден.")
            return

        advice = random.choice(self.advices)
        self.speaker.say(advice)
