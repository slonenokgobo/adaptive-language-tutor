---
name: read-story
description: Generate or reuse audio for a Markdown story in this language-tutor project. Use when the learner asks to read, listen to, hear aloud, or create audio for a story.
---

# Read Story

Generate narration with OpenAI text-to-speech when `OPENAI_API_KEY` is available. The language, locale, and optional macOS fallback voice come from `data/learner.json`. Never ask the learner to paste a key into the chat or save it in the repository.

1. Identify the requested story in `data/stories/`. If it is ambiguous, ask which story to read.
2. Run the script with the absolute Markdown path:

   ```bash
   python3 .claude/skills/read-story/scripts/read_story.py data/stories/001-example-story.md
   ```

3. The audio is saved beside the story and opened automatically in the macOS default audio player.
   - With an OpenAI key, use `data/stories/001-example-story.mp3`.
   - Without a key, use `data/stories/001-example-story.m4a` from the configured macOS voice.
   - If that non-empty file already exists, the script reuses it and does not call text-to-speech again.
   - Use `--force` only when the learner explicitly asks to recreate the audio after editing a story.
   - Use `--no-open` only if the learner asks to create the audio without playing it.
4. Tell the learner the audio file path and link to it. State that the narration is AI-generated. Do not modify the story Markdown.

The script narrates only the story body: it excludes the header, glossary, grammar table, Markdown formatting, exposure markers, and new-word markers.
