import re
from assistant.core import Command

class UnitConvertCommand(Command):

    def __init__(self, speaker):
        self.speaker = speaker

        self.length_units = {
            "метр": 1.0,
            "метра": 1.0,
            "метров": 1.0,
            "м": 1.0,

            "сантиметр": 0.01,
            "сантиметра": 0.01,
            "сантиметров": 0.01,
            "см": 0.01,

            "фут": 0.3048,
            "фута": 0.3048,
            "футов": 0.3048,
            "ft": 0.3048,

            "верста": 1066.8,
            "версты": 1066.8,
            "верст": 1066.8,

            "сажень": 2.1336,
            "сажени": 2.1336,
            "саженей": 2.1336,

            "миля": 1609.34,
            "мили": 1609.34,
            "miles": 1609.34
        }

        self.mass_units = {
            "грамм": 1.0,
            "грамма": 1.0,
            "граммов": 1.0,
            "г": 1.0,

            "килограмм": 1000.0,
            "килограмма": 1000.0,
            "кг": 1000.0,

            "унция": 28.3495,
            "унции": 28.3495,
            "унций": 28.3495,
            "oz": 28.3495,
        }

        self.speed_units = {
            "километр в час": 1.0,
            "километра в час": 1.0,
            "километров в час": 1.0,
            "км/ч": 1.0,

            "миля в час": 1.60934,
            "мили в час": 1.60934,
            "mph": 1.60934,

            "узел": 1.852,
            "узла": 1.852,
            "узлов": 1.852,
            "knot": 1.852,
            "knots": 1.852,
            "kn": 1.852,
        }

    def matches(self, text: str) -> bool:
        keywords = ["переведи", "сколько будет", "конвертируй"]
        return any(k in text.lower() for k in keywords)

    def execute(self, text: str):
        text = text.lower()

        match_num = re.search(r"(\d+(\.\d+)?)", text)
        if not match_num:
            self.speaker.say("Я не услышала число.")
            return

        value = float(match_num.group(1))

        units = list(self.length_units.keys()) + list(self.mass_units.keys()) + list(self.speed_units.keys())
        unit_from = None
        unit_to = None

        for u in units:
            if f" {u} " in text or text.endswith(" " + u):
                if unit_from is None:
                    unit_from = u
                else:
                    unit_to = u

        if not unit_from or not unit_to:
            self.speaker.say("Не поняла, какие единицы нужно перевести.")
            return

        result = self.convert(value, unit_from, unit_to)

        if result is None:
            self.speaker.say("Эти единицы несовместимы.")
            return

        self.speaker.say(self.pretty(result, unit_to))

    def convert(self, value, u_from, u_to):

        if u_from in self.length_units and u_to in self.length_units:
            meters = value * self.length_units[u_from]
            return meters / self.length_units[u_to]

        if u_from in self.mass_units and u_to in self.mass_units:
            grams = value * self.mass_units[u_from]
            return grams / self.mass_units[u_to]

        if u_from in self.speed_units and u_to in self.speed_units:
            kmh = value * self.speed_units[u_from]
            return kmh / self.speed_units[u_to]

        return None

    def pretty(self, result, unit):

        if "фут" in unit:
            meters = int(result * 0.3048)
            cm = round((result * 0.3048 - meters) * 100)
            return f"{meters} метров {cm} сантиметров"

        if "унц" in unit:
            if result >= 1000:
                return f"{result/1000:.3f} килограмма"
            return f"{result:.1f} граммов"

        if "узл" in unit:
            return f"{result:.1f} узлов"

        if result >= 1:
            return f"{result:.3f} {unit}"
        else:
            return f"{result:.5f} {unit}"
