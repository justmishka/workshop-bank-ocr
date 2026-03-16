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
        results = process_ocr(ocr)
        assert len(results) == 1
        assert results[0]["account"] == "000000000"
        assert results[0]["status"] == "OK"
        assert results[0]["valid"] is True

    def test_invalid_account(self):
        ocr = (
            "                           \n"
            "  |  |  |  |  |  |  |  |  |\n"
            "  |  |  |  |  |  |  |  |  |\n"
            "\n"
        )
        results = process_ocr(ocr)
        assert results[0]["status"] == "ERR"
        assert results[0]["valid"] is False

    def test_illegible_account(self):
        ocr = (
            " _  _  _  _  _  _  _  _  _ \n"
            "| || || || |X || || || || |\n"
            "|_||_||_||_||_||_||_||_||_|\n"
            "\n"
        )
        results = process_ocr(ocr)
        assert "?" in results[0]["account"]
        assert results[0]["status"] == "ILL"
        assert results[0]["valid"] is None

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
        results = process_ocr(ocr)
        assert len(results) == 2
        assert results[0]["status"] == "OK"
        assert results[1]["status"] == "OK"

    def test_empty_input(self):
        results = process_ocr("")
        assert results == []
