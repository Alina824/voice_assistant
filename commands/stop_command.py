from assistant.core import Command


class StopCommand(Command):

    def __init__(self):
        super().__init__(name="хватит")
        self.help_text = "Скажи 'хватит', чтобы остановить текущую операцию."

    def matches(self, text: str) -> bool:
        return text.strip().lower() == "хватит"

    def execute(self, text: str, speaker) -> None:
        speaker.speak("Останавливаю.")
        raise StopIteration("Пользователь сказал 'хватит'")
