"""Тесты для utils.text_files: load_lines, load_delimited, strip_numbered_prefix."""

import tempfile
from pathlib import Path

import pytest

from utils.text_files import load_lines, load_delimited, strip_numbered_prefix


@pytest.fixture
def tmpfile():
    """Временный файл; после теста удаляется."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False, encoding="utf-8") as f:
        yield f.name
    Path(f.name).unlink(missing_ok=True)


def test_strip_numbered_prefix():
    assert strip_numbered_prefix("1. Текст") == "Текст"
    assert strip_numbered_prefix("42. Длинный номер") == "Длинный номер"
    assert strip_numbered_prefix("просто текст") == "просто текст"
    assert strip_numbered_prefix("") == ""
    assert strip_numbered_prefix("  2.  с пробелами  ") == "с пробелами"


def test_load_lines_simple(tmpfile):
    Path(tmpfile).write_text("a\nb\nc\n", encoding="utf-8")
    assert load_lines(tmpfile) == ["a", "b", "c"]


def test_load_lines_skips_empty(tmpfile):
    Path(tmpfile).write_text("a\n\nb\n  \nc\n", encoding="utf-8")
    assert load_lines(tmpfile) == ["a", "b", "c"]


def test_load_lines_with_parse_line(tmpfile):
    Path(tmpfile).write_text("1. Первый\n2. Второй\n", encoding="utf-8")
    assert load_lines(tmpfile, parse_line=strip_numbered_prefix) == ["Первый", "Второй"]


def test_load_lines_numbered_joke_format(tmpfile):
    """Формат анекдотов/советов: «1. текст»."""
    Path(tmpfile).write_text(
        "1. Первый анекдот.\n2. Второй анекдот.\n\n3. Третий.\n",
        encoding="utf-8",
    )
    got = load_lines(tmpfile, parse_line=strip_numbered_prefix)
    assert got == ["Первый анекдот.", "Второй анекдот.", "Третий."]


def test_load_lines_file_not_found():
    assert load_lines("/nonexistent/file/12345.txt") == []


def test_load_delimited_semicolon(tmpfile):
    Path(tmpfile).write_text("вопрос один;ответ один\nвопрос два;ответ два\n", encoding="utf-8")
    got = load_delimited(tmpfile, delimiter=";")
    assert got == [("вопрос один", "ответ один"), ("вопрос два", "ответ два")]


def test_load_delimited_skips_lines_without_delimiter(tmpfile):
    Path(tmpfile).write_text("вопрос;ответ\nпросто строка\nещё;пара\n", encoding="utf-8")
    got = load_delimited(tmpfile, delimiter=";")
    assert got == [("вопрос", "ответ"), ("ещё", "пара")]


def test_load_delimited_utf8(tmpfile):
    Path(tmpfile).write_text("Сколько?;Пять.\n", encoding="utf-8")
    assert load_delimited(tmpfile, ";") == [("Сколько?", "Пять.")]


def test_load_delimited_file_not_found():
    assert load_delimited("/nonexistent/12345.txt", ";") == []


def test_load_delimited_questions_format(tmpfile):
    """Формат викторины: «вопрос;ответ»."""
    Path(tmpfile).write_text(
        "Столица России?;Москва\nДва плюс два?;Четыре\n",
        encoding="utf-8",
    )
    got = load_delimited(tmpfile, delimiter=";")
    assert got == [("Столица России?", "Москва"), ("Два плюс два?", "Четыре")]
