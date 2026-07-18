#!/usr/bin/env python3
"""Count how many times each private vocabulary item has appeared in the stories.

Usage:
    python3 scripts/count_words.py            # human-readable table, sorted by count
    python3 scripts/count_words.py --json     # {"item": count, ...} for tooling
    python3 scripts/count_words.py --zero     # only items never seen in any story
    python3 scripts/count_words.py --least 15 # 15 best items for the next story
    python3 scripts/count_words.py --least 15 --json  # selected items for tooling

Matching is exact and Unicode-aware, so it works predictably for any target
language. Add the form the learner should recognise to vocabulary.md; language-
specific lemmatisation is deliberately outside this portable core.
"""

import json
import os
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = Path(os.environ.get("TUTOR_DATA_DIR", ROOT / "data")).expanduser()
VOCAB = DATA_DIR / "vocabulary.md"
STORIES = DATA_DIR / "stories"

def normalize(text: str) -> str:
    # lowercase only — accents are kept, so "lã" never matches "lá"
    return unicodedata.normalize("NFC", text.lower())


def load_vocab() -> list[str]:
    if not VOCAB.is_file():
        raise SystemExit(
            f"Vocabulary file not found: {VOCAB}. "
            "Run `python3 scripts/init_learner.py` or set TUTOR_DATA_DIR."
        )
    items = []
    for line in VOCAB.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith(("#", "http")):
            continue
        items.append(line)
    return items


def search_key(item: str) -> str:
    """Return an exact Unicode word/phrase pattern for a vocabulary item."""
    text = normalize(item).strip()
    if not text:
        return ""
    return r"(?<!\w)" + re.escape(text) + r"(?!\w)"


def story_text() -> str:
    if not STORIES.is_dir():
        raise SystemExit(
            f"Stories directory not found: {STORIES}. "
            "Run `python3 scripts/init_learner.py` or set TUTOR_DATA_DIR."
        )
    chunks = []
    for path in sorted(STORIES.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        text = text.split("## Gloss")[0]  # don't count glossary tables
        text = text.replace("**", "")
        chunks.append(text)
    return normalize("\n".join(chunks))


def least_limit(args: list[str]) -> int | None:
    """Return the requested candidate-set size, if any."""
    if "--least" not in args:
        return None
    position = args.index("--least")
    try:
        value = int(args[position + 1])
    except (IndexError, ValueError):
        raise SystemExit("--least needs a positive whole number, e.g. --least 15")
    if value < 1:
        raise SystemExit("--least needs a positive whole number, e.g. --least 15")
    return value


def main() -> None:
    text = story_text()
    counts = {}
    for item in load_vocab():
        pattern = search_key(item)
        counts[item] = len(re.findall(pattern, text)) if pattern else 0

    limit = least_limit(sys.argv[1:])
    ranked_lowest = sorted(counts.items(), key=lambda kv: (kv[1], kv[0]))
    selected = ranked_lowest[:limit] if limit is not None else list(counts.items())

    if "--json" in sys.argv:
        print(json.dumps(dict(selected), ensure_ascii=False, indent=1))
        return

    only_zero = "--zero" in sys.argv
    ranked = selected if limit is not None else sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
    for item, n in ranked:
        if only_zero and n:
            continue
        print(f"{n:3d}  {item}")
    if limit is not None:
        print(f"\nSelected {len(selected)} least-seen items for the next story")
        return
    seen = sum(1 for n in counts.values() if n)
    print(f"\n{seen}/{len(counts)} vocabulary items seen at least once in {len(list(STORIES.glob('*.md')))} stories")


if __name__ == "__main__":
    main()
