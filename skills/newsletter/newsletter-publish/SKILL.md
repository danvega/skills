---
name: newsletter-publish
description: >-
  Republish a Beehiiv newsletter edition on danvega.dev — fetch the post via the Beehiiv MCP
  server, convert it to the site's markdown (frontmatter, :YouTube/:TweetEmbed components, local
  images, house footer), run a light quality pass, and save it into content/newsletter/. Use when
  Dan says "publish my newsletter", "convert the latest newsletter", "move this week's newsletter
  to the site", or names a specific edition to bring over. Do NOT use for writing a new post
  (blog-new-post), optimizing existing content (blog-seo-optimize), or sending the newsletter itself
  (that happens in Beehiiv).
---

# Publish Newsletter

Take a newsletter edition that already went out on Beehiiv and republish it on the site. The email
is the source of truth for the words; this skill's job is faithful conversion, not rewriting —
fix typos, never the voice.

## Paths

```
content/newsletter/YYYY/MM/DD/<slug>.md          the post   (in danvega-dev-nuxt)
public/images/newsletter/YYYY/MM/DD/<file>       its images
/images/newsletter/YYYY/MM/DD/<file>             how the markdown references them
```

Site repo: `/Users/vega/dev/danvega/danvega-dev-nuxt` (adjust if working from a different clone).

**Dates:** the newsletter normally gets republished the day it went out, so today's date is the
default for the directory *and* the `date` field. When converting an older edition, use the
original Beehiiv send date for both instead. Whatever happens, the directory date and the `date`
field must agree — same rule as blog posts, and it fails silently when broken. Never use Beehiiv's
draft-creation timestamp; that's the classic wrong-date source.

## Step 1 — Fetch the post

Use the Beehiiv MCP server: `beehiiv_get_posts` to list recent editions (default to the latest
confirmed/published one; show the list if the user didn't specify), then `beehiiv_get_post` for
full content. The content arrives as email HTML — convert it to clean markdown.

Strip what belongs to the email, not the article: "read online" links, subscribe/referral blocks,
sponsor slots unless the user wants them kept, and any tracking pixels.

## Step 2 — Convert

**Frontmatter** (matches the site's newsletter layout — no `author` field):

```yaml
---
title: "Edition Title"
slug: "edition-title"
date: "2026-07-16"
description: "One or two sentences, ~150 chars — the hook, not a summary."
tags: ["Spring Boot", "Java", "Spring AI"]
newsletter: true
published: true
---
```

Slug: kebab-case from the title unless the user provides one — it's the permanent URL. Tags: pull
from what the edition actually covers, capitalized the way the site already tags them (check
existing newsletter files when unsure).

**Embeds** — the site renders these as components; a raw link or iframe renders as nothing:
- YouTube (`youtube.com/watch?v=`, `youtu.be/`, `/embed/`) → `:YouTube{id=VIDEO_ID}`
- Twitter/X (`twitter.com`, `x.com` status links) → `:TweetEmbed{id=TWEET_ID}`
- Anything else embedded (CodePen, Gists) → leave a plain link and flag it in the report.

**Images** — download every image to the images directory and rewrite the reference:
- `curl -L -o <path>` each one; Beehiiv CDN URLs expire and are ugly, so nothing may reference
  them in the final file.
- Name files short and descriptive of what they show (`tampa-orlando-jug.jpg`), not
  `slug-image-3.png` — the name appears in the URL forever. Keep the original extension.

**Links** — unwrap Beehiiv click-tracking redirects to their real destination and drop the
`utm_*` noise Beehiiv appends. Keep genuine affiliate parameters. Links to danvega.dev become
relative paths.

**Footer** — the edition should end with the house sign-off, exactly:

```markdown
## Until Next Week

I hope you enjoyed this newsletter installment, and I will talk to you in the next one. If you have any questions for me or topics you would like me to cover please feel free to reply to this email or reach out to me on [Twitter](https://twitter.com/therealdanvega).

Happy Coding,  
Dan Vega  
[https://www.danvega.dev](https://www.danvega.dev/)
```

("Happy Coding," and "Dan Vega" end with two trailing spaces — markdown line breaks. Don't let an
editor strip them.)

## Step 3 — Quality pass (fix, don't rewrite)

Fix typos, punctuation, and technical capitalization: JavaScript, TypeScript, Spring Boot, Spring
AI, IntelliJ IDEA, VS Code, GraalVM, Kubernetes, GitHub, YouTube, Beehiiv, VMware, Tanzu. Fix
its/it's and obvious grammar slips. Do **not** smooth out conversational phrasing — "Happy Monday,
friends!" is the voice, not an error. Keep a list of every correction for the report.

## Step 4 — Validate, then report

Before reporting done:
- The markdown file exists at the right dated path and the frontmatter parses.
- Every image file exists and no `beehiiv` / `media.beehiiv` URL remains in the markdown.
- Every YouTube/Twitter link became a component embed.
- Directory date == `date` field.

Then report: file path, image count (with any failed downloads), embeds converted, corrections
made, and anything left for manual review. Offer to preview (`npm run dev` in the site repo).

## What this skill does NOT do

- Write or send the newsletter — Beehiiv is where editions are authored and sent.
- SEO work on the result (`blog-seo-optimize`) or cover images (`blog-cover`).
- Publish the site — committing/deploying the nuxt repo is Dan's call.
