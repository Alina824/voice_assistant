from assistant.core import Command


class SleepCommand(Command):
    is_sleep_command = True

    def __init__(self, assistant):
        self.assistant = assistant
        super().__init__(name="усни")
        self.help_text = "Скажи 'привет усни', чтобы усыпить ассистента."

    def matches(self, text: str) -> bool:
        return text in ["усни", "стоп", "замолчи", "спи"]

    def execute(self, text: str, speaker) -> None:
        if not self.assistant.sleeping:
            self.assistant.sleeping = True
            speaker.speak("Я засыпаю. Скажи 'привет проснись', чтобы меня разбудить.")
        else:
            speaker.speak("Я уже сплю.")