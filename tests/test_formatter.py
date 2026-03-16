"""Tests for output formatter."""
from src.formatter import classify_account, format_output


class TestClassifyAccount:
    def test_valid_account(self):
        assert classify_account("345882865") == "345882865"

    def test_invalid_checksum(self):
        assert classify_account("664371495") == "664371495 ERR"

    def test_illegible_digits(self):
        assert classify_account("86110??36") == "86110??36 ILL"

    def test_all_zeros_valid(self):
        assert classify_account("000000000") == "000000000"

    def test_all_ones_invalid(self):
        assert classify_account("111111111") == "111111111 ERR"


class TestFormatOutput:
    def test_single_valid_entry(self):
        content = (
            "    _  _     _  _  _  _  _ \n"
            "  | _| _||_||_ |_   ||_||_|\n"
            "  ||_  _|  | _||_|  ||_| _|\n"
            "\n"
        )
        result = format_output(content)
        assert result == "123456789"

    def test_mixed_entries(self):
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
        lines = format_output(content).split("\n")
        assert lines[0] == "000000000"
        assert lines[1] == "111111111 ERR"

    def test_empty_input(self):
        assert format_output("") == ""
