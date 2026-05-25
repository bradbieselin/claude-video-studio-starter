# Claude Video Studio — Agent Instructions

> You are operating inside the **Claude Video Studio Starter Kit**. The user has cloned this repo and opened Claude Code in it. Follow these instructions exactly — they make the experience clone-and-run.

## On every session: detect mode first

Before doing anything else, run:

```bash
python helpers/setup.py --check
```

Read the output:

- `STATUS: needs-setup` → enter **Setup Mode** (below)
- `STATUS: ready` → enter **Edit Mode** (below)

---

## Setup Mode (first session only)

Goal: get from "user just cloned the repo" to "ready to edit a video" in one conversation, no manual file editing.

### Step 1 — Verify prerequisites

```bash
python helpers/setup.py --check-prereqs
```

For any missing tool, tell the user the exact install command. Wait for them to install + confirm before continuing.

### Step 2 — Gather brand values via conversation

Ask these questions in order. Be casual and direct — match the brand voice. **Wait for an answer to each before asking the next.**

1. **Accent color** — "What's your brand's accent color? Give me a hex code (`#c6ff3d`) or a color name (`lime green`, `electric blue`, `warm orange`) and I'll pick a hex for you."
2. **Warn color** — "And a contrast color for punch-lines and 'wrong' moments? Default is `#ff4d2e` (orange-red). Hex code or color name."
3. **Handle** — "Your handle on social (e.g. `@yourname`)?"
4. **Instagram / TikTok / YouTube URLs** — "Paste your IG, TT, and YT URLs. Say 'none' for any you don't have yet."
5. **CTA destination** — "Where do you send people who comment your keyword? Skool community URL, email signup, Beehiiv, anything."
6. **CTA keyword** — "What's your default 'comment X' keyword? (e.g. `CLONE`, `STUDIO`, `STEAL`)"
7. **North Star** — "One sentence that filters every piece of content. (e.g. *'I am 30 and starting over with AI, building my way out on camera.'*) Optional but recommended."
8. **Tone** — "Describe your tone in one sentence. Optional. Default: *'Fast. Honest. A little restless. Builder mid-climb, not guru on stage.'*"

### Step 3 — Write the populated brand_voice_palette.md

Read `memory-templates/brand_voice_palette.md`. Use the Write tool to create a populated version directly at the user's per-project memory folder. Get the exact path from:

```bash
python helpers/setup.py --memory-path
```

Replace every `{{PLACEHOLDER}}` with the user's answer. For colors, if the user gave a color name, pick a sensible hex (lime → `#c6ff3d`, electric blue → `#3fb3ff`, etc.) and tell the user what hex you chose so they can override if they want.

### Step 4 — Finalize

```bash
python helpers/setup.py --finalize
```

This copies the other memory templates (playbook, safe zones, short-form style) to the user's memory folder, generates the SFX library, and writes a `.setup-complete` marker.

### Step 5 — ElevenLabs API key

Check if `.env` exists at repo root with `ELEVENLABS_API_KEY`. If not:

> "Last thing — paste your ElevenLabs API key. Get one at https://elevenlabs.io → Settings → API Keys. Free tier works fine to start."

When they paste it, write it to `.env`:

```
ELEVENLABS_API_KEY=sk_xxx
```

### Step 6 — Hand off

Tell the user:

> ✅ **You're set up.**
>
> Drop a vertical recording (1080×1920, .mp4, ~30s to 2min) in this folder and tell me **"edit this video at &lt;filename&gt;.mp4"**. I'll do the rest.

---

## Edit Mode (every subsequent session)

The user's memory now contains the full studio playbook. Read it at session start:

```
~/.claude/projects/<slugified-project-path>/memory/studio_playbook.md
```

When the user says "edit this video at X.mp4" or similar, follow the studio playbook's pipeline exactly:

1. `ffprobe` the source
2. `python helpers/transcribe.py --src <source.mp4> --edit-dir <edit-dir>`
3. `python helpers/cut_silences.py --src <source.mp4> --dst <composition>/assets/source_tight.mp4 --transcript <edit-dir>/transcripts/<name>.json --edit-dir <edit-dir>`
4. `bash <edit-dir>/ffmpeg_cut.cmd`
5. `python helpers/generate_captions.py --transcript <edit-dir>/transcripts/<name>.tight.json --out <edit-dir>/captions_generated.html --hook-end 3.5`
6. Build the composition HTML using the skeleton in `templates/composition/index.html` and the brand colors from the user's memory
7. `npx hyperframes lint` + `npx hyperframes inspect`
8. `npx hyperframes render . -o <edit-dir>/final.mp4 --quality high --fps 30 --crf 16`

Always read `brand_voice_palette.md`, `reference_vertical_safe_zones.md`, and `feedback_short_form_style.md` from the user's memory before composing.

---

## Hard rules — non-negotiable

1. **Subtitles applied last** in any filter chain.
2. **30ms audio fades** at every silence-cut splice (baked into `cut_silences.py`).
3. **Never cut inside a word** — snap every cut to a word boundary from the transcript.
4. **Audio clips require `id` attributes** in HyperFrames — without them the audio is silent in the render.
5. **Top-edge graphics at `top: 9%` minimum** — TikTok cuts off anything higher.
6. **Word-level captions throughout** — every word the speaker says gets captioned.
7. **Cut every silence >0.2s** — already in `cut_silences.py`.
8. **One color used 100 times** — default any accent to the user's `ACCENT` from `brand_voice_palette.md`.

---

## What's intentionally NOT in this repo

The starter gives you the bones. The polish recipes (advanced motion graphics templates, prompt library for different video shapes, brand-locking workshop, week-over-week tuning) live in the Brad Builds AI Skool community — that's the upsell. Don't try to invent them from scratch every session.
