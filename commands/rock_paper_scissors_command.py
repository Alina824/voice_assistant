import random
from assistant.core import Command

class RockPaperScissorsCommand(Command):
    def __init__(self, recognizer, speaker):
        self.recognizer = recognizer
        self.speaker = speaker
        self.words = {
            "камень": "rock",
            "ножницы": "scissors",
            "бумага": "paper"
        }

    def matches(self, text: str) -> bool:
        return "камень" in text and "ножницы" in text and "бумага" in text

    def execute(self, text: str):
        self.speaker.say("Раз, два, три!")

        bot_choice_word = random.choice(list(self.words.keys()))
        bot_choice = self.words[bot_choice_word]

        self.speaker.say("Твой ход?")
        user_text = self.recognizer.listen().lower()

        user_choice = None
        for w in self.words:
            if w in user_text:
                user_choice = self.words[w]
                break

        if not user_choice:
            self.speaker.say("Я не расслышал твой выбор. Давай попробуем снова.")
            return

        self.speaker.say(f"Я — {bot_choice_word}!")

        result = self.determine_winner(user_choice, bot_choice)

        if result == "draw":
            self.speaker.say("Ничья!")
        elif result == "user":
            self.speaker.say("Ты победил!")
        else:
            self.speaker.say("Я победил!")

    @staticmethod
    def determine_winner(user, bot):
        if user == bot:
            return "draw"
        if (
            (user == "rock" and bot == "scissors")
            or (user == "scissors" and bot == "paper")
            or (user == "paper" and bot == "rock")
        ):
            return "user"
        return "bot"
