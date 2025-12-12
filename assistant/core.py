from typing import List
from abc import ABC, abstractmethod


class Command(ABC):
    def __init__(self, name: str = None):
        self._name = name or self.__class__.__name__.lower()

    @property
    def name(self) -> str:
        return self._name

    @abstractmethod
    def matches(self, text: str) -> bool:
        pass

    @abstractmethod
    def execute(self, text: str, speaker) -> None:
        pass


class WakeUpCommand(Command):
    def matches(self, text: str) -> bool:
        return text.startswith("проснись")

    def execute(self, text: str, speaker) -> None:
        speaker.speak("Я проснулся. Слушаю.")


class SleepCommand(Command):
    def matches(self, text: str) -> bool:
        return text.startswith("усни")

    def execute(self, text: str, speaker) -> None:
        speaker.speak("Я засыпаю. Позови, когда понадобится.")


class VoiceAssistant:
    def __init__(self, recognizer, speaker, wake_word: str = "привет"):
        self.recognizer = recognizer
        self.speaker = speaker
        self.wake_word = wake_word.lower()
        self.commands: List[Command] = []
        self.sleeping = False

        self.system_commands = [WakeUpCommand(), SleepCommand()]

    def add_command(self, command: Command):
        self.commands.append(command)

    def run(self):
        print(f"Ассистент запущен. Скажи '{self.wake_word}' + команда.")

        try:
            while True:
                text = self.recognizer.recognize()
                if not text:
                    continue

                text = text.lower().strip()
                print(f"Распознано: {text}")

                if not text.startswith(self.wake_word):
                    continue

                command_text = text.replace(self.wake_word, "", 1).strip()

                if not command_text:
                    self.speaker.speak("Слушаю.")
                    continue

                if self.sleeping:
                    if WakeUpCommand().matches(command_text):
                        self.sleeping = False
                        WakeUpCommand().execute(command_text, self.speaker)
                    else:
                        print("Ассистент спит, команда проигнорирована.")
                    continue

                for cmd in self.system_commands + self.commands:
                    if cmd.matches(command_text):
                        cmd.execute(command_text, self.speaker)
                        if isinstance(cmd, SleepCommand):
                            self.sleeping = True
                        break
                else:
                    self.speaker.speak("Команда не распознана.")

        except KeyboardInterrupt:
            print("\nЗавершение работы ассистента...")
            self.speaker.stop()

