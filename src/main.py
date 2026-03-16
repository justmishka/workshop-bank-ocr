"""CLI entry point for Bank OCR."""
import sys
from src.formatter import format_output


def main():
    if len(sys.argv) < 2:
        print("Usage: bank-ocr <input-file>", file=sys.stderr)
        sys.exit(1)

    input_path = sys.argv[1]

    try:
        with open(input_path) as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    result = format_output(content)
    print(result)


if __name__ == "__main__":
    main()
