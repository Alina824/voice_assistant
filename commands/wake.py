from assistant.core import Command


class WakeCommand(Command):
    def __init__(self, assistant):
        self.assistant = assistant
        super().__init__(name="проснись")
        self.help_text = "Скажи 'привет проснись', чтобы разбудить ассистента."

    def matches(self, text: str) -> bool:
        return text in ["проснись", "вставай", "очнись"]

    def execute(self, text: str, speaker) -> None:
        if self.assistant.sleeping:
            self.assistant.sleeping = False
            speaker.speak("Я проснулся и снова слушаю тебя.")
        else:
            speaker.speak("Я и так не сплю.")
