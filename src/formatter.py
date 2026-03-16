"""Output formatter — combines parser + checksum into status-annotated output."""
from src.parser import parse_file
from src.checksum import is_valid


def classify_account(account: str) -> str:
    """Classify an account number and return formatted output line.

    Returns:
        "123456789"       — valid account
        "664371495 ERR"   — invalid checksum
        "86110??36 ILL"   — illegible digits
    """
    if "?" in account:
        return f"{account} ILL"

    if is_valid(account):
        return account
    else:
        return f"{account} ERR"


def format_output(ocr_content: str) -> str:
    """Parse an OCR file and produce formatted output with validation status.

    Each account number appears on its own line with optional status marker.
    """
    accounts = parse_file(ocr_content)
    lines = [classify_account(account) for account in accounts]
    return "\n".join(lines)
