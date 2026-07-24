---
name: video-thumbnail
description: Render the final thumbnail art for a YouTube video — composes real photo cutouts of Dan with HTML/CSS templates in the channel's design language (dark green, big white type, one green accent) and renders to PNG with headless Chrome; no AI image generation. Use when Dan wants the actual thumbnail image made — "make the thumbnail", "render the thumbnail", "thumbnail for <video>", or when a video-packaging concept is ready to become art. Do NOT use for thumbnail *concepts*/creative direction (video-packaging), blog cover images (blog-cover), or video ideas (video-ideation).
---

# Thumbnail

Compose, don't generate. AI image generation fails at exactly the two things a
thumbnail needs most — crisp text and Dan's real face — so this skill never
generates imagery. It fills an HTML/CSS template (text is perfect by
construction), drops in a real photo cutout, and renders with headless Chrome.
Same philosophy and pipeline as the blog `blog-cover` skill, pointed at YouTube.

## Files & assets

```
templates/hero-right.html     wordmark + pill + chips left, Dan right — the workhorse
templates/versus.html         two cards + VS badge — for comparison videos
templates/before-after.html   red-X line → green-check line story panel + hook badge —
                              for "broken thing becomes fixed thing" videos
templates/big-type-light.html light background, huge dark ink type — the
                              stands-out-in-a-dark-feed option
templates/big-shield.html     giant cracked-shield hero + stacked type, no Dan —
                              the big-object option; swap the SVG per concept
templates/merge-button.html   fake product UI as the hero (GitHub PR card + giant
                              button + hovering cursor) — the ui-artifact option
templates/quote-card.html     one damning quote at max size in a thin colored
                              frame, serif quote mark, mono attribution
templates/annotated-code.html IDE window + rough red marker ellipse/arrow +
                              sticky-note sticker + pointing Dan — hand-drawn
templates/file-explorer.html  editor-slate repo file tree with ONE file circled
                              in red marker + big type + pointing Dan — the
                              mystery-artifact hook ("you've seen this file")
scripts/cutout.swift          Apple Vision subject lift: swift cutout.swift <in> <out.png>
scripts/figma_client.py       JSON-RPC client for the remote Figma MCP when its
                              tools aren't attached: figma_client.py <tool> '<json>'
                              (auth reuses Claude Code's stored OAuth token)
scripts/paper_client.py       legacy — same idea for the Paper MCP (127.0.0.1:29979);
                              only for pulling old boards still in the Paper file
                              (see History). Args >argv limit: pass @path/to/args.json

/Users/vega/youtube/shared-assets/thumbnail/photos/    the photo catalog — a dump
                              directory of photos of Dan: raw shots or transparent
                              cutout PNGs, no curation or manifest required
/Users/vega/youtube/shared-assets/thumbnail/doodles/   hand-drawn PNG/SVG assets
                              (arrows, circles, scribbles), transparent PNG/SVG
```

Output goes to the video project's `06_Thumbnails/` folder as
`thumbnail-draft-v<N>.png` alongside its `.html` source (so the next iteration
edits the HTML, not the pixels).

## Workflow

1. **Get the concept.** Best input is a `video-packaging` brief (focal
   expression, ≤4 words of text, composition, what to leave out) — packaging
   locks it into the video's ContentOS project, so check there first:
   `mcp__contentos__list_videos(slug)` returns the long-form video's locked
   title and thumbnail concept. Given only a topic, derive a minimal concept
   first: subject, hook words, expression.

2. **Consult the inspiration board, then pick 3–5 directions.** Before
   choosing directions on a fresh request, pull an overview screenshot of
   the **"Thumbnail Inspiration" Figma file** (fileKey
   `vwHATW30WF1B8da9CVDHpv`, page `0:1` — `get_screenshot` at
   maxDimension ~2400, split into halves with sips to review) and extract
   the *structures* worth stealing for THIS concept: layout grid, hero
   device, where the tension comes from. Bones only, never their colors/
   assets/branding. This step exists because the failure mode is real and
   named (Dan, 2026-07): without it every option converges on the house
   formula — big type left, Dan right, one accent — and rounds come out
   "tired". Structural variety beats palette variety: vary the HERO ITSELF
   across the set (type / fake UI artifact / quote / annotated screenshot /
   giant object / code panel), and make at least one option something no
   existing template does — build it, then register it as a new template
   (see Growing the library).

   Every fresh request gets at least three options in genuinely different
   styles — different layout, palette, and hero device — not tweaks of one
   idea. Renders are cheap; distinct ideas are not: add a fourth or fifth
   option only when the concept genuinely supports another distinct angle,
   never to pad the count. Choose from **Style directions** below (or
   invent a new one); the dark-green house look has no reserved slot — it
   competes for a spot like any other direction, and some rounds it won't
   appear at all. Each direction gets its own text angle where possible
   (mechanism vs outcome vs reaction). Go straight to rendering — no
   wireframe/sketch step; Dan reacts to finished thumbnails, not boxes.

3. **Pick the photo(s).** Browse the photo catalog at
   `shared-assets/thumbnail/photos/` — Read the images and judge the
   expressions directly; there is no manifest. Pick the shot each concept
   calls for, then lift Dan out on the fly:
   `swift scripts/cutout.swift <photo> <out.png>` (skip the script if the
   file is already a transparent cutout). Generated cutouts live with the
   working files, not the catalog. If nothing in the catalog fits, pull a
   frame from this video's own footage (below). Options may share a photo,
   but different expressions sell "different style" harder.

4. **Fill a template per direction.** Copy the closest template to the
   scratchpad and edit the numbered `<!-- FILL -->` sections. Style rules
   (apply to every option regardless of palette):
   - ONE accent color hit — one word, number, or element. Never two.
   - Real text budget is ≤4 words; chips/code lines are texture and don't count.
   - Thumbnail text must not repeat the title (the pair reads together).
   - Keep type clear of the cutout's head — no text over the face.
   - No logos beyond the built-in AI-box/sparkle marks (leaf licensing isn't
     worth it; the type does the work).

5. **Render** each at 1920×1080 (Dan's standard output size, set 2026-07-22).
   Templates are authored at 1920×1080 CSS px (convention changed 2026-07-23
   so Figma captures arrive as full-size 1920×1080 boards — captures land at
   the page's CSS size, not the rendered-PNG size):

   ```bash
   "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
     --headless=new --disable-gpu --hide-scrollbars \
     --force-device-scale-factor=1 --window-size=1920,1080 \
     --screenshot=<out.png> "file://<abs-path-to-copy.html>"
   ```

   (A 1280×720-authored draft can be migrated by multiplying every CSS `px`
   value and every svg width=/height= attribute — NOT viewBox, NOT
   stroke-width attrs — by 1.5.)

6. **Verify each by Reading the PNG** — nothing clipped, no element touching
   the face, accent on the right word. Then the shrink test:
   `sips -Z 120 <out.png> --out <out_120.png>` and Read it — the biggest type,
   the hook phrase, and the face must all still read at 120px. Fix and
   re-render until both pass.

7. **Save and stop.** Copy the PNGs + HTML into the project's `06_Thumbnails/`
   as `thumbnail-v<N>-<style>.png` (e.g. `thumbnail-v1-story-panel.png`) and
   show Dan the full set. Then wait: iterate only on the option he reacts
   to — a few distinct directions beat many tweaks of one idea, and further
   rounds refine the winner, not the field.

8. **Winner variation round.** Once Dan picks a direction, the next round is
   THREE new takes on that winning CONCEPT (`v2a/v2b/v2c`) — what carries
   forward is the idea (the hook's meaning, the mystery/tension), NOT its
   styling. Re-consult the inspiration board and re-execute the same concept
   in genuinely different visual languages: vary palette, type treatment,
   and hero rendering across the takes (light vs dark, handwritten vs
   grotesk, zoomed artifact vs quote vs UI panel). At most ONE take may stay
   close to the winner's original styling as the safe pick. A cutout swap
   alone is NOT a variation, and neither is reshuffling the same hook text,
   palette, and accent around the frame (Dan's feedback 2026-07-23: three
   same-palette recompositions of the winner read as "pretty much the
   same"). Each take still changes the photo/expression. Size Dan generously — cutouts read smaller than you
   think at feed size; bottom-anchor at ~85–90% of frame height (chest-up)
   unless the take wants him small or absent. Render variations in Chrome
   first (seconds per iteration), then capture them into Figma (see
   **Figma** below) so Dan picks and hand-edits among real, editable frames —
   from that point the Figma file is the source of truth.

## Style directions

Vary at least two of {layout, palette, hero device} between options. Grow
this list as new directions land:

- **house-terminal** — dark green + plexus + big white type
  (`hero-right.html`, `versus.html`)
- **story-panel** — red-X → green-check before/after tension
  (`before-after.html`)
- **clean-light** — paper-light background, huge dark ink type, studio cutout
  for pop (`big-type-light.html`); rare in a dark-mode feed, so it stands out
- **big-object** — one giant object/logo/number as the hero, big type beside
  it, Dan small or absent (`big-shield.html` — cracked-shield build; adapt
  the SVG hero per concept)
- **ui-artifact** — a fake product UI as the hero: the click/decision moment
  rendered as a real interface (PR merge button, deploy modal, delete
  dialog), short hook line, Dan reacting (`merge-button.html`). Instantly
  legible to devs; the button/control is the accent. Variant: an editor
  file tree with one file circled in red marker (`file-explorer.html`) —
  for "what IS this file" mystery-artifact hooks.
- **quote-card** — one damning or intriguing quote at max size in a thin
  colored border frame, serif quote mark, mono attribution, Dan reacting
  (`quote-card.html`). For videos whose hook is a LINE someone/something says.
- **designer-komika** — Dan's published designer look: deep purple/navy
  background, Komika Axis display type (white line + green line, often a
  question: "TOO MANY TOOLS?"), JetBrains Mono code panel, studio cutout
  pointing at the content. Reference boards live in the legacy Paper file;
  build the template from Dan's published thumbnails when this direction is
  picked.
- **hand-drawn** — marker circles/arrows/scribbles over a photo or screenshot
  (`annotated-code.html` — IDE window + red ellipse + sticker + pointing Dan;
  or compose with assets from `shared-assets/thumbnail/doodles/`)

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
is sharp. Keep one-off cutouts in the project folder; when a source frame or
photo is a keeper, drop it into `shared-assets/thumbnail/photos/` so future
thumbnails can find it — no manifest, the catalog is browsed visually.

## Design tokens (house-terminal direction)

These bind only the dark-green house look; other directions define their own
palette but keep the same text discipline.

- Background: `linear-gradient(135deg, #0c1a10, #08120b, #060d08)` + soft green
  radial glows + the faint plexus SVG. Dark enough that white 900-weight type carries.
- Accent green `#6cd97e`; card/chip borders `#3f7a4d`; muted text `#9fc7a8`.
- Type: Inter/SF 800–900 weight, tight letter-spacing; text-shadow for depth.
- Cutout: bottom-anchored, right third, `drop-shadow(-18px 0 40px rgba(0,0,0,0.55))`
  over a soft green radial `.glow` to bed it into the scene. Err BIG: ~85–90%
  of frame height (Dan's feedback 2026-07: smaller cutouts read weak in the
  feed); let chips/panels overlap the shirt rather than shrinking him.

## Growing the library

New layout needed (big-object hero, "3 things" grid…)? Build it as a new
annotated template file next to the others, register it under a style
direction, test-render once with real content, and keep the FILL-comment
convention.

**From inspiration:** Dan can drop screenshots of other creators' thumbnails
he admires into `shared-assets/thumbnail/inspiration/`. When he points at one,
Read it and extract the *structure* — layout grid, type scale and placement,
face size/position, color logic, where the tension comes from — then rebuild
that composition as a new template in Dan's own design language and register
it as a style direction. Learn the bones, never copy the art: no lifting their
colors verbatim, assets, or branding.

Doodles for the hand-drawn direction can be authored in Figma (draw, then
export as transparent PNG into `shared-assets/thumbnail/doodles/`). Templates, cutouts, and doodles compound —
every video should leave the library slightly richer than it found it.

## Figma (design canvas, hand-edit + export)

Figma is where a draft becomes hand-editable. The remote Figma MCP server
(`https://mcp.figma.com/mcp`) is registered in Claude Code user config as
`figma` (OAuth already done; Dan is a Full seat on the Team Vega pro plan =
write access). If the tools aren't attached to the session, drive it with
`scripts/figma_client.py <tool> '<json>'` — same JSON-RPC over HTTP; it reads
the OAuth token Claude Code stored in the macOS keychain.

The **"YouTube Thumbnails" Figma file is the canonical board** — fileKey
`qxwLTGPFH4RPlV5cZOYrqS`. Every capture/promotion targets this file so all
thumbnail work accumulates in one place. Dan's **"Thumbnail Inspiration"**
Figma file — fileKey `vwHATW30WF1B8da9CVDHpv`, one page (`0:1`) of other
creators' thumbnails — is consulted at the START of every fresh round
(Workflow step 2), not just when explicitly asked.

**The capture flow that works (proven end-to-end, 2026-07):** Chrome drafts
become editable Figma layers via `generate_figma_design` — no element-by-
element porting.

1. Prep each draft HTML: add
   `<script src="https://mcp.figma.com/mcp/html-to-design/capture.js" async></script>`
   to `<head>`, and make every `img src` RELATIVE (absolute filesystem paths
   404 over HTTP and you get a blank cutout).
2. Serve the draft dir: `python3 -m http.server 8931` from the folder with
   the HTML + images.
3. Mint a capture: `generate_figma_design {"fileKey": ..., "url":
   "http://localhost:8931/<page>.html"}` → response contains a single-use
   `captureId` and a ready-made hash URL
   (`<url>#figmacapture=<id>&figmaendpoint=<urlencoded submit URL>&figmadelay=1500`).
4. Open that hash URL in a browser — the in-app Browser pane works and keeps
   Dan's screen clean, but plain `navigate` to localhost is blocked by
   policy: open the FIRST page via `preview_start {url: <hash-url>}` (which
   returns a tabId), then `navigate` with that tabId for subsequent pages.
   The page shows a "Sending to Figma…" toolbar while uploading; multi-MB
   cutout PNGs take 1–3 minutes. Two learned gotchas (2026-07): cutout PNGs
   much over ~2 MB can silently DROP OUT of the capture (page renders fine,
   Figma page arrives without Dan) — `sips -Z 1400` every cutout the HTML
   references before capturing; and use `figmadelay=4000` so large images
   finish decoding first. Always verify each capture with `get_screenshot`
   before telling Dan it's done.
5. Poll `generate_figma_design {"fileKey": ..., "captureId": ...}` every
   ~10s until the response says "The design has been added to your existing
   file" with a node id. Never mint a new id while one is pending.
6. Where a capture lands depends on the file's page structure: in the current
   single-page "YouTube Thumbnails" file (one page `0:1`, everything on it),
   each capture arrives as a 1920×1080 FRAME named "Document" placed in a row
   on that page — NOT as a new page (observed 2026-07-23; multi-page files may
   still get new pages). Verify with `get_screenshot {"fileKey", "nodeId"}`
   (returns an asset URL — plain curl downloads it). Rename the capture
   FRAMES to the `<Project> / v<N> <style>` convention via `use_figma` —
   check `node.parent.type` first and never blind-rename a node's page (a
   climb-to-PAGE loop renames the one shared page instead). Captures can
   also land offset vertically — align `y` with the existing row.

Fine-grained edits from here: `use_figma` runs Figma Plugin API JavaScript
against the file — but ALWAYS read the `skill://figma/figma-use/SKILL.md`
MCP resource first (font-loading and color-range rules); pass `skillNames`
as instructed. For final art: Dan hand-tweaks in Figma and exports PNG at
1920×1080 (or use the `download_assets` tool), then copy into
`06_Thumbnails/`.

The division of labor: headless Chrome renders every fresh round of options
(seconds per iteration, Claude holds the pen); winning designs are captured
into Figma (Dan holds the pen — element-level hand edits, then export for
the final PNG).

History: this role was played by Paper (paper.design) until 2026-07 — dropped
for its $200/yr price and weekly MCP call caps. Old artboards (v1 house-hero
and the designer-komika reference boards) still live in the Paper file;
rebuild references in Figma opportunistically.
