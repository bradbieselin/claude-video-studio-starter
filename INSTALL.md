# Install Guide

Everything you need to install on your machine before the first video edit. Plan for **20-30 minutes** the first time, **2 minutes** every time after.

---

## Prerequisites

| Tool | Why | Approx size |
|---|---|---|
| **Claude Code** | The agent that does the editing | ~50 MB |
| **Node.js 22+** | HyperFrames runs on this | ~100 MB |
| **Python 3.11+** | The helper scripts | ~150 MB |
| **ffmpeg + ffprobe** | All video / audio cuts and encoding | ~80 MB |
| **uv** *(optional, recommended)* | Faster Python deps | ~20 MB |
| **Git** | Cloning this repo | ~50 MB |

You also need:

- ✅ An **Anthropic Claude account** (Claude Pro recommended — the workflow uses a lot of context per video)
- ✅ One of: **ElevenLabs API key** *(recommended — best transcription quality)*, **Groq API key** *(free tier works)*, or **OpenAI API key** *(more expensive)*

---

## Step 1 — Install Claude Code

Follow the official guide at **[claude.com/code](https://claude.com/code)**.

After install, verify:

```bash
claude --version
```

You should see a version number.

---

## Step 2 — Install Node 22+

**macOS** (via Homebrew):
```bash
brew install node@22
```

**Windows** (PowerShell):
- Download the LTS installer from **[nodejs.org](https://nodejs.org)**
- Run it, accept defaults
- Restart your terminal

Verify:
```bash
node --version    # should be v22.x.x or higher
npx --version
```

---

## Step 3 — Install Python 3.11+

**macOS:**
```bash
brew install python@3.13
```

**Windows:**
- Download from **[python.org/downloads](https://www.python.org/downloads/)**
- During install, **check "Add Python to PATH"**

Verify:
```bash
python --version  # Windows
python3 --version # Mac/Linux
```

### Recommended: install `uv` for fast Python deps

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

---

## Step 4 — Install ffmpeg

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
- Easiest: `winget install Gyan.FFmpeg`
- Or download from **[ffmpeg.org/download.html](https://ffmpeg.org/download.html)** and add to PATH

Verify:
```bash
ffmpeg -version
ffprobe -version
```

---

## Step 5 — Get a transcription API key

The helper script uses **ElevenLabs Scribe** by default (best quality). Alternatives: Groq Whisper (free tier), OpenAI Whisper (paid).

### ElevenLabs (recommended)

1. Go to **[elevenlabs.io](https://elevenlabs.io)** → sign up
2. Settings → API Keys → create new key
3. Copy the key

### Save the key

Create a `.env` file in your project root:

```
ELEVENLABS_API_KEY=sk_xxx_your_key_here
```

> ⚠️ Add `.env` to `.gitignore` if you're putting your project in a public repo.

---

## Step 6 — Clone this starter kit

```bash
git clone https://github.com/bradbieselin/claude-video-studio-starter.git
cd claude-video-studio-starter
```

---

## Step 7 — Set up Claude memory

Claude Code reads project-specific memory from a folder under your home directory. The path depends on your OS:

| OS | Memory path |
|---|---|
| **macOS / Linux** | `~/.claude/projects/<your-project-slug>/memory/` |
| **Windows** | `C:\Users\<you>\.claude\projects\<your-project-slug>\memory\` |

The `<your-project-slug>` is the slugified path of your project folder. Example:

- Project at `/Users/jane/video-studio` → slug `Users-jane-video-studio`
- Project at `D:\my-studio` → slug `D--my-studio`

Copy the contents of `memory-templates/` from this repo into that folder:

```bash
# macOS / Linux
mkdir -p ~/.claude/projects/<your-slug>/memory
cp memory-templates/*.md ~/.claude/projects/<your-slug>/memory/

# Windows (PowerShell)
mkdir C:\Users\<you>\.claude\projects\<your-slug>\memory
Copy-Item memory-templates\*.md C:\Users\<you>\.claude\projects\<your-slug>\memory\
```

---

## Step 8 — Customize your brand

Open `~/.claude/projects/<your-slug>/memory/brand_voice_palette.md` and **replace every `{{PLACEHOLDER}}`** with your own values:

- `{{YOUR_ACCENT_HEX}}` — your single brand accent color (one color, used 100 times)
- `{{YOUR_WARN_HEX}}` — your "danger / punchline" color (used sparingly)
- `{{YOUR_HANDLE}}` — your social handle (e.g., `@yourname`)
- `{{YOUR_INSTAGRAM_URL}}` etc.
- `{{YOUR_SKOOL_URL}}` — your CTA destination (community, email list, whatever)
- `{{YOUR_NORTH_STAR}}` — the one-line filter for every piece of content

Do the same with `studio_playbook.md` — search for `{{` and fill in.

> 💡 The placeholders are deliberately obvious so you can't miss any. Search-and-replace with your editor's find tool.

---

## Step 9 — Test the install

In your project folder:

```bash
# Test Claude Code reads the memory
claude
# In Claude: "what's in my studio playbook?"
# Claude should summarize the playbook from memory.

# Test HyperFrames
npx --yes hyperframes@0.6.40 --help

# Test ffmpeg + ffprobe
ffmpeg -version
ffprobe -version

# Test Python helpers
python helpers/cut_silences.py --help
```

If all four work, you're set.

---

## Step 10 — First video

Follow **[examples/first-video-walkthrough.md](examples/first-video-walkthrough.md)** to take a raw recording all the way to a posted-ready MP4.

---

## Stuck?

Setup hiccups are very system-specific. If you hit one, **the Skool community has a dedicated `#setup-support` channel** — usually fastest place to get unblocked.

**[→ Join Brad Builds AI on Skool](https://www.skool.com/brad-builds-ai-9842/about)** — First week is free.
