---
name: brand-voice-palette
description: Single source of truth for the brand colors, typography, and voice used in every video.
metadata:
  type: brand
---

# Brand voice palette

> 🛠️ **Customize this file before your first render.** Search for `{{` and replace every placeholder with your own values. Claude reads this every session and applies it to every composition.

## Palette — "one color, used 100 times"

| Token | Hex | Purpose |
|-------|-----|---------|
| BASE | `#0a0a0a` | Composition / page background (default keeps this for most brands) |
| SURF | `#131313` | Off-black surfaces, panels, cards |
| TEXT | `#f3f1ea` | Warm off-white body text |
| **ACCENT** | `{{YOUR_ACCENT_HEX}}` | **Your single accent. Used everywhere on-brand.** |
| WARN | `{{YOUR_WARN_HEX}}` | Sparingly, only for punch-line / contrast moments |
| LINE | `#262626` | Hairline borders, dividers |
| MUTED | `#6f6f66` | Muted secondary text |

**Rule**: one color used 100 times beats five colors used once. Default any "accent" decision to your ACCENT color. Only reach for WARN when contrast against the accent is the explicit point.

**Accent gradient (for buttons / badges)**: lighten/darken the accent ±15% to build a 3-stop gradient. Example for `#c6ff3d`:

```
linear-gradient(180deg, #d8ff60 0%, #c6ff3d 55%, #97c500 100%)
```

## Typography

- **Display / captions**: `Inter`, bold/italic for video legibility. HyperFrames auto-resolves Inter from Google Fonts.
- **Alternative**: If your brand uses a different display font, add `@font-face` rules in your composition CSS and reference local `.woff2` files in `composition/assets/fonts/`.

## Tone

{{YOUR_TONE_DESCRIPTION}}

*Example: "Fast. Honest. A little restless. Talk like someone with two coffees and a new idea. Builder mid-climb, not guru on stage."*

## Phrases — use

- {{YOUR_GO_TO_PHRASE_1}}
- {{YOUR_GO_TO_PHRASE_2}}
- {{YOUR_GO_TO_PHRASE_3}}

## Phrases — avoid

- "Game-changer"
- "Unlock your potential"
- "Hey guys, welcome back"
- "Don't forget to like and subscribe"
- "Synergy / leverage / ecosystem"
- "As an AI enthusiast..."

## North Star

> *"{{YOUR_NORTH_STAR_QUOTE}}"* — filter every post through this.

## Social

- Primary handle: `{{YOUR_HANDLE}}`
- Instagram: {{YOUR_INSTAGRAM_URL}}
- TikTok: {{YOUR_TIKTOK_URL}}
- YouTube: {{YOUR_YOUTUBE_URL}}

## CTA destination

- Default CTA keyword (for "comment X" hooks): `{{YOUR_CTA_KEYWORD}}`
- Where you DM the freebie / land link: `{{YOUR_CTA_URL}}`

## Application notes (HyperFrames)

When building any new composition:
- Default body bg: `#0a0a0a`
- Default panel/card bg: `#131313`
- Default text: `#f3f1ea` — not pure white
- Default accent (titles, emphasis, CTAs, highlights): `{{YOUR_ACCENT_HEX}}`
- Strike-through / "wrong" / "real" punch-lines: `{{YOUR_WARN_HEX}}`
- Authentic third-party product brands inside content (ChatGPT, Claude, Higgsfield, OpenAI, etc.) keep their actual brand colors — those are content, not brand chrome.
