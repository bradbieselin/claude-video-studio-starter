"""
Setup orchestrator for the Claude Video Studio starter kit.

Used by Claude (per the repo's CLAUDE.md) to bootstrap a new install with
zero manual file editing required.

Modes:
  --check          Print STATUS line + memory path. Claude reads this to
                   decide whether to enter Setup Mode or Edit Mode.
  --check-prereqs  Verify ffmpeg, Node, Python deps. Print install hints
                   for anything missing.
  --memory-path    Print the per-project Claude memory path (where memory
                   templates should land).
  --finalize       Copy the rest of the memory templates to user's memory
                   folder, generate the SFX library, mark setup complete.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


# ---------------------------------------------------------------------------
# Memory path resolution
# ---------------------------------------------------------------------------

def slugify_project_path(path: Path) -> str:
    """Match Claude Code's per-project slug algorithm.

    Examples:
      /Users/jane/video-studio  -> Users-jane-video-studio
      D:\\HyperFrames Editor    -> D--HyperFrames-Editor
    """
    s = str(path)
    s = s.replace(":", "-").replace("\\", "-").replace("/", "-").replace(" ", "-")
    return s.lstrip("-")


def get_memory_dir() -> Path:
    home = Path.home()
    slug = slugify_project_path(REPO)
    return home / ".claude" / "projects" / slug / "memory"


# ---------------------------------------------------------------------------
# Modes
# ---------------------------------------------------------------------------

def cmd_check() -> None:
    memory = get_memory_dir()
    marker = memory / ".setup-complete"
    if marker.exists():
        print("STATUS: ready")
    else:
        print("STATUS: needs-setup")
    print(f"memory: {memory}")


def cmd_memory_path() -> None:
    print(str(get_memory_dir()))


def cmd_check_prereqs() -> None:
    print("Checking prerequisites:\n")

    cli_checks = [
        ("ffmpeg", ["ffmpeg", "-version"], "brew install ffmpeg  (Mac)  /  winget install Gyan.FFmpeg  (Win)"),
        ("ffprobe", ["ffprobe", "-version"], "comes with ffmpeg"),
        ("node", ["node", "--version"], "Install Node 22+ from https://nodejs.org/"),
        ("npx", ["npx", "--version"], "Comes with Node — reinstall Node if missing"),
        ("git", ["git", "--version"], "Install from https://git-scm.com/"),
    ]

    all_ok = True
    for name, cmd, hint in cli_checks:
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            ok = r.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            ok = False
        sym = "✓" if ok else "✗"
        msg = "" if ok else f"  →  install: {hint}"
        print(f"  {sym} {name}{msg}")
        if not ok:
            all_ok = False

    # Python deps
    py_deps = [
        ("requests", "pip install requests"),
        ("dotenv", "pip install python-dotenv"),
    ]
    for mod, hint in py_deps:
        try:
            __import__(mod)
            print(f"  ✓ python-{mod}")
        except ImportError:
            print(f"  ✗ python-{mod}  →  install: {hint}")
            all_ok = False

    print()
    if all_ok:
        print("All prerequisites installed. Ready to continue setup.")
    else:
        print("⚠ One or more prerequisites missing. Install them, then re-run.")
        sys.exit(1)


def cmd_finalize() -> None:
    memory = get_memory_dir()
    memory.mkdir(parents=True, exist_ok=True)

    src_templates = REPO / "memory-templates"
    copied = []
    skipped_existing = []
    skipped_palette = False

    for tpl in sorted(src_templates.glob("*.md")):
        # brand_voice_palette.md is written separately by Claude via the Write
        # tool with the user's actual answers — don't overwrite it here.
        if tpl.name == "brand_voice_palette.md":
            if not (memory / tpl.name).exists():
                print(f"  ⚠ brand_voice_palette.md not yet in memory at {memory} — Claude should write it before --finalize")
            skipped_palette = True
            continue
        dst = memory / tpl.name
        if dst.exists():
            skipped_existing.append(tpl.name)
            continue
        shutil.copy(tpl, dst)
        copied.append(tpl.name)

    for name in copied:
        print(f"  ✓ copied {name}")
    for name in skipped_existing:
        print(f"  · skipped {name} (already exists)")

    # Generate the SFX library
    sfx_dir = REPO / "templates" / "composition" / "assets" / "sfx"
    sfx_dir.mkdir(parents=True, exist_ok=True)
    print(f"\n  synthesizing SFX library at {sfx_dir}…")
    r = subprocess.run(
        [sys.executable, str(REPO / "helpers" / "synth_sfx.py"), "--out", str(sfx_dir)],
        capture_output=True, text=True,
    )
    if r.returncode != 0:
        print(f"  ⚠ SFX synthesis failed:\n{r.stderr}")
    else:
        for line in r.stdout.strip().splitlines():
            print(f"    {line}")

    # Setup-complete marker
    (memory / ".setup-complete").write_text(
        "Setup completed by Claude Video Studio installer.\n"
        f"Memory path: {memory}\n"
        f"Repo: {REPO}\n",
        encoding="utf-8",
    )
    print(f"\n✓ Setup complete. Memory ready at {memory}")


# ---------------------------------------------------------------------------
# Dispatch
# ---------------------------------------------------------------------------

def main() -> None:
    args = sys.argv[1:]
    if "--check" in args:
        cmd_check()
    elif "--check-prereqs" in args:
        cmd_check_prereqs()
    elif "--memory-path" in args:
        cmd_memory_path()
    elif "--finalize" in args:
        cmd_finalize()
    else:
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
