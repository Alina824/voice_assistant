import sqlite3
import random
import re
from assistant.core import Command

DB_NAME = "words.db"


def get_table_name(language: str) -> str:
    return f"{language.lower()}_words"


def create_table_if_not_exists(language: str):
    table = get_table_name(language)
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {table} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                foreign_word TEXT NOT NULL,
                russian_word TEXT NOT NULL
            )
        """)
        conn.commit()


def add_word(language: str, foreign: str, russian: str):
    create_table_if_not_exists(language)
    table = get_table_name(language)
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute(f"INSERT INTO {table} (foreign_word, russian_word) VALUES (?, ?)", (foreign, russian))
        conn.commit()


def delete_word(language: str, word: str):
    table = get_table_name(language)
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute(f"DELETE FROM {table} WHERE foreign_word = ? OR russian_word = ?", (word, word))
        deleted = cur.rowcount
        conn.commit()
        return deleted > 0


def get_all_words(language: str):
    table = get_table_name(language)
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute(f"SELECT foreign_word, russian_word FROM {table}")
        return cur.fetchall()


class VocabularyCommand(Command):
    def __init__(self):
        super().__init__(name="словарь")
        self.help_text = ("Форматы: "
                          "'добавь слово <язык> <иностранное> <перевод>', "
                          "'удали слово <язык> <слово>', "
                          "'запусти тренировку <язык>', "
                          "'запусти тренировку русский-<язык>'.")

    def matches(self, text: str) -> bool:
        text = text.lower()
        return any([
            "добавь слово" in text,
            "удали слово" in text,
            "запусти тренировку" in text
        ])

    def execute(self, text: str, speaker, recognizer=None) -> None:
        text = text.lower().strip()

        m = re.match(r"добавь слово (\w+) '(.+?)' '(.+?)'", text)
        if m:
            language, foreign, russian = m.groups()
            add_word(language, foreign, russian)
            speaker.speak(f"Слово {foreign} добавлено в {language}")
            return

        m = re.match(r"удали слово (\w+) '(.+?)'", text)
        if m:
            language, word = m.groups()
            if delete_word(language, word):
                speaker.speak(f"Слово {word} удалено из {language}")
            else:
                speaker.speak("Слово не найдено")
            return

        m = re.match(r"запусти тренировку (\w+)$", text)
        if m:
            language = m.group(1)
            words = get_all_words(language)
            if not words:
                speaker.speak("В базе нет слов")
                return

            speaker.speak(f"Начинаем тренировку {language} на перевод на русский")
            while True:
                foreign, russian = random.choice(words)
                speaker.speak(f"Переведи {foreign}")
                answer = recognizer.recognize() if recognizer else input("> ").strip()

                if not answer or answer.lower() in ("стоп", "выход", "всё"):
                    speaker.speak("Тренировка завершена")
                    break
                if answer.lower() == russian.lower():
                    speaker.speak("Верно")
                else:
                    speaker.speak(f"Неверно. Правильно: {russian}")
            return

        m = re.match(r"запусти тренировку русский-(\w+)$", text)
        if m:
            language = m.group(1)
            words = get_all_words(language)
            if not words:
                speaker.speak("В базе нет слов")
                return

            speaker.speak(f"Начинаем тренировку с русского на {language}")
            while True:
                foreign, russian = random.choice(words)
                speaker.speak(f"Переведи {russian}")
                answer = recognizer.recognize() if recognizer else input("> ").strip()

                if not answer or answer.lower() in ("стоп", "выход", "всё"):
                    speaker.speak("Тренировка завершена")
                    break
                if answer.lower() == foreign.lower():
                    speaker.speak("Верно")
                else:
                    speaker.speak(f"Неверно. Правильно: {foreign}")
            return

        speaker.speak("Команда не распознана")