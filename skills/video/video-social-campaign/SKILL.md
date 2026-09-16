---
name: video-social-campaign
description: >-
  Draft and schedule a staggered social campaign for a just-published YouTube video — 2–3 posts
  per platform (LinkedIn, Twitter/X, Bluesky), each written natively for its platform and mined
  from the video's transcript and brief, saved as drafts into ContentOS's social calendar and
  scheduled once Dan approves; checks off the SOCIAL_CAMPAIGN stage. Use when Dan says "social
  posts for this video", "promote the video", "post this to LinkedIn", "run the campaign", or a
  video hits VIDEO_PUBLISHED with SOCIAL_CAMPAIGN open. Do NOT use for cutting vertical clips
  (video-shorts), the companion blog post (blog-new-post), or the newsletter mention.
---

# Video Social Campaign

Social is the top of the funnel and voice-sensitive, so the app generates and publishes but the
*content* is designed here, with Dan in the loop. A campaign is not one announcement cross-posted
three times on three days — it's three different reasons to care about the same video, each written
natively for its platform, staggered so the video gets more than one shot at the feed.

The skill talks to ContentOS through its MCP tools (`save_social_post`, `list_social_posts`,
`list_social_accounts`, `schedule_social_post`, plus the usual project tools). If those tools
aren't available, ContentOS is either down or running a build older than 2026-07-24 — say so and
stop; don't fall back to pasting post text into the conversation as the deliverable.

## The arc (default shape, 3 posts)

| Post | When (default) | Job | Leads with |
|---|---|---|---|
| 1 — Launch | publish day (or next weekday 9:00 ET) | sell the promise | the hook, then the link |
| 2 — Value | +2 days, 9:00 ET | teach one real thing from the video | the gotcha/lesson itself; works even if nobody clicks |
| 3 — Conversation | +5–7 days, 9:00 ET | start a discussion | a question or a spicy-but-honest take; link in the body's tail |

Hard rules: the three posts must not share a first sentence or all lead with the title; every
specific (a number, a quoted line, a before/after) must come from the actual transcript or demo,
never invented; weekends only if Dan asks.

## Platform-native, not cross-posted

- **LinkedIn (3000 chars)** — the first ~200 characters are the hook (that's the "…more" fold).
  Short paragraphs, real line breaks, no hashtag walls (0–3 at the end if any), link at the end.
  Dev-to-dev voice: plain, first person, zero "🚀 Thrilled to announce".
- **Twitter/X (280 chars, link counts ~23)** — lead with the claim, not the link. One idea per
  post; if it doesn't fit, it's the wrong idea for this platform, not a reason to thread.
- **Bluesky (300 chars)** — most casual of the three; write like the dev community talks, links
  are fine inline, no algorithm-brain formatting.

Same arc position ≠ same text: post 2 on LinkedIn might be 800 chars with a code observation;
post 2 on X is the single sharpest sentence of that observation.

## Workflow

### Step 1 — Load the project

Resolve the slug (`list_projects`), then pull: `get_brief` (the promise and target keyword),
`list_videos` (locked title + hook), `get_youtube_metadata` and `get_transcripts` (the published
description and the transcript — the source of every quotable specific). Get the published video
URL from the metadata or the video record; if it's nowhere, ask Dan for the link — a campaign
without the link is pointless.

If ContentOS has no transcript yet, use `video-rough-cut/scripts/pipeline.py transcribe` on the
exact final export in `04_Exports/`, with `--work <project>/05_Transcripts/final`. This shares the
identity-checked transcript cache with shorts, extracts audio directly, and avoids silence analysis.
Read the actual transcript path from `transcripts.json`; do not reuse a rough-cut transcript.

### Step 2 — Check what already exists

`list_social_posts` first: ContentOS auto-generates a launch draft when a video publishes
(source `VIDEO_PUBLISHED`), and Dan may have posts of his own queued. Fold what exists into the
plan — an auto-generated draft becomes the launch-post candidate to rewrite (Dan edits/deletes
in the UI; there's no MCP update tool), never a reason to create a duplicate launch post.
`list_social_accounts` tells you which platforms are actually connected and their char limits —
don't draft for a platform with no active account.

### Step 3 — Mine the transcript for the three angles

Read the transcript and pull, with rough timestamps: the moment that states the promise best
(post 1), the single most teachable specific — the gotcha, the surprising number, the before/after
(post 2), and the most debatable or discussion-worthy claim (post 3). Quote real lines; the
specifics are what out-click generic copy in this niche.

### Step 4 — Draft the campaign and iterate with Dan

Present all posts grouped by arc position (not by platform), with char counts against each
platform's limit and the proposed schedule. This is a conversation, not a delivery: Dan reacts,
you revise. Voice check before presenting: would Dan say this sentence out loud on camera? If
not, cut it.

Media note: the scheduler attaches images in the UI, not over MCP. Recommend per post what to
attach (the thumbnail for post 1, a code screenshot for post 2, a short from `video-shorts` where
native video helps) and flag it in the calendar title, e.g. `2/3 — gotcha (attach code shot)`.

### Step 5 — Save, approve, schedule

On Dan's approval of the content: one `save_social_post` per arc position with the per-platform
texts and staggered `scheduledAt`, titled `1/3 — launch`, `2/3 — …`, `3/3 — …`. Posts land as
DRAFTs on the social calendar. Then — and only on an explicit go from Dan, because a SCHEDULED
post publishes itself — flip them with `schedule_social_post` (or `schedule=true` on save when
he's already said "ship it"). If he wants a final look or media attached first, leave them DRAFT
and point him at the calendar.

### Step 6 — Close the stage

When the campaign posts are saved (scheduled or deliberately left as drafts for media),
`set_pipeline_stage SOCIAL_CAMPAIGN` complete and summarize: what posts, when, what Dan still
needs to attach in the UI.

## Principles

- **Three reasons, not three reminders.** If a post only says "I made a video", it isn't done.
- **The transcript is the copywriter.** Real lines and real numbers from the video beat anything
  composed about the video.
- **Native or nothing.** A post that reads right on LinkedIn reads wrong on Bluesky; write each
  one on its home platform's terms.
- **Drafts are cheap, scheduling is real.** Save early, iterate freely, schedule only on an
  explicit yes — scheduled posts publish themselves.

## Lessons

Append a dated line when a run burns you.

- (seed) ContentOS auto-drafts a launch post on publish (source VIDEO_PUBLISHED) — always
  `list_social_posts` before drafting or the campaign ships two launch posts.
- (seed) Char limits count the link (X shortens to ~23 chars). Validate counts before saving;
  `save_social_post` rejects over-limit content per platform.
