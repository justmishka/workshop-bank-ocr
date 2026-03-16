"""Tests for web server API."""
from src.web import process_ocr


class TestProcessOCR:
    def test_valid_account(self):
        ocr = (
            " _  _  _  _  _  _  _  _  _ \n"
            "| || || || || || || || || |\n"
            "|_||_||_||_||_||_||_||_||_|\n"
            "\n"
        )
        result = process_ocr(ocr)
        assert result["errors"] == []
        assert len(result["accounts"]) == 1
        assert result["accounts"][0]["account"] == "000000000"
        assert result["accounts"][0]["status"] == "OK"
        assert result["accounts"][0]["valid"] is True

    def test_invalid_account(self):
        ocr = (
            "                           \n"
            "  |  |  |  |  |  |  |  |  |\n"
            "  |  |  |  |  |  |  |  |  |\n"
            "\n"
        )
        result = process_ocr(ocr)
        assert result["accounts"][0]["status"] == "ERR"
        assert result["accounts"][0]["valid"] is False

    def test_illegible_account(self):
        ocr = (
            " _  _  _  _  _  _  _  _  _ \n"
            "| || || || |X || || || || |\n"
            "|_||_||_||_||_||_||_||_||_|\n"
            "\n"
        )
        result = process_ocr(ocr)
        # Input has invalid char 'X' — validation catches it
        assert len(result["errors"]) > 0

    def test_multiple_accounts(self):
        ocr = (
            " _  _  _  _  _  _  _  _  _ \n"
            "| || || || || || || || || |\n"
            "|_||_||_||_||_||_||_||_||_|\n"
            "\n"
            "    _  _     _  _  _  _  _ \n"
            "  | _| _||_||_ |_   ||_||_|\n"
            "  ||_  _|  | _||_|  ||_| _|\n"
            "\n"
        )
        result = process_ocr(ocr)
        assert len(result["accounts"]) == 2
        assert result["accounts"][0]["status"] == "OK"
        assert result["accounts"][1]["status"] == "OK"

    def test_empty_input(self):
        result = process_ocr("")
        assert len(result["errors"]) > 0
        assert result["accounts"] == []
