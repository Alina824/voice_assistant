import random
from assistant.core import Command


class QuizCommand(Command):
    def __init__(self, questions_file, recognizer, speaker):
        self.questions_file = questions_file
        self.recognizer = recognizer
        self.speaker = speaker
        self.questions = self.load_questions()

        self.active = False
        self.total = 0
        self.correct = 0

    def load_questions(self):
        questions = []
        try:
            with open(self.questions_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if ";" in line:
                        q, a = line.split(";", 1)
                        questions.append((q.strip(), a.strip()))
        except FileNotFoundError:
            print(f"[QuizCommand] Файл не найден: {self.questions_file}")
        return questions

    def matches(self, text: str) -> bool:
        t = text.lower()
        if self.active:
            if any(w in t for w in ["продолж", "дальше", "ещё", "далее"]):
                return True
            if any(w in t for w in ["стоп", "выход", "заверш", "хватит"]):
                return True
            return True
        else:
            return "викторин" in t or "квиз" in t

    def execute(self, text: str):
        text = text.lower()

        if not self.active:
            if not self.questions:
                self.speaker.say("Файл с вопросами пуст или не найден.")
                return
            self.active = True
            self.total = 0
            self.correct = 0
            self.speaker.say("Начинаем викторину!")
            self.ask_question()
            return

        if any(w in text for w in ["стоп", "выход", "заверш", "хватит"]):
            self.finish()
            return

        if any(w in text for w in ["продолж", "дальше", "ещё"]):
            self.ask_question()
            return

        self.check_answer(text)

    def ask_question(self):
        self.current_question, self.current_answer = random.choice(self.questions)
        self.total += 1
        self.speaker.say(self.current_question)

    def check_answer(self, user_answer):
        ua = user_answer.strip().lower()
        ca = self.current_answer.strip().lower()

        if ua == ca:
            self.correct += 1
            self.speaker.say("Верно!")
        else:
            self.speaker.say(f"Неверно. Правильный ответ: {self.current_answer}.")

        self.speaker.say("Продолжить или завершить?")

    def finish(self):
        self.speaker.say(f"Викторина завершена. Правильных ответов {self.correct} из {self.total}.")
        self.active = False
