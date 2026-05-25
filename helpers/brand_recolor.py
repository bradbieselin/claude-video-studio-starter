"""
Batch hex/rgba color migration for a HyperFrames composition file.

Pass a JSON map of old hex/rgba strings to new ones. Useful when you want to
re-skin a composition to a new brand palette, or when an emphasis color needs
to shift across the whole file.

Usage:
  python brand_recolor.py --html composition/index.html --map recolor.json

recolor.json:
  {
    "#FFD60A": "#c6ff3d",
    "rgba(255, 214, 10, 0.45)": "rgba(198, 255, 61, 0.55)",
    "#3fb3ff": "#c6ff3d",
    ...
  }

The tool is a pure literal find-and-replace — no regex, no parsing. It WILL
replace every occurrence (including incidental ones in comments). Review the
map before running.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--html", required=True, help="Path to the HyperFrames composition HTML file.")
    ap.add_argument("--map", required=True, help="Path to a JSON file mapping old color strings to new color strings.")
    ap.add_argument("--dry-run", action="store_true", help="Print what would change without writing.")
    args = ap.parse_args()

    html_path = Path(args.html).resolve()
    map_path = Path(args.map).resolve()

    if not html_path.exists():
        print(f"ERROR: HTML not found: {html_path}", file=sys.stderr)
        sys.exit(1)
    if not map_path.exists():
        print(f"ERROR: map not found: {map_path}", file=sys.stderr)
        sys.exit(1)

    src = html_path.read_text(encoding="utf-8")
    color_map: dict[str, str] = json.loads(map_path.read_text(encoding="utf-8"))

    out = src
    applied = 0
    for old, new in color_map.items():
        count = out.count(old)
        if count > 0:
            out = out.replace(old, new)
            applied += 1
            print(f"  {count}× {old} → {new}")

    if out == src:
        print("No replacements made.")
        return

    if args.dry_run:
        print(f"\nDry run — would apply {applied} distinct mappings (file not written).")
    else:
        html_path.write_text(out, encoding="utf-8")
        print(f"\nWrote {html_path} — applied {applied} distinct mappings.")


if __name__ == "__main__":
    main()
