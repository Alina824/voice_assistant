from typing import List, Tuple, Optional, Callable

__all__ = ["strip_numbered_prefix", "load_lines", "load_delimited"]

def strip_numbered_prefix(line: str) -> str:
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
