---
name: word-counts
description: Count how many times each private data/vocabulary.md item has appeared across generated stories. Use before generating a story (to annotate words with their exposure count and pick under-practised words) or whenever the learner asks which words they have seen most/least.
---

# Word exposure counts

Run the counter script from the project root:

```bash
python3 scripts/count_words.py          # table sorted by count (most seen first)
python3 scripts/count_words.py --zero   # only words never seen in a story
python3 scripts/count_words.py --json   # machine-readable, for annotating stories
python3 scripts/count_words.py --least 15        # 15 least-seen story candidates
python3 scripts/count_words.py --least 15 --json # same candidate set for tooling
```

The script reads `data/vocabulary.md` (one item per line, URLs skipped) and all of `data/stories/*.md` (glossary tables excluded). Set `TUTOR_DATA_DIR` to use another private workspace. Matching is exact and Unicode-aware so it remains predictable across writing systems; add the forms the learner should recognise to the vocabulary list.

## How the counts are used in stories

When generating a new story (see AGENTS.md workflow):

1. Run `python3 scripts/count_words.py --least 15 --json` BEFORE writing. Select 10–20 items from this least-seen set (15 is the normal target) and make them the known-vocabulary target for the story.
2. Run `python3 scripts/count_words.py --json` to get the complete count map for annotations.
3. In the story text, annotate the **first occurrence** of each selected known vocabulary item with an eye icon and its count in superscript: `**palavra** 👁³` means the learner has already seen it 3 times in previous stories. Superscript digits: ⁰¹²³⁴⁵⁶⁷⁸⁹.
4. New words (not in `vocabulary.md`) keep the 🆕 marker instead — never both.
5. The low-count selection is mandatory unless an item cannot fit the requested theme without becoming unnatural. Do not add high-count known words merely to increase the total.

## Interpreting results for the learner

- High-count words are well-reinforced; low/zero-count words need a story soon.
- The final summary line ("N/M items seen") tracks overall coverage of the vocabulary.
