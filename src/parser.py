"""OCR digit parser — converts ASCII art account numbers to strings."""

DIGIT_PATTERNS = {
    (" _ "
     "| |"
     "|_|"): "0",
    ("   "
     "  |"
     "  |"): "1",
    (" _ "
     " _|"
     "|_ "): "2",
    (" _ "
     " _|"
     " _|"): "3",
    ("   "
     "|_|"
     "  |"): "4",
    (" _ "
     "|_ "
     " _|"): "5",
    (" _ "
     "|_ "
     "|_|"): "6",
    (" _ "
     "  |"
     "  |"): "7",
    (" _ "
     "|_|"
     "|_|"): "8",
    (" _ "
     "|_|"
     " _|"): "9",
}


def parse_digit(top: str, mid: str, bot: str) -> str:
    """Parse a single 3x3 character block into a digit character.

    Returns '?' if the pattern is not recognized.
    """
    pattern = top + mid + bot
    return DIGIT_PATTERNS.get(pattern, "?")


def parse_entry(lines: list[str]) -> str:
    """Parse a 3-line OCR entry into a 9-digit account number string.

    Each line should be 27 characters. Digits are 3 characters wide.
    Unrecognized patterns become '?'.
    """
    if len(lines) < 3:
        raise ValueError(f"Entry must have at least 3 lines, got {len(lines)}")

    top, mid, bot = lines[0], lines[1], lines[2]

    # Pad lines to 27 characters if shorter
    top = top.ljust(27)
    mid = mid.ljust(27)
    bot = bot.ljust(27)

    digits = []
    for i in range(9):
        start = i * 3
        end = start + 3
        digit = parse_digit(top[start:end], mid[start:end], bot[start:end])
        digits.append(digit)

    return "".join(digits)


class ParseError:
    """Represents a validation error found during parsing."""
    def __init__(self, message: str, line_number: int = None):
        self.message = message
        self.line_number = line_number

    def __repr__(self):
        if self.line_number is not None:
            return f"Line {self.line_number}: {self.message}"
        return self.message


def validate_ocr_input(content: str) -> list:
    """Validate OCR input and return list of errors (empty = valid).

    Checks: not empty, contains OCR characters only, lines form valid entries.
    """
    errors = []

    if not content or not content.strip():
        errors.append(ParseError("No OCR input provided"))
        return errors

    lines = content.split("\n")
    # Remove trailing empty lines
    while lines and lines[-1] == "":
        lines.pop()

    if len(lines) < 3:
        errors.append(ParseError(
            f"Input too short — need at least 3 lines for one entry, got {len(lines)}"
        ))
        return errors

    # Check for invalid characters (only space, pipe, underscore allowed in OCR)
    valid_chars = set(" |_\n")
    for i, line in enumerate(lines):
        if i % 4 == 3:  # separator lines can be anything
            continue
        invalid = set(line) - valid_chars
        if invalid:
            errors.append(ParseError(
                f"Invalid characters found: {invalid}",
                line_number=i + 1,
            ))

    return errors


def parse_file(content: str) -> list[str]:
    """Parse an OCR file into a list of account number strings.

    The file format: each entry is 4 lines (3 digit lines + 1 blank separator).
    The blank separator line is always the 4th line of each entry.
    Note: digit "1" has an all-spaces first line, so we cannot use
    blank detection — we must use strict 4-line grouping.
    """
    if not content or not content.strip():
        return []

    lines = content.split("\n")

    # Remove trailing empty line if present (from trailing newline)
    while lines and lines[-1] == "":
        lines.pop()

    accounts = []
    i = 0
    while i + 2 < len(lines):
        entry_lines = lines[i:i + 3]
        account = parse_entry(entry_lines)
        accounts.append(account)

        # Skip the 3 digit lines + 1 blank separator
        i += 4

    return accounts
