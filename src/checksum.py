"""Account number checksum validation."""
from typing import Optional


def is_valid(account: str) -> Optional[bool]:
    """Validate an account number using the checksum algorithm.

    Checksum: (d1 + 2*d2 + 3*d3 + ... + 9*d9) mod 11 = 0
    where d1 is the rightmost digit.

    Returns True if valid, False if invalid, None if account contains '?'.
    """
    if "?" in account:
        return None

    digits = [int(d) for d in account]
    digits.reverse()  # d1 = rightmost

    total = sum((i + 1) * d for i, d in enumerate(digits))
    return total % 11 == 0
