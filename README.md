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

## Start learning

This is a workspace for an AI agent, rather than a standalone web app. Install and sign in to one of the supported agent harnesses below, download or clone this repository, and open it as a project. After that, learning is entirely conversational—there are no Python commands to run.

| Harness | One-time setup | Open this project | Why it works |
|---|---|---|---|
| [Codex](https://openai.com/codex/get-started/) | Install or open the Codex app and sign in. | Create or open a project pointing at this folder. | Codex reads the repository's `AGENTS.md` instructions. |
| [Claude Code](https://docs.anthropic.com/en/docs/claude-code/getting-started) | Install Claude Code and sign in. | Open a terminal in this folder and start Claude Code. | `CLAUDE.md` loads the shared tutor instructions from `AGENTS.md`. |
| [OpenClaw](https://docs.openclaw.ai/start/openclaw) | Complete OpenClaw's onboarding. | Set this folder as an agent workspace, then begin a new conversation with that agent. | OpenClaw loads root `AGENTS.md` and the project skills under `.agents/skills/`. |
| Other agentic IDEs and terminal agents | Install and sign in to your preferred agent. | Open this folder and say “Read `AGENTS.md`, then set up my language tutor.” | The shared instructions are plain Markdown, so any agent with file access can follow them. |

The agent harness may have its own installation or account setup. Those are one-time platform steps; the tutor itself never asks a learner to operate its scripts or files.

When the project is open, say:

> Set up my language tutor.

The tutor will ask a few ordinary questions—what you want to learn, your current level, the language you want explanations in, your goals, and your interests. It creates and maintains your private learning space for you. You do not need to install packages, edit configuration files, or run commands.

Once set up, use natural requests such as:

- “I want to learn European Portuguese at A2 level for travel. I like cinema and cooking.”
- “Here are the words I learned today: chegar, embora, com fome.”
- “Make me a short, funny story for today.”
- “What should I revise next?”
- “Show my learning progress.”
- “Read my latest story aloud.”

You can change direction at any time: “Make the stories harder,” “I now want explanations in Spanish,” or “Focus on vocabulary for work.” The tutor updates the learning plan and uses it for future practice.

## Behind the scenes

The tutor keeps its private working files in `data/`: your profile, vocabulary, grammar history, generated stories, and optional audio. The folder is created automatically and is ignored by Git. The scripts and agent skills in this repository calculate exposure counts, progress statistics, and narration when the tutor needs them; they are not part of the learner-facing workflow.

For people maintaining or extending the engine, `scripts/init_learner.py` creates the private workspace and the optional skills provide statistics and narration. Each tool reads `data/` by default, or the location specified by `TUTOR_DATA_DIR`.

## Repository layout

| Path | Purpose |
|---|---|
| `AGENTS.md` | The agent's teaching and story-generation rules. |
| `CLAUDE.md` | Claude Code entry point; it imports the shared rules. |
| `templates/` | Safe starter files copied into a learner workspace. |
| `scripts/init_learner.py` | Creates a private workspace without overwriting existing files. |
| `scripts/count_words.py` | Calculates vocabulary exposure across stories. |
| `.claude/skills/` and `.agents/skills/` | Claude Code and OpenClaw skill entry points for counts, statistics, and narration. |
| `data/` | Private, generated learner material; always ignored by Git. |

## Privacy and publishing

`data/` is listed in `.gitignore`, so learner profiles, vocabulary, stories, and audio are not added to new commits. Always check `git status` before pushing.

Git ignore rules cannot remove information already committed to Git history. If you previously committed learner data, remove it from history before making the repository public (for example with `git filter-repo` or GitHub's sensitive data removal process), then carefully coordinate any required force-push with collaborators.
