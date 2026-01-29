"""
Загрузка конфигурации из JSON. Значения по умолчанию для отсутствующих ключей.
Override через переменные окружения: VOICE_ASSISTANT_<KEY> (ключ в UPPER_CASE).
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

_CONFIG_DIR = Path(__file__).resolve().parent
_DEFAULT_CONFIG_PATH = _CONFIG_DIR / "config.json"

_DEFAULTS = {
    "music_dir": "music",
    "notes_dir": "notes",
    "videos_dir": "videos",
    "jokes_file": "data/jokes.txt",
    "questions_file": "data/questions.txt",
    "advices_file": "data/advices",
    "cities_path": "data/cities_5000.csv",
    "vocabulary_db_path": "words.db",
    "vosk_model_path": "model",
    "whisper_model": "small",
    "wake_word": "привет",
    "voice_index": 0,
    "recognizer": "vosk",
}


def _env_override(key: str) -> str | None:
    """VOICE_ASSISTANT_<KEY> — например VOICE_ASSISTANT_MUSIC_DIR."""
    env_key = "VOICE_ASSISTANT_" + key.upper()
    return os.environ.get(env_key)


def load_config(path: str | Path | None = None) -> dict[str, Any]:
    """
    Загружает конфиг из JSON. Если файла нет или ключ отсутствует — подставляются _DEFAULTS.
    Переменные окружения: VOICE_ASSISTANT_CONFIG — путь к конфигу;
    VOICE_ASSISTANT_<KEY> — переопределение значения ключа.
    """
    config = _DEFAULTS.copy()
    cfg_path = Path(path or os.environ.get("VOICE_ASSISTANT_CONFIG") or _DEFAULT_CONFIG_PATH)

    if cfg_path.exists():
        try:
            with open(cfg_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict):
                config.update(data)
        except (json.JSONDecodeError, OSError) as e:
            print(f"Предупреждение: не удалось загрузить {cfg_path}: {e}")

    for key in list(config.keys()):
        ov = _env_override(key)
        if ov is not None:
            if key == "voice_index":
                try:
                    config[key] = int(ov)
                except ValueError:
                    pass
            else:
                config[key] = ov

    return config


def save_example_config(path: str | Path | None = None) -> None:
    """Сохраняет config.example.json с текущими _DEFAULTS (для документации)."""
    p = Path(path) if path else _CONFIG_DIR / "config.example.json"
    with open(p, "w", encoding="utf-8") as f:
        json.dump(_DEFAULTS, f, ensure_ascii=False, indent=2)
