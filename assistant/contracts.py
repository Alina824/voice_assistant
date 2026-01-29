from __future__ import annotations

__all__ = ["RecognizerProtocol", "SpeakerProtocol"]

from typing import Protocol, runtime_checkable


@runtime_checkable
class RecognizerProtocol(Protocol):
    def recognize(self) -> str:
        ...


@runtime_checkable
class SpeakerProtocol(Protocol):
    def speak(self, text: str) -> None:
        ...

    def stop(self) -> None:
        ...
