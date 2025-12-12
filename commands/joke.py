import random
from assistant.core import Command

class JokeCommand(Command):
    def __init__(self, jokes_file, speaker):
        self.jokes_file = jokes_file
        self.speaker = speaker
        self.jokes = self.load_jokes()

    def load_jokes(self):
        jokes = []
        try:
            with open(self.jokes_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        if line[0].isdigit() and "." in line:
                            line = line.split(".", 1)[1].strip()
                        jokes.append(line)
        except FileNotFoundError:
            print(f"[JokeCommand] Файл не найден: {self.jokes_file}")
        return jokes

    def matches(self, text: str) -> bool:
        text = text.lower()

        if "анекдот" in text:
            return True

        if "расскажи" in text and "анекдот" in text:
            return True

        return False

    def execute(self, text: str):
        text = text.lower()

        if "анекдот" in text and not any(ch.isdigit() for ch in text):
            if not self.jokes:
                self.speaker.say("Файл с анекдотами пуст или не найден.")
                return

            joke = random.choice(self.jokes)
            self.speaker.say(joke)
            return

        digits = "".join(ch for ch in text if ch.isdigit())
        if digits:
            index = int(digits) - 1

            if index < 0 or index >= len(self.jokes):
                self.speaker.say(f"Анекдота под номером {index + 1} не существует.")
                return

            self.speaker.say(self.jokes[index])
            return

        self.speaker.say("Не поняла, какой анекдот нужно рассказать.")
