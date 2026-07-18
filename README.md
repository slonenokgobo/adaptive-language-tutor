# Adaptive Language Tutor

An agentic framework for learning a new language. It keeps a private model of one learner—their vocabulary, level, goals, interests, grammar practice, and generated material—and uses that context to create targeted practice.

The public repository contains the reusable workflow and tools. A learner's data and generated content stay in an ignored local workspace, so the engine can be shared without exposing study history.

## What the tutor can do

The agent is guided by `AGENTS.md`. It can:

- Translate an unprompted phrase in the learner's target language and flag unfamiliar vocabulary.
- Choose under-practised vocabulary and turn it into an entertaining, level-appropriate story.
- Introduce a small amount of useful new vocabulary, with translations.
- Record grammar constructions practised in stories.
- Track how often vocabulary appears across generated stories.
- Create or reuse an audio narration of a story.

The workflow is language-neutral. The learner profile supplies the target language, locale, translation language, level, goals, and interests.

## How it works

```text
learner profile + vocabulary + grammar history
                    │
                    ▼
       agent skills select weak / low-exposure items
                    │
                    ▼
     personalised story, glossary, grammar practice, audio
                    │
                    ▼
          updated private learning history and counts
```

Vocabulary exposure is counted with exact, Unicode-aware matching. This is portable across writing systems; add the forms the learner should recognise to the vocabulary list.

## Quick start

Requirements: Python 3.10 or newer. No third-party Python packages are needed for the core workflow.

Create a private learner workspace:

```bash
python3 scripts/init_learner.py
```

This creates the following ignored files:

```text
data/
├── learner.json       # learner configuration
├── vocabulary.md      # one word, phrase, or sentence per line
├── gramma.md          # grammar constructions encountered in stories
├── STORIES.md         # story index
└── stories/           # generated Markdown stories and optional audio
```

Edit `data/learner.json` before starting. Its key settings are:

```json
{
  "name": "Your name",
  "language": "Target language",
  "locale": "es-ES",
  "translation_language": "English",
  "level": "A2",
  "goal": "hold everyday conversations",
  "interests": ["film", "technology"],
  "tts_voice": "Optional installed macOS voice"
}
```

Add the learner's existing vocabulary to `data/vocabulary.md`, one entry per line. Then use the agent in a Codex-compatible interface to request a story, a translation, or learning statistics.

## Useful commands

```bash
# Show vocabulary sorted by exposure count
python3 scripts/count_words.py

# Find vocabulary that has not appeared in a story
python3 scripts/count_words.py --zero

# Select the next 15 low-exposure items for a story
python3 scripts/count_words.py --least 15 --json

# Show story, vocabulary, and grammar totals
python3 .claude/skills/stats/scripts/stats.py

# Narrate a story; requires OPENAI_API_KEY for OpenAI TTS,
# otherwise uses the configured macOS voice when available
python3 .claude/skills/read-story/scripts/read_story.py data/stories/001-example-story.md
```

### Multiple learners or a custom data location

Every tool reads `data/` by default. Set `TUTOR_DATA_DIR` to isolate learners or store their data outside the repository:

```bash
TUTOR_DATA_DIR=/secure/path/learner python3 scripts/count_words.py --least 15
```

Run the initializer with the same setting to create that workspace:

```bash
TUTOR_DATA_DIR=/secure/path/learner python3 scripts/init_learner.py
```

## Repository layout

| Path | Purpose |
|---|---|
| `AGENTS.md` | The agent's teaching and story-generation rules. |
| `templates/` | Safe starter files copied into a learner workspace. |
| `scripts/init_learner.py` | Creates a private workspace without overwriting existing files. |
| `scripts/count_words.py` | Calculates vocabulary exposure across stories. |
| `.claude/skills/` | Optional agent skills for counts, statistics, and narration. |
| `data/` | Private, generated learner material; always ignored by Git. |

## Privacy and publishing

`data/` is listed in `.gitignore`, so learner profiles, vocabulary, stories, and audio are not added to new commits. Always check `git status` before pushing.

Git ignore rules cannot remove information already committed to Git history. If you previously committed learner data, remove it from history before making the repository public (for example with `git filter-repo` or GitHub's sensitive data removal process), then carefully coordinate any required force-push with collaborators.
