"""Tests for input validation."""
from src.parser import validate_ocr_input
from src.web import process_ocr


class TestValidateOCRInput:
    def test_empty_string(self):
        errors = validate_ocr_input("")
        assert len(errors) == 1
        assert "No OCR input" in str(errors[0])

    def test_whitespace_only(self):
        errors = validate_ocr_input("   \n  \n  ")
        assert len(errors) == 1
        assert "No OCR input" in str(errors[0])

    def test_too_few_lines(self):
        errors = validate_ocr_input(" _ \n| |")
        assert len(errors) == 1
        assert "too short" in str(errors[0])

    def test_invalid_characters(self):
        errors = validate_ocr_input(
            "HELLO WORLD 123456789012345\n"
            "THIS IS NOT OCR TEXT AT ALL\n"
            "JUST RANDOM GARBAGE CONTENT\n"
        )
        assert len(errors) > 0
        assert any("Invalid characters" in str(e) for e in errors)

    def test_valid_input_no_errors(self):
        ocr = (
            " _  _  _  _  _  _  _  _  _ \n"
            "| || || || || || || || || |\n"
            "|_||_||_||_||_||_||_||_||_|\n"
        )
        errors = validate_ocr_input(ocr)
        assert errors == []

    def test_ones_valid_all_spaces(self):
        ocr = (
            "                           \n"
            "  |  |  |  |  |  |  |  |  |\n"
            "  |  |  |  |  |  |  |  |  |\n"
        )
        errors = validate_ocr_input(ocr)
        assert errors == []


class TestProcessOCRValidation:
    def test_empty_returns_error(self):
        result = process_ocr("")
        assert len(result["errors"]) > 0
        assert result["accounts"] == []

    def test_garbage_returns_error(self):
        result = process_ocr("Hello this is not OCR\nJust some text\nNothing valid")
        assert len(result["errors"]) > 0

    def test_valid_returns_accounts(self):
        ocr = (
            " _  _  _  _  _  _  _  _  _ \n"
            "| || || || || || || || || |\n"
            "|_||_||_||_||_||_||_||_||_|\n"
        )
        result = process_ocr(ocr)
        assert result["errors"] == []
        assert len(result["accounts"]) == 1
        assert result["accounts"][0]["account"] == "000000000"
