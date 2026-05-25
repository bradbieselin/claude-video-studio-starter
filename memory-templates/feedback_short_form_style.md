---
name: feedback-short-form-style
description: Default aesthetic preferences for short-form / talking-head vertical edits.
metadata:
  type: feedback
---

# Short-form style preferences

Default preferences for AI-tutorial / talking-head short-form vertical edits. Override any of these by telling Claude what you want different.

1. **NO face-magnifier zoom-bubble overlay** — the circular floating bubble that magnifies a face detail in the upper corner. Common short-form convention; we skip it.

2. **Word-level captions THROUGHOUT THE ENTIRE VIDEO** — every word the speaker says gets captioned. Not just hooks and payoffs. Hook frames get the 3-line hero caption block; the rest of the video runs continuous word-grouped captions synced to speech. 2-3 words per phrase, centered, mid-frame, white bold italic with black stroke.

3. **Active zoom-in / zoom-out motion on the base talking-head** — noticeable movement, not just subtle Ken Burns drift. Push in on emphasis beats, pull out on reveals, vary continuously across the cut.

4. **Cut every silence longer than 0.2 seconds** — keeps the pacing tight. `cut_silences.py` handles this automatically.

5. **30ms audio fades at every splice** — prevents click/pop artifacts at silence-cut boundaries. Baked into `cut_silences.py`.

6. **Motion graphics fire on the spoken word, not approximately** — when adding an emphasis badge or chip, set its `data-start` to the exact word's timestamp from the tight transcript.

7. **When a big emphasis takes the frame, DELETE the redundant running caption** under it. The badge IS the caption — having both is visual noise.
