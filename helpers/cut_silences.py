"""
Cut silences > 0.2s from a transcribed source video, with 30ms audio fades at
every splice, mild video denoise (hqdn3d), and a broadcast-grade audio cleanup
chain (highpass + FFT denoise + compressor + loudnorm).

Reads the word-level transcript JSON (ElevenLabs Scribe format), detects
inter-word gaps > MAX_GAP, compresses each to exactly MAX_GAP, emits an
ffmpeg filter_complex command to produce a tight source, and writes a retimed
transcript.

Usage:
  python cut_silences.py \\
      --src /path/to/source.mp4 \\
      --dst /path/to/composition/assets/source_tight.mp4 \\
      --transcript /path/to/edit/transcripts/source.json \\
      --edit-dir /path/to/edit/

Then run the printed ffmpeg command (also written to <edit-dir>/ffmpeg_cut.cmd).
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

MAX_GAP = 0.20  # any gap longer than this gets compressed to exactly this
FADE = 0.030    # 30ms audio fade in/out per segment to mask splice clicks


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--src", required=True, help="Path to the raw source video.")
    ap.add_argument("--dst", required=True, help="Path where the tight (silence-cut) MP4 will land.")
    ap.add_argument("--transcript", required=True, help="Path to the word-level ASR JSON (ElevenLabs Scribe format).")
    ap.add_argument("--edit-dir", required=True, help="Directory where cuts.json, ffmpeg_cut.cmd, and the retimed transcript will be written.")
    ap.add_argument("--max-gap", type=float, default=MAX_GAP, help=f"Maximum allowed silence gap in seconds (default {MAX_GAP}).")
    ap.add_argument("--crf", type=int, default=15, help="x264 CRF for the cut output (default 15, lower = sharper).")
    args = ap.parse_args()

    src = Path(args.src).resolve()
    dst = Path(args.dst).resolve()
    edit_dir = Path(args.edit_dir).resolve()
    transcript_in = Path(args.transcript).resolve()
    transcript_out = edit_dir / "transcripts" / (transcript_in.stem + ".tight.json")
    cuts_out = edit_dir / "cuts.json"
    ffmpeg_out = edit_dir / "ffmpeg_cut.cmd"

    if not src.exists():
        print(f"ERROR: source not found: {src}", file=sys.stderr)
        sys.exit(1)
    if not transcript_in.exists():
        print(f"ERROR: transcript not found: {transcript_in}", file=sys.stderr)
        sys.exit(1)
    transcript_out.parent.mkdir(parents=True, exist_ok=True)
    dst.parent.mkdir(parents=True, exist_ok=True)

    data = json.loads(transcript_in.read_text(encoding="utf-8"))
    raw_words = data["words"]
    word_only = [w for w in raw_words if w.get("type") == "word"]

    # Find inter-word gaps > MAX_GAP. Each becomes a cut event.
    cuts: list[tuple[float, float]] = []
    half = args.max_gap / 2.0
    for i in range(1, len(word_only)):
        prev = word_only[i - 1]
        cur = word_only[i]
        gap = cur["start"] - prev["end"]
        if gap > args.max_gap:
            cut_start = prev["end"] + half
            cut_end = cur["start"] - half
            if cut_end > cut_start:
                cuts.append((cut_start, cut_end))

    # Head: silence before first word
    first_start = word_only[0]["start"]
    if first_start > args.max_gap:
        cuts.insert(0, (half, first_start - half))

    # Determine source duration via ffprobe
    src_duration = float(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(src),
    ]).decode().strip())

    # Tail: silence after last word
    last_end = word_only[-1]["end"]
    if src_duration - last_end > args.max_gap:
        cuts.append((last_end + half, src_duration - half))

    # Build keep segments from the inverse of cuts.
    keep: list[tuple[float, float]] = []
    cursor = 0.0
    for (cs, ce) in cuts:
        if cs > cursor:
            keep.append((cursor, cs))
        cursor = ce
    if cursor < src_duration:
        keep.append((cursor, src_duration))

    # Time remap function
    def remap(t: float) -> float:
        amount = 0.0
        for (cs, ce) in cuts:
            if ce <= t:
                amount += (ce - cs)
            elif cs < t < ce:
                amount += (t - cs)
        return round(t - amount, 4)

    new_duration = remap(src_duration)

    # Write the retimed transcript
    new_words = []
    for w in raw_words:
        nw = dict(w)
        nw["start"] = remap(w["start"])
        nw["end"] = remap(w["end"])
        new_words.append(nw)
    new_doc = dict(data)
    new_doc["words"] = new_words
    new_doc["tight_cut"] = {
        "max_gap_s": args.max_gap,
        "removed_total_s": round(sum(ce - cs for cs, ce in cuts), 4),
        "original_duration_s": src_duration,
        "tight_duration_s": new_duration,
        "cuts": [{"start": cs, "end": ce} for cs, ce in cuts],
    }
    transcript_out.write_text(json.dumps(new_doc, indent=2), encoding="utf-8")

    # Write cuts.json
    cuts_out.write_text(
        json.dumps(
            {
                "src": str(src),
                "dst": str(dst),
                "src_duration_s": src_duration,
                "tight_duration_s": new_duration,
                "removed_total_s": round(sum(ce - cs for cs, ce in cuts), 4),
                "cuts": [{"start": cs, "end": ce, "length": round(ce - cs, 4)} for cs, ce in cuts],
                "keep_segments": [{"start": s, "end": e, "length": round(e - s, 4)} for s, e in keep],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    # Build ffmpeg filter_complex:
    # - Per-segment video: mild hqdn3d denoise to clean sensor grain.
    # - Per-segment audio: 30ms fades at splice points.
    # - Post-concat audio: highpass + FFT denoise + gentle compressor + loudnorm.
    parts_v = []
    parts_a = []
    labels = []
    for i, (s, e) in enumerate(keep):
        seg_dur = e - s
        fade_out_start = max(0.0, seg_dur - FADE)
        parts_v.append(
            f"[0:v]trim={s:.4f}:{e:.4f},setpts=PTS-STARTPTS,"
            f"hqdn3d=2:1.5:3:3[v{i}]"
        )
        parts_a.append(
            f"[0:a]atrim={s:.4f}:{e:.4f},asetpts=PTS-STARTPTS,"
            f"afade=t=in:st=0:d={FADE},afade=t=out:st={fade_out_start:.4f}:d={FADE}[a{i}]"
        )
        labels.append(f"[v{i}][a{i}]")
    n = len(keep)
    audio_chain = (
        "highpass=f=80,"
        "afftdn=nf=-25,"
        "acompressor=threshold=0.12:ratio=3:attack=8:release=80:makeup=2,"
        "loudnorm=I=-16:TP=-1.5:LRA=11"
    )
    filter_complex = ";".join(
        parts_v
        + parts_a
        + [
            f"{''.join(labels)}concat=n={n}:v=1:a=1[v][a_raw]",
            f"[a_raw]{audio_chain}[a]",
        ]
    )

    cmd = (
        f'ffmpeg -y -i "{src}" -filter_complex "{filter_complex}" '
        f'-map "[v]" -map "[a]" -c:v libx264 -preset slow -crf {args.crf} -pix_fmt yuv420p '
        f'-c:a aac -b:a 256k "{dst}"'
    )
    ffmpeg_out.write_text(cmd + "\n", encoding="utf-8")

    print(f"Original duration: {src_duration:.3f}s")
    print(f"Tight duration:    {new_duration:.3f}s")
    print(f"Removed silence:   {sum(ce - cs for cs, ce in cuts):.3f}s across {len(cuts)} gap(s)")
    print(f"Keep segments:     {len(keep)}")
    for i, (s, e) in enumerate(keep):
        print(f"  seg {i}: {s:.3f} - {e:.3f}  ({e - s:.3f}s)")
    print()
    print(f"Wrote: {cuts_out.name}, {ffmpeg_out.name}, transcripts/{transcript_out.name}")
    print()
    print("Run this to produce the tight source:")
    print(f"  bash {ffmpeg_out}")


if __name__ == "__main__":
    main()
