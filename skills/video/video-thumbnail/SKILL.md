---
name: video-thumbnail
description: >-
  Render a YouTube thumbnail from real photo cutouts and HTML/CSS templates in the
  channel's visual style, using headless Chrome rather than AI image generation.
  Use when Dan asks to make or render a thumbnail, or a video-packaging hook is
  ready to become art. Do not use for thumbnail hooks and titles (video-packaging),
  blog cover images (blog-cover), or video ideas (video-ideation).
---

# Thumbnail

Compose, don't generate. AI image generation fails at exactly the two things a
thumbnail needs most: crisp text and Dan's real face. So this skill never
generates imagery. It fills an HTML/CSS template (text is perfect by
construction), drops in a real photo cutout, and renders with headless Chrome.
Same pipeline as `blog-cover`, pointed at YouTube.

## The budget: one sitting, three rounds, about 15 minutes

A review of the last six videos (2026-09) found the same pattern every time:

- Round 1's structure is what shipped. Later rounds only ever changed the face,
  the copy, or the accent word.
- The one video that took two days did so because the hook moved mid-way.
  That is a packaging problem. No amount of rendering fixes an unlocked promise.
- The same six cutouts got copied into every project folder by hand.

So the process is: lock the hook first, render real options fast, tighten the
winner, stop. Renders are cheap. Rounds are not.

## Files & assets

```
templates/hero-right.html     wordmark + pill + chips left, Dan right (house look)
templates/versus.html         two cards + VS badge, for comparison videos
templates/before-after.html   red-X line to green-check line story panel + hook badge
templates/big-type-light.html light background, huge dark ink type
templates/big-shield.html     giant cracked-shield hero + stacked type, no Dan
templates/merge-button.html   fake product UI as the hero (PR card + button + cursor)
templates/quote-card.html     one quote at max size in a thin colored frame
templates/annotated-code.html IDE window + red marker ellipse/arrow + sticky note
templates/file-explorer.html  repo file tree with ONE file circled in red marker

scripts/render.sh             render every draft HTML to 1920x1080 PNG (~3s each)
scripts/contact_sheet.py      one feed-style sheet: each option at 360px with its
                              title, plus a 120px copy. The verify step AND the
                              thing Dan reacts to.
scripts/cutout.swift          Apple Vision subject lift: swift cutout.swift <in> <out.png>
scripts/figma_client.py       JSON-RPC client for the remote Figma MCP when its
                              tools aren't attached: figma_client.py <tool> '<json>'
scripts/paper_client.py       legacy (Paper MCP), only for pulling old boards

/Users/vega/youtube/shared-assets/thumbnail/cutouts/
                              THE cutout library. Named transparent PNGs
                              (<expression>-<outfit>.png), manifest.md, and
                              cutouts-sheet.png (every cutout with its name in
                              one image). Templates reference these by absolute path.
/Users/vega/youtube/shared-assets/thumbnail/photos/
                              raw Photo Booth shots. Source material for new
                              cutouts only. Never browse this during a round.
/Users/vega/youtube/shared-assets/thumbnail/doodles/
                              hand-drawn PNG/SVG assets (arrows, circles)
```

Output goes to the video project's `06_Thumbnails/` folder. If the project
folder does not exist under `/Users/vega/youtube/`, run `video-project` first.

## Workflow

### Round 0: get the hook. Do not render without it.

`mcp__contentos__list_videos(slug)` returns the long-form video's locked title
and thumbnail hook (text, hero device, expression). If either is missing or
vague, stop and run `video-packaging`. Rendering against an unlocked promise is
how a thumbnail takes two days.

### Round 1: three or four real options (about 5 minutes)

1. **Pick the hero devices.** Choose 3 or 4 from the structure list below,
   each a different device. Each gets its own text angle where possible
   (mechanism, outcome, reaction). Add a fourth only when the hook genuinely
   supports another angle, never to pad. The house look has no reserved slot.
2. **Pick the faces.** Read `cutouts/cutouts-sheet.png` once. Choose by
   expression name. Different expressions across options sell "different
   style" harder than palette does. Make a new cutout only when the library
   lacks the expression the hook needs (see Getting a new cutout).
3. **Fill a template per option.** Copy the closest template into the
   scratchpad and edit the numbered `<!-- FILL -->` sections. Rules for
   every option, whatever the palette:
   - ONE accent color hit: one word, number, or element. Never two.
   - Real text budget is 4 words or fewer. Chips and code lines are texture
     and don't count.
   - Thumbnail text must not repeat the title. The pair reads together.
   - Keep type clear of the cutout's head. No text over the face.
   - Cutouts read smaller than you think. Bottom-anchor at 85 to 90% of frame
     height (chest-up) unless the option wants Dan small or absent.
   - No logos beyond the built-in AI-box/sparkle marks.
4. **Render them in one call** (sequential, about 3 seconds each; do not
   parallelize Chrome, it stops exiting):

   ```bash
   scripts/render.sh draft-*.html
   ```

5. **Build one sheet and Read it.** This is the verify step and the shrink
   test in one image:

   ```bash
   scripts/contact_sheet.py -o round1.png -t "<candidate title>" ... draft-*.png
   ```

   Pass one `-t` per image (repeat the same title if only the thumbnails
   differ). On the sheet, check: nothing clipped, nothing touching the face,
   accent on the right word, and the hook phrase plus face still read in the
   120px copy. Fix and re-render until it passes. Do not Read the individual
   PNGs; the sheet is enough.
6. **Save, send, stop.** Copy the PNGs and HTML into `06_Thumbnails/` as
   `thumbnail-v1-<style>.png` and `.html`. Send the sheet with `SendUserFile`
   so Dan can react from his phone. Then wait. Dan picks one and says what's off.

### Round 2: tighten the winner (about 5 minutes)

Three takes (`v2a`, `v2b`, `v2c`) that keep the winner's structure and vary
what actually changed in past shipped versions:

- **Expression:** a different cutout in at least two takes.
- **Copy:** the hook words or which word carries the accent.
- **One composition move:** flip Dan to the other side, size the hero up or
  down, or tighten the crop. One move per take.

Do not re-execute the concept in a new visual language, palette, or template.
That was the old "winner variation round", and Dan's verdict on it was
"pretty much the same" (2026-07-23). If he wants a different direction he will
say so. If he is torn between two titles, put both on the sheet. Same render,
same sheet, same send.

### Lock

1. Copy the winner to `06_Thumbnails/thumbnail-final.png` and `.html`.
2. `mcp__contentos__set_pipeline_stage(slug, "THUMBNAIL_READY")`.
3. `mcp__contentos__update_video_packaging(slug, thumbnailConcept="<hook> · final: 06_Thumbnails/thumbnail-final.png")`
   so the record points at the art.

**Face swap first, Figma second.** When Dan loves the thumbnail but not the
photo, change the `img.dan` src to another library cutout and run `render.sh`.
That is seconds. Offer the Figma capture only when he wants to hand-edit
something a src swap can't do.

## Structure list (hero devices)

Vary at least two of {layout, palette, hero device} between options. Tagged
with what has shipped on the channel so the picks are evidence, not taste:

- **ui-artifact** (`merge-button.html`): a fake product UI as the hero. The
  click or decision moment rendered as a real interface; the button is the
  accent. Shipped: "WOULD YOU?" merge button, "TRUST AI?" fix-everything button.
- **file-explorer** (`file-explorer.html`): editor file tree with one file
  circled in red marker, for "what IS this file" hooks. Shipped: "YOU'VE SEEN
  THIS FILE".
- **story-panel** (`before-after.html`): red-X line to green-check line.
  Shipped: "IT LEAKS!", "ONE LINE".
- **hand-drawn** (`annotated-code.html`, or freehand SVG over a dark ground):
  marker circles, arrows, a map. Shipped: "you are here" adoption map.
- **house-terminal** (`hero-right.html`, `versus.html`): dark green + plexus +
  big white type. Shipped: "Tool Search", most 2025 thumbnails. Competes for a
  slot like any other direction; some rounds it won't appear.
- **designer-komika**: deep purple/navy, Komika Axis display type (white line
  + green line, often a question), JetBrains Mono code panel. Shipped: "WATCH
  IT THINK?!". No template yet; build from the published thumbnail when picked.
- **code-panel** (`annotated-code.html` without the sticker): the hook is a
  line of code or config, shown huge, one token in the accent color.
- **big-object** (`big-shield.html`): one giant object as the hero, Dan small
  or absent. Rendered several times, never shipped. Use when the hook IS an
  object.
- **quote-card** (`quote-card.html`): one line someone says, at max size.
  Rendered, never shipped. Use only when the hook is a quote.
- **clean-light** (`big-type-light.html`): paper background, huge dark type.
  Rendered often, never shipped, but it is the only option that stands out in
  a dark feed. Keep offering it as the odd one out.

The **"Thumbnail Inspiration" Figma file** (fileKey `vwHATW30WF1B8da9CVDHpv`,
page `0:1`) is where new structures come from. Consult it when adding a
direction to this list (see Growing the library), not every round. The list
above is the distilled result of past consults.

## Getting a new cutout

**From any photo** (photoshoot, phone shot; plain background works best):

```bash
swift scripts/cutout.swift <photo.jpg> <expression>-<outfit>.png
```

**From this video's raw footage** (the shirt matches the video; expressions
are free because Dan makes them all on camera):

```bash
# contact sheet: one small frame every 5s. Read a few to pick a timestamp
ffmpeg -i <raw.mp4> -vf "fps=1/5,scale=480:-1" -q:v 4 frames/f_%03d.jpg
# extract the chosen moment at full res, then cut it out
ffmpeg -ss <timestamp> -i <raw.mp4> -frames:v 1 frame.png
swift scripts/cutout.swift frame.png <expression>-<outfit>.png
```

Watch for motion blur and mid-word mouths. Step the `-ss` by 0.1s until the
frame is sharp. Every keeper goes into `shared-assets/thumbnail/cutouts/`
with the naming scheme, a row in `manifest.md`, and a rebuilt
`cutouts-sheet.png` (snippet below). Never leave cutouts only in a project
folder; that is how the library went stale in 2026-07.

## Design tokens (house-terminal direction)

These bind only the dark-green house look. Other directions define their own
palette but keep the same text discipline.

- Background: `linear-gradient(135deg, #0c1a10, #08120b, #060d08)` + soft
  green radial glows + the faint plexus SVG. Dark enough that white 900-weight
  type carries.
- Accent green `#6cd97e`; card/chip borders `#3f7a4d`; muted text `#9fc7a8`.
- Type: Inter/SF 800 to 900 weight, tight letter-spacing; text-shadow for depth.
- Cutout: bottom-anchored, right third,
  `drop-shadow(-18px 0 40px rgba(0,0,0,0.55))` over a soft green radial
  `.glow`. Err big: 85 to 90% of frame height. Let chips overlap the shirt
  rather than shrinking Dan.

## Growing the library

**New structure:** when a hook fits nothing on the list, pull an overview of
the inspiration file (`get_screenshot` on page `0:1` at maxDimension ~2400,
split with sips to review), extract the bones (layout grid, hero device, where
the tension comes from), build it as a new annotated template with the FILL
convention, test-render once, and add it to the structure list. Bones only,
never their colors, assets, or branding.

**New cutout:** see above. Rebuild the picker sheet after adding one:

```bash
cd /Users/vega/youtube/shared-assets/thumbnail/cutouts && python3 - <<'EOF'
import os
from PIL import Image, ImageDraw, ImageFont
files=sorted(f for f in os.listdir('.') if f.endswith('.png') and f!='cutouts-sheet.png')
W,H=300,330; cols=5; rows=(len(files)+cols-1)//cols
sheet=Image.new('RGB',(cols*W,rows*H),'#3a3a3a'); dr=ImageDraw.Draw(sheet)
fnt=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf',15)
for i,f in enumerate(files):
    im=Image.open(f).convert('RGBA'); im.thumbnail((W-10,H-40))
    x,y=(i%cols)*W,(i//cols)*H
    bg=Image.new('RGBA',im.size,'#3a3a3a'); bg.alpha_composite(im); sheet.paste(bg.convert('RGB'),(x+5,y+5))
    dr.text((x+8,y+H-28),f.replace('.png',''),fill='white',font=fnt)
sheet.save('cutouts-sheet.png')
EOF
```

Doodles for the hand-drawn direction can be authored in Figma and exported as
transparent PNG into `shared-assets/thumbnail/doodles/`. Templates, cutouts,
and doodles compound. Every video should leave the library slightly richer.

## Figma (opt-in: hand-edit the winner)

Figma is where a finished thumbnail becomes hand-editable, for the cases a
src swap can't cover. It is not part of the rounds. Capture only the winner,
only when Dan asks, and only after the face-swap offer.

The remote Figma MCP server (`https://mcp.figma.com/mcp`) is registered in
Claude Code user config as `figma` (OAuth done; Dan is a Full seat on the Team
Vega pro plan). If the tools aren't attached, drive it with
`scripts/figma_client.py <tool> '<json>'`; it reads the OAuth token Claude
Code stored in the macOS keychain.

The **"YouTube Thumbnails" Figma file is the canonical board**, fileKey
`qxwLTGPFH4RPlV5cZOYrqS`, one page `0:1`. Dan's monthly grid of published
thumbnails lives there; captured drafts land in a row to the right of it.

**The capture recipe (proven end-to-end, 2026-07):**

1. Prep the winner's HTML: add
   `<script src="https://mcp.figma.com/mcp/html-to-design/capture.js" async></script>`
   to `<head>`, copy the cutout next to the HTML and make the `img src`
   RELATIVE (absolute paths 404 over HTTP and you get a blank cutout), and
   `sips -Z 1400` that copy. Cutout PNGs much over 2 MB silently drop out of
   the capture.
2. Serve the folder: `python3 -m http.server 8931`.
3. Mint a capture: `generate_figma_design {"fileKey": ..., "url":
   "http://localhost:8931/<page>.html"}`. The response contains a single-use
   `captureId` and a hash URL. Change its `figmadelay` to `4000` so the image
   finishes decoding.
4. Open the hash URL in the in-app Browser pane: `preview_start {url:
   <hash-url>}` (plain `navigate` to localhost is blocked by policy). The page
   shows "Sending to Figma…" while uploading; allow 1 to 3 minutes.
5. Poll `generate_figma_design {"fileKey": ..., "captureId": ...}` every ~10s
   until it reports the design was added, with a node id. Never mint a new id
   while one is pending.
6. The capture arrives as a 1920x1080 FRAME named "Document" on page `0:1`.
   Verify with `get_screenshot {"fileKey", "nodeId"}` before telling Dan it's
   there. Rename the frame to `<Project> / final` via `use_figma` (check
   `node.parent.type` first; never rename the page). Align its `y` with the
   existing row if it lands offset.

Fine-grained edits from there use `use_figma` (Figma Plugin API JavaScript).
ALWAYS read the `skill://figma/figma-use/SKILL.md` MCP resource first. For
the final PNG: Dan exports at 1920x1080 (or `download_assets`), then copy it
over `06_Thumbnails/thumbnail-final.png`.

History: Paper (paper.design) played this role until 2026-07 and was dropped
for its price and MCP call caps. Old artboards (v1 house-hero, the
designer-komika reference boards) still live in the Paper file.

## Chain mode

When `contentos-next` invokes this skill with "chain mode" in the arguments, run round 1
exactly as above, save the options to `06_Thumbnails/`, send the sheet, and return. Do not
lock. Dan picks at the Edit stop, or earlier if he asks. If `THUMBNAIL_READY` is already
ticked with a working concept from packaging, leave it; the lock step replaces the concept
with the rendered art once he picks.
