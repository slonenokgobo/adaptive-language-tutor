#!/usr/bin/env python3
"""Create or reuse an OpenAI TTS MP3 narration for a language-learning story."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import tempfile
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from pathlib import Path


def story_body(markdown: str) -> str:
    """Extract the narrative between the first two horizontal rules."""
    parts = re.split(r"(?m)^---\s*$", markdown)
    body = parts[1] if len(parts) >= 3 else markdown
    body = re.sub(r"(?m)^#{1,6}\s*", "", body)
    body = body.replace("**", "").replace("*", "").replace("`", "")
    body = re.sub(r"[👁🆕]\s*[⁰¹²³⁴⁵⁶⁷⁸⁹]*", "", body)
    body = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", body)
    body = re.sub(r"[ \t]+", " ", body)
    body = re.sub(r"\n{3,}", "\n\n", body)
    return body.strip()


def open_audio(audio: Path) -> None:
    """Open the narration in the default macOS audio player."""
    subprocess.run(["open", str(audio)], check=True)


def learner_voice_settings() -> tuple[str, str, str | None]:
    """Read language, locale, and optional macOS voice from the private profile."""
    profile = Path(os.environ.get("TUTOR_DATA_DIR", "data")) / "learner.json"
    try:
        settings = json.loads(profile.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return "the learner's configured language", "", None
    language = settings.get("language", "the learner's configured language")
    locale = settings.get("locale", "")
    voice = settings.get("tts_voice")
    return language, locale, voice if voice and not voice.startswith("Optional") else None


def generate_audio(text: str, output: Path, language: str, locale: str) -> None:
    """Stream OpenAI TTS audio directly to an MP3 file."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:  # pragma: no cover - selected by main before this function is called
        raise RuntimeError("OPENAI_API_KEY is required for OpenAI TTS")

    payload = json.dumps(
        {
            "model": "gpt-4o-mini-tts",
            "voice": "marin",
            "input": text,
            "instructions": (
                f"Speak naturally in {language} {f'({locale})' if locale else ''}, with clear diction, "
                "warm storytelling intonation, and a calm, moderate pace."
            ),
            "response_format": "mp3",
        }
    ).encode("utf-8")
    request = Request(
        "https://api.openai.com/v1/audio/speech",
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urlopen(request, timeout=120) as response, output.open("wb") as audio_file:
            while chunk := response.read(64 * 1024):
                audio_file.write(chunk)
    except HTTPError as error:
        output.unlink(missing_ok=True)
        raise SystemExit(f"OpenAI TTS request failed ({error.code}: {error.reason}).")
    except URLError as error:
        output.unlink(missing_ok=True)
        raise SystemExit(f"Could not reach OpenAI TTS: {error.reason}")


def generate_macos_audio(text: str, output: Path, voice: str | None) -> None:
    """Generate offline narration with an optional configured macOS voice."""
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".txt", delete=False) as text_file:
        text_file.write(text)
        text_path = Path(text_file.name)
    try:
        command = ["say"]
        if voice:
            command.extend(["-v", voice])
        command.extend(
            ["-o",
                str(output),
                "--file-format=m4af",
                "--data-format=aac",
                "-f",
                str(text_path),
            ]
        )
        subprocess.run(command, check=True)
    finally:
        text_path.unlink(missing_ok=True)


def default_output(story: Path, has_openai_key: bool) -> Path:
    """Prefer existing audio; otherwise choose the format for the available engine."""
    openai_output = story.with_suffix(".mp3")
    macos_output = story.with_suffix(".m4a")
    if openai_output.exists() and openai_output.stat().st_size > 0:
        return openai_output
    if macos_output.exists() and macos_output.stat().st_size > 0 and not has_openai_key:
        return macos_output
    return openai_output if has_openai_key else macos_output


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("story", type=Path, help="Markdown story to narrate")
    parser.add_argument("--force", action="store_true", help="Regenerate existing audio")
    parser.add_argument("--no-open", action="store_true", help="Create or reuse audio without opening it")
    parser.add_argument("--output", type=Path, help="Override the default sibling .mp3 path")
    args = parser.parse_args()

    story = args.story.resolve()
    if not story.is_file() or story.suffix.lower() != ".md":
        raise SystemExit(f"Story Markdown file not found: {args.story}")

    has_openai_key = bool(os.environ.get("OPENAI_API_KEY"))
    language, locale, macos_voice = learner_voice_settings()
    output = args.output.resolve() if args.output else default_output(story, has_openai_key)
    if output.exists() and output.stat().st_size > 0 and not args.force:
        print(f"Reusing existing audio: {output}")
        if not args.no_open:
            open_audio(output)
        return

    text = story_body(story.read_text(encoding="utf-8"))
    if not text:
        raise SystemExit("The story has no narratable text.")

    output.parent.mkdir(parents=True, exist_ok=True)
    if has_openai_key:
        generate_audio(text, output, language, locale)
        engine = "OpenAI TTS"
    else:
        generate_macos_audio(text, output, macos_voice)
        engine = f"macOS {macos_voice or 'default'} voice"

    if not output.exists() or output.stat().st_size == 0:
        raise SystemExit(f"Text-to-speech did not create audio: {output}")
    print(f"Generated audio with {engine}: {output}")
    if not args.no_open:
        open_audio(output)


if __name__ == "__main__":
    main()
