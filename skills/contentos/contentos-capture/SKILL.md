---
name: contentos-capture
description: >-
  Capture a content idea into ContentOS from whatever Dan hands over: dictated thoughts,
  a repo link, an article URL, a viewer email, or pasted notes. Reads the links, drafts the
  idea record (a YouTube-style working title, hook, why-now with only real evidence, a
  keyword, and Dan's words verbatim in the notes), checks for duplicates, saves it, and
  promotes it to a project with the repo attached, because an idea Dan brings himself is
  already a decision. Use whenever Dan says "capture this", "new idea", "add this to
  contentos", "kick off this idea", "I want to make a video about X" with a link or notes,
  or pastes a repo or URL and wants it in the pipeline. Do NOT use to generate ideas from
  scratch (video-ideation), to research whether an idea is worth making
  (video-develop-idea), or to move an existing project forward (contentos-next).
---

# ContentOS Capture

Dan talks, the system types. The slow part of starting a video was never the decision.
It was filling in the idea form. This skill turns whatever Dan hands over into the
ContentOS record in one pass, saves it, and hands off to `contentos-next`.

Capture takes minutes. It does no research, no verdict, no packaging, no verification.

## Rules that matter

1. **Check for duplicates first.** `list_ideas` and `list_projects`, matched by topic, not
   exact title. If a project already exists, do not create a second one. A duplicate
   promote had to be deleted by hand in July 2026. Update the existing record and say so.
2. **Dan's words go into the notes verbatim.** Dictation is messy, but it is the closest
   thing to his intent, and the brief and packaging read those notes later as the source
   of truth. Put them first under a heading `## Dan's notes (verbatim)`.
3. **Only evidence that exists.** The why-now carries links, dates, and numbers that are
   in the source material: the repo README, the release notes, the article. Never invent
   view counts or claims. With no evidence, the why-now is one line in Dan's words.
4. **Read every link before drafting.** A repo: README, file tree, and last push date
   (`gh api repos/<owner>/<repo>/readme -H "Accept: application/vnd.github.raw"`, the
   tree endpoint, and the repo endpoint). An article: fetch it. A viewer email: quote the
   question verbatim in the notes and record the sender in `source`.
5. **Promote when Dan brought it.** A dictated idea is a decision. Save it, then
   `promote_idea`, then `update_project` with the repo URL, the audience, and why it
   matters. Ideas that come out of an ideation batch stay in the inbox; that is
   `video-ideation`'s flow, not this one.
6. **Demo already written?** If Dan says the code is done, tick `DEMO_CODE_WORKING` with
   `set_pipeline_stage` on his word. Do not clone it, run it, or install anything to check
   it. Verification is only for demos the agent builds.
7. **Route article ideas to Writing.** If Dan calls it a post, an article, or a write-up,
   or the source is clearly a written piece, it belongs in Writing > Ideas
   (`/blog-posts/ideas`), not the video inbox. There is no MCP tool for that page yet, so
   deliver the drafted title and notes in the conversation and say where they go.
8. **Never install tooling and never start research here.** Both have derailed a capture
   before. If something needs checking, note it for `contentos-next`.

## Workflow

### Step 1: gather

Parse the message for links, dictated text, and constraints: a deadline, "the demo is
done", "this is a course", "this is happening". Fetch the links. Note the last push date
of a repo; it often is the why-now.

### Step 2: duplicate check

`list_ideas` (all statuses) and `list_projects`. Same topic under a different name counts.

### Step 3: draft the record

Map to `save_idea`:

- `title`: written like a real YouTube title, under about 65 characters. It is a working
  title. Packaging replaces it.
- `hook`: how the first 30 seconds open, taken from Dan's words or the source's most
  demonstrable moment (the flag flip, the before and after, the surprising output).
- `whyNow`: the evidence, with links. A release date, a JEP, a version bump, a viewer
  request.
- `targetKeyword`: the obvious learner phrasing if it is clear. Otherwise leave it out.
- `source`: who and when. "Dan, dictated 2026-09-16", the repo URL with its push date, or
  "Viewer email, first name and last initial".
- `notes`: Dan's words verbatim, then a summary of each link (a repo: the files, what each
  shows, requirements such as the JDK version; an article: its key claims), then a short
  `## Status at capture` block: decided or not, demo written or not, course or not.
- Leave `score`, `briefMarkdown`, and `briefVerdict` empty. Capture does not score or
  brief.

### Step 4: save

1. `save_idea`.
2. If Dan brought it: `promote_idea`, then `update_project` with `githubUrl`,
   `primaryAudience`, and `whyThisMatters`. Keep the description as the notes.
3. If he said the demo is done: `set_pipeline_stage DEMO_CODE_WORKING`.
4. If he called it a course: say that sections come later through `save_section` and do
   not create any now. See the courses memory: a course is a project with sections.

### Step 5: report and hand off

One compact message: the project slug and title, what was ticked, and one line on how to
fix anything ("say the word and I'll change the title"). Do not paste the notes back.

Then hand off. If Dan's message already said "run it", "go", or "keep going", invoke
`contentos-next` on the new slug right away. Otherwise end with: say next to run it
forward.

## What this skill does not do

- No demand research and no verdict. A decided idea skips the verdict entirely;
  `contentos-next` writes the short GO brief.
- No title, thumbnail, or intro. That is packaging, run by `contentos-next`.
- No project folder under `/Users/vega/youtube/`. `video-project` scaffolds it when
  thumbnails or footage need it.
