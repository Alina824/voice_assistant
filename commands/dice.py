import random
import re
from assistant.core import Command

class DiceFlipCommand(Command):
    def __init__(self):
        super().__init__("dice_roll")

        self.pattern_num_rus = re.compile(
            r"(подбрось|кинь|брось|дай)\s+(\d+)\s+кубик"
        )
        self.pattern_one_rus = re.compile(
            r"(подбрось|кинь|брось|дай)\s+(один|1)\s+кубик"
        )

        self.pattern_dnd = re.compile(r"(\d+)[dд](\d+)")

    def matches(self, text: str) -> bool:
        t = text.lower()
        return (
            "кубик" in t
            or self.pattern_dnd.search(t) is not None
        )

    def execute(self, text: str, speaker):
        t = text.lower().strip()

        if self.pattern_one_rus.search(t):
            result = random.randint(1, 6)
            speaker.speak(f"Выпало {result}")
            return

        m_rus = self.pattern_num_rus.search(t)
        if m_rus:
            n = int(m_rus.group(2))
            if n < 1:
                speaker.speak("Нужно хотя бы один кубик.")
                return
            if n > 20:
                speaker.speak("Максимум могу кинуть двадцать кубиков.")
                return

            rolls = [random.randint(1, 6) for _ in range(n)]
            s = ", ".join(str(r) for r in rolls)
            speaker.speak(f"Выпало: {s}. Сумма {sum(rolls)}")
            return

        m_dnd = self.pattern_dnd.search(t)
        if m_dnd:
            n = int(m_dnd.group(1))
            sides = int(m_dnd.group(2))

            if n < 1:
                speaker.speak("Нужно хотя бы один кубик.")
                return
            if n > 20:
                speaker.speak("Максимум могу кинуть двадцать кубиков.")
                return

            if sides != 6:
                speaker.speak("Пока я умею бросать только шестигранные кубики.")
                return

            rolls = [random.randint(1, 6) for _ in range(n)]
            s = ", ".join(str(r) for r in rolls)
            speaker.speak(f"Выпало: {s}. Сумма {sum(rolls)}")
            return

        if "кубик" in t:
            result = random.randint(1, 6)
            speaker.speak(f"Выпало {result}")
            return

        speaker.speak("Не понял запрос.")
