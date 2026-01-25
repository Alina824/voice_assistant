"""Тесты для utils.filesystem на временной директории."""

import os
import tempfile
from pathlib import Path

import pytest

from utils.filesystem import (
    list_files,
    find_file_by_name,
    resolve_path,
    path_exists,
    ensure_directory,
)


@pytest.fixture
def tmpdir():
    """Временная директория; после теста удаляется."""
    with tempfile.TemporaryDirectory() as d:
        yield d


def test_list_files_empty_dir(tmpdir):
    assert list_files(tmpdir) == []
    assert list_files(tmpdir, ".txt") == []


def test_list_files_all_extensions(tmpdir):
    (Path(tmpdir) / "a.txt").write_text("")
    (Path(tmpdir) / "b.mp3").write_text("")
    (Path(tmpdir) / "c.MP3").write_text("")
    (Path(tmpdir) / "d.log").write_text("")
    names = list_files(tmpdir)
    assert set(names) == {"a.txt", "b.mp3", "c.MP3", "d.log"}


def test_list_files_filter_by_extension(tmpdir):
    (Path(tmpdir) / "a.txt").write_text("")
    (Path(tmpdir) / "b.mp3").write_text("")
    (Path(tmpdir) / "c.mp3").write_text("")
    assert set(list_files(tmpdir, ".mp3")) == {"b.mp3", "c.mp3"}
    assert list_files(tmpdir, ".txt") == ["a.txt"]
    assert list_files(tmpdir, ".xyz") == []


def test_list_files_ignores_subdirs(tmpdir):
    (Path(tmpdir) / "file.txt").write_text("")
    (Path(tmpdir) / "sub").mkdir()
    (Path(tmpdir) / "sub" / "inner.txt").write_text("")
    assert list_files(tmpdir, ".txt") == ["file.txt"]


def test_list_files_nonexistent_dir():
    assert list_files("/nonexistent/path/12345") == []


def test_find_file_by_name(tmpdir):
    (Path(tmpdir) / "my track.mp3").write_text("")
    (Path(tmpdir) / "other.mp3").write_text("")
    p = find_file_by_name(tmpdir, "my track", (".mp3",))
    assert p is not None
    assert "my track" in p or "my" in p
    assert p.endswith(".mp3")


def test_find_file_by_name_fuzzy(tmpdir):
    (Path(tmpdir) / "Summer Hit 2024.mp3").write_text("")
    # подстрока без пробелов
    p = find_file_by_name(tmpdir, "summer hit", (".mp3",))
    assert p is not None and p.endswith(".mp3")


def test_find_file_by_name_not_found(tmpdir):
    (Path(tmpdir) / "a.mp3").write_text("")
    assert find_file_by_name(tmpdir, "xyz", (".mp3",)) is None
    assert find_file_by_name(tmpdir, "a", (".txt",)) is None


def test_find_file_by_name_nonexistent_dir():
    assert find_file_by_name("/nonexistent/12345", "x", (".mp3",)) is None


def test_resolve_path():
    assert resolve_path("/base", "a", "b") == os.path.join("/base", "a", "b")
    assert resolve_path("C:\\data", "videos", "s1") == os.path.join("C:\\data", "videos", "s1")


def test_path_exists(tmpdir):
    f = Path(tmpdir) / "f.txt"
    f.write_text("")
    assert path_exists(str(f)) is True
    assert path_exists(str(Path(tmpdir) / "nope")) is False


def test_ensure_directory(tmpdir):
    sub = os.path.join(tmpdir, "a", "b", "c")
    ensure_directory(sub)
    assert os.path.isdir(sub)
    ensure_directory(sub)  # повторный вызов не должен падать
    assert os.path.isdir(sub)
