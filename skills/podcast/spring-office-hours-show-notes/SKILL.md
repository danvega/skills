---
name: spring-office-hours-show-notes
description: >-
  Assemble the episode page content for a Spring Office Hours episode in the exact format the
  show publishes on Transistor: fetch the pre-decided title and description from the YouTube live
  stream, and build the Show Notes link list from the episode transcript. Use whenever
  Dan asks for "show notes", "episode description", "write up this episode", "notes for S5E18",
  or right after spring-office-hours-edit produced an episode transcript. Input is a transcript
  (preferred) or a recording/mp3 to transcribe first. Do NOT use for editing the audio itself
  (spring-office-hours-edit), YouTube titles/thumbnails (video-packaging), blog posts
  (blog-new-post), or other people's shows (podcast-appearance).
---

# Spring Office Hours: Show Notes

Assemble the episode page content Dan pastes into Transistor: title, description paragraph, and
a "Show Notes" list of the resources mentioned in the episode.

The title, description, and guest are decided BEFORE the show is recorded and published on the
YouTube live stream. Do not write them; fetch them. The only content this skill creates is the
Show Notes link list, which comes from what was actually said in the episode.

## Inputs

- Episode token (`S5E18`). Ask if unclear.
- Episode transcript, for the link list. spring-office-hours-edit leaves `$EP.txt` and `$EP.srt`
  in `/tmp/soh-edit/<episode>/` and next to the mp3 in
  `/Users/vega/youtube/spring-office-hours/exports/`. Look there first.
- If only a recording or mp3 exists, transcribe it:
  `mlx_whisper <audio> --model mlx-community/whisper-small.en-mlx --output-format txt`
  (`whisper` CLI is not installed; `mlx_whisper` is, via miniforge).

## Fetch the planned title and description

The live stream on the SpringDeveloper YouTube channel carries the final, pre-decided title and
description (verified against the published feed: they match verbatim).

```bash
yt-dlp --no-warnings --flat-playlist --print "%(id)s | %(channel)s | %(title)s" \
  "ytsearch5:Spring Office Hours S5E18"   # pick the SpringDeveloper channel hit
yt-dlp --no-warnings --skip-download --print "%(title)s" --print "%(description)s" \
  "https://www.youtube.com/watch?v=<id>"
```

- **Title**: strip the leading "Spring Office Hours: " from the YouTube title. The podcast title
  is just `S5E18 - The Latest from OpenAI, Anthropic and Spring AI 2.0`.
- **Description**: use verbatim. It already follows the house shape (fixed "Join Dan Vega and
  DaShaun Carter..." opener, episode summary, fixed "...catch the replay on your preferred
  podcast platform." closer) and names any guest. Fixing an obvious typo (a missing space, a
  doubled word) is fine; flag the fix to Dan. Rewording is not.
- If the show went somewhere very different from the planned description (it happens on a live
  show), keep the description as-is anyway, but tell Dan about the mismatch so he can decide.
- If the stream can't be found, ask Dan for the planned title and description. Do not invent
  either one.

**Show Notes list**: the resources actually mentioned or shown in the episode. Blog posts,
release notes, projects, repos, books, sites.

**Standing footer**: every episode ends with the same block, after the Show Notes list. Fixed
content, no per-episode judgment:

```html
<p><strong>The show:</strong></p><ul><li><a href="https://www.springofficehours.io">springofficehours.io</a> - episodes, schedule, community</li><li><a href="https://www.youtube.com/@SpringDeveloper">Spring Developer on YouTube</a> - join us live every Monday</li><li><a href="https://www.danvega.dev">Dan Vega</a></li><li><a href="https://dashaun.com">DaShaun Carter</a></li><li><a href="https://spring.io/blog">The Spring Blog</a> - the news we cover each week</li></ul>
```

## Finding the links (the part that needs care)

The transcript gives you *names*, not URLs. Whisper also mangles names (it has produced
"springofficesowers.io" for springofficehours.io). So:

- Collect every resource the hosts mention or clearly screen-share. The phrases "I'll drop a
  link", "check out", "there's a blog post", "the release notes" mark them.
- Resolve each one to a real URL with a web search, and verify the URL responds before including
  it. Never guess a URL from a spoken name.
- Prefer canonical sources: spring.io/blog for Spring announcements, the project's GitHub for
  repos, the vendor's own post for product news.
- 3 to 6 links is the normal range for this show. If you found 15, you are listing every noun;
  keep the ones a listener would actually open.

## Deliver

Write `<exports_dir>/$EP-show-notes.md` containing:

1. The title on the first line.
2. The description paragraph as plain text.
3. The Show Notes links as a markdown list (Dan reuses this elsewhere).
4. A fenced HTML block in the feed's exact shape:

```html
<p>Join Dan Vega and DaShaun Carter for the latest updates from the Spring Ecosystem. In this
episode, ...</p><p><strong>Show Notes:</strong></p><ul><li><a href="...">Link title</a></li>...</ul>
```

Then put the formatted version on the clipboard. Transistor's description box is a rich text
editor: markdown or raw HTML pasted as plain text stays literal brackets and tags. Rich text
pastes correctly, and macOS can convert:

```bash
textutil -convert rtf -stdout desc.html | pbcopy -Prefer rtf
```

(`desc.html` is just the HTML block from the file.) Tell Dan the clipboard is loaded and one
Cmd+V into the description box gives real links.

Then surface the title and description for a quick read (in chat, or in the final report when
running as a subagent), and list any mentioned resource you could NOT confidently resolve to a
URL so Dan can fill the gap. Do not publish or upload anything; Transistor is Dan's step.

## Pitfalls log

Append a dated line every time a run burns you.

- (seed) Whisper mangles proper nouns and URLs spoken aloud. Resolve names via search; never
  transcribe a URL literally.
- (seed) The title, description, and guest exist before the show is recorded, on the YouTube
  live stream. Fetch them; never write or paraphrase them. The transcript only feeds the link
  list.
- (seed) The SpringDeveloper channel has no /streams tab for yt-dlp. Use ytsearch and filter on
  channel == SpringDeveloper.
- 2026-07-27 (S5E19): ytsearch can return TWO SpringDeveloper hits for one episode (the live
  stream plus a Short with the same title and an emoji). Pick by duration, not just channel.
- 2026-07-27 (S5E19): LinkedIn Pulse URLs are undated slugs. An article titled exactly like the
  resource you want ("Devoxx Belgium CFP results & AI") turned out to be from 2022. Always
  confirm the publication date before including a link, not just that it responds.
- 2026-08-17 (S5E20): a top search hit can be a dead site. programmingpodcast.com ranked first
  for The Programming Podcast and fails TLS outright (TLSV1_ALERT_INTERNAL_ERROR, curl code 000).
  Search ranking is not liveness. curl every URL before it goes in the list, and when the obvious
  domain is dead, fall back to the host's own site (dthompsondev.com/podcast worked).
- 2026-08-17 (S5E20): the planned description can promise a segment that never happened. S5E20's
  description sold "his path from a decade in gas stations to a career in software" and the story
  was never told; zero hits for gas, station, convenience, pumping, decade, career change or
  self-taught. Grep the transcript for the description's SPECIFIC claims, not just its topic, and
  flag misses in the delivered file. Keep the description verbatim regardless; it is Dan's call.
- 2026-08-17 (S5E20): guest intros are a name minefield. Whisper rendered co-authors Jacob
  Orshalick and Jerry M. Reghunadh as "Jacob Orshalik" and "Jerry Rogde". Always confirm author
  and co-host names against the publisher or book page before using them anywhere.
- 2026-09-14 (S5E22): `pbpaste -Prefer rtf` printed 0 bytes right after a good `pbcopy`, which
  looked like an empty clipboard. It was not: the clipboard held the full RTF with all 11 links.
  pbpaste just doesn't hand back this RTF-only clipboard. Verify with
  `osascript -e 'the clipboard as «class RTF »'`, decode the hex, and count `HYPERLINK` entries
  against the number of anchors in the HTML.
- 2026-09-14 (S5E22): Medium blocks curl and WebFetch outright (403), so a Medium article can't
  pass the liveness check. Look for the author's own index instead: Craig Walls' Spring AI
  Recipes live at habuma.com/springairecipes/, linked from his GitHub repo README. Also,
  conference homepages roll over to next year's dates as soon as the event ends (kcdc.info showed
  only 2027 three days after KCDC 2026). Take dates from the transcript or last episode's notes,
  or leave them out of the blurb.
- 2026-09-14 (S5E22): the chat report ended with a markdown "Sources:" list (the web search tool
  asks for one) that looked just like a Show Notes list. That list, not the clipboard, ended up
  live on Transistor: a recipe link that had been ruled out, a GitHub repo, and no "The show:"
  footer. Never end the report with a bare link list. Label research sources plainly as "not
  for the episode page" and keep them short, or put them in the notes file's Notes for Dan.

## What this skill does NOT do

- Audio editing (spring-office-hours-edit).
- Chapters, YouTube metadata, or social posts.
- Uploading to Transistor.
