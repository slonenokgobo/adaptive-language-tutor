#!/usr/bin/env python3
"""Create a private learner workspace from the public templates.

Use --data-dir or TUTOR_DATA_DIR to keep multiple learners separate.
Existing files are never overwritten unless --force is supplied.
"""

from __future__ import annotations

import argparse
import os
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
TEMPLATES = ROOT / "templates"


def data_dir(value: str | None) -> Path:
    return Path(value or os.environ.get("TUTOR_DATA_DIR", ROOT / "data")).expanduser()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", help="private workspace directory (default: data/)")
    parser.add_argument("--force", action="store_true", help="replace existing template files")
    args = parser.parse_args()

    destination = data_dir(args.data_dir)
    destination.mkdir(parents=True, exist_ok=True)
    (destination / "stories").mkdir(exist_ok=True)

    for name in ("learner.json", "vocabulary.md", "gramma.md", "STORIES.md"):
        target = destination / name
        if target.exists() and not args.force:
            print(f"Keeping existing: {target}")
            continue
        shutil.copyfile(TEMPLATES / name, target)
        print(f"Created: {target}")

    print(f"\nEdit {destination / 'learner.json'} and {destination / 'vocabulary.md'} to begin.")


if __name__ == "__main__":
    main()
