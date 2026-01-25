import sqlite3
import random
import re
from assistant.core import Command

DEFAULT_DB_PATH = "words.db"


def get_table_name(language: str) -> str:
    return f"{language.lower()}_words"


def create_table_if_not_exists(language: str, db_path: str = DEFAULT_DB_PATH):
    table = get_table_name(language)
    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {table} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                foreign_word TEXT NOT NULL,
                russian_word TEXT NOT NULL
            )
        """)
        conn.commit()


def add_word(language: str, foreign: str, russian: str, db_path: str = DEFAULT_DB_PATH):
    create_table_if_not_exists(language, db_path)
    table = get_table_name(language)
    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        cur.execute(f"INSERT INTO {table} (foreign_word, russian_word) VALUES (?, ?)", (foreign, russian))
        conn.commit()


def delete_word(language: str, word: str, db_path: str = DEFAULT_DB_PATH):
    table = get_table_name(language)
    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        cur.execute(f"DELETE FROM {table} WHERE foreign_word = ? OR russian_word = ?", (word, word))
        deleted = cur.rowcount
        conn.commit()
        return deleted > 0


def get_all_words(language: str, db_path: str = DEFAULT_DB_PATH):
    table = get_table_name(language)
    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        cur.execute(f"SELECT foreign_word, russian_word FROM {table}")
        return cur.fetchall()


class VocabularyCommand(Command):
    def __init__(self, db_path: str = DEFAULT_DB_PATH, recognizer=None):
        super().__init__(name="словарь")
        self.db_path = db_path
        self.recognizer = recognizer
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

    def execute(self, text: str, speaker) -> None:
        text = text.lower().strip()
        rec = self.recognizer

        m = re.match(r"добавь слово (\w+) '(.+?)' '(.+?)'", text)
        if m:
            language, foreign, russian = m.groups()
            add_word(language, foreign, russian, self.db_path)
            speaker.speak(f"Слово {foreign} добавлено в {language}")
            return

        m = re.match(r"удали слово (\w+) '(.+?)'", text)
        if m:
            language, word = m.groups()
            if delete_word(language, word, self.db_path):
                speaker.speak(f"Слово {word} удалено из {language}")
            else:
                speaker.speak("Слово не найдено")
            return

        m = re.match(r"запусти тренировку (\w+)$", text)
        if m:
            language = m.group(1)
            words = get_all_words(language, self.db_path)
            if not words:
                speaker.speak("В базе нет слов")
                return

            speaker.speak(f"Начинаем тренировку {language} на перевод на русский")
            while True:
                foreign, russian = random.choice(words)
                speaker.speak(f"Переведи {foreign}")
                answer = rec.recognize() if rec else input("> ").strip()

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
            words = get_all_words(language, self.db_path)
            if not words:
                speaker.speak("В базе нет слов")
                return

            speaker.speak(f"Начинаем тренировку с русского на {language}")
            while True:
                foreign, russian = random.choice(words)
                speaker.speak(f"Переведи {russian}")
                answer = rec.recognize() if rec else input("> ").strip()

                if not answer or answer.lower() in ("стоп", "выход", "всё"):
                    speaker.speak("Тренировка завершена")
                    break
                if answer.lower() == foreign.lower():
                    speaker.speak("Верно")
                else:
                    speaker.speak(f"Неверно. Правильно: {foreign}")
            return

        speaker.speak("Команда не распознана")