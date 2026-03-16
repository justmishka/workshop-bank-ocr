"""Tests for OCR digit parser."""
import pytest
from src.parser import parse_digit, parse_entry, parse_file


class TestParseDigit:
    def test_zero(self):
        assert parse_digit(" _ ", "| |", "|_|") == "0"

    def test_one(self):
        assert parse_digit("   ", "  |", "  |") == "1"

    def test_two(self):
        assert parse_digit(" _ ", " _|", "|_ ") == "2"

    def test_three(self):
        assert parse_digit(" _ ", " _|", " _|") == "3"

    def test_four(self):
        assert parse_digit("   ", "|_|", "  |") == "4"

    def test_five(self):
        assert parse_digit(" _ ", "|_ ", " _|") == "5"

    def test_six(self):
        assert parse_digit(" _ ", "|_ ", "|_|") == "6"

    def test_seven(self):
        assert parse_digit(" _ ", "  |", "  |") == "7"

    def test_eight(self):
        assert parse_digit(" _ ", "|_|", "|_|") == "8"

    def test_nine(self):
        assert parse_digit(" _ ", "|_|", " _|") == "9"

    def test_unrecognized_returns_question_mark(self):
        assert parse_digit("   ", "   ", "   ") == "?"


class TestParseEntry:
    def test_all_zeros(self):
        lines = [
            " _  _  _  _  _  _  _  _  _ ",
            "| || || || || || || || || |",
            "|_||_||_||_||_||_||_||_||_|",
        ]
        assert parse_entry(lines) == "000000000"

    def test_all_ones(self):
        lines = [
            "                           ",
            "  |  |  |  |  |  |  |  |  |",
            "  |  |  |  |  |  |  |  |  |",
        ]
        assert parse_entry(lines) == "111111111"

    def test_123456789(self):
        lines = [
            "    _  _     _  _  _  _  _ ",
            "  | _| _||_||_ |_   ||_||_|",
            "  ||_  _|  | _||_|  ||_| _|",
        ]
        assert parse_entry(lines) == "123456789"

    def test_illegible_digit(self):
        lines = [
            "    _  _     _  _  _  _  _ ",
            "  | _| _||_||_ |_   ||_||_|",
            "  ||_  _|  | _||_|  ||_| _|",
        ]
        # Corrupt the first digit
        lines[0] = "___" + lines[0][3:]
        result = parse_entry(lines)
        assert result[0] == "?"

    def test_short_lines_padded(self):
        lines = [
            " _ ",
            "| |",
            "|_|",
        ]
        result = parse_entry(lines)
        assert result[0] == "0"


class TestParseFile:
    def test_single_entry(self):
        content = (
            " _  _  _  _  _  _  _  _  _ \n"
            "| || || || || || || || || |\n"
            "|_||_||_||_||_||_||_||_||_|\n"
            "\n"
        )
        result = parse_file(content)
        assert result == ["000000000"]

    def test_multiple_entries(self):
        content = (
            " _  _  _  _  _  _  _  _  _ \n"
            "| || || || || || || || || |\n"
            "|_||_||_||_||_||_||_||_||_|\n"
            "\n"
            "                           \n"
            "  |  |  |  |  |  |  |  |  |\n"
            "  |  |  |  |  |  |  |  |  |\n"
            "\n"
        )
        result = parse_file(content)
        assert result == ["000000000", "111111111"]

    def test_empty_file(self):
        result = parse_file("")
        assert result == []


class TestParseEntryEdgeCases:
    """Dex QA — additional edge case tests."""

    def test_entry_with_too_few_lines_raises(self):
        with pytest.raises(ValueError, match="at least 3 lines"):
            parse_entry(["   ", "  |"])

    def test_all_twos(self):
        lines = [
            " _  _  _  _  _  _  _  _  _ ",
            " _| _| _| _| _| _| _| _| _|",
            "|_ |_ |_ |_ |_ |_ |_ |_ |_ ",
        ]
        assert parse_entry(lines) == "222222222"

    def test_all_threes(self):
        lines = [
            " _  _  _  _  _  _  _  _  _ ",
            " _| _| _| _| _| _| _| _| _|",
            " _| _| _| _| _| _| _| _| _|",
        ]
        assert parse_entry(lines) == "333333333"

    def test_all_fours(self):
        lines = [
            "                           ",
            "|_||_||_||_||_||_||_||_||_|",
            "  |  |  |  |  |  |  |  |  |",
        ]
        assert parse_entry(lines) == "444444444"

    def test_all_fives(self):
        lines = [
            " _  _  _  _  _  _  _  _  _ ",
            "|_ |_ |_ |_ |_ |_ |_ |_ |_ ",
            " _| _| _| _| _| _| _| _| _|",
        ]
        assert parse_entry(lines) == "555555555"

    def test_mixed_illegible_and_valid(self):
        lines = [
            " _  _  _  _  _  _  _  _  _ ",
            "| || || || || || || || || |",
            "|_||_||_||_||_||_||_||_||_|",
        ]
        # Corrupt middle digit
        lines[1] = lines[1][:12] + "X" + lines[1][13:]
        result = parse_entry(lines)
        assert result[4] == "?"
        assert result[0] == "0"
