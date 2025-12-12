import random
from assistant.core import Command


class CitiesGameCommand(Command):
    def __init__(self, db_path="cities.csv"):
        super().__init__(name="города")
        self.help_text = (
            "Скажи 'сыграем в города', чтобы начать игру. "
            "Отвечай названиями городов на нужную букву. "
            "Можно спросить 'что это', чтобы узнать про город."
        )
        self.db = self._load_db(db_path)
        self.session_data = {}

    def matches(self, text: str, user_id="default") -> bool:
        state = self.session_data.get(user_id, {"active": False})
        return state["active"] or "сыграем в города" in text.lower()

    def execute(self, text: str, speaker, user_id="default") -> None:
        text = text.lower().strip()
        state = self.session_data.setdefault(user_id, {
            "active": False,
            "used": set(),
            "last_letter": None,
            "last_city": None
        })

        if not state["active"] and "сыграем в города" in text:
            state["active"] = True
            state["used"].clear()
            state["last_city"] = None
            state["last_letter"] = None
            speaker.speak("Начнём! Назови город.")
            return

        if not state["active"]:
            return

        if "что это" in text and state["last_city"]:
            info = self.db.get(state["last_city"], {})
            speaker.speak(
                f"{state['last_city']} — {info.get('country')}, {info.get('region')}, {info.get('continent')}"
            )
            return

        city = text.capitalize()

        if city not in self.db:
            speaker.speak("Не знаю такого города. Попробуй другой.")
            return
        if city in state["used"]:
            speaker.speak("Уже было. Назови другой город.")
            return

        state["used"].add(city)
        state["last_city"] = city
        state["last_letter"] = self._get_last_letter(city)

        last_letter_lower = state["last_letter"].lower()
        candidates = [c for c in self.db if c not in state["used"] and c[0].lower() == last_letter_lower]

        if not candidates:
            speaker.speak("Я сдаюсь! Ты победил.")
            state["active"] = False
            return

        bot_city = random.choice(candidates)
        state["used"].add(bot_city)
        state["last_city"] = bot_city
        state["last_letter"] = self._get_last_letter(bot_city)
        speaker.speak(f"{bot_city}. Тебе на {state['last_letter'].upper()}.")

    def _load_db(self, path):
        import csv
        db = {}
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                db[row["name"]] = row
        return db

    def _get_last_letter(self, city):
        for ch in reversed(city.lower()):
            if ch not in ["ь", "ъ", "ы", "й"]:
                return ch
        return city[-1].lower()
