"""Утилиты для загрузки и парсинга текстовых файлов."""

from typing import List, Tuple, Optional, Callable

__all__ = ["strip_numbered_prefix", "load_lines", "load_delimited"]


def strip_numbered_prefix(line: str) -> str:
    """Срезает префикс вида '1. ' или '42. ' с начала строки. Для use как parse_line в load_lines."""
    s = line.strip() if line else ""
    if not s:
        return ""
    if s[0].isdigit() and "." in s:
        return s.split(".", 1)[1].strip()
    return s


def load_lines(
    filepath: str,
    parse_line: Optional[Callable[[str], str]] = None,
    skip_empty: bool = True,
) -> List[str]:
    """
    Загружает строки из файла.
    - parse_line: вызывается для каждой непустой (после strip) строки; по умолчанию strip.
      Можно передать strip_numbered_prefix для формата «1. текст».
    - skip_empty: не добавлять пустые строки после strip/parse_line.
    """
    result = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                s = line.strip()
                if parse_line is not None:
                    s = parse_line(s) if s else ""
                if skip_empty and not s:
                    continue
                result.append(s)
    except FileNotFoundError:
        pass
    return result


def load_delimited(
    filepath: str,
    delimiter: str = ";",
    skip_empty: bool = True,
) -> List[Tuple[str, ...]]:
    """
    Загружает строки в формате «часть1;часть2;...», возвращает список кортежей.
    Для «вопрос;ответ» и аналогов. Строки без delimiter пропускаются.
    """
    result = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                s = line.strip()
                if not s or delimiter not in s:
                    if skip_empty:
                        continue
                parts = tuple(p.strip() for p in s.split(delimiter, 1))
                if skip_empty and not all(parts):
                    continue
                result.append(parts)
    except FileNotFoundError:
        pass
    return result
