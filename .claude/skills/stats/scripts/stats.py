#!/usr/bin/env python3
"""Report the Portuguese tutor project's core totals."""

import json
import os
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
DATA_DIR = Path(os.environ.get("TUTOR_DATA_DIR", ROOT / "data")).expanduser()


def vocabulary_entries() -> int:
    return sum(
        1
        for line in (DATA_DIR / "vocabulary.md").read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith(("#", "http"))
    )


def grammar_entries() -> int:
    entries = 0
    for line in (DATA_DIR / "gramma.md").read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("|") and not stripped.startswith("| Construção") and "---" not in stripped:
            entries += 1
    return entries


def main() -> None:
    totals = {
        "stories": len(list((DATA_DIR / "stories").glob("*.md"))),
        "vocabulary_entries": vocabulary_entries(),
        "grammar_constructions": grammar_entries(),
    }
    if "--json" in sys.argv:
        print(json.dumps(totals, ensure_ascii=False))
        return
    print(f"Histórias geradas: {totals['stories']}")
    print(f"Entradas de vocabulário: {totals['vocabulary_entries']}")
    print(f"Construções gramaticais: {totals['grammar_constructions']}")


if __name__ == "__main__":
    main()
