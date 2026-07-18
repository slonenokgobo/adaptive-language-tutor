# Private learner data, public language-tutor engine

This repository is arranged so that its tutor workflow can be published without
publishing a learner's personal profile or study history.

## What is public

- `AGENTS.md` — the language-tutor workflow
- `scripts/` and `.claude/skills/` — reusable tools
- `templates/` — safe starter files

## What stays private

Everything in `data/` is ignored by Git: the learner profile, vocabulary,
grammar tracker, generated stories, and generated audio. Existing repositories
must also remove those files from Git tracking before publishing (see below).

## Set up a learner

```bash
python3 scripts/init_learner.py
```

Then edit `data/learner.json` to set the learner's name, target language and
locale, translation language, level, goal, interests, and optional macOS TTS
voice. Add known vocabulary in `data/vocabulary.md`, one item per line.

By default all tools read `data/`. To use another private directory, set
`TUTOR_DATA_DIR`:

```bash
TUTOR_DATA_DIR=/secure/path/learner python3 scripts/count_words.py --least 15
```

## Publishing an existing repository

`.gitignore` stops future additions; it cannot remove personal data that is
already in Git history. This refactor moves the current learner data to
`data/`, which is ignored. Before making a repository public, review the
history and rewrite it if those old commits were pushed anywhere. For example,
use `git filter-repo` (or GitHub's documented sensitive-data removal flow),
then force-push only after confirming every collaborator understands the
rewrite.

Also review `git status` before committing: the old root-level learner files
and `stories/` should be committed as deletions, while `data/` must not appear
in the commit.
