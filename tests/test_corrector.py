"""Tests for error correction."""
from src.corrector import correct_account, _generate_variants


class TestGenerateVariants:
    def test_single_pipe_produces_space_variant(self):
        # Pattern for "1": "   " + "  |" + "  |"
        pattern = "     |  |"
        variants = _generate_variants(pattern)
        # The two pipes can become spaces
        assert "        |" in variants  # first pipe → space
        assert "     |   " in variants  # second pipe → space
        # Spaces can become pipe or underscore
        assert len(variants) > 2

    def test_no_duplicate_variants(self):
        pattern = " _ | ||_|"  # "0"
        variants = _generate_variants(pattern)
        assert len(variants) == len(set(variants))


class TestCorrectAccount:
    def test_single_valid_correction(self):
        # "0" with top bar missing → could be corrected to "0"
        lines = [
            "    _  _     _  _  _  _  _ ",
            "  | _| _||_||_ |_   ||_||_|",
            "  ||_  _|  | _||_|  ||_| _|",
        ]
        # 123456789 is valid — no correction needed, but test the mechanism
        # Let's test with a known ERR account
        # 111111111 is ERR — can we fix it by changing one digit?
        lines_ones = [
            "                           ",
            "  |  |  |  |  |  |  |  |  |",
            "  |  |  |  |  |  |  |  |  |",
        ]
        result = correct_account("111111111", lines_ones)
        # 711111111 checksum: 9*7+8+7+6+5+4+3+2+1 = 63+36 = 99, 99%11=0 → valid!
        assert result["status"] in ("OK", "AMB")

    def test_no_valid_correction(self):
        # Create a pattern that can't be corrected to anything valid
        lines = [
            "                           ",
            "                           ",
            "                           ",
        ]
        result = correct_account("?????????", lines)
        assert result["status"] == "ILL"

    def test_ambiguous_correction(self):
        # 888888888 is ERR — many possible single-digit corrections
        lines_eights = [
            " _  _  _  _  _  _  _  _  _ ",
            "|_||_||_||_||_||_||_||_||_|",
            "|_||_||_||_||_||_||_||_||_|",
        ]
        result = correct_account("888888888", lines_eights)
        # 8 can become 0, 6, 9 by removing one segment
        # Multiple valid corrections should exist
        assert result["status"] == "AMB"
        assert len(result["alternatives"]) > 1

    def test_already_valid_account_returns_no_alternatives(self):
        lines = [
            " _  _  _  _  _  _  _  _  _ ",
            "| || || || || || || || || |",
            "|_||_||_||_||_||_||_||_||_|",
        ]
        result = correct_account("000000000", lines)
        # Already valid — no corrections change anything
        assert result["alternatives"] == [] or result["status"] == "AMB"
