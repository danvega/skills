---
name: spring-office-hours-spring-io-pr
description: >-
  Open the spring.io blog PR for a Spring Office Hours episode: build the episode markdown
  (description, Transistor audio embed, Show Notes links) in the spring-website-content repo,
  push the episode branch, and open the PR. The final publishing step, after the episode is live
  on Transistor. Use whenever Dan says "send the spring.io PR", "PR to the spring website",
  "publish the episode on spring.io", or "finish publishing S5E19". Do NOT use for editing audio
  (spring-office-hours-edit), writing the notes themselves (spring-office-hours-show-notes), or
  Dan's personal site (that is the danvega-dev-nuxt repo).
---

# Spring Office Hours: spring.io PR

Every episode gets a short post on the spring.io blog. The content already exists by this point;
this skill assembles it in the right shape, on the right branch, and opens the PR.

## Prerequisites

- The episode must already be published on Transistor. The embed hash comes from the public
  feed, so an unpublished episode has no hash yet.
- The show-notes file from spring-office-hours-show-notes:
  `/Users/vega/youtube/spring-office-hours/exports/$EP-show-notes.md` (description + links).
  If it does not exist, run that skill first.

## Repo

`/Users/vega/dev/spring/spring-website-content`, origin = `spring-io/spring-website-content`.
Dan has push access; episode branches are pushed straight to origin (no fork) and the PR goes
to `main`. gh is authenticated as danvega.

## Step 1: Get the Transistor embed hash (no Transistor visit needed)

The RSS feed carries the share URL per episode. The embed src is the same hash with `/s/`
swapped for `/e/`:

```bash
curl -s "https://feeds.transistor.fm/spring-office-hours" | grep -A2 "$EP"
# item <link> looks like https://share.transistor.fm/s/fd48b861
# embed src is       https://share.transistor.fm/e/fd48b861
```

If the episode is not in the feed yet, stop and tell Dan; it is not published on Transistor.

## Step 2: Build the episode file

Path: `blog/<yyyy>/<mm>/spring-office-hours-podcast-$EP.md` (year/month of the episode date).

Exact shape, verified against S5E17 and S5E18:

```markdown
---
title: "Spring Office Hours Podcast: S5E18 - The Latest from OpenAI, Anthropic and Spring AI 2.0"
category: Engineering
publishedAt: 2026-07-13
author: danvega
order: 1
---

<description paragraph, verbatim from the show-notes file>

<iframe width="100%" height="180" frameborder="no" scrolling="no" seamless="" src="https://share.transistor.fm/e/<hash>"></iframe>

**Show Notes**
- [Link title](url)
- ...

**The show:**
- [springofficehours.io](https://www.springofficehours.io) - episodes, schedule, community
- [Spring Developer on YouTube](https://www.youtube.com/@SpringDeveloper) - join us live every Monday
- [Dan Vega](https://www.danvega.dev)
- [DaShaun Carter](https://dashaun.com)
- [The Spring Blog](https://spring.io/blog) - the news we cover each week
```

- Title separator is ` - ` after the episode token, matching the YouTube title.
- `publishedAt` is the episode date (the Monday it streamed).
- Show Notes are the episode's resource links; the "The show:" footer is fixed and identical
  every episode (same block the Transistor notes carry, added starting S5E19).
- No blank line variations, no extra sections beyond these. Match the previous episode files.

## Step 3: Branch, commit, push, PR

Branch off up-to-date main; never commit to main directly:

```bash
git fetch origin
git checkout -b spring-office-hours-$EP origin/main
git add blog/<yyyy>/<mm>/spring-office-hours-podcast-$EP.md
git commit -s --no-gpg-sign -m "Adding Spring Office Hours $EP"
git push -u origin spring-office-hours-$EP
gh pr create --repo spring-io/spring-website-content --base main \
  --title "Adding Spring Office Hours $EP" --body ""
```

- Branch name: `spring-office-hours-$EP` with the unpadded token (`S5E19`; the one `S05E13` was
  an outlier).
- Commit message and PR title: `Adding Spring Office Hours $EP`. PR body is empty; that matches
  every previous episode PR.
- No `Co-Authored-By: Claude` trailer, even if the session's attribution settings ask for one.
  Dan had it dropped from S5E22 (#1495). The DCO sign-off is the only trailer.
- `-s` is required: the repo enforces DCO, and a commit without a
  `Signed-off-by: danvega <danvega@gmail.com>` line blocks the PR.
- `--no-gpg-sign` matters: GPG signing hangs non-interactive commits on this machine, and the
  history is unsigned anyway. (DCO sign-off and GPG signing are different things; the repo wants
  the former.)
- Show Dan the file content and the PR URL. Do not merge; the Spring team merges.

## Pitfalls log

Append a dated line every time a run burns you.

- (seed) The embed hash is in the RSS feed item link (`/s/<hash>`); swap to `/e/<hash>` for the
  iframe. No need to log into Transistor.
- (seed) Leave local `main` alone and branch from `origin/main` after a fetch; the local clone
  often sits weeks behind. (Confirmed 2026-08-17: local main was 5 commits behind origin/main.)
- (2026-08-17, S5E20) The RSS feed lags the Transistor publish action by several minutes. Dan
  said "published" and the episode was genuinely absent: cache-busted refetch, byte-identical
  response, zero hits. It appeared on a retry a few minutes later. So "not in the feed" right
  after publishing is NOT proof of a draft. Say it is not there yet and offer to retry, rather
  than sending Dan back to Transistor to hunt for a problem that does not exist.
- (2026-08-17, S5E20) The show-notes file and the blog post format links differently. show-notes
  entries may carry a trailing " - context" suffix for the Transistor description; the blog post
  Show Notes list is bare `- [Title](url)`, no suffixes. Strip them when copying across. The
  fixed "The show:" footer is the exception and keeps its suffixes in both.
- (2026-08-17, S5E20) Cheap pre-commit check that catches shape drift: diff the new file against
  the previous episode with URLs, titles and prose blanked out. The only diff should be the
  number of Show Notes lines. Also curl the `/e/<hash>` embed for a 200 before committing.
- (2026-09-14, S5E22) Cross-check the live feed against the show-notes file before committing.
  S5E22 went live on Transistor with the wrong links (a research "Sources" list from the chat,
  no "The show:" footer) while the show-notes file was right. The PR follows the file, so it was
  fine, but Dan had to fix Transistor. The item's `<description>` holds the live HTML: pull its
  `<a href>`s and compare them to the file's links.
- (2026-09-14, S5E22) `publishedAt` is the stream date, which is not always a Monday. The
  live-from-KCDC special streamed on a Wednesday, so it used 2026-09-09.

## What this skill does NOT do

- Write descriptions or find links (spring-office-hours-show-notes).
- Touch Transistor, the audio, or danvega.dev.
- Merge the PR.
