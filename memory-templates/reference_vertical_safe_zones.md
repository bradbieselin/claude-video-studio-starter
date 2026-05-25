---
name: reference-vertical-safe-zones
description: Combined 2026 safe-zone specs for 1080×1920 vertical video on Instagram Reels and TikTok. Apply by default to any short-form composition.
metadata:
  type: reference
---

# Vertical safe zones (2026)

## Canvas

- **Resolution**: 1080×1920 (9:16) — correct for both platforms
- **Frame rate**: 30fps standard; 24fps acceptable for cinematic
- **Codec**: h264 + AAC stereo

## Safe-zone margins

Combined Reels + TikTok worst-case — use these to be safe on BOTH platforms:

| Edge | Pixels | Percent | Source |
|------|--------|---------|--------|
| Top | 140px | 7.3% | TikTok username overlay |
| Bottom | 324px | 16.9% | TikTok caption + buttons |
| Right | 164px | 8.5% | TikTok action button column |
| Left | 60px | 5.6% | Instagram left margin |

**Effective safe content area: 856×1456px** (between top 140 and bottom 1596, left 60 and right 916).

## Practical defaults for HyperFrames CSS

- **Top-edge graphics** (chips, badges, step titles): `top: 9%` (172px). Gives 32px breathing room above TikTok's 140px line.
- **Mid-frame hero captions / hooks**: `top: 50%` — always safe.
- **Running captions**: `top: 56-58%` — well inside, safe from both top and bottom unsafe zones.
- **Bottom-edge graphics**: keep above `top: 80%` (1536px) to clear TikTok's 324px bottom unsafe zone.
- **CTAs / dense text blocks**: center vertically around `top: 38-42%` for max visibility on both platforms.
- **Right-edge elements** (PiPs, decorations): keep `right: > 164px` from frame edge.

## Anti-checklist

- ❌ Don't place captions/badges at `top: 5%` or lower — TikTok username will cover them
- ❌ Don't place CTAs at `bottom: 0` to `bottom: 320px` — Reels caption + buttons cover the entire bottom strip
- ❌ Don't push key visuals into the right 164px — TikTok's like/comment/share column lives there

## Verification

When the composition is ready, mentally lay the safe-zone box over it:
- `60px` from left
- `916px` from left (= 1080 - 164 right)
- `140px` from top
- `1596px` from top (= 1920 - 324 bottom)

Every important text, face, CTA, and chip must sit inside this box. The base video can extend to the edges (it's allowed to be slightly cropped by platform UI overlays).
