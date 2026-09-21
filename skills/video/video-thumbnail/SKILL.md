---
name: video-thumbnail
description: >-
  Design varied YouTube thumbnails using Dan's real photos, recent channel art,
  and concept-specific HTML/CSS compositions rendered with headless Chrome.
  Use when Dan asks to make or render a thumbnail, or a video-packaging hook is
  ready to become art. Do not use for thumbnail hooks and titles (video-packaging),
  blog cover images (blog-cover), or video ideas (video-ideation).
---

# Thumbnail

Compose with real photos and HTML/CSS. Keep Dan recognizable and the type crisp.
Choose the visual story first; templates are implementation shortcuts, not the
creative brief. A new background behind the same pose and text block is not a
new direction. Full studio photos are valid assets alongside transparent cutouts.

## Keep the rounds useful

Get the promise clear, explore distinct visual stories, then tighten the winner.
Aim for one sitting, but do not trade away photo discovery or visual variety to
meet a time limit. September 2026 feedback: the options had become repetitive
despite different template names. Judge variety by what the viewer sees.

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
scripts/photo_sheet.py        paginated picker for original photos or cutouts,
                              with numbered source-path index
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
                              original Photo Booth shots. Browse when choosing
                              poses; use as full photos or make new cutouts.
/Users/vega/youtube/shared-assets/thumbnail/doodles/
                              hand-drawn PNG/SVG assets (arrows, circles)
```

Output goes to the video project's `06_Thumbnails/` folder; only the locked winner goes
in `06_Thumbnails/final/`. If the project
folder does not exist under `/Users/vega/youtube/`, run `video-project` first.

## Workflow

### Round 0: establish the promise

Read the video's title, brief, and thumbnail hook from ContentOS when its tools
are available. Lock the promise, not the template or expression: packaging's
suggested device and pose are starting points unless Dan explicitly chose them.
For a normal production round, resolve a vague promise through `video-packaging`.
For an explicitly exploratory request, use a stated working promise and label
drafts as exploratory. If ContentOS is unavailable, use supplied context or a
local brief and disclose the gap; never claim to have read or updated the record.
Before concluding ContentOS is unavailable, check the client's MCP configuration.
The local server is `http://localhost:8888/mcp`, authenticated with `X-API-Key`;
the browser's form-login screen does not test MCP access. Reuse the existing
configured connection without printing credentials. Discover the tool schemas,
then read `get_project`, `get_brief`, and `list_videos` for the matched slug.

### Check the channel and the photo library

Before picking concepts, read [references/creative-range.md](references/creative-range.md).
Review a small recent set of selected/published thumbnails, ideally 6 to 10, from
ContentOS, the canonical Figma board, or local final files. Prefer actual publish
order; modification times only establish local recency. Label drafts as drafts
and state when the available sample is incomplete. Note repeated pose families,
face position/size, layout, and visual devices in `06_Thumbnails/selection.md`.

Inspect the cutout picker **and** the original-photo picker when exploring new
directions or when recent thumbnails repeat a pose. Build missing picker pages:

```bash
python3 scripts/photo_sheet.py /Users/vega/youtube/shared-assets/thumbnail/photos \
  -o /Users/vega/youtube/shared-assets/thumbnail/photo-picker
```

Use the numbered index to recover exact sources. Reuse current picker pages
within the session. Select by gesture, gaze, emotion, and crop potential before
outfit. Do not treat a differently dressed version of the same pointing pose as
new visual range. Recent use breaks ties between equally suitable photos; it
does not outweigh a pose that actually tells the story. See the reference for
the lightweight selection record and how to find unused source photos.

### Round 1: three or four real options (about 5 minutes)

1. **Pick visual stories.** Usually three options are enough. Each should make
   a different visual argument for the same promise, such as disproportionate
   effort, a simpler alternative, or a decision boundary. Write one sentence
   per option before looking for a template. Use the structure list as examples,
   not a closed menu. The house look has no reserved slot.
2. **Cast each photo.** Choose a different source and pose family for each
   face-led direction where suitable assets exist. Match gaze and gesture to
   the focal object. Consider calm confidence, skepticism, and natural studio
   photos as well as surprise. Do not force every face into the right third.
   A new cutout is worthwhile for a fresher suitable pose, even when the library
   already has an expression with the same name. Note any asset limitation.
3. **Compose each option.** Adapt a template or build fresh HTML/CSS. Clear the
   template's sample photo, badges, chips, and code before adding what this
   concept needs. Do not preserve decoration just because it was in the file.
   Rules for every option, whatever the palette:
   - Give the eye one dominant focal point. Color supports hierarchy; a
     comparison may need more than one semantic color.
   - Aim for 4 words or fewer across the readable message. Labels, chips, and
     code create clutter too; they are not a loophole in the text budget.
   - Thumbnail text must not repeat the title. The pair reads together.
   - Keep type clear of the cutout's head. No text over the face.
   - Choose face size and position per story: close portrait, left, center,
     small reaction, or absent. Check recognition at feed size. Do not mirror
     shirt lettering/logos to manufacture a different gaze direction.
   - Use logos only when they identify the actual subject. No automatic AI
     sparkle, pills, or branding ornament on unrelated videos.
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
   clear hierarchy, and the main idea still reads in the 120px copy. Also check
   **range**: ignore color and copy. If the options still have the same face
   placement, silhouette, and object relationship, replace a concept before
   presenting. Compare with the recent channel sample, not just this round.
   Fix and re-render until it passes. Inspect individual PNGs when the sheet
   cannot reveal a cutout edge, crop, or text issue.
6. **Save, send, stop.** Copy the PNGs and HTML into `06_Thumbnails/` as
   `thumbnail-v1-<concept>.png` and `.html`. Include the source photos, visual
   differences, and provisional/selected status in `selection.md`. Show the
   sheet inline with a local image link, or use `SendUserFile` if available.
   Recommend one and explain its tradeoff. Dan picks one and says what's off.

### Round 2: tighten the winner (about 5 minutes)

Make only the variants needed to answer Dan's feedback. When he likes the
concept, keep its structure and vary the unresolved choice:

- **Expression:** compare suitable poses if the photo is the unresolved choice.
- **Copy:** the hook words or which word carries the accent.
- **One composition move:** flip Dan to the other side, size the hero up or
  down, or tighten the crop. One move per take.

If the feedback is "same", "boring", or "blah", reopen the visual concept;
more face swaps or palette changes will not answer it. If he is torn between
two titles, put both on the sheet. Same render, same sheet, same delivery.

### Lock

1. Copy the winner to `06_Thumbnails/final/thumbnail-final.png` and `.html`. The
   `final/` folder holds only the locked thumbnail (plus its HTML) so Dan can find it
   without digging through rounds and takes. Create the folder if the template did not.
   Every draft, take, and sheet stays in `06_Thumbnails/` itself; never put them in `final/`.
2. `mcp__contentos__set_video_thumbnail(slug, filePath="<absolute path to final/thumbnail-final.png>")`
   so the art itself lands on the video in ContentOS. Dan should never have to
   drag it in by hand. It stores under a fixed name, so re-locking replaces the
   old final. PNG or JPEG, 5MB max. If the tool is missing from the session's
   tool list (the list loads at session start), call it over the MCP endpoint.
3. `mcp__contentos__set_pipeline_stage(slug, "THUMBNAIL_READY")`.
4. `mcp__contentos__update_video_packaging(slug, thumbnailConcept="<hook> · final: 06_Thumbnails/final/thumbnail-final.png")`
   so the record points at the art.
5. Update `selection.md` with the selected source photo/cutout, pose family,
   composition, hero device, and decision date. Record published status only
   when verified. Future rounds read this record instead of guessing usage.

If ContentOS tools are unavailable, save the local result and report the pending
record update. Do not call drafts final or tick stages before Dan selects.

**Face swap first, Figma second.** When Dan loves the thumbnail but not the
photo, change the `img.dan` src to another library cutout and run `render.sh`.
That is seconds. Offer the Figma capture only when he wants to hand-edit
something a src swap can't do.

## Structure list (hero devices)

Vary the composition and visual argument, not merely palette. Tagged
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
  Rendered often, never shipped in the original sample. Use when a light field
  serves this concept; it does not earn a slot just for being light.
- **photo-editorial**: an original studio photo, deliberate crop, and minimal
  type; the expression and setting carry the argument. No cutout required.
- **scale-metaphor**: make effort or stakes visible through a large/small
  object relationship. Keep any illustrative document/UI clearly conceptual;
  do not invent measured results or pass it off as a real product screenshot.

The **"Thumbnail Inspiration" Figma file** (fileKey `vwHATW30WF1B8da9CVDHpv`,
page `0:1`) is one source of new structures. Consult it when the existing
directions repeat or lack a suitable story. If access is unavailable, design
from the concept; do not block or invent a review of the board.

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

**New structure:** build a composition that fits the hook. When the inspiration
file is accessible, an overview (`get_screenshot` on page `0:1` at maxDimension
~2400) can help identify layout, hero device, and the source of tension. Borrow
structure, not someone else's assets or branding. Promote a successful reusable
composition into an annotated template after review; do not grow the template
library for every exploratory draft.

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
over `06_Thumbnails/final/thumbnail-final.png`.

History: Paper (paper.design) played this role until 2026-07 and was dropped
for its price and MCP call caps. Old artboards (v1 house-hero, the
designer-komika reference boards) still live in the Paper file.

## Chain mode

When `contentos-next` invokes this skill with "chain mode" in the arguments, run round 1
exactly as above, save the options to `06_Thumbnails/`, send the sheet, and return. Do not
lock. Dan picks at the Edit stop, or earlier if he asks. If `THUMBNAIL_READY` is already
ticked with a working concept from packaging, leave it; the lock step replaces the concept
with the rendered art once he picks.
