from assistant.core import Command


class HelpCommand(Command):
    def __init__(self, commands: list):
        super().__init__(name="help")
        self.help_text = "Скажи 'help <команда>' или 'помощь <команда>', чтобы узнать, как её использовать."
        self.commands = commands

    def matches(self, text: str) -> bool:
        text = text.lower().strip()
        return text.startswith("help") or text.startswith("помощь")

    def execute(self, text: str, speaker) -> None:
        parts = text.lower().split(maxsplit=1)

        if len(parts) == 1:
            available = ", ".join(
                cmd.name for cmd in self.commands if hasattr(cmd, "name")
            )
            speaker.speak(f"Доступные команды: {available}. "
                          f"Скажи 'help <команда>' или 'помощь <команда>' для деталей.")
            return

        query = parts[1]
        for cmd in self.commands:
            if hasattr(cmd, "name") and query in cmd.name.lower():
                if hasattr(cmd, "help_text"):
                    speaker.speak(f"{cmd.name}: {cmd.help_text}")
                else:
                    speaker.speak(f"У команды {cmd.name} пока нет описания.")
                return

        speaker.speak(f"Команда {query} не найдена.")