import pytest

from utils.numeric import words_to_numbers, parse_number


class TestWordsToNumbers:
    def test_single_digit_words(self):
        assert words_to_numbers("один два три") == "1 2 3"
        assert words_to_numbers("ноль") == "0"
        assert words_to_numbers("пять") == "5"

    def test_teens(self):
        assert words_to_numbers("одиннадцать") == "11"
        assert words_to_numbers("девятнадцать") == "19"

    def test_tens(self):
        assert words_to_numbers("двадцать") == "20"
        assert words_to_numbers("тридцать") == "30"
        assert words_to_numbers("пятьдесят") == "50"

    def test_compound_tens(self):
        assert words_to_numbers("двадцать одна") == "21"
        assert words_to_numbers("двадцать один") == "21"
        assert words_to_numbers("тридцать две") == "32"
        assert words_to_numbers("сорок пять") == "45"
        assert words_to_numbers("пятьдесят девять") == "59"

    def test_mixed_with_other_words(self):
        assert words_to_numbers("напомни через пять минут") == "напомни через 5 минут"
        assert words_to_numbers("три манула") == "3 манула"
        assert words_to_numbers("двадцать одна серия") == "21 серия"

    def test_one_and_raz(self):
        assert words_to_numbers("раз") == "1"
        assert words_to_numbers("одна") == "1"
        assert words_to_numbers("две") == "2"


class TestParseNumber:
    def test_digits_only(self):
        assert parse_number("5") == 5
        assert parse_number("42") == 42
        assert parse_number("  10  ") == 10
        assert parse_number("abc 7 xyz") == 7

    def test_single_word(self):
        assert parse_number("один") == 1
        assert parse_number("пять") == 5
        assert parse_number("десять") == 10
        assert parse_number("ноль") == 0

    def test_compound_words(self):
        assert parse_number("двадцать одна") == 21
        assert parse_number("тридцать две") == 32
        assert parse_number("сорок пять") == 45

    def test_embedded_in_phrase(self):
        assert parse_number("через пять минут") == 5
        assert parse_number("скажи три манула") == 3
        assert parse_number("серия двадцать одна") == 21

    def test_empty_or_no_number(self):
        assert parse_number("") is None
        assert parse_number("   ") is None
        assert parse_number("привет") is None
        assert parse_number("нет числа") is None

    def test_first_number_wins(self):
        assert parse_number("5 и 10") == 5
        assert parse_number("три или пять") == 3
