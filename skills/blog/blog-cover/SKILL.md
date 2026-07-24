---
name: blog-cover
description: Generate a cover image for a blog post — renders an on-brand HTML template to PNG with headless Chrome, choosing from a library of seven visual styles (terminal, blueprint, brutalist, editorial, aurora, bauhaus, poster). Use when the user wants a cover image, thumbnail, or og-image for a post, or when a finished post is missing its cover. Photo/YouTube-style thumbnails with Dan's face are the video `video-thumbnail` skill, NOT this one.
---

# Post Cover

Generate a blog cover by picking one of seven visual styles, filling its HTML template with content written from the post's actual argument, and rendering to PNG.

This is deliberately NOT AI image generation. Covers are HTML/CSS rendered to PNG, so they are deterministic, every text element is intentional, and each style stays consistent across uses.

## Files

```
scripts/cover/styles/*.html    one annotated template per style — copy, never edit in place
scripts/cover/render.mjs       HTML → PNG via headless Chrome (no dependencies)
```

Output goes to `public/images/blog/YYYY/MM/DD/<slug>.png` (same date path as the post) and the post's frontmatter gets `cover: <slug>.png` (bare filename).

## The style library

| Style | Vibe | Use when |
|---|---|---|
| `terminal` | dark green, $-prompt, terminal window — the house look | tutorials, how-tos, news; default when in doubt |
| `blueprint` | engineering drawing, drafting blue, box-and-arrow diagram | architecture, pipelines, any concept that diagrams as a flow |
| `brutalist` | yellow, thick black borders, stickers, marquee — loud | opinion pieces, hot takes, "stop doing X" |
| `editorial` | warm paper, serif, masthead, byline — magazine front page | essays, "state of X", reflective/analytical posts |
| `aurora` | dark, gradient blobs, glass pills — SaaS launch page | release announcements, AI-topic posts, launch energy |
| `bauhaus` | cream, geometric shapes, giant uppercase type — art print | milestones, retrospectives, celebration posts |
| `poster` | black, outline-to-solid stacked headline, acid green | big announcements where the title alone carries it |

Each template's header comment documents its customizable sections and gotchas. Read it before filling in the copy.

## Choosing a style

1. Match the post's **content type** using the table above.
2. Match the post's **tone**: brutalist on a somber post or editorial on a meme post is a miss.
3. **Anti-repetition rule**: check the covers of the last 3–4 published posts (`grep -r "cover:" content/blog/` sorted by date, or just look at the newest date folders under `public/images/blog/`). Never use the style of the most recent post; prefer one not used in the last 3–4.
4. When two styles fit, pick the one used less recently. When none clearly fits, use `terminal`.

State the chosen style and one-line reason to Dan when showing the render. If he asks for "options", render the same content in 2–3 styles and let him pick.

## Workflow

1. **Read the post.** Title, thesis, and the strongest concrete details. The cover content must come from the post's actual argument, not generic filler.

2. **Pick the style** (rules above), copy `scripts/cover/styles/<style>.html` to the scratchpad, and fill in the sections listed in its header comment. All example content in the templates is from a real post and must be replaced.

3. **Render**: `node scripts/cover/render.mjs <copy.html> public/images/blog/YYYY/MM/DD/<slug>.png`
   Default output is 5040x2836 (16:9 at 2x). Pass `WxH` and `scale` args to override.

4. **Verify by Reading the PNG.** Check: nothing clipped, nothing overlapping, headline fits, accent lands on the right word. Fix the HTML and re-render until it's right. Long headlines: shrink the `h1` font-size before allowing an extra line.

5. **Show Dan the rendered image and the style choice, then wait for his reaction before iterating on taste.** One render + his feedback beats five speculative variants.

6. **Set frontmatter** `cover: <slug>.png` on the post once he approves (or immediately if he asked for the whole thing done).

## Style rules (all styles)

- No em dashes in any cover text (same rule as prose). The `·` separator is the house alternative.
- One accent color per cover, and it should land on the payoff word.
- Text must be specific to the post; if a line could sit on any cover, rewrite it.
- Don't add logos. Spring leaf/Java Duke licensing is not worth it; the type does the work.
- Keep each style's palette as shipped in its template — variety comes from switching styles, not from drifting a style's colors.
- Terminal-specific: terminal text lowercase, headline Title Case; `.term-body` is `white-space: pre`, so count characters when aligning columns; green accents for positive posts, red (`warn`, `.bad`) only for warnings (EOL, breaking change, deprecation).

## Renderer notes

- Requires Chrome at `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`.
- Fonts are system: SF Mono/Menlo for mono, Inter/system sans, Georgia for editorial's serif. Nothing to install.
- If a JPG is needed (rare): `sips -s format jpeg <png> --out <jpg>`.
