"""
Протоколы (контракты) для Recognizer, Speaker и описание Command.
Используются для типизации; реализации (VoskRecognizer, WhisperRecognizer, PyttsxSpeaker)
соответствуют этим контрактам по структуре.
"""
from __future__ import annotations

__all__ = ["RecognizerProtocol", "SpeakerProtocol"]

from typing import Protocol, runtime_checkable


@runtime_checkable
class RecognizerProtocol(Protocol):
    """
    Распознавание речи. Вход: аудио (микрофон). Выход: строка в UTF-8.
    """

    def recognize(self) -> str:
        """
        Слушает микрофон, возвращает распознанный текст.
        Пустая строка — тишина или не распознано.
        """
        ...


@runtime_checkable
class SpeakerProtocol(Protocol):
    """
    Синтез речи. Единый метод — speak; say не используется.
    """

    def speak(self, text: str) -> None:
        """Озвучить текст. Кодировка: UTF-8."""
        ...

    def stop(self) -> None:
        """Остановить воспроизведение (при выходе и т.п.)."""
        ...


# Command — ABC в assistant.core:
#   matches(text: str) -> bool
#   execute(text: str, speaker: SpeakerProtocol) -> None
# Опционально: name, help_text (атрибуты).
