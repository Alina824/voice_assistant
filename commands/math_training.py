import random
import time
from assistant.core import Command


class MathTrainerCommand(Command):
    def __init__(self, recognizer, speaker):
        super().__init__(name="тренировка математики")
        self.help_text = ("Скажи 'тренировка', чтобы начать. "
                          "Ассистент спросит операцию: сложение, вычитание, умножение или деление. "
                          "Можно сказать 'сложнее' или 'проще', чтобы изменить уровень. "
                          "Скажи 'стоп тренировка', чтобы выйти.")
        self.recognizer = recognizer
        self.speaker = speaker
        self.active = False
        self.digits = 1
        self.operation = None

    def matches(self, text: str) -> bool:
        keywords = ["тренировка", "сложнее", "проще", "стоп тренировка"]
        return any(word in text for word in keywords)

    def execute(self, text: str):
        if "стоп" in text:
            self.active = False
            self.speaker.speak("Тренировка остановлена")
            return

        if "сложнее" in text:
            self.digits = min(self.digits + 1, 4)
            self.speaker.speak(f"Сложность увеличена, теперь {self.digits}-значные числа")
            return

        if "проще" in text:
            self.digits = max(self.digits - 1, 1)
            self.speaker.speak(f"Сложность уменьшена, теперь {self.digits}-значные числа")
            return

        if "тренировка" in text:
            self.speaker.speak("Какую операцию будем тренировать? сложение, вычитание, умножение или деление?")
            op_text = self.recognizer.listen(timeout=10)
            if not op_text:
                self.speaker.speak("Я не расслышала операцию.")
                return

            if "сложение" in op_text:
                self.operation = "+"
            elif "вычитание" in op_text:
                self.operation = "-"
            elif "умножение" in op_text:
                self.operation = "*"
            elif "деление" in op_text:
                self.operation = "/"
            else:
                self.speaker.speak("Неизвестная операция.")
                return

            self.active = True
            self.speaker.speak(f"Начинаем тренировку {op_text}")
            self.training_loop()

    def training_loop(self):
        while self.active:
            min_val = 10 ** (self.digits - 1)
            max_val = 10 ** self.digits - 1

            a = random.randint(min_val, max_val)
            b = random.randint(min_val, max_val)

            if self.operation == "/" and b == 0:
                b = 1

            if self.operation == "+":
                correct = a + b
                op_word = "плюс"
            elif self.operation == "-":
                correct = a - b
                op_word = "минус"
            elif self.operation == "*":
                correct = a * b
                op_word = "умножить на"
            elif self.operation == "/":
                correct = a // b
                op_word = "разделить на"

            self.speaker.speak(f"Сколько будет {a} {op_word} {b}?")
            time.sleep(2)

            answer_text = self.recognizer.listen(timeout=7)
            if not answer_text:
                self.speaker.speak("Не расслышала ответ. Продолжим.")
                continue

            try:
                answer = int(answer_text)
            except ValueError:
                self.speaker.speak("Ответ не является числом. Давайте дальше.")
                continue

            if answer == correct:
                self.speaker.speak("Правильно!")
            else:
                diff = abs(answer - correct)
                self.speaker.speak(f"Неправильно. Правильный ответ {correct}. Вы ошиблись на {diff}.")
