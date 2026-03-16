"""Tests for checksum validation."""
from src.checksum import is_valid


class TestChecksum:
    def test_valid_account(self):
        assert is_valid("345882865") is True

    def test_invalid_account(self):
        assert is_valid("664371495") is False

    def test_all_zeros_valid(self):
        # 0+0+0+...+0 = 0, 0 mod 11 = 0
        assert is_valid("000000000") is True

    def test_illegible_returns_none(self):
        assert is_valid("86110??36") is None

    def test_123456789(self):
        # d1=9, d2=8, d3=7, ..., d9=1
        # 1*9 + 2*8 + 3*7 + 4*6 + 5*5 + 6*4 + 7*3 + 8*2 + 9*1
        # = 9 + 16 + 21 + 24 + 25 + 24 + 21 + 16 + 9 = 165
        # 165 mod 11 = 0
        assert is_valid("123456789") is True

    def test_single_question_mark_returns_none(self):
        assert is_valid("12345678?") is None

    def test_all_ones_invalid(self):
        # 1+2+3+4+5+6+7+8+9 = 45, 45 mod 11 = 1
        assert is_valid("111111111") is False
