---
name: word-counts
description: Count how many private vocabulary items have appeared across generated stories. Use before generating a story (to annotate words with their exposure count and pick under-practised words) or whenever the learner asks which words they have seen most or least.
---

# Word exposure counts

Run `python3 scripts/count_words.py` from the project root. Use `--zero` for unseen vocabulary, `--json` for annotations, and `--least 15 --json` to select story candidates. Do not ask the learner to run the command.

The counter reads `data/vocabulary.md` and `data/stories/*.md`, excluding glossary tables. Matching is exact and Unicode-aware. Before every story, select 10–20 naturally fitting items from the low-exposure candidates, and use the complete count map to annotate each selected item's first occurrence. New words receive 🆕, never an exposure marker.
