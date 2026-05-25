# Claude Video Studio — Starter Kit

> *Drop a video on your desktop. Tell Claude "edit this video." Get a posted-ready short-form vertical.*

This is the open-source starter kit for editing short-form vertical videos with Claude Code as your editor. It's the same stack that produces my videos — sanitized and templated so you can plug in your own brand.

**What you get:**

- ✅ A working **silence-cutter** with audio cleanup + video denoise baked in
- ✅ A **word-level caption generator** that pulls from your transcript
- ✅ A **brand-color recolor utility** for batching CSS changes
- ✅ A **composition skeleton** wired for HyperFrames (HTML-based video framework)
- ✅ **Memory templates** for Claude — the runbook, brand palette, safe zones, style preferences
- ✅ A **first-video walkthrough** that takes you from `git clone` to a rendered MP4

**What it costs**: $0 if you already have Claude Pro. Otherwise the only paid line item is a transcription API key (ElevenLabs / Groq / OpenAI — pick one).

---

## 30-second elevator pitch

Most AI video tools are slow, branded for "AI vibes," and lock you into their templates.

This stack is the opposite:

- **You own the editor** — it's open-source HTML + ffmpeg, runs locally
- **You own the brand** — every color, font, motion graphic, caption style is defined by *you* in a single markdown file
- **You own the output** — a 1080×1920 MP4 you can post anywhere

Claude does the labor (transcribing, cutting silences, building captions, timing motion graphics to spoken words, layering SFX, rendering). You give the brief.

---

## Quick start

> 📦 Full install instructions — including how to install each prerequisite — are in **[INSTALL.md](INSTALL.md)**.

```bash
# 1. Clone this repo
git clone https://github.com/bradbieselin/claude-video-studio-starter.git
cd claude-video-studio-starter

# 2. Install Python dependencies
pip install requests python-dotenv

# 3. Copy memory templates into your Claude Code project folder
#    See INSTALL.md for the exact path on your OS

# 4. Customize your brand
#    Open memory-templates/brand_voice_palette.md and fill in every {{PLACEHOLDER}}

# 5. Get an ElevenLabs API key (free tier works) and put it in .env:
#    ELEVENLABS_API_KEY=sk_xxx

# 6. Pre-synthesize the SFX library (one time):
python helpers/synth_sfx.py --out templates/composition/assets/sfx/

# 7. Drop your first raw video into a new project folder, then tell Claude:
#    "edit this video"
```

**[→ First video walkthrough, step-by-step](examples/first-video-walkthrough.md)**

---

## What's in this repo

```
claude-video-studio-starter/
├── README.md                     ← you are here
├── INSTALL.md                    ← detailed prereq install (Mac + Windows)
├── LICENSE                       ← MIT
├── .gitignore
│
├── memory-templates/             ← copy to ~/.claude/projects/<your-project>/memory/
│   ├── MEMORY.md                 ← the index Claude reads first
│   ├── studio_playbook.md        ← the editing runbook (THE most important file)
│   ├── brand_voice_palette.md    ← customize your colors / fonts / voice
│   ├── reference_vertical_safe_zones.md  ← Reels/TikTok safe-zone spec
│   └── feedback_short_form_style.md      ← short-form aesthetic rules
│
├── helpers/                      ← Python helpers — argv-parameterized, copy into each project's edit/
│   ├── transcribe.py             ← extract audio → ElevenLabs Scribe → cached word-level JSON
│   ├── cut_silences.py           ← detect gaps >0.2s, ffmpeg-cut, fade splices, denoise, clean audio
│   ├── generate_captions.py      ← Scribe JSON → phrase-level HTML caption clips
│   ├── synth_sfx.py              ← synthesize the 5-cue SFX library from ffmpeg lavfi (no external assets)
│   └── brand_recolor.py          ← batch hex/rgba migration in composition HTML
│
├── templates/
│   └── composition/              ← HyperFrames starter scaffold
│       ├── index.html            ← skeleton with brand-color placeholders
│       └── assets/
│           └── sfx/              ← drop ffmpeg-synthesized SFX here (recipes in playbook)
│
└── examples/
    ├── first-video-walkthrough.md ← end-to-end first render
    └── recolor.example.json       ← example mapping for brand_recolor.py
```

---

## How it differs from a "post a video to AI tool" workflow

| Typical AI video tools | This stack |
|---|---|
| Web app, locked-in templates | Local — you own everything |
| Fixed aesthetic | You define the brand in markdown |
| Monthly subscription | One-time setup + your existing Claude Pro |
| Generic captions / motion | Word-boundary precise, on-brand |
| Black-box edits | Every decision is in a Claude conversation you can re-prompt |

---

## What's NOT in here (for a reason)

This is the **bones**. The starter gives you a working pipeline that produces a clean short-form video with captions, silence cuts, brand-tinted hook, zoom motion, SFX, and CTA. Enough to ship.

**Intentionally NOT included** — these are the polish recipes that distinguish a good edit from a great one:

- 🎬 **Advanced motion graphics templates** — niche-tag countdown rows, BIG "#1" reveals with rotated ribbons, matrix RGB-glitch overlays, animated workflow node graphs, AI mock UIs (ChatGPT, Higgsfield, Pinterest panels)
- 🧠 **Prompt library** for different video shapes (countdown, hook+payoff, tutorial, listicle, sales reveal, etc.)
- 🎙️ **Week-over-week tuning** of the playbook — what's working, what's flopping, the timing tweaks
- 🎨 **Brand-locking workshop** — how to fill in `brand_voice_palette.md` for *your* brand in a way that produces consistent results
- 🆘 **Setup support** when your first render breaks at 11pm

All of that lives in **[Brad Builds AI on Skool](https://www.skool.com/brad-builds-ai-9842/about)**. First week is free.

---

## License

MIT. Steal it. Build with it. Sell the videos you make with it. If you ship something cool, tag **[@bradbuildsai](https://www.instagram.com/bradbuildsai)** — I love seeing what people make.

---

*Built by [@bradbuildsai](https://www.instagram.com/bradbuildsai) · [Instagram](https://www.instagram.com/bradbuildsai) · [TikTok](https://www.tiktok.com/@bradbuildsai) · [YouTube](https://www.youtube.com/@bradbuildsai). New AI workflow every week. Steal anything that works.*
