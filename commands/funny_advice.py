import random
from assistant.core import Command
from utils.text_files import load_lines, strip_numbered_prefix


class AdviceCommand(Command):
    def __init__(self, advices_file, speaker=None):
        super().__init__(name="совет")
        self.advices_file = advices_file
        self.advices = load_lines(advices_file, parse_line=strip_numbered_prefix)

    def matches(self, text: str) -> bool:
        text = text.lower()
        return "совет" in text or "вредный совет" in text or ("дай" in text and "совет" in text)

    def execute(self, text: str, speaker) -> None:
        if not self.advices:
            speaker.speak("Файл советов пуст или не найден.")
            return
        advice = random.choice(self.advices)
        speaker.speak(advice)
