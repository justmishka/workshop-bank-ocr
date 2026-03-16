# Bank OCR

Workshop Product 01 — Parse and validate machine-scanned account numbers.

**Source:** [codingdojo.org/kata/BankOCR](https://codingdojo.org/kata/BankOCR/)

## What it does

A bank's scanning machine produces files with account numbers written in ASCII art using pipes and underscores. This tool:

1. Parses OCR output into readable account numbers
2. Validates numbers using a checksum algorithm
3. Generates output with validation status (valid / ERR / ILL)
4. Attempts error correction for invalid or illegible numbers

## Setup

```bash
pip install -e ".[dev]"
```

## Usage

```bash
bank-ocr input.txt
```

## Run tests

```bash
pytest
pytest --cov
```

## Project

- **Team:** The AI Dev Team
- **Sprint:** 1 day
- **Jira:** WRKSHP project, Bank OCR epic
- **Kick-off notes:** [kick-off.md](kick-off.md)
