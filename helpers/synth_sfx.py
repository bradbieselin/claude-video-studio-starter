"""
Synthesize the 5-cue SFX library used by the composition skeleton.

Runs 5 ffmpeg lavfi commands in sequence to produce:
  - hit-low.mp3   (hook hits, CTA slams)
  - pop.mp3       (chip entrances)
  - tap.mp3       (caption pops)
  - whoosh.mp3    (tension rises)
  - sting.mp3     (keyword punches)

All commands use only ffmpeg's built-in lavfi source — no external assets.
Deterministic, reproducible, and customizable (read the recipes inline).

Usage:
  python synth_sfx.py --out composition/assets/sfx/

  # Skip files that already exist:
  python synth_sfx.py --out composition/assets/sfx/

  # Re-synthesize all files even if they exist:
  python synth_sfx.py --out composition/assets/sfx/ --force

Requires: ffmpeg on PATH.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

# (filename, ffmpeg-lavfi-input, ffmpeg-filter-chain)
RECIPES: list[tuple[str, str, str]] = [
    (
        "hit-low.mp3",
        "anoisesrc=color=brown:duration=0.45",
        "lowpass=f=180,afade=t=in:d=0.005:curve=exp,afade=t=out:st=0.05:d=0.4:curve=exp,volume=3.5",
    ),
    (
        "pop.mp3",
        "sine=frequency=900:duration=0.10",
        "afade=t=out:st=0:d=0.10:curve=exp,volume=0.55",
    ),
    (
        "tap.mp3",
        "sine=frequency=1400:duration=0.06",
        "afade=t=out:st=0:d=0.06:curve=exp,volume=0.35",
    ),
    (
        "whoosh.mp3",
        "anoisesrc=color=white:duration=0.55",
        "highpass=f=400,lowpass=f=2600,afade=t=in:d=0.08,afade=t=out:st=0.35:d=0.20,volume=0.65",
    ),
    (
        "sting.mp3",
        "sine=frequency=660:duration=0.40",
        "afade=t=in:d=0.005:curve=exp,afade=t=out:st=0.05:d=0.35:curve=exp,volume=0.50",
    ),
]


def synth(out_path: Path, lavfi_input: str, filter_chain: str) -> None:
    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi",
        "-i", lavfi_input,
        "-af", filter_chain,
        "-ac", "2",
        "-ar", "44100",
        "-b:a", "192k",
        str(out_path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"ERROR synthesizing {out_path.name}:\n{result.stderr}", file=sys.stderr)
        sys.exit(1)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", required=True, help="Output directory for the .mp3 files.")
    ap.add_argument("--force", action="store_true", help="Re-synthesize even if files exist.")
    args = ap.parse_args()

    if not shutil.which("ffmpeg"):
        print("ERROR: ffmpeg not found on PATH. Install ffmpeg first.", file=sys.stderr)
        sys.exit(1)

    out_dir = Path(args.out).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    for name, lavfi_input, filter_chain in RECIPES:
        target = out_dir / name
        if target.exists() and not args.force:
            print(f"  ✓ {name} already exists (use --force to re-synth)")
            continue
        print(f"  synthesizing {name}…")
        synth(target, lavfi_input, filter_chain)
        size_kb = target.stat().st_size / 1024
        print(f"    saved ({size_kb:.1f} KB)")

    print(f"\n✓ SFX library ready at {out_dir}")


if __name__ == "__main__":
    main()
