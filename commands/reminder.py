import re
import threading
from datetime import datetime, timedelta
from assistant.core import Command

NUMBERS = {
    "ноль": 0,
    "один": 1,
    "два": 2,
    "три": 3,
    "четыре": 4,
    "пять": 5,
    "шесть": 6,
    "семь": 7,
    "восемь": 8,
    "девять": 9,
    "десять": 10,
    "одиннадцать": 11,
    "двенадцать": 12,
    "тринадцать": 13,
    "четырнадцать": 14,
    "пятнадцать": 15,
    "шестнадцать": 16,
    "семнадцать": 17,
    "восемнадцать": 18,
    "девятнадцать": 19,
    "двадцать": 20,
    "двадцать одна": 21,
    "двадцать две": 22,
    "двадцать три": 23,
    "двадцать четыре": 24,
    "двадцать пять": 25,
    "двадцать шесть": 26,
    "двадцать семь": 27,
    "двадцать восемь": 28,
    "двадцать девять": 29,
    "тридцать": 30,
    "тридцать одна": 31,
    "тридцать две": 32,
    "тридцать три": 33,
    "тридцать четыре": 34,
    "тридцать пять": 35,
    "тридцать шесть": 36,
    "тридцать семь": 37,
    "тридцать восемь": 38,
    "тридцать девять": 39,
    "сорок": 40,
    "сорок один": 41,
    "сорок два": 42,
    "сорок три": 43,
    "сорок четыре": 44,
    "сорок пять": 45,
    "сорок шесть": 46,
    "сорок семь": 47,
    "сорок восемь": 48,
    "сорок девять": 49,
    "пятьдесят": 50,
    "пятьдесят один": 51,
    "пятьдесят два": 52,
    "пятьдесят три": 53,
    "пятьдесят четыре": 54,
    "пятьдесят пять": 55,
    "пятьдесят шесть": 56,
    "пятьдесят семь": 57,
    "пятьдесят восемь": 58,
    "пятьдесят девять": 59,
}

def words_to_numbers(text: str) -> str:
    words = text.lower().split()
    result = []
    i = 0
    while i < len(words):
        if i + 1 < len(words):
            pair = f"{words[i]} {words[i+1]}"
            if pair in NUMBERS:
                result.append(str(NUMBERS[pair]))
                i += 2
                continue
        if words[i] in NUMBERS:
            result.append(str(NUMBERS[words[i]]))
        else:
            result.append(words[i])
        i += 1
    return " ".join(result)



class ReminderCommand(Command):
    def __init__(self):
        super().__init__(name="напоминание")
        self.help_text = ("Форматы: "
                          "'Поставь напоминание ужин на 17', "
                          "'Поставь напоминание бильярд на 17 05', "
                          "'Напоминание встреча на 18 30'.")

    def matches(self, text: str) -> bool:
        return "напоминание" in text

    def execute(self, text: str, speaker) -> None:
        cleaned = words_to_numbers(text.lower())

        cleaned = cleaned.replace("поставь", "").replace("напоминание", "").strip()

        match = re.search(r"(.+?) на (\d{1,2})(?:[:\s](\d{1,2}))?", cleaned)
        if not match:
            speaker.speak("Не поняла время для напоминания.")
            return

        message = match.group(1).strip()
        hour = int(match.group(2))
        minute = int(match.group(3)) if match.group(3) else 0

        now = datetime.now()
        reminder_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)

        if reminder_time <= now:
            reminder_time += timedelta(days=1)

        delay = (reminder_time - now).total_seconds()

        speaker.speak(f"Напоминание '{message}' установлено на {reminder_time.strftime('%H:%M')}.")

        def notify():
            speaker.speak(f"Напоминание: {message}")

        t = threading.Timer(delay, notify)
        t.daemon = True
        t.start()
