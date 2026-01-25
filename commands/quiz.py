import random
from assistant.core import Command
from utils.text_files import load_delimited


class QuizCommand(Command):
    def __init__(self, questions_file, recognizer=None, speaker=None):
        super().__init__(name="викторина")
        self.questions_file = questions_file
        self.questions = load_delimited(questions_file, delimiter=";")

        self.active = False
        self.total = 0
        self.correct = 0

    def matches(self, text: str) -> bool:
        t = text.lower()
        if self.active:
            return any(w in t for w in ["продолж", "дальше", "ещё", "далее", "стоп", "выход", "заверш", "хватит"]) or True
        return "викторин" in t or "квиз" in t

    def execute(self, text: str, speaker) -> None:
        text = text.lower()

        if not self.active:
            if not self.questions:
                speaker.speak("Файл с вопросами пуст или не найден.")
                return
            self.active = True
            self.total = 0
            self.correct = 0
            speaker.speak("Начинаем викторину!")
            self.ask_question(speaker)
            return

        if any(w in text for w in ["стоп", "выход", "заверш", "хватит"]):
            self.finish(speaker)
            return

        if any(w in text for w in ["продолж", "дальше", "ещё"]):
            self.ask_question(speaker)
            return

        self.check_answer(text, speaker)

    def ask_question(self, speaker) -> None:
        raw = random.choice(self.questions)
        self.current_question = raw[0].strip() if len(raw) > 0 else ""
        self.current_answer = raw[1].strip() if len(raw) > 1 else ""
        self.total += 1
        speaker.speak(self.current_question)

    def check_answer(self, user_answer: str, speaker) -> None:
        ua = user_answer.strip().lower()
        ca = self.current_answer.strip().lower()
        if ua == ca:
            self.correct += 1
            speaker.speak("Верно!")
        else:
            speaker.speak(f"Неверно. Правильный ответ: {self.current_answer}.")
        speaker.speak("Продолжить или завершить?")

    def finish(self, speaker) -> None:
        speaker.speak(f"Викторина завершена. Правильных ответов {self.correct} из {self.total}.")
        self.active = False
