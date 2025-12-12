from assistant import VoskRecognizer, WhisperRecognizer, PyttsxSpeaker, VoiceAssistant
from commands import (
    TimeCommand, TimerCommand, ReminderCommand,
    NoteCommand, NoteReaderCommand, DeleteNoteCommand,
    MusicCommand, CitiesGameCommand, VocabularyCommand,
    MathTrainerCommand, HelpCommand, CartoonCommand,
    StopCommand, PauseCommand, ResumeCommand,
    SleepCommand, WakeCommand, SneezingCommand, RockPaperScissorsCommand, JokeCommand, UnitConvertCommand, QuizCommand,
    ManulCounterCommand, RandomNumberCommand, CoinFlipCommand, DiceFlipCommand, AdviceCommand
)

if __name__ == "__main__":
    recognizer = VoskRecognizer(model_path="model")
    # recognizer = WhisperRecognizer(model_name="small")

    speaker = PyttsxSpeaker()
    speaker.list_voices()
    speaker.set_voice(0)

    assistant = VoiceAssistant(recognizer, speaker, wake_word="привет")

    music_cmd = MusicCommand(music_dir="D:/User/Desktop/Music", recognizer=recognizer)
    reader = NoteReaderCommand(notes_dir="D:/User/Notes", recognizer=recognizer)
    cartoon_cmd = CartoonCommand(videos_dir="D:/User/Videos", recognizer=recognizer, speaker=speaker)

    commands = [TimeCommand(), TimerCommand(), ReminderCommand(), NoteCommand(notes_dir="D:/User/Notes"), music_cmd,
                CitiesGameCommand(db_path="data/cities_5000.csv"), VocabularyCommand(),
                MathTrainerCommand(recognizer, speaker), cartoon_cmd, StopCommand(),
                PauseCommand([music_cmd, reader, cartoon_cmd]), ResumeCommand([music_cmd, reader, cartoon_cmd]),
                SleepCommand(assistant), WakeCommand(assistant), reader, DeleteNoteCommand(reader),
                SneezingCommand(speaker), RockPaperScissorsCommand(recognizer, speaker),
                JokeCommand(jokes_file="D:/MyProject/data/jokes.txt", speaker=speaker), UnitConvertCommand(speaker),
                QuizCommand(questions_file="D:/MyProject/data/questions.txt", recognizer=recognizer, speaker=speaker),
                ManulCounterCommand(recognizer, speaker), RandomNumberCommand(), CoinFlipCommand(), DiceFlipCommand(),
                AdviceCommand(advices_file="D:/MyProject/data/advices.txt", speaker=speaker)]

    for cmd in commands:
        assistant.add_command(cmd)

    assistant.run()
