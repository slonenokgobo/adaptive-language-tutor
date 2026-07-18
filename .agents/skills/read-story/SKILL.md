---
name: read-story
description: Generate or reuse audio for a Markdown story in this language-tutor project. Use when the learner asks to read, listen to, hear aloud, or create audio for a story.
---

# Read Story

Generate narration with OpenAI text-to-speech when `OPENAI_API_KEY` is available. The language, locale, and optional macOS fallback voice come from `data/learner.json`. Never ask the learner to paste a key into the chat or save it in the repository.

1. Identify the requested story in `data/stories/`. If it is ambiguous, ask which story to read.
2. Run `python3 .claude/skills/read-story/scripts/read_story.py` with the absolute Markdown path.
3. The audio is saved beside the story and opened automatically in the macOS default audio player. Reuse an existing non-empty audio file unless the learner explicitly asks to recreate it after editing. Use `--force` only for that request and `--no-open` only if the learner asks not to play it.
4. Tell the learner the audio file path and link to it. State that the narration is AI-generated. Do not modify the story Markdown.

The script narrates only the story body: it excludes the header, glossary, grammar table, Markdown formatting, exposure markers, and new-word markers.
