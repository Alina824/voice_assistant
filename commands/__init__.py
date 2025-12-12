from .time_command import TimeCommand
from .time_command import TimeCommand
from .timer import TimerCommand
from  .reminder import ReminderCommand
from .note import NoteCommand
from .note_reader import NoteReaderCommand
from .delete_note_command import DeleteNoteCommand
from .music import MusicCommand
from .cities_game import CitiesGameCommand
from .vocabulary import VocabularyCommand
from .math_training import MathTrainerCommand
from .help import HelpCommand
from .multfilms import CartoonCommand
from .stop_command import StopCommand
from .pause_resume import PauseCommand
from .pause_resume import ResumeCommand
from .sleep import SleepCommand
from .wake import WakeCommand
from .sneezing_command import SneezingCommand
from .rock_paper_scissors_command import RockPaperScissorsCommand
from .joke import JokeCommand
from .unit_converter import UnitConvertCommand
from .quiz import QuizCommand
from .manul_counter import ManulCounterCommand
from .random import RandomNumberCommand
from .coin_flip import CoinFlipCommand
from .dice import DiceFlipCommand
from .funny_advice import AdviceCommand


__all__ = ["TimeCommand", "TimerCommand", "ReminderCommand", "NoteCommand", "NoteReaderCommand", "DeleteNoteCommand",
           "MusicCommand", "CitiesGameCommand", "VocabularyCommand", "MathTrainerCommand", "HelpCommand",
           "CartoonCommand", "StopCommand", "PauseCommand", "ResumeCommand", "SleepCommand", "WakeCommand",
           "SneezingCommand", "RockPaperScissorsCommand", "JokeCommand", "UnitConvertCommand", "QuizCommand",
           "ManulCounterCommand", "RandomNumberCommand", "CoinFlipCommand", "DiceFlipCommand", "AdviceCommand"]