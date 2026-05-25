# Your first video — end to end

You've finished `INSTALL.md`. All prereqs check out. Brand palette filled in. Memory templates copied into your Claude folder.

Now ship the first video.

---

## 1. Record

- Phone, vertical (9:16), well-lit.
- 30 seconds to 2 minutes is the sweet spot.
- One take. Don't try to be perfect — silence cuts will tidy it up.
- Save the file somewhere easy to find. Desktop is fine.

---

## 2. Create the project folder

```
projects/my-first-video/
├── source.mp4                 ← drop your recording here
├── edit/
│   └── transcripts/
└── composition/
    └── assets/
```

Copy the helper scripts from this repo's `helpers/` folder into your new project's `edit/` folder.

Copy `templates/composition/index.html` into your new project's `composition/` folder.

---

## 3. Open Claude Code in the project root

```bash
cd projects/my-first-video
claude
```

Claude reads your memory automatically. The studio playbook loads first.

---

## 4. The one-line prompt

In Claude, paste:

```
edit this video at source.mp4
```

That's it. Claude will:

1. **ffprobe** the source — confirms dimensions, fps, duration.
2. **Transcribe** with ElevenLabs Scribe (or your chosen provider). Cached.
3. **Cut silences** > 0.2s using `cut_silences.py`. Audio fades, denoise, audio cleanup all baked in.
4. **Generate captions** from the tight transcript.
5. **Build the composition** by editing `composition/index.html` — hook, captions, motion graphics, SFX.
6. **Lint + inspect** the composition.
7. **Render** the final MP4.

Total active time on your end: **answering 2-3 clarifying questions** if Claude has them. Otherwise it just executes.

---

## 5. Review the preview

While the render runs, you can preview the composition live in your browser:

```bash
# In a new terminal, from the project's composition folder:
cd composition
npx --yes hyperframes@latest preview
```

Open `http://localhost:3002`. Scrub the timeline. See every beat exactly as it'll render.

---

## 6. Iterate (or ship)

If anything's off, tell Claude what to fix. Examples:

- *"the 'X' badge is too early — move it to when I actually say 'X'"*
- *"the SFX on the keyword is masking my voice — drop it 50%"*
- *"add a big '#1' emphasis on the final reveal"*
- *"this lime is too saturated — knock it back 10%"*

Each tweak is a re-render (~1-3 min depending on length).

When you're happy with the preview, the final MP4 is at:

```
projects/my-first-video/edit/final.mp4
```

---

## 7. Post it

Drag `final.mp4` into your Reels / TikTok / YouTube Shorts uploader. It's 1080×1920 at 30fps with AAC stereo — every platform accepts it as-is.

---

## 8. Repeat

Every future video: drop the source, open Claude, paste the one-liner. Active time per video after this drops to **under a minute**.

---

## Troubleshooting

| Issue | Fix |
|---|---|
| "ELEVENLABS_API_KEY not set" | Add it to `.env` at the project root |
| Audio is silent in the render | Every `<audio class="clip">` needs a unique `id` |
| Captions in wrong place | Check `--hook-end` arg to `generate_captions.py` |
| Chips clipped at the top | Move them to `top: 9%` minimum (safe zone) |
| Audio clicks at cut points | Re-run `cut_silences.py` (30ms fades should be auto) |
| Choppy / grainy footage | Make sure you re-ran cut after pulling latest scripts — `hqdn3d` + audio chain are baked into newer versions |

For anything not on this list — or weird system-specific issues — **join the community at [Brad Builds AI on Skool](https://www.skool.com/brad-builds-ai-9842/about)**. First week free, dedicated `#setup-support` channel.

---

## What's next

- 📺 Watch your first three videos. Note what feels off, iterate the playbook.
- 🧪 Try different content shapes: countdown, hook+payoff, tutorial, listicle.
- 🎨 Refine your brand palette as you see what reads on small screens.
- 💬 Drop into the Skool community for prompt templates, motion graphics presets, and weekly walkthroughs of advanced video shapes.

**[→ Join Brad Builds AI on Skool](https://www.skool.com/brad-builds-ai-9842/about)** — Steal what works.
