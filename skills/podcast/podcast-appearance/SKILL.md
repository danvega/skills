---
name: podcast-appearance
description: >-
  Log a guest appearance on someone else's podcast in both ContentOS and danvega.dev — fetch the
  episode details from a URL, save the GuestAppearance record via the ContentOS MCP server, add
  the entry to the site's appearances.json, and open a PR. Use when Dan says "I was on a podcast",
  "log this podcast appearance", "add this episode to my appearances", or shares an episode URL
  of a show he guested on. Also handles scheduling future appearances (status SCHEDULED) and
  flipping them to PUBLISHED when the episode airs. Do NOT use for Dan's OWN shows (Spring Office
  Hours, Fundamentals of Software Engineering — those sync from Transistor automatically) or for
  conference talks (speaking module).
---

# Podcast Guest Appearance

Dan appeared (or is scheduled to appear) as a guest on someone else's podcast. Record it in two
places: ContentOS (the `guest_appearance` table, via MCP) and danvega.dev (the Guest Appearances
list on `/podcasts`). The published-episode case does both; a future booking only touches
ContentOS until the episode airs.

## Inputs

Usually an episode URL. Fetch it and extract: podcast name, host name(s), episode title,
publish/air date, a one-paragraph topic summary. If there is no URL yet (a future booking),
collect podcast name, host, topic, and recording date from the conversation; ask only for what's
genuinely missing.

## Step 1 — ContentOS record

Use the ContentOS MCP server (the `contentos` server; tools live in `mcp/ContentOsMcpTools`):

1. `list_guest_appearances` first — the appearance may already exist as SCHEDULED/RECORDED
   (Dan often books ahead). Match on podcast name + rough date.
2. `save_guest_appearance`:
   - **New published episode:** omit `id`; pass `podcastName`, `hostName`, `topic` (the episode
     title works well), `airDate` (yyyy-MM-dd), `episodeUrl`, and `podcastUrl` if known. Status
     defaults to PUBLISHED.
   - **Existing record now aired:** pass its `id` plus `status: PUBLISHED`, `airDate`, and
     `episodeUrl`. Only fields you pass are changed.
   - **Future booking:** omit `id`, pass `status: SCHEDULED` with `recordingDate` and whatever
     else is known.

If the MCP server is unreachable (app not running), say so and note the record still needs
saving — don't silently skip it. ContentOS runs via `./mvnw spring-boot:run` on :8888.

## Step 2 — danvega.dev entry (published episodes only)

Site repo: `/Users/vega/dev/danvega/danvega-dev-nuxt`. Guest appearances live in
`assets/data/appearances.json` — an array rendered by `app/pages/podcasts.vue`, **ordered newest
first** (order in the file is display order; there is no date sort).

Add one object at the correct position (usually the top):

```json
{
  "show": "Inside Java Podcast",
  "host": "Lize Raes",
  "title": "AI Solutions with Spring AI 2.0",
  "dateLabel": "Jul 2026",
  "description": "One sentence in Dan's first-person voice about what the conversation covered.",
  "url": "https://inside.java/2026/07/23/podcast-063/"
}
```

- `title` is the episode title as published, minus any "Episode 63:" prefix.
- `dateLabel` is "Mon YYYY" of the air date.
- `description` is first person ("Lize and I dig into…"), one sentence, Dan's voice — see the
  existing entries for tone.

Verify: start the dev server (`npm run dev`), fetch `/podcasts`, confirm the new show name and
title render. Then branch, commit, push, and open a PR — never commit to main directly. The
`origin` remote is SSH but this environment authenticates via `gh` over HTTPS, so push with
`git push -u https://github.com/danvega/danvega-dev-nuxt.git <branch>`. Use `--no-gpg-sign`
if signing hangs.

## Step 3 — Report

Tell Dan what was saved where: the ContentOS record (status + id) and the PR URL. If the
appearance is worth promoting (social post, newsletter mention), suggest it — don't do it
unprompted.
