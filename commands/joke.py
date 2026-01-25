import random
from assistant.core import Command
from utils.text_files import load_lines, strip_numbered_prefix


class JokeCommand(Command):
    def __init__(self, jokes_file, speaker=None):
        super().__init__(name="анекдот")
        self.jokes_file = jokes_file
        self.jokes = load_lines(jokes_file, parse_line=strip_numbered_prefix)

    def matches(self, text: str) -> bool:
        text = text.lower()
        return "анекдот" in text or ("расскажи" in text and "анекдот" in text)

    def execute(self, text: str, speaker) -> None:
        text = text.lower()

        if "анекдот" in text and not any(ch.isdigit() for ch in text):
            if not self.jokes:
                speaker.speak("Файл с анекдотами пуст или не найден.")
                return
            joke = random.choice(self.jokes)
            speaker.speak(joke)
            return

        digits = "".join(ch for ch in text if ch.isdigit())
        if digits:
            index = int(digits) - 1
            if index < 0 or index >= len(self.jokes):
                speaker.speak(f"Анекдота под номером {index + 1} не существует.")
                return
            speaker.speak(self.jokes[index])
            return

        speaker.speak("Не поняла, какой анекдот нужно рассказать.")
