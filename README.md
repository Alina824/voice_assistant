# Голосовой ассистент

Голосовой ассистент на Python с поддержкой распознавания (Vosk или Whisper) и синтеза речи (pyttsx3). Активация по слову «привет» (настраивается). Команды: таймеры, напоминания, заметки, музыка, мультики, игры (города, математика, викторина, словарь), анекдоты, советы, рандомайзеры и др.

---

## Запуск

### 1. Конфигурация

Скопируйте шаблон и укажите свои пути и параметры:

```bash
copy config.example.json config.json
```

Отредактируйте `config.json`: `music_dir`, `notes_dir`, `videos_dir`, пути к файлам (`jokes_file`, `questions_file`, `advices_file`, `cities_path`, `vocabulary_db_path`), `vosk_model_path` или `whisper_model`, `wake_word`, `voice_index`, `recognizer` (`vosk` или `whisper`).

Переменные окружения (опционально):

- `VOICE_ASSISTANT_CONFIG` — путь к файлу конфига.
- `VOICE_ASSISTANT_<KEY>` — переопределение ключа (например `VOICE_ASSISTANT_MUSIC_DIR`).

### 2. Запуск приложения

```bash
python main.py
```

При первом запуске будет выведен список голосов; в конфиге можно задать `voice_index`.

---

## Тесты

```bash
pip install -r requirements-dev.txt
python -m pytest tests/ -v
```

Тесты: `utils.numeric` (words_to_numbers, parse_number), `utils.filesystem` (list_files, find_file_by_name, resolve_path, path_exists, ensure_directory), `utils.text_files` (load_lines, load_delimited, strip_numbered_prefix).

---

## Изменения в API (после рефакторинга)

- **Конфиг:** все пути и основные параметры — в `config.json`; в `main.py` нет захардкоженных путей.
- **Контракты:** `Recognizer` — `recognize() -> str`; `Speaker` — `speak(text)`, `stop()`; везде `speak` (не `say`), `recognize` (не `listen`).
- **Команды:** единая сигнатура `execute(text, speaker)`. Базовые классы: `Command`, `FileSystemCommand`, `TextFileCommand`, `InteractiveCommand` (в `assistant`).
- **Публичный API:** `assistant/__all__`, `commands/__all__`, `utils/__all__`; контракты в `assistant.contracts` (`RecognizerProtocol`, `SpeakerProtocol`).

Подробнее: `docs/CONTRACTS.md`, `docs/ARCHITECTURE.md`, `docs/SCENARIOS.md`.
