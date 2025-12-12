from assistant.core import Command
import pygame


class PauseCommand(Command):
    def __init__(self, pausable_commands):
        super().__init__(name="пауза")
        self.help_text = "Скажи 'пауза', чтобы приостановить воспроизведение."
        self.pausable_commands = pausable_commands

    def matches(self, text: str) -> bool:
        return text.strip().lower() in ["пауза", "останови", "приостанови"]

    def execute(self, text: str, speaker) -> None:
        try:
            pygame.mixer.music.pause()
        except Exception:
            pass

        for cmd in self.pausable_commands:
            if hasattr(cmd, "pause"):
                cmd.pause()

        speaker.speak("Пауза. Скажи 'продолжить', чтобы возобновить.")


class ResumeCommand(Command):
    def __init__(self, pausable_commands):
        super().__init__(name="продолжить")
        self.help_text = "Скажи 'продолжить', чтобы возобновить воспроизведение."
        self.pausable_commands = pausable_commands

    def matches(self, text: str) -> bool:
        return text.strip().lower() in ["продолжить", "дальше", "продолжай"]

    def execute(self, text: str, speaker) -> None:
        try:
            pygame.mixer.music.unpause()
        except Exception:
            pass

        for cmd in self.pausable_commands:
            if hasattr(cmd, "resume"):
                cmd.resume()

        speaker.speak("Продолжаю воспроизведение.")

