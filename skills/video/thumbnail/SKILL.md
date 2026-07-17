---
name: thumbnail
description: Render the final thumbnail art for a YouTube video — composes real photo cutouts of Dan with HTML/CSS templates in the channel's design language (dark green, big white type, one green accent) and renders to PNG with headless Chrome; no AI image generation. Use when Dan wants the actual thumbnail image made — "make the thumbnail", "render the thumbnail", "thumbnail for <video>", or when a video-packaging concept is ready to become art. Do NOT use for thumbnail *concepts*/creative direction (video-packaging), blog cover images (blog post-cover), or video ideas (video-ideation).
---

# Thumbnail

Compose, don't generate. AI image generation fails at exactly the two things a
thumbnail needs most — crisp text and Dan's real face — so this skill never
generates imagery. It fills an HTML/CSS template (text is perfect by
construction), drops in a real photo cutout, and renders with headless Chrome.
Same philosophy and pipeline as the blog `post-cover` skill, pointed at YouTube.

## Files & assets

```
templates/hero-right.html     wordmark + pill + chips left, Dan right — the workhorse
templates/versus.html         two cards + VS badge — for comparison videos
templates/before-after.html   red-X line → green-check line story panel + hook badge —
                              for "broken thing becomes fixed thing" videos
templates/big-type-light.html light background, huge dark ink type — the
                              stands-out-in-a-dark-feed option
scripts/cutout.swift          Apple Vision subject lift: swift cutout.swift <in> <out.png>
scripts/paper_client.py       JSON-RPC client for the Paper MCP when its tools
                              aren't attached: paper_client.py <tool> '<json>'

/Users/vega/youtube/shared-assets/thumbnail/cutouts/   transparent PNGs of Dan
/Users/vega/youtube/shared-assets/thumbnail/cutouts/manifest.md   expression catalog
/Users/vega/youtube/shared-assets/thumbnail/doodles/   hand-drawn PNG/SVG assets
                              (arrows, circles, scribbles) exported from Paper
```

Output goes to the video project's `06_Thumbnails/` folder as
`thumbnail-draft-v<N>.png` alongside its `.html` source (so the next iteration
edits the HTML, not the pixels).

## Workflow

1. **Get the concept.** Best input is a `video-packaging` brief (focal
   expression, ≤4 words of text, composition, what to leave out). Given only a
   topic, derive a minimal concept first: subject, hook words, expression.

2. **Pick THREE directions.** Every fresh request gets three options in
   genuinely different styles — different layout, palette, and hero device —
   not three tweaks of one idea. Choose from **Style directions** below (or
   invent a new one); at most ONE option wears the dark-green house look.
   Each direction gets its own text angle where possible (mechanism vs
   outcome vs reaction).

   **Sketch gate (when Dan is present):** wireframe the three options first
   with the Excalidraw MCP (`create_view`) — three rough 16:9 frames with
   labeled blocks for type / panel / face — so Dan can veto or redirect a
   direction before any rendering happens. Skip when running unattended.

3. **Pick the cutout(s).** Read `cutouts/manifest.md` and choose the expression
   each concept calls for. If nothing fits, either use `smile-neutral.png` (the
   safe default) or pull a frame from this video's own footage (below).
   Options may share a cutout, but different expressions sell "different
   style" harder.

4. **Fill a template per direction.** Copy the closest template to the
   scratchpad and edit the numbered `<!-- FILL -->` sections. Style rules
   (apply to every option regardless of palette):
   - ONE accent color hit — one word, number, or element. Never two.
   - Real text budget is ≤4 words; chips/code lines are texture and don't count.
   - Thumbnail text must not repeat the title (the pair reads together).
   - Keep type clear of the cutout's head — no text over the face.
   - No logos beyond the built-in AI-box/sparkle marks (leaf licensing isn't
     worth it; the type does the work).

5. **Render** each at 1280×720 @2x:

   ```bash
   "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
     --headless=new --disable-gpu --hide-scrollbars \
     --force-device-scale-factor=2 --window-size=1280,720 \
     --screenshot=<out.png> "file://<abs-path-to-copy.html>"
   ```

6. **Verify each by Reading the PNG** — nothing clipped, no element touching
   the face, accent on the right word. Then the shrink test:
   `sips -Z 120 <out.png> --out <out_120.png>` and Read it — the biggest type,
   the hook phrase, and the face must all still read at 120px. Fix and
   re-render until both pass.

7. **Save and stop.** Copy the PNGs + HTML into the project's `06_Thumbnails/`
   as `thumbnail-v<N>-<style>.png` (e.g. `thumbnail-v1-story-panel.png`) and
   show Dan all three. Then wait: iterate only on the option he reacts to —
   three distinct directions beat five tweaks of one idea, and further rounds
   refine the winner, not the field.

## Style directions

Vary at least two of {layout, palette, hero device} between options; at most
one option per round in the dark-green house look. Grow this list as new
directions land:

- **house-terminal** — dark green + plexus + big white type
  (`hero-right.html`, `versus.html`)
- **story-panel** — red-X → green-check before/after tension
  (`before-after.html`)
- **clean-light** — paper-light background, huge dark ink type, studio cutout
  for pop (`big-type-light.html`); rare in a dark-mode feed, so it stands out
- **big-object** — one giant object/logo/number as the hero, tiny text, Dan
  small or absent (no template yet — build it when a concept calls for it)
- **designer-komika** — Dan's published designer look: deep purple/navy
  background, Komika Axis display type (white line + green line, often a
  question: "TOO MANY TOOLS?"), JetBrains Mono code panel, studio cutout
  pointing at the content. Reference boards live in the Paper file (below);
  build the template from them when this direction is picked.
- **hand-drawn** — marker circles/arrows/scribbles over a photo or screenshot,
  using assets from `shared-assets/thumbnail/doodles/`

## Getting a new cutout

**From any photo** (photoshoot, phone shot — plain background works best):

```bash
swift scripts/cutout.swift <photo.jpg> <name>.png
```

**From this video's raw footage** (shirt matches the video; expressions are
free because Dan makes them all on camera):

```bash
# contact sheet: one small frame every 5s — Read a few to pick a timestamp
ffmpeg -i <raw.mp4> -vf "fps=1/5,scale=480:-1" -q:v 4 frames/f_%03d.jpg
# extract the chosen moment at full res, then cut it out
ffmpeg -ss <timestamp> -i <raw.mp4> -frames:v 1 frame.png
swift scripts/cutout.swift frame.png <name>.png
```

Watch for motion blur and mid-word mouths — step ±0.1s (`-ss`) until the frame
is sharp. Keep one-off cutouts in the project folder; promote the good ones to
`shared-assets/thumbnail/cutouts/` **and add a manifest row** so future
thumbnails can find them.

## Design tokens (house-terminal direction)

These bind only the dark-green house look; other directions define their own
palette but keep the same text discipline.

- Background: `linear-gradient(135deg, #0c1a10, #08120b, #060d08)` + soft green
  radial glows + the faint plexus SVG. Dark enough that white 900-weight type carries.
- Accent green `#6cd97e`; card/chip borders `#3f7a4d`; muted text `#9fc7a8`.
- Type: Inter/SF 800–900 weight, tight letter-spacing; text-shadow for depth.
- Cutout: bottom-anchored, right third, `drop-shadow(-18px 0 40px rgba(0,0,0,0.55))`
  over a soft green radial `.glow` to bed it into the scene.

## Growing the library

New layout needed (big-object hero, "3 things" grid…)? Build it as a new
annotated template file next to the others, register it under a style
direction, test-render once with real content, and keep the FILL-comment
convention.

Doodles for the hand-drawn direction can be authored in Paper (draw or
write_html them, export as transparent PNG into
`shared-assets/thumbnail/doodles/`). Templates, cutouts, and doodles compound —
every video should leave the library slightly richer than it found it.

## Paper (design canvas, hand-edit + export)

Paper (paper.design desktop app) is where a draft becomes hand-editable. Its
MCP server runs at `http://127.0.0.1:29979/mcp` (app must be running). If the
Paper tools aren't attached to the session, drive it with
`scripts/paper_client.py <tool> '<json-args>'` — same JSON-RPC tools over HTTP.

The **"YouTube Thumbnails" Paper file** is the canonical board: it holds Dan's
real published thumbnails (the designer-komika reference boards) as 1920×1080
artboards. Study it before matching his style; his cutouts live in it as image
fills.

The loop that works (proven end-to-end):
1. `get_guide {"topic":"paper-mcp-instructions"}` once per session, then
   `get_basic_info`; `get_font_family_info` before first typographic styling.
2. `create_artboard` at 1920×1080 (file convention — not 1280×720).
3. `write_html` the option in small chunks (glows → wordmark → panel → badge →
   cutout), everything absolutely positioned, sizes at 1.5× the 1280-template
   values. Cutout PNGs go in as base64 data URIs (downscale to ~900px height
   first or the payload gets huge).
4. `get_screenshot` the artboard and fix issues with `update_styles` nudges,
   not rewrites. Then `finish_working_on_nodes`.
5. Dan hand-tweaks in Paper whenever he wants; `export` (format png, scale 1x)
   writes the final PNG to `~/Downloads/` — copy it into `06_Thumbnails/`.

Headless Chrome remains the fast path for quick drafts; Paper is the path when
a draft is worth Dan's hands.
