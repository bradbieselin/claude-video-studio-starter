"""
Transcribe a video to word-level JSON using ElevenLabs Scribe.

Extracts the audio with ffmpeg, uploads it to the ElevenLabs Speech-to-Text
API, and writes the response to <edit-dir>/transcripts/<source-stem>.json in
the exact format that cut_silences.py and generate_captions.py expect.

Caches by source filename — if the transcript already exists, it's reused
(pass --force to re-transcribe).

Usage:
  # Set your key once
  echo "ELEVENLABS_API_KEY=sk_..." >> .env

  python transcribe.py --src /path/to/source.mp4 --edit-dir /path/to/edit/

Requires:
  pip install requests python-dotenv
  ffmpeg on PATH
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    import requests
except ImportError:
    print("ERROR: missing dependency. Run: pip install requests python-dotenv", file=sys.stderr)
    sys.exit(1)

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # .env loading is best-effort — env vars still work

API_URL = "https://api.elevenlabs.io/v1/speech-to-text"
MODEL_ID = "scribe_v1"


def extract_audio(src: Path, dst: Path) -> None:
    """Extract mono 16kHz PCM WAV from a video — Scribe-friendly + small."""
    cmd = [
        "ffmpeg", "-y",
        "-i", str(src),
        "-vn",                # no video
        "-ac", "1",           # mono
        "-ar", "16000",       # 16 kHz
        "-c:a", "pcm_s16le",  # uncompressed
        str(dst),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"ERROR: ffmpeg audio extraction failed:\n{result.stderr}", file=sys.stderr)
        sys.exit(1)


def call_scribe(audio_path: Path, api_key: str, num_speakers: int | None) -> dict:
    """Upload audio to ElevenLabs Scribe and return the parsed JSON response."""
    headers = {"xi-api-key": api_key}
    with audio_path.open("rb") as f:
        files = {"file": (audio_path.name, f, "audio/wav")}
        data: dict = {"model_id": MODEL_ID}
        if num_speakers is not None:
            data["num_speakers"] = str(num_speakers)
        size_mb = audio_path.stat().st_size / (1024 * 1024)
        print(f"  uploading {audio_path.name} ({size_mb:.1f} MB)")
        response = requests.post(API_URL, headers=headers, files=files, data=data, timeout=300)
    if response.status_code != 200:
        print(
            f"ERROR: ElevenLabs API returned {response.status_code}:\n{response.text}",
            file=sys.stderr,
        )
        sys.exit(1)
    return response.json()


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--src", required=True, help="Path to the source video.")
    ap.add_argument("--edit-dir", required=True, help="Project edit/ directory. Transcripts land in <edit-dir>/transcripts/.")
    ap.add_argument("--num-speakers", type=int, default=1, help="Number of speakers in the audio (default 1).")
    ap.add_argument("--force", action="store_true", help="Re-transcribe even if a cached transcript exists.")
    args = ap.parse_args()

    src = Path(args.src).resolve()
    edit_dir = Path(args.edit_dir).resolve()
    transcripts_dir = edit_dir / "transcripts"
    transcripts_dir.mkdir(parents=True, exist_ok=True)
    out_path = transcripts_dir / (src.stem + ".json")

    if not src.exists():
        print(f"ERROR: source not found: {src}", file=sys.stderr)
        sys.exit(1)

    if out_path.exists() and not args.force:
        size_kb = out_path.stat().st_size / 1024
        print(f"✓ cached transcript exists: {out_path} ({size_kb:.1f} KB)")
        print("  pass --force to re-transcribe")
        return

    api_key = os.environ.get("ELEVENLABS_API_KEY", "").strip()
    if not api_key:
        print(
            "ERROR: ELEVENLABS_API_KEY is not set.\n"
            "Get one at https://elevenlabs.io → Settings → API Keys, then either:\n"
            "  • Put it in a .env file at your project root:  ELEVENLABS_API_KEY=sk_xxx\n"
            "  • Or export it in your shell:                  export ELEVENLABS_API_KEY=sk_xxx",
            file=sys.stderr,
        )
        sys.exit(1)

    print(f"  extracting audio from {src.name}")
    with tempfile.TemporaryDirectory() as tmp:
        wav = Path(tmp) / (src.stem + ".wav")
        extract_audio(src, wav)
        result = call_scribe(wav, api_key, args.num_speakers)

    out_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    word_count = sum(1 for w in result.get("words", []) if w.get("type") == "word")
    size_kb = out_path.stat().st_size / 1024
    print(f"  saved: {out_path.name} ({size_kb:.1f} KB)")
    print(f"  words: {word_count}")


if __name__ == "__main__":
    main()
