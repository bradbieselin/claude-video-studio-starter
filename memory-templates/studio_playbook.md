---
name: studio-playbook
description: The complete runbook for editing short-form vertical videos with Claude Code + HyperFrames + ffmpeg. Read this FIRST every session that involves video editing.
metadata:
  type: process
  priority: high
---

# Studio Playbook

> The complete process for editing a vertical short-form video. Re-read every session.

---

## 0. What this studio is for

This setup turns Claude Code into a video editor.

Drop a raw vertical recording into a project folder, tell Claude `"edit this video"`, and get back a 1080×1920 MP4 ready to upload to Instagram Reels, TikTok, and YouTube Shorts — captions, motion graphics, sound effects, color-correction, and audio cleanup all baked in.

---

## 1. Project setup — every new video

1. Create the project folder structure:
   ```
   projects/<short-slug>/
   ├── source.mp4                    ← copy of the raw source here
   ├── edit/                         ← all deliverables land here
   │   ├── transcripts/              ← Scribe JSON cache
   │   ├── cut_silences.py
   │   ├── generate_captions.py
   │   ├── brand_recolor.py
   │   └── final.mp4
   └── composition/                  ← HyperFrames composition
       ├── index.html
       ├── hyperframes.json
       └── assets/
           ├── source_tight.mp4      ← silence-cut version
           ├── face-thumb.jpg        ← extracted still (if needed)
           └── sfx/                  ← synthesized SFX library
   ```
2. Copy the helper scripts from `helpers/` into each project's `edit/` folder. They're parameterized by `--src`, `--dst`, `--edit-dir`.

---

## 2. The standard pipeline (in order)

### Step 1 — Inventory
- `ffprobe` the source: confirm dimensions, fps, duration, audio track.
- Standard target: **1080×1920 @ 30fps**. Source can be any size — HyperFrames will downscale on render. If source is 24fps, output at 30fps is fine.

### Step 2 — Transcribe (cached)
- Use a word-level verbatim ASR provider. ElevenLabs Scribe is recommended for quality; Groq Whisper works on a free tier.
- Word-level verbatim ASR only. Never SRT/phrase mode.
- Cache per source — don't re-transcribe.

### Step 3 — Pack transcript
- Optional but useful: write a phrase-level view of what was said for easier human reading.

### Step 4 — Cut silences > 0.2s (NON-NEGOTIABLE)
- Use `cut_silences.py --src <source.mp4> --edit-dir <edit>`. Detects every word-gap > 0.2s, compresses to exactly 0.2s, emits an ffmpeg filter_complex to produce `composition/assets/source_tight.mp4`, and writes a retimed transcript.
- **CRITICAL — must apply 30ms audio fades at every segment boundary.** Without fades, every splice produces an audible click. The cut script bakes this in:
  ```
  atrim={s}:{e},asetpts=PTS-STARTPTS,afade=t=in:st=0:d=0.030,afade=t=out:st={dur-0.030}:d=0.030
  ```
- **Audio cleanup chain (post-concat, broadcast voice quality):**
  ```
  highpass=f=80,afftdn=nf=-25,acompressor=threshold=0.12:ratio=3:attack=8:release=80:makeup=2,loudnorm=I=-16:TP=-1.5:LRA=11
  ```
  Removes mic rumble, FFT-denoises hiss, gently compresses dynamics, and loudness-normalizes to -16 LUFS (TikTok/IG/YT-friendly).
- **Video denoise (per-segment, removes sensor grain without softening the image):**
  ```
  hqdn3d=2:1.5:3:3
  ```
- **Encoder settings**: `libx264 -preset slow -crf 15` for the source_tight.mp4. AAC bitrate 256k for crisp voice.

### Step 5 — Generate word-level captions
- Use `generate_captions.py --transcript <tight.json> --out captions_generated.html` pointed at the **tight** transcript.
- 2-3 words per phrase, breaks on punctuation or 320ms+ gaps.
- `--hook-end <seconds>` skips phrases inside the hook window so the hero block has the frame to itself.

### Step 6 — Scaffold the HyperFrames composition
- `npx --yes hyperframes@latest init . --example blank --non-interactive --skip-skills`
- Replace the default `index.html` with the studio skeleton (see §5).
- Always 1080×1920 (NOT the default 1920×1080).

### Step 7 — Build the composition (see §5 for layout)
- Brand colors baked in from the start (see brand_voice_palette.md).
- All overlays in the safe zone (see reference_vertical_safe_zones.md).
- Continuous zoom motion on the base footage.
- Word captions throughout.
- SFX cues at punch moments (see §6).

### Step 8 — Lint relentlessly
- `npx hyperframes lint` — fix every error. Warnings are advisory but read them.
- `npx hyperframes inspect` at key timestamps — catches layout overflows.

### Step 9 — Render
- `npx hyperframes render . -o <edit>/final.mp4 --quality high --fps 30 --crf 16`
- Long videos take a few minutes — run in the background.

### Step 10 — Self-eval
- ffprobe the output — confirm duration, dimensions.
- Spot-check a few frames if needed.
- Report the path + size + duration to the user.

---

## 3. Brand defaults

See `brand_voice_palette.md` for the full palette and voice spec. The TL;DR:

- **One color, used 100 times.** Default any accent decision to the brand ACCENT color.
- **WARN sparingly** — only for punch-line / contrast moments.
- **Body text is warm off-white** (`#f3f1ea`), not pure white.
- **Body bg is brand BASE** (`#0a0a0a`), not pure black.
- **Third-party product brands** inside content (ChatGPT, Claude, Higgsfield, OpenAI, etc.) keep their actual brand colors for recognition.

---

## 4. Safe zones

See `reference_vertical_safe_zones.md`. The TL;DR:

| Edge | Px | Rule |
|------|-----|------|
| Top | 140px | Chips/badges go at `top: 9%` minimum |
| Bottom | 324px | Nothing below `top: 80%` |
| Right | 164px | Nothing right of `right: 164px` |
| Left | 60px | Standard gutter |

---

## 5. The composition skeleton

Every composition starts from this structure. Adapt content, keep the bones.

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      * { margin: 0; padding: 0; box-sizing: border-box; }
      html, body {
        margin: 0; width: 1080px; height: 1920px;
        overflow: hidden;
        background: #0a0a0a;                /* BRAND BASE — not #000 */
        font-family: "Inter", sans-serif;
      }
      #root {
        position: relative;
        width: 1080px; height: 1920px;
        overflow: hidden;
      }
      .base-wrap {                          /* non-timed wrapper for zoom transform */
        position: absolute; inset: 0;
        width: 100%; height: 100%;
        overflow: hidden;
        will-change: transform;
        transform-origin: 50% 38%;           /* anchor on face area */
      }
      .base-video {
        position: absolute; inset: 0;
        width: 100%; height: 100%;
        object-fit: cover;
      }
      /* ... section CSS goes here ... */
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0"
         data-duration="<TIGHT_DURATION>" data-width="1080" data-height="1920">
      <div class="base-wrap" id="base-wrap">
        <video id="base-video" class="clip base-video"
               data-start="0" data-duration="<TIGHT_DURATION>" data-track-index="0"
               src="assets/source_tight.mp4" muted playsinline></video>
      </div>
      <audio id="base-audio" class="clip"
             data-start="0" data-duration="<TIGHT_DURATION>" data-track-index="2"
             data-volume="1" src="assets/source_tight.mp4"></audio>

      <!-- SFX clips on tracks 100+ — see §6 -->
      <!-- Hero hook caption -->
      <!-- Top chips / badges (top: 9% minimum) -->
      <!-- Running word captions (paste from generate_captions.py output) -->
      <!-- CTA section -->
    </div>
    <script>
      window.__timelines = window.__timelines || {};
      const tl = gsap.timeline({ paused: true });
      // Base zoom keyframes
      // Hook stagger
      // Chips
      // Caption per-phrase pop
      // CTA reveal
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
```

### Short-form structural pattern (default layout)

For tutorial / how-to videos, the canonical structure (adapt durations to content length):

| Beat | Content | Layout |
|------|---------|--------|
| Hook (~2s) | 3-line caption misdirect | Centered top:50%, white/accent/white |
| B&W interrupt (~1s) | The reveal punchline | Saturation-blend overlay + bold caption |
| Setup (~5s) | What we'll do, tools listed | Tool chips top:9%, running captions |
| Steps (5-12s each) | Mock UI panels in bottom half | Step titles top:9% + UI panel bottom |
| Glitch (~1s) | Action moment | Matrix RGB-rain overlay, deterministic seeded PRNG |
| Payoff (~7s) | Result reveal + reaction | Inverted PiP, bold-keyword emphasis |
| CTA (~3s) | Black canvas + node graph + comment KEYWORD | Accent keyword in quotes + subtitle |

**Hard rules across all sections:**

- **NEVER use the face-magnifier zoom-bubble** — common short-form convention; skip it.
- **Word-level captions THROUGHOUT** — every word the speaker says gets captioned. Hook frames excluded (hero block covers them).
- **Active zoom motion** on the base footage — not subtle Ken Burns. Push 1.06-1.10× on emphasis beats, pull back on reveals.
- **Never cover the face with overlay graphics.** Chips/badges go in the top safe area (`top: 9%`). UI panels go in the bottom half. The face stays clear unless an inverted-PiP / payoff layout is in play.

**Motion graphics timing rule:**

- Emphasis badges and chips MUST fire on the precise WORD they call out, not approximately. Always pull the exact word's `start` time from the tight transcript and set `data-start` to that timestamp.
- When a big emphasis badge takes over the frame, DELETE the redundant running caption that says the same thing in that window.

---

## 6. Sound effects (SFX)

Every video gets a layered SFX track. Synthesize the library with ffmpeg (no external assets):

```bash
mkdir -p composition/assets/sfx && cd composition/assets/sfx

# Low boom (hook hits, CTA slams)
ffmpeg -y -f lavfi -i "anoisesrc=color=brown:duration=0.45" \
  -af "lowpass=f=180,afade=t=in:d=0.005:curve=exp,afade=t=out:st=0.05:d=0.4:curve=exp,volume=3.5" \
  -ac 2 -ar 44100 -b:a 192k hit-low.mp3

# Pop (chip entrances)
ffmpeg -y -f lavfi -i "sine=frequency=900:duration=0.10" \
  -af "afade=t=out:st=0:d=0.10:curve=exp,volume=0.55" \
  -ac 2 -ar 44100 -b:a 192k pop.mp3

# Soft tap (caption pops)
ffmpeg -y -f lavfi -i "sine=frequency=1400:duration=0.06" \
  -af "afade=t=out:st=0:d=0.06:curve=exp,volume=0.35" \
  -ac 2 -ar 44100 -b:a 192k tap.mp3

# Whoosh (tension rises)
ffmpeg -y -f lavfi -i "anoisesrc=color=white:duration=0.55" \
  -af "highpass=f=400,lowpass=f=2600,afade=t=in:d=0.08,afade=t=out:st=0.35:d=0.20,volume=0.65" \
  -ac 2 -ar 44100 -b:a 192k whoosh.mp3

# Sting (keyword punch)
ffmpeg -y -f lavfi -i "sine=frequency=660:duration=0.40" \
  -af "afade=t=in:d=0.005:curve=exp,afade=t=out:st=0.05:d=0.35:curve=exp,volume=0.50" \
  -ac 2 -ar 44100 -b:a 192k sting.mp3
```

### Mount in HTML

Each SFX is an `<audio class="clip">` element with a unique `id`. HyperFrames REQUIRES `id` on every audio clip — without it the audio is SILENT in the render. Put them on tracks 100+ so they never conflict with the base audio (track 2).

```html
<audio id="sfx-hook" class="clip" data-start="0.16" data-duration="0.45"
       data-track-index="100" data-volume="0.85" src="assets/sfx/hit-low.mp3"></audio>
```

### Standard cue map

| Moment | SFX | Volume |
|--------|-----|--------|
| Hook caption slam | hit-low | 0.85 |
| Chip pop-in (each) | pop | 1.0 |
| Caption pop-in (each, sparingly) | tap | 0.9 |
| Tension build before CTA | whoosh | 0.6 |
| CTA black canvas slam | hit-low | 0.95 |
| Keyword punch | sting | 0.55 |

**Audio masking rule:** SFX volumes around a spoken emphasis word should drop. If a sting plays AT the same moment as the speaker saying the keyword, the SFX masks the word. Move the sting to fire JUST AFTER the word ends, or drop its volume to ~0.55.

---

## 7. Deliverables for every video

### final.mp4

- Path: `projects/<slug>/edit/final.mp4`
- Specs: 1080×1920, 30fps, h264 + AAC stereo
- Tell the user the exact path + size + duration when done.

### Description (for IG / TikTok / YT Shorts)

- Opens with a brand-voice hook line (first sentence is the searchable headline — algorithm weights it heavily).
- Keyword-dense prose in the middle (tool names, use cases — natural, not stuffed).
- Direct CTA matching the in-video CTA.
- Hashtags spanning tool tags, use-case tags, creator-economy tags.
- Stay in brand voice. Avoid the avoid-phrases list from `brand_voice_palette.md`.

---

## 8. Anti-patterns — never do these

- Face-magnifier zoom-bubble overlay
- Subtle ken-burns motion (too quiet for short-form)
- Captions only on hooks / payoffs (need every word)
- Overlay graphics covering the face
- `top: 5%` or lower for top-edge graphics (TikTok cuts it off)
- `background: #000` (use brand BASE `#0a0a0a`)
- Pure-white `#fff` body text (use warm off-white `#f3f1ea`)
- Silences ≥ 0.2s left in the cut
- Audio clips without `id` attributes (HF renders them silent)
- Generic CTA buttons / boilerplate
- Avoid-list phrases (game-changer, hey guys, like and subscribe, etc.)

---

## 9. Quick session-start checklist

When the user asks for a video edit:

1. ✓ Read this playbook
2. ✓ Read `brand_voice_palette.md` for exact colors and voice
3. ✓ Read `reference_vertical_safe_zones.md` for layout safe area
4. ✓ Read `feedback_short_form_style.md` for content layout patterns
5. ✓ Confirm transcription API key is set in `.env`
6. ✓ Confirm `ffmpeg` is on PATH
7. ✓ Confirm Node.js 22+ for HyperFrames
8. ✓ Start at §1 of this playbook and execute the pipeline.

---

*Customize this file as you develop your own preferences. The technical recipes (audio chain, video denoise, safe zones, SFX synthesis) work across brands. The structural patterns (hook, niche tags, big reveal, CTA) are templates — adapt them to your content type.*
