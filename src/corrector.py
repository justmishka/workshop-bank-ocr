"""Error correction — attempts to fix ERR and ILL accounts."""
from typing import List
from src.parser import DIGIT_PATTERNS, parse_digit
from src.checksum import is_valid


# Reverse mapping: digit -> pattern string (9 chars: top+mid+bot)
DIGIT_TO_PATTERN = {v: k for k, v in DIGIT_PATTERNS.items()}

# Characters that can appear in OCR patterns
PIPE_UNDERSCORE = "|_"
SPACE = " "


def _generate_variants(pattern: str) -> List[str]:
    """Generate all single-character modifications of a 9-char pattern.

    Each pipe or underscore can be replaced with a space, and each space
    can be replaced with a pipe or underscore.
    """
    variants = []
    for i, char in enumerate(pattern):
        if char in PIPE_UNDERSCORE:
            # Replace with space
            variant = pattern[:i] + SPACE + pattern[i + 1:]
            variants.append(variant)
        elif char == SPACE:
            # Replace with pipe or underscore
            for replacement in PIPE_UNDERSCORE:
                variant = pattern[:i] + replacement + pattern[i + 1:]
                variants.append(variant)
    return variants


def _pattern_to_digit(pattern: str) -> str:
    """Convert a 9-char pattern to a digit, or '?' if unrecognized."""
    return DIGIT_PATTERNS.get(pattern, "?")


def correct_account(account: str, entry_lines: List[str]) -> dict:
    """Attempt to correct an ERR or ILL account number.

    For each digit position, generates all single-character modifications
    and checks if the resulting account number has a valid checksum.

    Returns:
        {"account": str, "status": str, "alternatives": list[str]}
    """
    top, mid, bot = entry_lines[0], entry_lines[1], entry_lines[2]
    top = top.ljust(27)
    mid = mid.ljust(27)
    bot = bot.ljust(27)

    valid_alternatives = []

    for pos in range(9):
        start = pos * 3
        end = start + 3
        original_pattern = top[start:end] + mid[start:end] + bot[start:end]

        for variant_pattern in _generate_variants(original_pattern):
            digit = _pattern_to_digit(variant_pattern)
            if digit == "?":
                continue

            # Build candidate account with this digit substituted
            candidate = list(account)
            candidate[pos] = digit
            candidate_str = "".join(candidate)

            if "?" not in candidate_str and is_valid(candidate_str):
                if candidate_str != account and candidate_str not in valid_alternatives:
                    valid_alternatives.append(candidate_str)

    if len(valid_alternatives) == 1:
        return {
            "account": valid_alternatives[0],
            "status": "OK",
            "alternatives": [],
        }
    elif len(valid_alternatives) > 1:
        return {
            "account": account,
            "status": "AMB",
            "alternatives": sorted(valid_alternatives),
        }
    else:
        return {
            "account": account,
            "status": "ILL" if "?" in account else "ERR",
            "alternatives": [],
        }
