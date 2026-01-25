"""Утилиты для навигации по файловой системе."""

import os
from typing import List, Optional

__all__ = [
    "list_files",
    "find_file_by_name",
    "resolve_path",
    "path_exists",
    "ensure_directory",
]

def list_files(directory: str, *extensions: str) -> List[str]:
    """
    Список файлов в директории с указанными расширениями.
    Если extensions пусто — возвращаются все файлы.
    """
    if not os.path.exists(directory):
        return []
    names = []
    for f in os.listdir(directory):
        path = os.path.join(directory, f)
        if os.path.isfile(path):
            if not extensions or any(f.lower().endswith(ext) for ext in extensions):
                names.append(f)
    return names


def find_file_by_name(
    directory: str,
    name: str,
    extensions: tuple = (".mp3",),
) -> Optional[str]:
    """
    Нечёткий поиск файла по подстроке в имени.
    Нормализует пробелы: name и имена файлов приводятся к без-пробельной форме для сравнения.
    """
    if not os.path.exists(directory):
        return None
    name_norm = name.lower().replace(" ", "")
    for f in os.listdir(directory):
        if not any(f.lower().endswith(ext) for ext in extensions):
            continue
        base = os.path.splitext(f)[0].lower().replace(" ", "")
        if name_norm in base:
            return os.path.join(directory, f)
    return None


def resolve_path(base: str, *parts: str) -> str:
    """Собирает путь base / part1 / part2 ..."""
    return os.path.join(base, *parts)


def path_exists(path: str) -> bool:
    """Проверка существования пути."""
    return os.path.exists(path)


def ensure_directory(path: str) -> None:
    """Создаёт директорию, если не существует (makedirs exist_ok=True)."""
    os.makedirs(path, exist_ok=True)
