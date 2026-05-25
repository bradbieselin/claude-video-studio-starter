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

# 2. Install the helper script dependencies
pip install requests python-dotenv

# 3. Copy memory templates into your Claude Code project folder
#    See INSTALL.md for the exact path on your OS

# 4. Customize your brand
#    Open memory-templates/brand_voice_palette.md and replace every {{PLACEHOLDER}}
#    with your own colors, font, voice, social handles, and CTA links

# 5. Set up a transcription provider
#    Get an API key from elevenlabs.io / groq.com / openai.com
#    Put it in .env at the project root: ELEVENLABS_API_KEY=...

# 6. Drop your first raw video into a new project folder and tell Claude:
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
│   ├── cut_silences.py           ← detect gaps >0.2s, ffmpeg-cut, fade splices, denoise, clean audio
│   ├── generate_captions.py      ← Scribe JSON → phrase-level HTML caption clips
│   └── brand_recolor.py          ← batch hex/rgba migration in composition HTML
│
├── templates/
│   └── composition/              ← HyperFrames starter scaffold
│       ├── index.html            ← skeleton with brand-color placeholders
│       └── assets/
│           └── sfx/              ← drop ffmpeg-synthesized SFX here (recipes in playbook)
│
└── examples/
    └── first-video-walkthrough.md ← end-to-end first render
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

This is the **bones**. The starter that gets you a clean working pipeline.

What's not in here:

- 🎨 *My specific brand palette and aesthetic presets* — yours will be different
- 🎬 *The advanced motion graphics templates* — matrix glitches, node graphs, niche-tag systems, etc.
- 🧠 *My prompt library* for different video shapes (countdown, hook+payoff, tutorial, listicle, etc.)
- 🎙️ *The week-over-week tuning* I do on my own playbook

If you want those — and you want help when your first render breaks at 11pm — join the community at **[Brad Builds AI on Skool](https://www.skool.com/brad-builds-ai-9842/about)**. First week is free.

---

## License

MIT. Steal it. Build with it. Sell the videos you make with it. If you ship something cool, tag **[@bradbuildsai](https://www.instagram.com/bradbuildsai)** — I love seeing what people make.

---

*Built by [@bradbuildsai](https://www.instagram.com/bradbuildsai) · [Instagram](https://www.instagram.com/bradbuildsai) · [TikTok](https://www.tiktok.com/@bradbuildsai) · [YouTube](https://www.youtube.com/@bradbuildsai). New AI workflow every week. Steal anything that works.*
