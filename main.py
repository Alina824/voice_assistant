from config import load_config

from assistant import VoskRecognizer, WhisperRecognizer, PyttsxSpeaker, VoiceAssistant
from commands import (
    TimeCommand, TimerCommand, ReminderCommand,
    NoteCommand, NoteReaderCommand, DeleteNoteCommand,
    MusicCommand, CitiesGameCommand, VocabularyCommand,
    MathTrainerCommand, HelpCommand, CartoonCommand,
    StopCommand, PauseCommand, ResumeCommand,
    SleepCommand, WakeCommand, SneezingCommand, RockPaperScissorsCommand,
    JokeCommand, UnitConvertCommand, QuizCommand,
    ManulCounterCommand, RandomNumberCommand, CoinFlipCommand, DiceFlipCommand, AdviceCommand,
)


def _create_recognizer(cfg):
    if cfg.get("recognizer") == "whisper":
        return WhisperRecognizer(model_name=cfg.get("whisper_model", "small"))
    return VoskRecognizer(model_path=cfg.get("vosk_model_path", "model"))


def _create_commands(assistant, recognizer, speaker, cfg):
    music_cmd = MusicCommand(
        music_dir=cfg["music_dir"],
        recognizer=recognizer,
    )
    reader = NoteReaderCommand(notes_dir=cfg["notes_dir"], recognizer=recognizer)
    cartoon_cmd = CartoonCommand(
        videos_dir=cfg["videos_dir"],
        recognizer=recognizer,
        speaker=speaker,
    )

    commands = [
        TimeCommand(),
        TimerCommand(),
        ReminderCommand(),
        NoteCommand(notes_dir=cfg["notes_dir"]),
        music_cmd,
        CitiesGameCommand(db_path=cfg["cities_path"]),
        VocabularyCommand(db_path=cfg["vocabulary_db_path"], recognizer=recognizer),
        MathTrainerCommand(recognizer, speaker),
        cartoon_cmd,
        StopCommand(),
        PauseCommand([music_cmd, reader, cartoon_cmd]),
        ResumeCommand([music_cmd, reader, cartoon_cmd]),
        SleepCommand(assistant),
        WakeCommand(assistant),
        reader,
        DeleteNoteCommand(reader),
        SneezingCommand(speaker),
        RockPaperScissorsCommand(recognizer, speaker),
        JokeCommand(jokes_file=cfg["jokes_file"], speaker=speaker),
        UnitConvertCommand(speaker),
        QuizCommand(
            questions_file=cfg["questions_file"],
            recognizer=recognizer,
            speaker=speaker,
        ),
        ManulCounterCommand(recognizer, speaker),
        RandomNumberCommand(),
        CoinFlipCommand(),
        DiceFlipCommand(),
        AdviceCommand(advices_file=cfg["advices_file"], speaker=speaker),
    ]

    help_cmd = HelpCommand(commands)
    commands.append(help_cmd)

    return commands


if __name__ == "__main__":
    cfg = load_config()

    recognizer = _create_recognizer(cfg)
    speaker = PyttsxSpeaker()
    speaker.list_voices()
    speaker.set_voice(cfg.get("voice_index", 0))

    assistant = VoiceAssistant(
        recognizer,
        speaker,
        wake_word=cfg.get("wake_word", "привет"),
    )

    for cmd in _create_commands(assistant, recognizer, speaker, cfg):
        assistant.add_command(cmd)

    assistant.run()
